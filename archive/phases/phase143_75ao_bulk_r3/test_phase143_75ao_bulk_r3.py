from homotopy_groups import (
  FiniteHomotopyGroupStatement,
  HomotopyGroup,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def test_phase143_75ao_r3_finite_group():
  statement = FiniteHomotopyGroupStatement(
    group=HomotopyGroup(
      group_dimension=11,
      sphere_dimension=9,
    ),
  )
  assert (
    render_toda_proof_statement_latex(statement)
    == r"\pi_{11}^{9} \text{ is finite}"
  )
