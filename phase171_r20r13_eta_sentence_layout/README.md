# Phase 171 R20R13 — Source-bound Eta Equation Layout

This package performs a presentation-only update to the existing completed narrative renderer. It combines adjacent, verified eta suspension equalities sharing an actual cited definition and inserts Markdown paragraph breaks at sentence-ending periods in the proof body. It does not change any mathematical rule, proof search result, source database, or bibliography identity.

## Installation

From the EHP Proof Tracer repository root on Windows:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R20R13_ETA_SENTENCE_LAYOUT.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r13_eta_sentence_layout\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r13_eta_sentence_layout\run.ps1"
```

The installer accepts either of two verified repository states: the earlier uncommitted R20R12 renderer applied over the pre-R20R12 HEAD, or the committed R20R12 renderer. Any unrelated renderer modification fails closed. Running again on the newly installed version is idempotent if the HEAD base is the reviewed committed renderer.

The local output folder contains `audit.json`, `web_narrative.md`, `CODE_FULL_JA.md`, and `phase168_r3_5_model_renderer.py.FULL` after execution. The focused pytest suite runs before the narrative audit. No full suite is run in this phase step.
