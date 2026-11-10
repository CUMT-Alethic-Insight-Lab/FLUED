# V05 access diagnostic

2026-11-09. Completed access diagnosis. The prior session's urllib TLS failures and browser connection failures are route-specific observations, **not** evidence that public sources are generally unavailable. No 403, TLS verification, proxy or other access restriction will be bypassed.

Available tools: Git for Windows curl 8.16.0 using Schannel, `pdftotext`, and Python 3.14. A targeted filename search under `docs/research/` found no pre-existing staged files matching `2309.16042*` or `asiaee26d*`.

Ordinary `curl --fail --location` with normal TLS verification and the inherited network environment successfully downloaded **all seven** locked public originals (HTTP 200); this includes W0533 and the formal UAI PDF. W0533's first request timed out after 75 seconds despite receiving partial data; its single ordinary retry with a longer timeout succeeded. This confirms the prior failures were tool/route specific, not a general source outage. No proxy settings or TLS validation were modified; no 403 or challenge was bypassed. Each complete response passed PDF magic-byte validation, SHA-256 was calculated, and `pdftotext -layout` returned success. See [staging manifest](STAGING_MANIFEST.md) for exact source URLs, sizes and hashes. No proxy values were printed.
