# Phase 174 R67 — Common zero-map arrow repair

This patch fixes precisely one extra TeX backslash in the `ImageZeroStatement`
branch of the shared `typed_sentence` projector. No mathematical rule, GIVEN,
proof tree, reference or data entry is changed. The entire reviewed production
file is Git-blob pinned, tolerating **whole-file** LF or CRLF. Re-running the
installer is idempotent only if the reconstructed original matches that pin.

Unzip into the EHP Proof Tracer repository root. Run `run.ps1 -DryRun` and then
`run.ps1` from the included package. The real two published proofs and the
presentation regression tests are checked without running the full test suite.

The complete updated `typed_sentence` function is in
`output/typed_sentence_FULL_AFTER.py`. An original-byte backup is written
outside the repository under `%LOCALAPPDATA%/EHPProofTracerAudit/`.
