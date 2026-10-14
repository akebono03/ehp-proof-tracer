# Phase 165 R27-R49-R1 installer fix

This patch updates only the default discovery branch in `search_group_structure_automatically()` in `phase165_r52_r5_auto_search.py`.

The previous installer required literal names from the original GitHub implementation and could reject a locally revised search branch. This installer checks the actual syntax tree, accepts a partially migrated legacy branch, and preserves the remaining function. It rejects branches without an identified registry discovery call or with unknown code.

Run `run.ps1` from the extracted folder under the repository root. It backs up the modified source in `phase165_r27_r49_r1_backup`, performs the patch, runs nine targeted installer tests, and writes `phase165_r27_r49_r1_audit.json`. Full pytest is not run.

This change does not migrate the legacy `toda_calculation.py` calculation API and does not certify a mathematical group result.
