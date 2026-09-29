Phase 132-6 package

Purpose
-------
Add the minimal deterministic Narrative renderer for TodaGroupProofPresentation.

Files
-----
- toda_group_proof_narrative_renderer.py
- tests/test_phase132_6_group_proof_narrative_renderer.py

No existing source file is replaced in this phase.

Prerequisites
-------------
Phase 132-4 and Phase 132-5 must already be installed.

Focused test
------------
python -m pytest tests/test_phase132_6_group_proof_narrative_renderer.py -q

Related regression
------------------
python -m pytest `
  tests/test_phase131_3_group_result_proof_replay.py `
  tests/test_phase131_4_group_result_proof_replay_cli.py `
  tests/test_phase131_5_web_group_proof.py `
  tests/test_phase132_4_group_proof_presentation.py `
  tests/test_phase132_5_group_proof_outline_renderer.py `
  tests/test_phase132_6_group_proof_narrative_renderer.py `
  -q

Do not run the repository-wide test suite until the end of Phase 132.

Phase boundary
--------------
Included:
- deterministic Japanese narrative rendering
- source theorem sentence
- actual premise-edge ordering
- fixed Japanese connective templates
- supported LaTeX statement reuse
- inference-rule-name fallback
- nested premise before parent consequence
- deterministic / non-mutating rendering

Not included:
- CLI integration
- Web integration
- free-form prose generation
- new theorem inference
- new mathematical statement semantics
