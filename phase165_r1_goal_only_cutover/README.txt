Phase 165 R1 - Goal-only cutover / fail closed
=============================================
This is a deliberately limited switch: the former phase164_r5 web proof function
no longer invokes Phase162 pi5_3 replay, phase-specific prerequisite selection,
or R4-R8 manually supplied leaves. It delegates to a goal-only search entry
point, which explicitly fails until registered premise discovery is implemented.
Therefore pi5_3 narrative will NOT work yet. This is not proof-search completion.

Changed existing file: phase164_r5_web_registry_connection.py
Changed function (full replacement): build_phase164_r5_web_pi5_3_proof
New: phase165_goal_only_search.py (new class and function), tests/test_phase165_goal_only_cutover.py
No README.md, design.md, development_log.md, roadmap.md, proof_records.md changes.
The installer saves the previous production file as *.phase165_r1_before_cutover.bak.

Run from repository root after extraction:
powershell -ExecutionPolicy Bypass -File '.\phase165_r1_goal_only_cutover\run.ps1'

Focused pytest only. Phase-end full suite is deferred.
