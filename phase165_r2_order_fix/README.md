# Phase 165 R2 — Narrative order repair

This package replaces the previous R2 terminal insertion inside the existing public narrative function. No new renderer or group-specific adapter is introduced.

Run `run.ps1` from the project root. The script captures the original public pi3_2 narrative, verifies the previous R2 patch, applies a minimal replacement, then checks pi3_2 byte-for-byte and checks the key pi4_3 proof statements in order. On check failure it restores the pre-change source file.

Changed production file: `toda_group_proof_narrative_renderer.py`, function `render_toda_group_proof_narrative_markdown` only. No imports outside that function change. `patch.py` and `check.py` are installer/audit utilities and are not imported into production.

The patch inserts the certified kernel after the existing Delta-image sentence and the certified quotient after the existing surjectivity and earlier-group statements. It refuses to proceed if those anchors are ambiguous. This is a limited order repair, not a complete prose-quality refactor. Internal English rule leakage and other duplicate wording remain candidates for subsequent focused diagnosis.

No full pytest is executed. The end-of-phase full suite and actual browser rendering remain Phase 165 R6 requirements.
