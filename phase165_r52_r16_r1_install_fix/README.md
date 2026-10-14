# Phase 165 R52-R16-R1 installation repair

R15 already passed 27 tests, but its original installer only patched `phase165_r3_recursive_search.py` and did not copy `phase165_r52_r15_ordered_citation.py` into the repository root. R16 expected that missing module and therefore stopped before modifying source or running pytest.

This repair copies the unchanged R15 module to the project root, then installs the same R16 screening code and replaces the complete `search_shared_group_goal()` function. It performs preflight checks first, makes a backup, and can be rerun. It preserves existing R15 eligibility rules and does not run the full suite.

Run from PowerShell after expanding the zip at project root:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase165_r52_r16_r1_install_fix\run.ps1"
```
