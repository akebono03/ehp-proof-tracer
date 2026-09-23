Phase 132-4 package

Purpose
-------
Add the minimal TodaGroupProofPresentation core only.

Files
-----
- toda_group_proof_presentation.py
- tests/test_phase132_4_group_proof_presentation.py

No existing source file is replaced in this phase.

Install
-------
Extract this ZIP directly into the repository root.

Focused test
------------
python -m pytest tests/test_phase132_4_group_proof_presentation.py -q

Related regression
------------------
python -m pytest tests/test_phase131_3_group_result_proof_replay.py tests/test_phase131_4_group_result_proof_replay_cli.py tests/test_phase131_5_web_group_proof.py tests/test_phase132_4_group_proof_presentation.py -q

Do not run the repository-wide test suite until the end of Phase 132.

Phase boundary
--------------
Included:
- replay identity preservation
- root/source identity preservation
- replay-step node preservation
- depth-limited edge filtering
- premise_index preservation
- non-mutating presentation build

Not included:
- Outline renderer
- Narrative renderer
- CLI changes
- Web changes
- new proof search
- new theorem inference
