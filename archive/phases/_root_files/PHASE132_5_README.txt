Phase 132-5 package

Purpose
-------
Add the minimal deterministic Outline renderer for TodaGroupProofPresentation.

Files
-----
- toda_group_proof_outline_renderer.py
- tests/test_phase132_5_group_proof_outline_renderer.py

No existing source file is replaced in this phase.

Prerequisite
------------
Phase 132-4 must already be installed:
- toda_group_proof_presentation.py

Focused test
------------
python -m pytest tests/test_phase132_5_group_proof_outline_renderer.py -q

Related regression
------------------
python -m pytest `
  tests/test_phase131_3_group_result_proof_replay.py `
  tests/test_phase131_4_group_result_proof_replay_cli.py `
  tests/test_phase131_5_web_group_proof.py `
  tests/test_phase132_4_group_proof_presentation.py `
  tests/test_phase132_5_group_proof_outline_renderer.py `
  -q

Do not run the repository-wide test suite until the end of Phase 132.

Phase boundary
--------------
Included:
- deterministic proof-outline rendering
- source metadata
- root conclusion
- premise_index ordering
- nested outline from actual presentation edges
- supported LaTeX statement reuse
- inference-rule-name fallback for unsupported statements
- deterministic / non-mutating rendering

Not included:
- Narrative prose
- CLI integration
- Web integration
- new proof search
- new theorem inference
- new mathematical statement semantics
