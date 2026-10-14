# Phase 165 R27-R23-R1 CLI layout repair

This package repairs the failed R27-R23 installation without broadening the phase scope. It identifies the default CLI group-query tail with Python AST instead of matching a fixed string layout. It preserves all existing command dispatch branches and replaces only the group query and group proof implementations with the previously specified unified backward-search flow.

`apply.py` backs up `main.py` to `main_before_r23.py` before modification. It checks imports and leaves unrelated modules untouched. `run.ps1` applies the patch and runs only the focused R27-R23 tests plus installer tests. Full pytest is not run.

From the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase165_r27_r23_r1_layout_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r27_r23_r1_layout_fix\run.ps1"
```

Completion requires 11 focused tests to pass on the user's current source. The legacy calculation facade and other legacy bootstrap consumers remain outside this repair's scope.
