# Phase 165 R27-R56: Conservative group-entry import cleanup

This package removes **only unused top-level imports** of legacy group report and renderer modules in `web_group_query.py` and `web_group_proof.py`. It does not rewrite public methods, change group results, or remove remaining repository calculation modules. When an imported symbol is used, its import is retained. An audit describes both outcomes. Test coverage is targeted only.

Run `run.ps1` from the extracted package. Backups are written to `phase165_r27_r56_backup`. Inspect `phase165_r27_r56_audit.json` before planning removal of legacy APIs.
