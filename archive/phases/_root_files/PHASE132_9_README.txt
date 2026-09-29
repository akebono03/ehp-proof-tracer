Phase 132-9 package

Purpose
-------
Connect Trace / Outline / Narrative to the existing Web group-proof flow
without duplicating proof semantics in the Web layer.

Modified files
--------------
- web_group_proof.py
- web_app.py
- templates/index.html

New test
--------
- tests/test_phase132_9_web_group_proof_modes.py

Design
------
Trace remains the default.

The Web form adds:

  Proof view: Trace / Outline / Narrative

The existing group_proof_depth value is shared across all three modes.

Outline and Narrative reuse the existing Phase 132 renderers. Their Markdown
output is adapted into WebGroupProofRenderedLineView rows. Math fragments are
kept separately as LaTeX and rendered by the existing static/web_math.js
through data-latex attributes.

No proof graph, theorem inference, Outline semantics, or Narrative semantics
are reimplemented in the Web layer.

Apply
-----
python apply_phase132_9.py

Focused test
------------
python -m pytest tests/test_phase132_9_web_group_proof_modes.py -q

Related regression
------------------
python -m pytest `
  tests/test_phase131_5_web_group_proof.py `
  tests/test_phase132_5_group_proof_outline_renderer.py `
  tests/test_phase132_6_group_proof_narrative_renderer.py `
  tests/test_phase132_7_group_proof_cli_modes.py `
  tests/test_phase132_8_group_proof_narrative_dedup.py `
  tests/test_phase132_9_web_group_proof_modes.py `
  -q

Then Phase 131-132 related regression:

python -m pytest `
  tests/test_phase131_3_group_result_proof_replay.py `
  tests/test_phase131_4_group_result_proof_replay_cli.py `
  tests/test_phase131_5_web_group_proof.py `
  tests/test_phase132_4_group_proof_presentation.py `
  tests/test_phase132_5_group_proof_outline_renderer.py `
  tests/test_phase132_6_group_proof_narrative_renderer.py `
  tests/test_phase132_7_group_proof_cli_modes.py `
  tests/test_phase132_8_group_proof_narrative_dedup.py `
  tests/test_phase132_9_web_group_proof_modes.py `
  -q

Do not run the repository-wide test suite until the end of Phase 132.

Phase boundary
--------------
Included:
- Web mode selector
- Trace default compatibility
- Outline/Narrative renderer reuse
- KaTeX preservation via data-latex
- shared depth semantics
- explicit invalid-mode handling

Not included:
- CSS redesign
- new proof semantics
- Narrative wording changes
- shared-dependency policy changes
- repository changes
