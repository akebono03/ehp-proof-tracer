# Phase 168 R3-41C1 — Web Heading Capture Fix

This is a narrow correction of the R3-41C test and audit harness. Web heading rows keep their text in `prefix`, not in `segments`. The original harness ignored those heading rows and falsely reported missing diagnostics.

The two production replacement functions are **byte-for-byte identical** to R3-41C. This package only adjusts its test and audit text extraction and verifies real heading rows. It preserves the explicit legacy route, direct no-model fallback, finished narratives, search behavior, and reference provenance.

Run `run.ps1` at the repository root after extracting the archive. Focused tests and comparison checks run; full pytest is deferred until the end of Phase 168. On failure, the package restores the two production files.
