from expression import (
  ScalarSymbol,
)
from scalar_rules import (
  OddScalarStatement,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_phase153_r3_6_component_latex,
  _render_phase153_r3_6_component_list_prose,
)


def test_phase157_r20_repair40_unsupported_odd_scalar_component_returns_none():
  statement = OddScalarStatement(
    scalar=ScalarSymbol(
      name="x",
    ),
  )

  assert (
    _render_phase153_r3_6_component_latex(
      statement
    )
    is None
  )


def test_phase157_r20_repair40_component_list_skips_unsupported_odd_scalar_component():
  statement = OddScalarStatement(
    scalar=ScalarSymbol(
      name="x",
    ),
  )

  assert (
    _render_phase153_r3_6_component_list_prose(
      (
        statement,
      )
    )
    is None
  )
