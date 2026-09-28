import inspect

from toda_group_proof_narrative_contribution_ordering import (
  _group_key,
)


def test_phase144_6_r25_15_contribution_identity_uses_statement_semantics():
  source = inspect.getsource(
    _group_key
  )

  assert "repr(" in source
  assert "occurrence.proof_step.conclusion" in source
  assert "_render_generic_narrative_step" not in source
  assert "_normalized" not in source
