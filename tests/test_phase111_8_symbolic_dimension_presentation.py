from expression import (
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  TodaPrimaryGroup,
)
from toda_proof_narrative_renderer import (
  render_toda_primary_group_latex,
)


def test_phase111_8_symbolic_primary_group_dimensions_render_as_latex():
  n = ScalarSymbol(
    name="n",
  )

  group = TodaPrimaryGroup(
    group_dimension=ScalarSum(
      left=n,
      right=7,
    ),
    sphere_dimension=n,
  )

  rendered = (
    render_toda_primary_group_latex(
      group
    )
  )

  assert (
    rendered
    == r"\pi_{n + 7}^{n}"
  )

  assert (
    "ScalarSum"
    not in rendered
  )

  assert (
    "ScalarSymbol"
    not in rendered
  )


def test_phase111_8_concrete_primary_group_dimensions_remain_unchanged():
  group = TodaPrimaryGroup(
    group_dimension=18,
    sphere_dimension=11,
  )

  assert (
    render_toda_primary_group_latex(
      group
    )
    == r"\pi_{18}^{11}"
  )
