"""Anonymized mirror sync for double-blind submission (ICLR).

Builds a sanitized copy of the main repo as a SEPARATE git repo whose history
is a sequence of sync snapshots (no original commits, no author metadata).
All identifying strings are rewritten to the project codename.

Usage:
  python tools/maintenance/anonymize_mirror.py            # build/refresh local mirror
  python tools/maintenance/anonymize_mirror.py --push     # also push to the mirror remote

Discipline (AGENTS.md rule 6): mirror commits must never contain the original
project name; the mirror is one-way (main -> mirror), never merge back.

NOTE: this script is itself synced into the mirror (its own text passes
through the same scrubber). Any sensitive literal it must reference — identity
terms, excluded-path names, ops-filter vocabulary — is therefore written as
adjacent string fragments so the verbatim string never appears in this file.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

MAIN = Path(__file__).resolve().parents[2]
MIRROR = MAIN.parent / "mentiner_mirror"
# PLACEHOLDER — anonymous hosting URL goes here. Never point this at a
# real-name account.
REMOTE = "https://example.org/ANONYMOUS_HOST_PLACEHOLDER.git"

# identity scrub map — order: longest/most specific first
REPLACEMENTS = [
    ("China University of Mining and Technology", "Anonymous University"),
    # the acronym expansions are themselves distinctive/searchable -- neutralize
    ("Fluid Language Unified Encoder-Decoder", "learned byte-level latent compression"),
    ("fluid language unified encoder-decoder", "learned byte-level latent compression"),
    ("中国矿业大学", "某高校"),
    ("CUMT", "ANON_UNIV"),
    ("矿大", "某高校"),
    ("Alethic Insight", "Anonymous"),
    ("alethicinsight.com", "anonymous.example.org"),
    ("AlethicInsight", "Anonymous"),
    ("Zhangjia Wang", "Anonymous"),
    ("SoulMamba", "DataHost"),
    ("soulvlm_project", "datahost_project"),
    ("soulvlm", "datahost"),
    ("wdd9700.github.io", "anonymous.example.org"),
    ("wdd9700", "anonymous"),
    ("740904068@qq.com", "anonymous@example.org"),
    ("74090", "user"),
    ("FLexible Unified Encoder-Decoder", "learned byte-level latent codec"),
    ("flexible unified encoder-decoder", "learned byte-level latent codec"),
    ("学院断电", "机房断电"),
    # institution names inside annotation-rule examples (third-party sample
    # strings, but they trip institution-name scans) -- neutral stand-ins
    ("中国农业科学院", "中国农业研究院"),
    ("芝加哥大学商学院", "芝加哥大学商学部"),
    # pipe-interrupted variant of the same example (`中国农|业科学院`)
    ("科学院", "研究院"),
    # excluded audit dirs: inline mentions in kept docs point at the renamed
    # (absent) path instead of the real one
    ("audit_export", "audit_snapshot"),
    ("FLUED", "MENTINER"),
    ("Flued", "Mentiner"),
    ("flued", "mentiner"),
    ("fursuit", "proj_x"),
    # dev-timeline narrative dates in code comments -- exact forms; the
    # DATE_PAREN_RE net (below, code files only) covers the paren-wrapped
    # ones, these catch the shapes it cannot reach
    ("(built 2026-08-08, put to use 2026-08-09)", ""),
    ("(fixed 2026-08-09)", ""),
    ("(launched around 13:42 on 2026-06-11)", ""),
    ("(read 2026-08-02)", ""),
    ("(2026-08-05)", ""),
    ("built 2026-08-09", ""),
    # bare ruling words (backstop for non-parenthesized forms; fragment-joined
    # so this file's own mirror copy stays clean)
    ("user" "-ruled", ""),
    ("user" "-proposed", ""),
    # platform / path generalization (mirror-side only; main repo unaffected).
    # The eval_data pair must stay AFTER the FLUED trio above: main-repo text
    # says E:/projects/FLUED/eval_data and only becomes the MENTINER form once
    # the trio has run.
    ("E:/projects/MENTINER/eval_data", "<eval_data>"),
    ("AutoDL", "cloud GPU"),
    ("for GitHub Release", "for release"),
    ("K 盘", "归档盘"),
    ("K盘", "归档盘"),
    ("E 盘", "数据盘"),
    ("E盘", "数据盘"),
    ("N 盘", "语料盘"),
    ("N盘", "语料盘"),
]

# internal collaboration docs never leave the main repo
EXCLUDE_PATTERNS = [
    "FLUED_HANDOFF",
    "FLUED_TODO",
    "__pycache__",
    ".pytest_cache",
    "checkpoints/",
    "outputs/",
    "FlashKDA/",
    "session-",  # exported session logs are internal artifacts
    "s0_annotation_samples.txt",  # raw annotation work product, not needed for review
    "docs/" "audit" "_export_",  # internal audit snapshots (incl. .docx binaries)
    "docs/" "REVIEW" "_CHECKLIST",  # cites main-repo branch names / commit hashes
    "extract" "_v4_log.py",  # session-transcript extraction tool (internal paths/UUIDs)
]

# segment-exact excludes: matched against whole path segments only, so ".git"
# cannot swallow .gitignore / .gitattributes via substring matching
EXCLUDE_SEGMENTS = {".git"}

# binary document formats never enter the mirror (their bytes cannot be
# scrubbed); a hit here means an exclude rule missed one -- loud, not silent
BINARY_BLOCKLIST = {".docx", ".doc", ".pdf"}

# mirror-operations vocabulary: any docs/CURRENT_STATE.md changelog entry
# mentioning one of these is about the anonymization pipeline itself and is
# dropped wholesale (an entry = a `- 2026-` bullet up to the next bullet/EOF,
# continuation lines included)
OPS_TERMS = [
    "SEG" "LIN",
    "yr" "ruf",
    "4" "open",
    "anonymous.4" "open",
    "小号" "仓",
    "PAT",
    "匿名" "页",
    "匿名" "镜像",
    "镜像" "仓",
    "脱" "敏",
    "anonymiz",
]
OPS_RE = re.compile("|".join(re.escape(t) for t in OPS_TERMS))

# docs/README.md index rows that link to excluded docs (dangling in the mirror)
EXCLUDED_DOC_REFS = ("audit" "_export_", "REVIEW" "_CHECKLIST", "extract" "_v4_log")

# internal ruling-narrative vocabulary: a parenthesized aside containing any
# of these is dev-timeline texture, not technical content -- drop the whole
# aside, CJK or ASCII parens, continuation lines included (fragment-joined:
# this file is itself synced into the mirror)
RULING_WORDS = [
    "user" "-ruled",
    "user" "-proposed",
    "user" "-requested",
    "user" "-specified",
    "scout" " ruling",
    "methodology" " fix",
    "research" " sweep",
    "pre" "-registered",
]
RULING_PAREN_RE = re.compile(
    r"\s*[(（][^)）]*(?:" + "|".join(RULING_WORDS) + r")[^)）]*[)）]"
)

# date-narrative parens in code comments. Applied to non-markdown text only:
# in .md docs dates are substantive content (evidence registry, changelog,
# doc history), which is why this net must not run there.
DATE_PAREN_RE = re.compile(
    r"\s*[(（](?:built|fixed|launched|read|updated|created)?"
    r"\s*20\d{2}-\d{2}-\d{2}[^)）]*[)）]"
)

# short commit hashes in full-width parens, markdown only
MD_HASH_RE = re.compile(r"\s*（[0-9a-f]{7,8}）")

CHANGELOG_ENTRY_RE = re.compile(r"^- 2026-")
AGENTS_MIRROR_RULE_ANCHOR = "6. **匿名" "镜像纪律"

MIRROR_AGENTS_NOTE = """

## Anonymity discipline (double-blind mirror)

This repository is an anonymized mirror. Hard rules for every commit here:
1. NEVER write the original project name (or any contributor identity) in
   code, comments, docs, filenames, or commit messages — use the codename
   only.
2. This mirror is generated by `tools/maintenance/anonymize_mirror.py` from
   the development repo; do not hand-edit — hand edits are overwritten by
   the next sync. One-way only: never merge mirror content back.
3. If a new identity string ever appears in the mirror, treat it as a leak:
   extend the replacement map in the sync script and re-sync immediately.
"""


def run(cmd: list[str], cwd: Path, **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, check=True, text=True, capture_output=True, **kw)


def is_excluded(rel: str) -> bool:
    if any(seg in EXCLUDE_SEGMENTS for seg in rel.split("/")):
        return True
    return any(rel.startswith(p) or p in rel for p in EXCLUDE_PATTERNS)


def is_binary(data: bytes) -> bool:
    return b"\x00" in data[:8192]


def sanitize_text(text: str, *, is_markdown: bool) -> tuple[str, list[str]]:
    """Apply the regex nets (first) then the literal scrub map.

    Returns the scrubbed text plus one human-readable fragment per regex hit,
    so every sync prints an audit trail of what the nets removed.
    """
    hits: list[str] = []

    def _sub(rx: re.Pattern[str], label: str, s: str) -> str:
        def _rep(m: re.Match[str]) -> str:
            frag = " ".join(m.group(0).split())
            hits.append(f"{label}: {frag[:120]}")
            return ""

        return rx.sub(_rep, s)

    text = _sub(RULING_PAREN_RE, "ruling-paren", text)
    if is_markdown:
        text = _sub(MD_HASH_RE, "md-hash", text)
    else:
        text = _sub(DATE_PAREN_RE, "date-paren", text)
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    return text, hits


def filter_changelog_ops(text: str) -> tuple[str, list[str]]:
    """Drop mirror-ops changelog entries (applied to sanitized text).

    Returns the filtered text plus the head line of each dropped entry.
    """
    lines = text.split("\n")
    out: list[str] = []
    dropped: list[str] = []
    i = 0
    while i < len(lines):
        if CHANGELOG_ENTRY_RE.match(lines[i]):
            j = i + 1
            while j < len(lines) and not CHANGELOG_ENTRY_RE.match(lines[j]):
                j += 1
            if OPS_RE.search("\n".join(lines[i:j])):
                dropped.append(lines[i].strip())
            else:
                out.extend(lines[i:j])
            i = j
        else:
            out.append(lines[i])
            i += 1
    return "\n".join(out), dropped


def filter_excluded_doc_refs(text: str) -> tuple[str, list[str]]:
    """Drop index lines that link to excluded docs (dangling in the mirror)."""
    kept: list[str] = []
    dropped: list[str] = []
    for line in text.split("\n"):
        if any(ref in line for ref in EXCLUDED_DOC_REFS):
            dropped.append(line.strip())
        else:
            kept.append(line)
    return "\n".join(kept), dropped


def filter_agents_mirror_rule(text: str) -> str:
    """Remove the mirror-discipline rule block from AGENTS.md.

    That rule describes the anonymization channel itself (real-name account,
    homepage/lab-site linkage, exclusion list, script path); it must not exist
    inside the mirror. The block runs from its numbered anchor to the next
    numbered rule or section header; one blank line is kept before a header.
    """
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].startswith(AGENTS_MIRROR_RULE_ANCHOR):
            i += 1
            while i < len(lines) and not (
                lines[i].startswith("7. ") or lines[i].startswith("## ")
            ):
                i += 1
            if i < len(lines) and out and out[-1] != "":
                out.append("")
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


def mirror_path(rel: str) -> str:
    """Path rewrite: package dir and filename renames (any case variant)."""
    out = rel
    if out.startswith("flued/"):
        out = "mentiner/" + out[len("flued/"):]
    if out == "flued":
        out = "mentiner"
    parts = out.split("/")
    parts = [
        p.replace("FLUED", "MENTINER").replace("Flued", "Mentiner").replace("flued", "mentiner")
        for p in parts
    ]
    return "/".join(parts)


def _on_rm_error(func, path, _exc_info):
    # Windows: git object files are read-only; chmod then retry
    os.chmod(path, 0o777)
    func(path)


def build() -> None:
    files = run(["git", "ls-files"], MAIN).stdout.splitlines()
    if MIRROR.exists():
        shutil.rmtree(MIRROR, onerror=_on_rm_error)
    MIRROR.mkdir(parents=True)
    n_files, n_skipped = 0, 0
    dropped_entries: list[str] = []
    dropped_refs: list[str] = []
    scrub_hits: list[str] = []
    for rel in files:
        if is_excluded(rel):
            n_skipped += 1
            continue
        src = MAIN / rel
        if src.suffix.lower() in BINARY_BLOCKLIST:
            print(f"[mirror] WARNING: blocked binary document: {rel}")
            n_skipped += 1
            continue
        data = src.read_bytes()
        dst_rel = mirror_path(rel)
        dst = MIRROR / dst_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if is_binary(data):
            dst.write_bytes(data)
        else:
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                dst.write_bytes(data)
                n_files += 1
                continue
            if rel == "docs/README.md":
                text, dropped_refs = filter_excluded_doc_refs(text)
            text, hits = sanitize_text(text, is_markdown=rel.endswith(".md"))
            scrub_hits.extend(f"{rel} :: {h}" for h in hits)
            if rel == "docs/CURRENT_STATE.md":
                text, dropped_entries = filter_changelog_ops(text)
            if rel == "AGENTS.md":
                text = filter_agents_mirror_rule(text)
                text += MIRROR_AGENTS_NOTE
            dst.write_text(text, encoding="utf-8", newline="\n")
        n_files += 1
    print(f"[mirror] wrote {n_files} files (skipped {n_skipped} internal)")
    for line in dropped_refs:
        print(f"[mirror] dropped doc index ref: {line}")
    for line in dropped_entries:
        print(f"[mirror] dropped changelog entry: {line}")
    for line in scrub_hits:
        print(f"[mirror] scrubbed {line}")


def commit_and_maybe_push(push: bool, remote: str) -> None:
    if not (MIRROR / ".git").exists():
        run(["git", "init", "-q"], MIRROR)
        run(["git", "checkout", "-q", "-b", "main"], MIRROR)
        run(["git", "remote", "add", "origin", remote], MIRROR)
    run(["git", "add", "-A"], MIRROR)
    status = run(["git", "status", "--porcelain"], MIRROR).stdout.strip()
    if not status:
        print("[mirror] no changes vs last sync")
        return
    # neutral message: NEVER embed the dev HEAD hash -- the main repo is
    # public, so a hash in the mirror history is a direct de-anonymizing link
    msg = "sync snapshot"
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "Anonymous",
        "GIT_AUTHOR_EMAIL": "anonymous@example.org",
        "GIT_COMMITTER_NAME": "Anonymous",
        "GIT_COMMITTER_EMAIL": "anonymous@example.org",
    }
    run(["git", "commit", "-q", "-m", msg], MIRROR, env=env)
    print(f"[mirror] committed '{msg}'")
    if push:
        run(["git", "push", "-u", "origin", "main", "--force"], MIRROR)
        print("[mirror] pushed (force: snapshot history)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--push", action="store_true")
    parser.add_argument("--remote", default=REMOTE)
    args = parser.parse_args()
    build()
    commit_and_maybe_push(args.push, args.remote)


if __name__ == "__main__":
    main()
