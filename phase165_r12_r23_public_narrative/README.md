# Phase 165 R12-R23 — Shared proof to public Narrative audit

Read-only R12-R22 proof reconstruction and common renderer audit. This phase does not certify the mathematical exposition or change the renderer. `pi43_public_narrative_certified` signals generated, nonempty, cited output only; human review remains necessary.

From the project root, unpack this archive and run `powershell -ExecutionPolicy Bypass -File .\phase165_r12_r23_public_narrative\run.ps1`.

The script copies the one new Python module into the project root, runs three focused tests, and writes `audit_result.json` and `public_narrative.md` in the package directory. No full pytest suite is run.
