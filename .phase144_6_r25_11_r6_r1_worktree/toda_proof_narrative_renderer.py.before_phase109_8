from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
  TodaSuspensionMap,
)
from proof import (
  LiteratureStatement,
  ProofRule,
  Relation,
  RelationType,
)
from toda_end_to_end_presentation import (
  TodaEndToEndCandidatePresentation,
)
from toda_human_readable_renderer import (
  render_toda_expression_latex,
)
from toda_proof_dependency import (
  TodaProofDependencyRole,
)
from toda_proof_presentation import (
  TodaProofStepPresentation,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  TodaDeltaInjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaNuFamilyDefinitionStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionSurjectiveStatement,
)


def render_toda_primary_group_latex(
  group: TodaPrimaryGroup,
) -> str:
  if not isinstance(
    group,
    TodaPrimaryGroup,
  ):
    raise TypeError(
      "group must be a TodaPrimaryGroup"
    )

  return (
    r"\pi_{"
    + str(
      group.group_dimension
    )
    + "}^{"
    + str(
      group.sphere_dimension
    )
    + "}"
  )


def render_toda_raw_group_structure_latex(
  group,
) -> str:
  if isinstance(
    group,
    FreeCyclicGroup,
  ):
    return (
      r"\mathbb{Z}\{"
      + render_toda_expression_latex(
        group.generator
      )
      + r"\}"
    )

  if isinstance(
    group,
    FiniteCyclicGroup,
  ):
    return (
      r"\mathbb{Z}/"
      + str(
        group.order
      )
      + r"\{"
      + render_toda_expression_latex(
        group.generator
      )
      + r"\}"
    )

  if isinstance(
    group,
    DirectSumGroup,
  ):
    return r" \oplus ".join(
      render_toda_raw_group_structure_latex(
        summand
      )
      for summand in group.summands
    )

  raise TypeError(
    "unsupported raw group structure"
  )


def _render_toda_map_name_latex(
  group_map,
) -> str:
  if isinstance(
    group_map,
    TodaSuspensionMap,
  ):
    return "E"

  if isinstance(
    group_map,
    TodaHopfInvariantMap,
  ):
    return "H"

  if isinstance(
    group_map,
    TodaDeltaMap,
  ):
    return r"\Delta"

  raise TypeError(
    "unsupported Toda map"
  )


def _render_toda_group_map_latex(
  group_map,
) -> str:
  return (
    _render_toda_map_name_latex(
      group_map
    )
    + ": "
    + render_toda_primary_group_latex(
      group_map.source_group
    )
    + r" \to "
    + render_toda_primary_group_latex(
      group_map.target_group
    )
  )


def _render_toda_ehp_map_symbol_latex(
  map_symbol,
) -> str:
  names = {
    "E": "E",
    "H": "H",
    "Δ": r"\Delta",
  }

  name = getattr(
    map_symbol,
    "name",
    None,
  )

  if (
    not isinstance(
      name,
      str,
    )
    or name not in names
  ):
    raise TypeError(
      "unsupported EHP map symbol"
    )

  return names[
    name
  ]


def _render_toda_exactness_window_latex(
  window: TodaEHPExactnessWindow,
) -> str:
  if not isinstance(
    window,
    TodaEHPExactnessWindow,
  ):
    raise TypeError(
      "window must be a "
      "TodaEHPExactnessWindow"
    )

  return (
    render_toda_primary_group_latex(
      window.source_term
    )
    + r" \xrightarrow{"
    + _render_toda_ehp_map_symbol_latex(
      window.first_map
    )
    + "} "
    + render_toda_primary_group_latex(
      window.middle_term
    )
    + r" \xrightarrow{"
    + _render_toda_ehp_map_symbol_latex(
      window.second_map
    )
    + "} "
    + render_toda_primary_group_latex(
      window.target_term
    )
  )


def _render_relation_side_latex(
  value,
) -> str:
  if isinstance(
    value,
    TodaPrimaryGroup,
  ):
    return (
      render_toda_primary_group_latex(
        value
      )
    )

  if isinstance(
    value,
    (
      FreeCyclicGroup,
      FiniteCyclicGroup,
      DirectSumGroup,
    ),
  ):
    return (
      render_toda_raw_group_structure_latex(
        value
      )
    )

  try:
    return render_toda_expression_latex(
      value
    )
  except TypeError:
    return str(
      value
    )


def _render_relation_latex(
  relation: Relation,
) -> str:
  if not isinstance(
    relation,
    Relation,
  ):
    raise TypeError(
      "relation must be a Relation"
    )

  lhs = _render_relation_side_latex(
    relation.lhs
  )

  rhs = _render_relation_side_latex(
    relation.rhs
  )

  if (
    relation.relation_type
    is RelationType.EQUALITY
  ):
    return (
      lhs
      + " = "
      + rhs
    )

  if (
    relation.relation_type
    is RelationType.ZERO
  ):
    return (
      lhs
      + " = 0"
    )

  if (
    relation.relation_type
    is RelationType.ORDER
  ):
    return (
      r"\operatorname{ord}\left("
      + lhs
      + r"\right) = "
      + rhs
    )

  if (
    relation.relation_type
    is RelationType.INEQUALITY
  ):
    return (
      lhs
      + r" \ne "
      + rhs
    )

  raise ValueError(
    "unsupported relation type"
  )


def render_toda_proof_statement_latex(
  statement,
) -> str | None:
  if isinstance(
    statement,
    Relation,
  ):
    return (
      _render_relation_latex(
        statement
      )
    )

  if isinstance(
    statement,
    TodaPrimaryGroupZeroStatement,
  ):
    return (
      render_toda_primary_group_latex(
        statement.group
      )
      + " = 0"
    )

  if isinstance(
    statement,
    TodaEHPExactnessWindow,
  ):
    return (
      _render_toda_exactness_window_latex(
        statement
      )
    )

  if isinstance(
    statement,
    TodaProp42ExactnessStatement,
  ):
    return (
      _render_toda_exactness_window_latex(
        statement.window
      )
      + r" \text{ is exact}"
    )

  if isinstance(
    statement,
    TodaDeltaInjectiveStatement,
  ):
    return (
      _render_toda_group_map_latex(
        statement.map
      )
      + r" \text{ is injective}"
    )

  if isinstance(
    statement,
    TodaHopfInvariantZeroStatement,
  ):
    return (
      _render_toda_group_map_latex(
        statement.map
      )
      + r" \text{ is the zero map}"
    )

  if isinstance(
    statement,
    TodaSuspensionSurjectiveStatement,
  ):
    return (
      _render_toda_group_map_latex(
        statement.map
      )
      + r" \text{ is surjective}"
    )

  if isinstance(
    statement,
    TodaDeltaImageUpToSignStatement,
  ):
    return (
      r"\Delta\left("
      + render_toda_expression_latex(
        statement.element
      )
      + r"\right)"
      + r" = \pm "
      + render_toda_expression_latex(
        statement.positive_value
      )
    )

  if isinstance(
    statement,
    TodaNuFamilyDefinitionStatement,
  ):
    return (
      render_toda_expression_latex(
        statement.element
      )
      + r" \text{ is the defined }"
      + r"\nu\text{-family element}"
    )

  if isinstance(
    statement,
    LiteratureStatement,
  ):
    return None

  return None


def _proof_role_label(
  role: TodaProofDependencyRole,
) -> str:
  labels = {
    TodaProofDependencyRole.EHP_EXACTNESS: (
      "EHP exactness"
    ),
    TodaProofDependencyRole.EHP_WINDOW: (
      "EHP window"
    ),
    TodaProofDependencyRole.GROUP_STRUCTURE: (
      "group structure"
    ),
    TodaProofDependencyRole.RELATION: (
      "relation"
    ),
    TodaProofDependencyRole.ORDER: (
      "order"
    ),
    TodaProofDependencyRole.MAP_PROPERTY: (
      "map property"
    ),
    TodaProofDependencyRole.DEFINITION: (
      "definition"
    ),
    TodaProofDependencyRole.LITERATURE: (
      "literature"
    ),
    TodaProofDependencyRole.OTHER: (
      "prerequisite"
    ),
  }

  return labels[
    role
  ]


def render_toda_proof_step_mathematical_markdown(
  step: TodaProofStepPresentation,
) -> str:
  if not isinstance(
    step,
    TodaProofStepPresentation,
  ):
    raise TypeError(
      "step must be a "
      "TodaProofStepPresentation"
    )

  statement_latex = (
    render_toda_proof_statement_latex(
      step.conclusion
    )
  )

  if statement_latex is None:
    return (
      "**"
      + _proof_role_label(
        step.role
      )
      + "** — `"
      + type(
        step.conclusion
      ).__name__
      + "`"
    )

  return (
    "**"
    + _proof_role_label(
      step.role
    )
    + "** — $"
    + statement_latex
    + "$"
  )


def _narrative_lead_for_step(
  step: TodaProofStepPresentation,
) -> str:
  source_step = step.source_step

  if (
    source_step.rule
    is ProofRule.GIVEN
  ):
    if (
      step.role
      is TodaProofDependencyRole.DEFINITION
    ):
      return "Definition"

    if (
      step.role
      is TodaProofDependencyRole.EHP_WINDOW
    ):
      return "Consider the EHP window"

    return "Use the input"

  if (
    step.role
    is TodaProofDependencyRole.EHP_EXACTNESS
  ):
    return "By exactness of the EHP sequence"

  if (
    step.role
    is TodaProofDependencyRole.MAP_PROPERTY
  ):
    return "From the preceding statements"

  if (
    step.role
    is TodaProofDependencyRole.GROUP_STRUCTURE
  ):
    return "Therefore the group structure is"

  if (
    step.role
    is TodaProofDependencyRole.RELATION
  ):
    return "Using the preceding results"

  if (
    step.role
    is TodaProofDependencyRole.ORDER
  ):
    return "Hence"

  if source_step.premises:
    return "From the preceding statements"

  return "Use the derived statement"


def render_toda_readable_proof_narrative_markdown(
  presentation: TodaEndToEndCandidatePresentation,
) -> str:
  if not isinstance(
    presentation,
    TodaEndToEndCandidatePresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaEndToEndCandidatePresentation"
    )

  lines = [
    "## Readable proof narrative",
    "",
  ]

  for index, node in enumerate(
    presentation.proof_flow.nodes,
    start=1,
  ):
    step = node.step

    statement_latex = (
      render_toda_proof_statement_latex(
        step.conclusion
      )
    )

    lead = (
      _narrative_lead_for_step(
        step
      )
    )

    if statement_latex is None:
      statement_text = (
        "`"
        + type(
          step.conclusion
        ).__name__
        + "`"
      )
    else:
      statement_text = (
        "$"
        + statement_latex
        + "$"
      )

    shared_suffix = ""

    if node.is_shared_dependency:
      shared_suffix = (
        " This statement is reused "
        + str(
          node.incoming_use_count
        )
        + " times."
      )

    lines.append(
      (
        str(index)
        + ". "
        + lead
        + ": "
        + statement_text
        + "."
        + shared_suffix
      )
    )

  return "\n".join(
    lines
  ) + "\n"
