Phase 165 R3 — Generic backward recursive search

R1 production cutover and R2 lookup must already be installed.
New module: phase165_r3_recursive_search.py
New tests: tests/test_phase165_r3_recursive_search.py
Modified production boundary: phase165_goal_only_search.py (complete module replacement, with backup).

This implements a generic recursive inference/registry resolver but does not
claim that the pi_5^3 production Goal-only facade is operational: it still
requires an independently verified typed registry and registered rule catalog.
No historical replays, GIVEN fabrication or fallback is added.

Run in project root: powershell -ExecutionPolicy Bypass -File .\phase165_r3_recursive_search\run.ps1
