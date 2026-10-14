# Phase 165 R27-R46 — Typed CLI execution

Installs a single function replacement in `main.py`: `_run_execute_command` now uses the common typed search and execution API, without legacy proof replay. Existing CLI arguments (`generator_input`, `candidate_number`) remain unchanged. A missing candidate returns code 1, ambiguous candidates are listed for explicit selection, and an executed result prints the actual inference rule, premises and conclusion.

Run `run.ps1` from PowerShell after extraction. The script makes a backup, runs installer tests and targeted actual-inference tests. It never runs the full test suite. This patch does not change Group Calculation, the historical applicability catalog, or any future Phase features.
