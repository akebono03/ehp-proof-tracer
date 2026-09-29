Phase 148 RC2-5 Repair R2

Production change
-----------------
toda_group_proof_narrative_semantics.py
- depth=0 semantic closure is identity.
- one-level equality calculation closure is restricted to an original equality step
  having at least two direct equality premises.
- registered definition semantic closure remains unchanged.
- no group, rule-name, block-index, or LaTeX special case is introduced.

Test repair
-----------
Historical tests whose contracts were superseded by RC2 or R4.2 are updated:
- raw exactness windows are expected to be suppressed.
- public Narrative is expected to apply semantic closure before the direct renderer.
- pi6 depth=2 closure expects two calculation equality premises plus one definition endpoint.

New focused test
----------------
tests/test_phase148_rc2_5_semantic_closure_scope.py

This package runs focused regression only.
It does NOT run repository-wide pytest.
