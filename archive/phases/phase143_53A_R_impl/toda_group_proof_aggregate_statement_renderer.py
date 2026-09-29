from toda_group_proof_aggregate_statement_catalog import (
  is_toda_group_proof_aggregate_statement,
)
from toda_proof_narrative_renderer import (
  render_toda_primary_group_latex,
  render_toda_raw_group_structure_latex,
)
from toda_rules import (
  Toda48Pi16_9OrderAndE4InjectiveStatement,
  Toda514SecondShortExactStatement,
  Toda515Sigma8TransportedDecompositionStatement,
  TodaProp56Pi8_5QuotientStatement,
)


def _render_iterated_suspension_name(
  group_map,
) -> str:
  exponent = group_map.exponent

  if exponent == 1:
    return "E"

  return (
    r"E^{"
    + str(
      exponent
    )
    + "}"
  )


def _render_primary_group(
  group,
) -> str:
  return render_toda_primary_group_latex(
    group
  )


def _render_prop56_quotient(
  statement: TodaProp56Pi8_5QuotientStatement,
) -> str:
  ambient = _render_primary_group(
    statement.ambient_group
  )
  source = _render_primary_group(
    statement.subobject_map.source_group
  )
  map_name = _render_iterated_suspension_name(
    statement.subobject_map
  )

  return (
    "$"
    + ambient
    + "/"
    + map_name
    + r"\left("
    + source
    + r"\right)"
    + r" \cong \mathbb{Z}/"
    + str(
      statement.quotient_order
    )
    + "$"
  )


def _render_second_short_exact(
  statement: Toda514SecondShortExactStatement,
) -> str:
  source = _render_primary_group(
    statement.source_group
  )
  middle = _render_primary_group(
    statement.middle_group
  )
  target = _render_primary_group(
    statement.target_group
  )

  return (
    "次の短完全列を得る.\n\n"
    "$0\\longrightarrow "
    + source
    + r"\xrightarrow{E} "
    + middle
    + r"\xrightarrow{H} "
    + target
    + r"\longrightarrow 0$"
  )


def _render_transported_decomposition(
  statement: Toda515Sigma8TransportedDecompositionStatement,
) -> str:
  target = _render_primary_group(
    statement
    .prop44_isomorphism
    .map
    .target_group
  )
  transported = (
    render_toda_raw_group_structure_latex(
      statement.transported_group
    )
  )

  return (
    "$"
    + target
    + r" \cong "
    + transported
    + "$"
  )


def _render_order_and_iterated_suspension_injective(
  statement: Toda48Pi16_9OrderAndE4InjectiveStatement,
) -> str:
  group_map = (
    statement.iterated_suspension_map
  )
  target = _render_primary_group(
    group_map.target_group
  )
  source = _render_primary_group(
    group_map.source_group
  )
  map_name = (
    _render_iterated_suspension_name(
      group_map
    )
  )

  return (
    "$|"
    + target
    + "| = "
    + str(
      statement.target_order
    )
    + "$ であり, "
    + "$"
    + map_name
    + ": "
    + source
    + r" \to "
    + target
    + "$ は単射である."
  )


def render_toda_group_proof_aggregate_statement_prose(
  statement,
) -> str | None:
  if not is_toda_group_proof_aggregate_statement(
    statement
  ):
    return None

  if isinstance(
    statement,
    TodaProp56Pi8_5QuotientStatement,
  ):
    return _render_prop56_quotient(
      statement
    )

  if isinstance(
    statement,
    Toda514SecondShortExactStatement,
  ):
    return _render_second_short_exact(
      statement
    )

  if isinstance(
    statement,
    Toda515Sigma8TransportedDecompositionStatement,
  ):
    return _render_transported_decomposition(
      statement
    )

  if isinstance(
    statement,
    Toda48Pi16_9OrderAndE4InjectiveStatement,
  ):
    return (
      _render_order_and_iterated_suspension_injective(
        statement
      )
    )

  raise ValueError(
    "aggregate statement catalog and renderer "
    "dispatch are inconsistent"
  )
