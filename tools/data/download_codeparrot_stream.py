#!/usr/bin/env python3
"""Stream-download + stream-clean pipeline for codeparrot/github-code.

The original copy of this dataset lived on the missing X: drive with no local
backup, so it is re-downloaded from HuggingFace (via a mirror endpoint) while
being cleaned on the fly:

* Download workers pull parquet shards from the HF endpoint into a buffer
  directory (default ``F:\\codeparrot_buffer``) with HTTP Range resume and
  retry/backoff. The full file manifest (name/size/sha256) is fetched once via
  ``huggingface_hub`` and cached in the pipeline state DB.
* Clean workers watch the buffer and run the *unchanged* corpus_v5 cleaning
  contract from ``build_corpus_v5.py`` (same normalization, blake2b-128 hash
  contract, deterministic sampling, code license/path/secret rules, chunking)
  on every completed parquet. Output shards land in an independent output
  directory on P: (default ``P:\\FLUED_corpus\\FLUED_corpus_codeparrot``) —
  the F: corpus_v5 store is never touched.
* Deduplication checks each chunk against THREE blake2b-128 hash sets: this
  pipeline's own output state DB (read-write), the corpus_v4 baseline DB on P:
  (read-only) and the corpus_v5 increment DB on F: (read-only). The reference
  DBs are attached read-only per batch; unlike build_corpus_v5 they are NOT
  copied into the local state DB (saves ~16 GiB of backup copies).
* A disk guard polls the buffer drive; when free space drops below
  ``--min-free-gib`` (default 50 GiB) it deletes raw parquets whose state is
  ``cleaned`` (oldest first, with hysteresis). Files still pending download or
  cleaning are never deleted. With ample space, downloaded originals are kept.
* All per-file state transitions live in
  ``<output_dir>/state/pipeline_state.sqlite3`` so restarts are idempotent:
  ``downloading`` files fall back to ``pending`` (``.part`` files resume via
  HTTP Range), ``cleaning`` files fall back to ``downloaded`` and are re-cleaned
  — deterministic chunking + content-hash dedupe makes re-cleaning a no-op for
  already-written chunks.

Exit codes: 0 = everything done, 2 = output storage limit reached (v5
semantics), 3 = finished with per-file failures, 1 = fatal error.

This script must remain import-compatible with tools/data/build_corpus_v5.py;
that file is imported read-only (editing it would invalidate the main v5
build's pipeline_sha256 fingerprint).
"""

from __future__ import annotations

import argparse
import json
import os
import queue
import shutil
import sqlite3
import subprocess
import sys
import threading
import time
from collections import Counter
from pathlib import Path
from typing import Any

os.environ.setdefault("OMP_NUM_THREADS", "4")
os.environ.setdefault("MKL_NUM_THREADS", "4")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_corpus_v5 as v5  # noqa: E402  (read-only import of the v5 pipeline)

SOURCE_NAME = "codeparrot_github_code"
ACTIVE_STATES = ("pending", "downloading", "downloaded", "cleaning")
GIB = 1024**3

_LOG_LOCK = threading.Lock()
_LOG_FILE = None


def log(msg: str, *, thread: str = "main") -> None:
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} [{thread}] {msg}"
    with _LOG_LOCK:
        # Write to the real stdout directly: print() would route through Tee,
        # which also takes _LOG_LOCK and would deadlock (non-reentrant lock).
        sys.__stdout__.write(line + "\n")
        sys.__stdout__.flush()
        if _LOG_FILE is not None:
            _LOG_FILE.write(line + "\n")
            _LOG_FILE.flush()


class Tee:
    """Mirror stdout/stderr (incl. build_corpus_v5 prints) into the run log."""

    def __init__(self, stream):
        self.stream = stream

    def write(self, data: str) -> int:
        with _LOG_LOCK:
            self.stream.write(data)
            self.stream.flush()
            if _LOG_FILE is not None:
                _LOG_FILE.write(data)
                _LOG_FILE.flush()
        return len(data)

    def flush(self) -> None:
        self.stream.flush()


class StateDB:
    """Thread-safe wrapper around the pipeline state database."""

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(path), check_same_thread=False, timeout=60)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=FULL")
        self.conn.execute("PRAGMA busy_timeout=60000")
        self.lock = threading.Lock()
        with self.lock:
            self.conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS files (
                    name TEXT PRIMARY KEY,
                    size INTEGER NOT NULL,
                    sha256 TEXT NOT NULL DEFAULT '',
                    state TEXT NOT NULL DEFAULT 'pending',
                    attempts INTEGER NOT NULL DEFAULT 0,
                    worker TEXT NOT NULL DEFAULT '',
                    claimed_at REAL,
                    downloaded_at REAL,
                    cleaned_at REAL,
                    deleted INTEGER NOT NULL DEFAULT 0,
                    records_seen INTEGER NOT NULL DEFAULT 0,
                    records_sampled INTEGER NOT NULL DEFAULT 0,
                    records_rejected INTEGER NOT NULL DEFAULT 0,
                    chunks_written INTEGER NOT NULL DEFAULT 0,
                    chunks_duplicate INTEGER NOT NULL DEFAULT 0,
                    output_bytes INTEGER NOT NULL DEFAULT 0,
                    rejection_reasons TEXT NOT NULL DEFAULT '{}',
                    updated_at REAL NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                """
            )
            self.conn.commit()

    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        with self.lock:
            cur = self.conn.execute(sql, params)
            self.conn.commit()
            return cur

    def query(self, sql: str, params: tuple = ()) -> list[tuple]:
        with self.lock:
            return list(self.conn.execute(sql, params))

    def claim(self, from_state: str, to_state: str, worker: str, name: str | None = None) -> dict | None:
        with self.lock:
            if name is None:
                row = self.conn.execute(
                    "SELECT name,size,sha256 FROM files WHERE state=? ORDER BY name LIMIT 1",
                    (from_state,),
                ).fetchone()
            else:
                row = self.conn.execute(
                    "SELECT name,size,sha256 FROM files WHERE state=? AND name=?",
                    (from_state, name),
                ).fetchone()
            if row is None:
                return None
            self.conn.execute(
                "UPDATE files SET state=?, worker=?, claimed_at=?, updated_at=? WHERE name=? AND state=?",
                (to_state, worker, time.time(), time.time(), row[0], from_state),
            )
            self.conn.commit()
            return {"name": row[0], "size": int(row[1]), "sha256": row[2]}

    def set_state(self, name: str, state: str, **fields: Any) -> None:
        assignments = ["state=?", "updated_at=?"]
        params: list[Any] = [state, time.time()]
        for key, value in fields.items():
            assignments.append(f"{key}=?")
            params.append(value)
        params.append(name)
        self.execute(f"UPDATE files SET {', '.join(assignments)} WHERE name=?", tuple(params))

    def recover_interrupted(self) -> dict[str, int]:
        with self.lock:
            cur1 = self.conn.execute(
                "UPDATE files SET state='pending', worker='', updated_at=? WHERE state='downloading'",
                (time.time(),),
            )
            cur2 = self.conn.execute(
                "UPDATE files SET state='downloaded', worker='', updated_at=? WHERE state='cleaning'",
                (time.time(),),
            )
            self.conn.commit()
            return {"requeued_downloads": cur1.rowcount, "requeued_cleans": cur2.rowcount}

    def counts(self) -> dict[str, int]:
        rows = self.query("SELECT state, COUNT(*), SUM(deleted) FROM files GROUP BY state")
        out: dict[str, int] = {}
        deleted = 0
        for state, count, d in rows:
            out[state] = int(count)
            deleted += int(d or 0)
        out["deleted"] = deleted
        return out

    def all_terminal(self) -> bool:
        row = self.query(
            f"SELECT COUNT(*) FROM files WHERE state IN ({','.join('?' for _ in ACTIVE_STATES)})",
            ACTIVE_STATES,
        )
        return row[0][0] == 0

    def close(self) -> None:
        with self.lock:
            self.conn.close()


class CodeparrotStore(v5.OutputStore):
    """OutputStore that keeps reference hash DBs external and read-only.

    build_corpus_v5.OutputStore copies the reference DB into the local state
    DB via SQLite backup. With two large references (v4: 4.5 GiB, v5: 11.9 GiB)
    that copy is wasteful, so this subclass creates an empty local ``seen``
    table and attaches both reference DBs as read-only lookups inside
    ``add_many``. The dedupe coverage is identical (own + v4 + v5).
    """

    def __init__(self, output_dir: Path, reference_dbs: list[Path], **kwargs: Any) -> None:
        self.reference_paths = [Path(p) for p in reference_dbs]
        self.ref_conns: list[sqlite3.Connection] = []
        super().__init__(output_dir, self.reference_paths[0], **kwargs)
        self.ref_conns = [
            sqlite3.connect(f"file:{p.as_posix()}?mode=ro", uri=True, check_same_thread=False)
            for p in self.reference_paths
        ]
        for conn in self.ref_conns:
            conn.execute("PRAGMA busy_timeout=60000")

    def _initialize_db(self, reference_db: Path, run_fingerprint: dict[str, str]) -> None:
        if self.db_path.exists():
            return
        partial = self.db_path.with_suffix(".sqlite3.partial")
        if partial.exists():
            partial.unlink()
        dest = sqlite3.connect(str(partial))
        dest.execute("CREATE TABLE seen (h BLOB PRIMARY KEY)")
        dest.execute("CREATE TABLE IF NOT EXISTS v5_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
        dest.execute(
            "INSERT OR REPLACE INTO v5_meta(key,value) VALUES('reference_count','0')"
        )
        dest.execute(
            "INSERT OR REPLACE INTO v5_meta(key,value) VALUES('reference_db',?)",
            (json.dumps([str(p) for p in self.reference_paths]),),
        )
        for key, value in run_fingerprint.items():
            dest.execute(
                "INSERT OR REPLACE INTO v5_meta(key,value) VALUES(?,?)",
                (f"fingerprint:{key}", value),
            )
        dest.commit()
        dest.close()
        partial.replace(self.db_path)

    def add_many(self, records: list[tuple[str, str]]) -> tuple[int, int, int]:
        """Same contract as OutputStore.add_many, plus extra read-only references."""

        candidates: dict[bytes, tuple[str, bytes, str]] = {}
        duplicates = 0
        for text, source in records:
            digest = v5.legacy_hash_text(text)
            if digest in candidates:
                duplicates += 1
                continue
            candidates[digest] = (text, digest, source)
        digests = list(candidates)
        existing = self._batch_existing(self.conn, digests)
        for ref in self.ref_conns:
            existing.update(self._batch_existing(ref, digests))
        duplicates += len(existing)
        unique = [record for digest, record in candidates.items() if digest not in existing]
        if not unique:
            return 0, duplicates, 0
        batch_bytes = sum(len(text.encode("utf-8")) + 2 for text, _, _ in unique)
        self._check_storage(batch_bytes)
        self._rotate_if_needed(batch_bytes)
        self._write_pending(unique)
        self.conn.executemany("INSERT INTO seen(h) VALUES (?)", [(d,) for _, d, _ in unique])
        self.conn.executemany(
            "INSERT INTO v5_records(h,source,shard,byte_offset,byte_length) VALUES(?,?,?,?,?)",
            self._record_index_rows(unique, shard=self.shard_path, offset=self.shard_size),
        )
        self.conn.commit()
        written = self._append_records(unique)
        self.total_output_bytes += written
        self.pending_path.unlink()
        return len(unique), duplicates, written

    def close(self) -> None:
        for conn in self.ref_conns:
            conn.close()
        super().close()


def build_source_spec(args: argparse.Namespace) -> v5.SourceSpec:
    return v5.SourceSpec(
        name=SOURCE_NAME,
        category="code",
        kind="parquet",
        root=str(args.buffer_dir),
        pattern="*.parquet",
        text_field="content",
        sample_rate=args.sample_rate,
        max_output_gib=args.max_output_gib,
        min_chars=args.min_chars,
        max_chars=args.max_chars,
        code=True,
        qwen_review=False,
        license_status="per_record_permissive_filter",
        source_url=f"https://huggingface.co/datasets/{args.repo_id}",
    )


def fetch_manifest(args: argparse.Namespace, state: StateDB) -> int:
    """Fetch (once) and cache the repo file manifest. Returns total file count."""

    existing = state.query("SELECT COUNT(*) FROM files")
    if existing[0][0] > 0 and not args.refresh_manifest:
        limited = state.query("SELECT value FROM meta WHERE key='manifest_limited'")
        was_limited = bool(limited and limited[0][0] == "1")
        # A smoke run registered only a prefix of the manifest; a later
        # unlimited run must register the remaining files (states are kept).
        if not (was_limited and not args.max_files):
            return int(existing[0][0])
    os.environ["HF_ENDPOINT"] = args.hf_endpoint
    from huggingface_hub import HfApi

    api = HfApi(endpoint=args.hf_endpoint, token=read_token(args))
    files = None
    for attempt in range(1, 9):
        try:
            entries = api.list_repo_tree(args.repo_id, repo_type="dataset", path_in_repo="data", recursive=True)
            files = [f for f in entries if f.path.endswith(".parquet")]
            break
        except Exception as exc:  # network is flaky; retry with backoff
            log(f"manifest fetch attempt {attempt} failed: {type(exc).__name__}: {exc}", thread="manifest")
            time.sleep(min(60, 5 * attempt))
    if files is None:
        raise RuntimeError("could not fetch dataset manifest from HF endpoint")
    rows = []
    for f in files:
        name = Path(f.path).name
        sha = f.lfs.sha256 if getattr(f, "lfs", None) else ""
        rows.append((name, int(f.size), sha))
    rows.sort()
    if args.max_files and args.max_files > 0:
        rows = rows[: args.max_files]
    with state.lock:
        state.conn.executemany(
            "INSERT OR IGNORE INTO files(name,size,sha256,state,updated_at) VALUES(?,?,?,'pending',?)",
            [(name, size, sha, time.time()) for name, size, sha in rows],
        )
        state.conn.execute(
            "INSERT OR REPLACE INTO meta(key,value) VALUES('manifest',?)",
            (json.dumps({"repo_id": args.repo_id, "endpoint": args.hf_endpoint, "files": len(rows),
                         "fetched_at": time.time()}),),
        )
        state.conn.execute(
            "INSERT OR REPLACE INTO meta(key,value) VALUES('manifest_limited',?)",
            ("1" if (args.max_files and args.max_files > 0) else "0",),
        )
        state.conn.commit()
    log(f"manifest: {len(rows)} parquet files registered from {args.hf_endpoint}", thread="manifest")
    return len(rows)


def read_token(args: argparse.Namespace) -> str | None:
    """HF token is read from a repo-external file only; never logged."""

    if not args.hf_token_file:
        return None
    path = Path(args.hf_token_file)
    if not path.exists():
        raise FileNotFoundError(f"HF token file not found: {path}")
    token = path.read_text(encoding="utf-8").strip()
    return token or None


def http_client(args: argparse.Namespace):
    import httpx

    headers = {}
    token = read_token(args)
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return httpx.Client(
        follow_redirects=True,
        timeout=httpx.Timeout(connect=30.0, read=180.0, write=60.0, pool=30.0),
        headers=headers,
    )


def download_one(args: argparse.Namespace, client, name: str, size: int, worker: str) -> bool:
    """Stream one parquet to the buffer with Range resume. Returns success."""

    url = f"{args.hf_endpoint}/datasets/{args.repo_id}/resolve/main/data/{name}"
    final_path = args.buffer_dir / name
    part_path = args.buffer_dir / (name + ".part")
    headers = {}
    mode = "wb"
    offset = 0
    if part_path.exists():
        offset = part_path.stat().st_size
        if 0 < offset < size:
            headers["Range"] = f"bytes={offset}-"
            mode = "ab"
        elif offset >= size:
            part_path.unlink()
            offset = 0
    started = time.time()
    with client.stream("GET", url, headers=headers) as resp:
        if resp.status_code == 416:  # range not satisfiable: start over
            part_path.unlink(missing_ok=True)
            return download_one(args, client, name, size, worker)
        if headers.get("Range") and resp.status_code == 200:
            mode = "wb"  # server ignored the range; rewrite from scratch
            offset = 0
        resp.raise_for_status()
        last_log = started
        written = offset
        with part_path.open(mode) as f:
            for chunk in resp.iter_bytes(4 * 1024 * 1024):
                f.write(chunk)
                written += len(chunk)
                now = time.time()
                if now - last_log > 60:
                    speed = (written - offset) / max(now - started, 1) / 1024**2
                    log(f"{name}: {written/1024**2:.0f}/{size/1024**2:.0f} MiB ({speed:.1f} MiB/s)", thread=worker)
                    last_log = now
    if part_path.stat().st_size != size:
        raise IOError(f"size mismatch: got {part_path.stat().st_size}, expected {size}")
    part_path.replace(final_path)
    elapsed = time.time() - started
    log(
        f"downloaded {name} ({size/1024**2:.0f} MiB in {elapsed:.0f}s, {size/max(elapsed,1)/1024**2:.1f} MiB/s)",
        thread=worker,
    )
    return True


def download_one_curl(args: argparse.Namespace, name: str, size: int, worker: str) -> bool:
    """curl-subprocess variant of download_one.

    Fallback for networks where Python's TLS handshake is cut by a middlebox
    but curl's client fingerprint passes (observed 2026-08-16 on hf-mirror).
    Resume is handled by ``curl -C -`` against the ``.part`` file.
    """

    url = f"{args.hf_endpoint}/datasets/{args.repo_id}/resolve/main/data/{name}"
    final_path = args.buffer_dir / name
    part_path = args.buffer_dir / (name + ".part")
    if part_path.exists() and part_path.stat().st_size >= size:
        part_path.unlink()
    started = time.time()
    cmd = [
        "curl", "--fail", "-L", "-sS",
        "--connect-timeout", "30",
        "--speed-time", "120", "--speed-limit", "10240",
        "--retry", "3", "--retry-delay", "5", "--retry-all-errors",
        "-C", "-", "-o", str(part_path), url,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        if proc.returncode == 33:  # server ignored the range; restart clean
            part_path.unlink(missing_ok=True)
        raise IOError(f"curl rc={proc.returncode}: {proc.stderr.strip()[:200]}")
    if part_path.stat().st_size != size:
        raise IOError(f"size mismatch: got {part_path.stat().st_size}, expected {size}")
    part_path.replace(final_path)
    elapsed = time.time() - started
    log(
        f"downloaded {name} ({size/1024**2:.0f} MiB in {elapsed:.0f}s, {size/max(elapsed,1)/1024**2:.1f} MiB/s)",
        thread=worker,
    )
    return True


def verify_sha256_if_requested(args: argparse.Namespace, path: Path, expected: str, worker: str) -> None:
    if args.verify_sha256 and expected:
        actual = v5.file_sha256(path)
        if actual != expected:
            raise IOError(f"sha256 mismatch: {actual} != {expected}")
        log(f"sha256 OK {path.name}", thread=worker)


def download_worker(args: argparse.Namespace, state: StateDB, stop: threading.Event, worker: str) -> None:
    client = http_client(args) if args.download_backend == "httpx" else None
    while not stop.is_set():
        nxt = state.query("SELECT name,size,sha256 FROM files WHERE state='pending' ORDER BY name LIMIT 1")
        if not nxt:
            # Cleaners may requeue a corrupt parquet for re-download; stay alive
            # while any file is still being cleaned.
            active_clean = state.query(
                "SELECT COUNT(*) FROM files WHERE state IN ('cleaning','downloaded')"
            )[0][0]
            if active_clean == 0:
                return
            stop.wait(10)
            continue
        name, size, sha256 = nxt[0][0], int(nxt[0][1]), nxt[0][2]
        # Space gate: never start a download that would breach the guard floor.
        while not stop.is_set():
            free = shutil.disk_usage(args.buffer_dir).free
            needed = size + int((args.min_free_gib + 2) * GIB)
            if free >= needed:
                break
            log(
                f"buffer space low ({free/GIB:.1f} GiB free < {needed/GIB:.1f} GiB needed); waiting for guard",
                thread=worker,
            )
            stop.wait(20)
        if stop.is_set():
            return
        claimed = state.claim("pending", "downloading", worker, name=name)
        if claimed is None:
            continue
        attempts = state.query("SELECT attempts FROM files WHERE name=?", (name,))[0][0]
        try:
            if args.download_backend == "curl":
                download_one_curl(args, name, size, worker)
            else:
                download_one(args, client, name, size, worker)
            verify_sha256_if_requested(args, args.buffer_dir / name, sha256, worker)
            state.set_state(name, "downloaded", downloaded_at=time.time(), worker="")
        except Exception as exc:
            attempts += 1
            log(f"download failed {name} (attempt {attempts}): {type(exc).__name__}: {exc}", thread=worker)
            if attempts >= args.max_attempts:
                part = args.buffer_dir / (name + ".part")
                if part.exists():
                    part.unlink()
                state.set_state(name, "download_failed", attempts=attempts, worker="")
            else:
                state.set_state(name, "pending", attempts=attempts, worker="")
                stop.wait(min(120, 10 * attempts))


def clean_one_file(
    args: argparse.Namespace,
    source: v5.SourceSpec,
    path: Path,
    write_queue: queue.Queue,
    stop: threading.Event,
    worker: str,
) -> dict[str, Any]:
    """Run the v5 cleaning contract on one parquet; push chunk batches to the writer."""

    stats: dict[str, Any] = {
        "records_seen": 0,
        "records_sampled": 0,
        "records_rejected": 0,
        "rejection_reasons": Counter(),
    }
    valid, reason = v5.validate_parquet(path)
    if not valid:
        raise ValueError(f"invalid_parquet:{reason}")
    buffer: list[str] = []
    for record in v5.iter_parquet_records(path, source, args.parquet_batch_size):
        if stop.is_set():
            raise InterruptedError("stop requested")
        stats["records_seen"] += 1
        metadata_reason = v5.record_allowed_by_metadata(record, source)
        if metadata_reason:
            stats["records_rejected"] += 1
            stats["rejection_reasons"][metadata_reason] += 1
            continue
        clean = v5.clean_record(record, source)
        if clean.text is None:
            stats["records_rejected"] += 1
            stats["rejection_reasons"][clean.reason] += 1
            continue
        digest = v5.legacy_hash_text(clean.text)
        if v5.hash_fraction(digest) >= source.sample_rate:
            stats["rejection_reasons"]["deterministic_sample"] += 1
            continue
        stats["records_sampled"] += 1
        for chunk in v5.deterministic_chunks(
            clean.text,
            max_chars=min(args.max_chunk_chars, 24_000),
            min_chars=source.min_chars,
            code=source.code,
        ):
            buffer.append(chunk)
            if len(buffer) >= args.output_batch_size:
                write_queue.put(("batch", path.name, buffer))
                buffer = []
    if buffer:
        write_queue.put(("batch", path.name, buffer))
    return stats


def clean_worker(args: argparse.Namespace, source: v5.SourceSpec, state: StateDB,
                 write_queue: queue.Queue, stop: threading.Event, worker: str) -> None:
    while not stop.is_set():
        claimed = state.claim("downloaded", "cleaning", worker)
        if claimed is None:
            # Idle instead of exiting while downloads may still arrive.
            upstream = state.query(
                "SELECT COUNT(*) FROM files WHERE state IN ('pending','downloading','downloaded')"
            )[0][0]
            if upstream == 0:
                return
            stop.wait(10)
            continue
        name = claimed["name"]
        path = args.buffer_dir / name
        if not path.exists():  # raw file vanished (should not happen; guard only deletes cleaned)
            log(f"{name} missing from buffer; requeueing download", thread=worker)
            state.set_state(name, "pending", worker="")
            continue
        attempts = state.query("SELECT attempts FROM files WHERE name=?", (name,))[0][0]
        try:
            stats = clean_one_file(args, source, path, write_queue, stop, worker)
        except InterruptedError:
            state.set_state(name, "downloaded", worker="")
            return
        except Exception as exc:
            attempts += 1
            log(f"clean failed {name} (attempt {attempts}): {type(exc).__name__}: {exc}", thread=worker)
            if attempts >= args.max_attempts:
                state.set_state(name, "clean_failed", attempts=attempts, worker="")
            else:
                # Corrupt or unreadable parquet: drop the raw file and re-download.
                path.unlink(missing_ok=True)
                state.set_state(name, "pending", attempts=attempts, worker="")
            continue
        write_queue.put(("file_done", name, stats))


def writer_thread(args: argparse.Namespace, state: StateDB, write_queue: queue.Queue,
                  stop: threading.Event, ready: threading.Event,
                  result: dict[str, Any], run_fingerprint: dict[str, str]) -> None:
    try:
        store = CodeparrotStore(
            args.output_dir,
            [Path(p) for p in args.reference_dbs],
            shard_gib=args.shard_gib,
            dry_run=False,
            max_output_gib=args.max_output_gib,
            min_free_gib=args.output_min_free_gib,
            run_fingerprint=run_fingerprint,
            shard_prefix=args.shard_prefix,
        )
    except Exception as exc:
        result["init_error"] = f"{type(exc).__name__}: {exc}"
        ready.set()
        return
    ready.set()
    storage_limited = False
    per_file_written: Counter[str] = Counter()
    per_file_dup: Counter[str] = Counter()
    per_file_bytes: Counter[str] = Counter()
    totals = {"chunks_written": 0, "chunks_duplicate": 0, "output_bytes": 0}
    done_files = 0
    try:
        while True:
            try:
                kind, name, payload = write_queue.get(timeout=5)
            except queue.Empty:
                if stop.is_set():
                    break
                continue
            if kind == "stop":
                break
            if kind == "batch":
                if storage_limited:
                    continue
                try:
                    written, dup, nbytes = store.add_many([(chunk, SOURCE_NAME) for chunk in payload])
                except v5.StorageLimitReached as exc:
                    log(f"output storage limit reached: {exc}", thread="writer")
                    storage_limited = True
                    stop.set()
                    continue
                per_file_written[name] += written
                per_file_dup[name] += dup
                per_file_bytes[name] += nbytes
                totals["chunks_written"] += written
                totals["chunks_duplicate"] += dup
                totals["output_bytes"] += nbytes
            elif kind == "file_done":
                if storage_limited:
                    # Batches of this file were dropped after the limit; leave it
                    # in 'cleaning' so a restart requeues it for a full re-clean.
                    continue
                stats = payload
                state.set_state(
                    name,
                    "cleaned",
                    worker="",
                    cleaned_at=time.time(),
                    records_seen=stats["records_seen"],
                    records_sampled=stats["records_sampled"],
                    records_rejected=stats["records_rejected"],
                    chunks_written=per_file_written.pop(name, 0),
                    chunks_duplicate=per_file_dup.pop(name, 0),
                    output_bytes=per_file_bytes.pop(name, 0),
                    rejection_reasons=json.dumps(dict(stats["rejection_reasons"]), ensure_ascii=False),
                )
                done_files += 1
                row = state.query("SELECT chunks_written,chunks_duplicate,output_bytes FROM files WHERE name=?", (name,))[0]
                log(
                    f"cleaned {name} ({done_files} this run): seen={stats['records_seen']:,} "
                    f"sampled={stats['records_sampled']:,} rejected={stats['records_rejected']:,} "
                    f"written={row[0]:,} dup={row[1]:,} out={row[2]/GIB:.3f} GiB",
                    thread="writer",
                )
    finally:
        store.close()
        result.update(totals)
        result["storage_limited"] = storage_limited
        log(
            f"store closed: written={totals['chunks_written']:,} dup={totals['chunks_duplicate']:,} "
            f"out={totals['output_bytes']/GIB:.2f} GiB",
            thread="writer",
        )


def guard_sweep(args: argparse.Namespace, state: StateDB, stop: threading.Event) -> None:
    """One deletion pass: free buffer space by removing cleaned raw parquets."""

    min_free = int(args.min_free_gib * GIB)
    hysteresis = int(args.guard_hysteresis_gib * GIB)
    free = shutil.disk_usage(args.buffer_dir).free
    if free >= min_free:
        return
    candidates = state.query(
        "SELECT name,size FROM files WHERE state='cleaned' AND deleted=0 ORDER BY cleaned_at"
    )
    for name, size in candidates:
        if stop.is_set():
            break
        free = shutil.disk_usage(args.buffer_dir).free
        if free >= min_free + hysteresis:
            break
        path = args.buffer_dir / name
        try:
            path.unlink(missing_ok=True)
            (args.buffer_dir / (name + ".part")).unlink(missing_ok=True)
            state.execute("UPDATE files SET deleted=1, updated_at=? WHERE name=?", (time.time(), name))
            free = shutil.disk_usage(args.buffer_dir).free
            log(
                f"deleted cleaned raw {name} ({int(size)/GIB:.2f} GiB); buffer free now {free/GIB:.1f} GiB",
                thread="guard",
            )
        except OSError as exc:
            log(f"failed to delete {name}: {exc}", thread="guard")
    free = shutil.disk_usage(args.buffer_dir).free
    if free < min_free and not candidates:
        log(
            f"buffer low ({free/GIB:.1f} GiB) but no cleaned files left to delete",
            thread="guard",
        )


def guard_thread(args: argparse.Namespace, state: StateDB, stop: threading.Event) -> None:
    while not stop.is_set():
        try:
            guard_sweep(args, state, stop)
        except Exception as exc:
            log(f"guard error: {type(exc).__name__}: {exc}", thread="guard")
        stop.wait(args.guard_interval)


def print_status(state: StateDB) -> None:
    counts = state.counts()
    total = sum(v for k, v in counts.items() if k != "deleted")
    parts = [f"{k}={v}" for k, v in sorted(counts.items())]
    log(f"state: total={total} " + " ".join(parts), thread="status")
    agg = state.query(
        "SELECT COUNT(*), SUM(records_seen), SUM(records_sampled), SUM(chunks_written), "
        "SUM(chunks_duplicate), SUM(output_bytes) FROM files WHERE state='cleaned'"
    )[0]
    log(
        f"cleaned files={int(agg[0] or 0)} seen={int(agg[1] or 0):,} sampled={int(agg[2] or 0):,} "
        f"written={int(agg[3] or 0):,} dup={int(agg[4] or 0):,} out={int(agg[5] or 0)/GIB:.2f} GiB",
        thread="status",
    )


def build_run_fingerprint(args: argparse.Namespace, state: StateDB) -> dict[str, str]:
    refs = {}
    for p in args.reference_dbs:
        path = Path(p)
        stat = path.stat()
        refs[str(path)] = f"{stat.st_size}:{stat.st_mtime_ns}"
    params = {
        "repo_id": args.repo_id,
        "text_field": "content",
        "sample_rate": args.sample_rate,
        "min_chars": args.min_chars,
        "max_chars": args.max_chars,
        "max_chunk_chars": args.max_chunk_chars,
        "shard_prefix": args.shard_prefix,
        "code": True,
    }
    return {
        "source_params_sha256": v5.json_sha256(params),
        "references": v5.json_sha256(refs),
        "cleaner_sha256": v5.file_sha256(Path(v5.__file__)),
        "pipeline_sha256": v5.file_sha256(Path(__file__)),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-id", default="codeparrot/github-code")
    parser.add_argument("--hf-endpoint", default=os.environ.get("HF_ENDPOINT", "https://hf-mirror.com"))
    parser.add_argument("--hf-token-file", default="", help="Repo-external file containing an HF token (dataset is public; usually not needed)")
    parser.add_argument("--buffer-dir", type=Path, default=Path(r"F:\codeparrot_buffer"))
    parser.add_argument("--output-dir", type=Path, default=Path(r"P:\FLUED_corpus\FLUED_corpus_codeparrot"))
    parser.add_argument(
        "--reference-dbs",
        nargs="+",
        default=[
            r"P:\FLUED_corpus\FLUED_corpus_v4\state\dedupe_hashes.sqlite3",
            r"F:\FLUED_corpus\FLUED_corpus_v5\state\dedupe_hashes.sqlite3",
        ],
    )
    parser.add_argument("--download-workers", type=int, default=6)
    parser.add_argument("--download-backend", choices=["httpx", "curl"], default="httpx",
                        help="curl = shell out to curl.exe (use when Python TLS is blocked but curl passes)")
    parser.add_argument("--clean-workers", type=int, default=3)
    parser.add_argument("--max-files", type=int, default=0, help="Limit to the first N parquets (smoke tests)")
    parser.add_argument("--refresh-manifest", action="store_true", help="Re-fetch the repo file list and register new files")
    parser.add_argument("--max-attempts", type=int, default=5)
    parser.add_argument("--verify-sha256", action="store_true", help="Hash every downloaded file against the repo manifest")
    # Cleaning contract (mirrors configs/data/corpus_v5_sources_20260808.json github_code_permissive)
    parser.add_argument("--sample-rate", type=float, default=0.25)
    parser.add_argument("--min-chars", type=int, default=80)
    parser.add_argument("--max-chars", type=int, default=2_000_000)
    parser.add_argument("--max-chunk-chars", type=int, default=32_768)
    parser.add_argument("--parquet-batch-size", type=int, default=4096)
    parser.add_argument("--output-batch-size", type=int, default=5000)
    # Output store
    parser.add_argument("--shard-prefix", default="codeparrot")
    parser.add_argument("--shard-gib", type=float, default=4.0)
    parser.add_argument("--max-output-gib", type=float, default=75.0)
    parser.add_argument("--output-min-free-gib", type=float, default=30.0, help="Free-space reserve on the P: output drive")
    # Buffer guard
    parser.add_argument("--min-free-gib", type=float, default=50.0, help="Delete cleaned raw parquets below this free space on the buffer drive")
    parser.add_argument("--guard-hysteresis-gib", type=float, default=10.0)
    parser.add_argument("--guard-interval", type=float, default=30.0)
    parser.add_argument("--status", action="store_true", help="Print pipeline progress and exit")
    parser.add_argument("--force-unlock", action="store_true", help="Remove a stale RUNNING.lock after verifying no run is active")
    return parser.parse_args()


def main() -> int:
    global _LOG_FILE
    args = parse_args()
    args.buffer_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "state").mkdir(parents=True, exist_ok=True)
    log_path = args.output_dir / "logs" / f"pipeline_{time.strftime('%Y%m%d_%H%M%S')}.log"
    _LOG_FILE = log_path.open("a", encoding="utf-8")
    sys.stdout = Tee(sys.__stdout__)
    sys.stderr = Tee(sys.__stderr__)

    state = StateDB(args.output_dir / "state" / "pipeline_state.sqlite3")

    if args.status:
        print_status(state)
        state.close()
        return 0

    for ref in args.reference_dbs:
        if not Path(ref).exists():
            raise FileNotFoundError(f"reference dedupe DB missing: {ref}")

    lock = v5.RunLock(args.output_dir, enabled=True)
    if args.force_unlock:
        lock.remove_if_stale()
    lock.acquire()
    exit_code = 0
    try:
        recovered = state.recover_interrupted()
        if recovered["requeued_downloads"] or recovered["requeued_cleans"]:
            log(f"recovered interrupted state: {recovered}")
        total_files = fetch_manifest(args, state)
        run_fingerprint = build_run_fingerprint(args, state)
        source = build_source_spec(args)
        print_status(state)
        if state.all_terminal():
            log("nothing to do: all files are in terminal states")
            # Even with no work left, the buffer may be over the guard floor
            # (e.g. interrupted before the final sweep): run one pass.
            guard_sweep(args, state, threading.Event())
            print_status(state)
            failed = state.query("SELECT COUNT(*) FROM files WHERE state IN ('download_failed','clean_failed')")[0][0]
            return 3 if failed else 0

        stop = threading.Event()
        ready = threading.Event()
        write_queue: queue.Queue = queue.Queue(maxsize=max(8, 2 * args.clean_workers))
        result: dict[str, Any] = {}
        threads: list[threading.Thread] = []

        writer = threading.Thread(
            target=writer_thread,
            args=(args, state, write_queue, stop, ready, result, run_fingerprint),
            name="writer",
            daemon=True,
        )
        writer.start()
        if not ready.wait(timeout=3600):
            raise RuntimeError("writer thread failed to initialize the output store")
        if "init_error" in result:
            raise RuntimeError(f"output store initialization failed: {result['init_error']}")
        threads.append(writer)

        guard = threading.Thread(target=guard_thread, args=(args, state, stop), name="guard", daemon=True)
        guard.start()
        threads.append(guard)

        for i in range(args.download_workers):
            t = threading.Thread(
                target=download_worker, args=(args, state, stop, f"download-{i}"), name=f"download-{i}", daemon=True
            )
            t.start()
            threads.append(t)
        for i in range(args.clean_workers):
            t = threading.Thread(
                target=clean_worker,
                args=(args, source, state, write_queue, stop, f"clean-{i}"),
                name=f"clean-{i}",
                daemon=True,
            )
            t.start()
            threads.append(t)

        log(
            f"pipeline started: files={total_files} download_workers={args.download_workers} "
            f"clean_workers={args.clean_workers} buffer={args.buffer_dir} output={args.output_dir} "
            f"endpoint={args.hf_endpoint}"
        )
        try:
            while True:
                time.sleep(30)
                print_status(state)
                if state.all_terminal():
                    log("all files reached terminal states")
                    break
                workers_alive = any(t.is_alive() for t in threads if t.name.startswith(("download-", "clean-")))
                if not workers_alive:
                    # Workers only exit early when stopped or when no work remains.
                    if stop.is_set():
                        log("stop requested by writer (storage limit) — draining")
                    else:
                        remaining = state.query(
                            f"SELECT COUNT(*) FROM files WHERE state IN ({','.join('?' for _ in ACTIVE_STATES)})",
                            ACTIVE_STATES,
                        )[0][0]
                        if remaining:
                            log(f"WARN: workers exited but {remaining} files are not terminal", thread="main")
                    break
        except KeyboardInterrupt:
            log("KeyboardInterrupt: stopping after current units")
            stop.set()
        stop.set()
        for t in threads:
            if t.name.startswith(("download-", "clean-")):
                t.join(timeout=600)
        # Tell the writer to finish after all producers are done.
        write_queue.put(("stop", "", None))
        writer.join(timeout=1800)
        stop.set()
        guard.join(timeout=10)

        failed = state.query("SELECT name,state,attempts FROM files WHERE state IN ('download_failed','clean_failed')")
        if failed:
            log(f"failed files ({len(failed)}): {[r[0] for r in failed][:20]}")
            exit_code = 3
        if result.get("storage_limited"):
            exit_code = 2
        elif not state.all_terminal() and not failed:
            log("run ended with non-terminal files remaining", thread="main")
            exit_code = 3
        print_status(state)
        log(f"run finished with exit_code={exit_code}")
        return exit_code
    finally:
        state.close()
        lock.release()


if __name__ == "__main__":
    raise SystemExit(main())
