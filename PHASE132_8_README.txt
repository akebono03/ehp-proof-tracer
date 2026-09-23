Phase 132-8 package

Purpose
-------
Deduplicate shared ProofStep ancestry in the deterministic group-proof
Narrative renderer.

Modified source
---------------
toda_group_proof_narrative_renderer.py

Changed functions
-----------------
- _append_narrative_for_step()
- render_toda_group_proof_narrative_markdown()

Behavior
--------
The first occurrence of one ProofStep identity expands its subtree normally.

A later occurrence of the same ProofStep identity does not recursively expand
the same ancestry again. It emits a short deterministic reference:

  既出の...を用いる。

Trace, Outline, proof graph, and source provenance are unchanged.

Apply
-----
python apply_phase132_8.py

Focused test
------------
python -m pytest tests/test_phase132_8_group_proof_narrative_dedup.py -q

Related regression
------------------
python -m pytest `
  tests/test_phase132_6_group_proof_narrative_renderer.py `
  tests/test_phase132_7_group_proof_cli_modes.py `
  tests/test_phase132_8_group_proof_narrative_dedup.py `
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
  -q

Do not run the repository-wide test suite until the end of Phase 132.

Phase boundary
--------------
Included:
- ProofStep-identity-based shared dependency deduplication
- one full subtree expansion per ProofStep identity
- deterministic "既出の..." reference for later uses
- CLI narrative automatically benefits from the renderer change

Not included:
- Trace changes
- Outline changes
- Web integration
- theorem/rule semantic expansion
- free-form prose generation
