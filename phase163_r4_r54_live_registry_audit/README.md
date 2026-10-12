# Phase 163 R4-R54 Live Registry Bridge Content Audit

Run `run.ps1` from the repository root after R4-R53 has created `phase163_r4_r53_output/overlap_audit.json`.

This step constructs the current in-memory registry bridge with the repository's fixed-component and theorem-fact defaults. It does **not** pass a proof repository or modify any production module, registry ID, TeX document, or catalog. It records the actual provenance and Python content type of every bridge assertion. Metadata-only components are not falsely treated as typed mathematical definitions. Unattributed theorem facts remain unresolved.

Results are written under `phase163_r4_r54_output/` as `live_audit.json`, `comparison_queue.csv`, and `report.md`. The focused suite has nine tests. The full test suite is not run.
