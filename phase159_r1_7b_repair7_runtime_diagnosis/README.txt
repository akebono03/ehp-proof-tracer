Phase 159-R1-7b repair7 — runtime diagnosis only

Purpose:
- inspect the actual pi11_4 baseline proof body seen by R1-7b
- compare original presentation vs semantic-closure presentation
- inspect typed exactness steps in nodes and recursive ancestry
- test the current inline exactness parser against actual runtime lines
- compare normalization using original vs closure presentation

Production changes: none
Test changes: none
pytest: not run

Run:
powershell -ExecutionPolicy Bypass -File ".\phase159_r1_7b_repair7_runtime_diagnosis\run_phase159_r1_7b_repair7.ps1"
