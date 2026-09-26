from expression import (
  ScalarSymbol,
)
from proof import (
  ProofRule,
  ProofStep,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_group_proof_narrative_renderer import (
  _render_group_proof_narrative_fact,
)
from toda_rules import (
  toda_eta_family_definition_statement,
)


def test_phase143_73a_scalar_greater_equal_statement_renders_as_latex():
  n = ScalarSymbol(
    name="n",
  )

  step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=n,
      right=5,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    _render_group_proof_narrative_fact(
      step
    )
    == r"$n \ge 5$"
  )


def test_phase143_73a_eta_family_definition_uses_human_readable_label():
  n = ScalarSymbol(
    name="n",
  )

  step = ProofStep(
    conclusion=(
      toda_eta_family_definition_statement(
        n
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    _render_group_proof_narrative_fact(
      step
    )
    == "\u03b7-family \u306e\u5b9a\u7fa9"
  )
