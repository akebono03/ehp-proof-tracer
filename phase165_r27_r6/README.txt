Phase 165 R27-R6: remove old proof constructors from automatic search and normal Group proof route.
Run from repository root:
  Expand-Archive -Path "$HOME\Downloads\phase165_r27_r6.zip" -DestinationPath . -Force
  powershell -ExecutionPolicy Bypass -File ".\phase165_r27_r6\run.ps1"
Changed functions: phase165_r52_r5_auto_search.py::search_group_structure_automatically;
web_app.py::create_app.index (group_proof branch only).
Existing typed registry and generic rules untouched. No old code deleted at this step.
No proof result is fabricated if a typed goal is unresolved.
Group query's old numeric/result facade is NOT migrated by this change; planned for later phase.
Tests: focused R27-R6, R52-R5 and R52-R4 only; full suite at end of Phase 165.
