# Phase 176 R3R60R2 — Public Citation and Premise Elision

Connect the already tested R3R60R1 projection as the last complete-Narrative formatting operation. No proof rules, source registrations, search providers, trust boundary, trace renderer, or proof model objects change.

## Reviewed baseline

- develop: `0ef54be058423e43c9bfb0f73cb3c8ae697c0e52`.
- R3R60R1 projection blob: `d57075464d3b39a06f31e5be17b86d66a3306bbe`.
- Exact source pins and complete BEFORE/FULL function replacements are in `apply.py` and the adjacent templates. The patch rejects unknown edits and mixed or partially applied stages, preserves LF/CRLF, and is idempotent. It does not change module-level imports in existing files.

## Scope

One production function changes: `phase171_r20r13_eta_sentence_layout/projection.py::format_complete_proof_sentences`. Historical compatibility changes are limited to `R59R4/apply.py::previous_stage`, three R59R4 connection tests, and the R60R1 isolated test fixture. These tests retain their original assertions against inverse-verified historical bytes and the appropriate historical display hook. The scoped contexts are not part of public proof rendering.

The current accepted proof is expected to retain 62 steps (51 inference, 11 GIVEN), ten internal citations, and no open goals. Only the Narrative displays nine citations: internal citation 9 is hidden, internal citation 10 is displayed as 9. The body changes from 19 to 18 nonblank rows. The partial view is unchanged. The complete proof conclusion is displayed once.

The public audit observes the actual Web adapter and accepted renderer via the R53 trust audit. It deliberately does not use R54's old assertion that displayed and internal reference counts are equal. It reuses the R54 diagnostics, original R60 typed candidate audit, and independent R60R1 projection on the exact pre-hook input. All retained reference blocks and the expected proof body are checked. The existing historical standalone audit entry points are stage-pinned; run this package's audit for the new public stage.

## Run

From the repository root, execute `run.ps1 -DryRun`, then `run.ps1`. The runner executes focused suites in separate processes (60 expected tests) and the public audit. No full pytest is run. A failed focused suite or audit stops the script; review its output before committing. The patch itself rolls back files if a file write fails, but a later failed test does not undo the patch.

Reports are stored outside the repository under `%LOCALAPPDATA%/EHPProofTracerAudit/phase176_r3r60r2_public_citation_premise_elision/`: `report.json`, `plan.json`, `before.md`, `actual_narrative.md`, `partial.md`, and `narrative.diff`.

Expected gate: `PASS_R3R60R2_PUBLIC_CITATION_PREMISE_ELISION_CONNECTED`.
