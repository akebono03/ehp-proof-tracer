from expression import (
  Composition,
  HomotopyElement,
)
from homotopy_groups import (
  TodaDeltaMap,
  TodaHopfInvariantMap,
  TodaSuspensionMap,
)
from proof import (
  ProofStep,
)
from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeSemanticSidecar,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_human_readable_renderer import (
  render_toda_expression_latex,
)
from toda_proof_narrative_renderer import (
  render_toda_primary_group_latex,
  render_toda_proof_statement_latex,
)
from toda_rules import (
  TodaDeltaInjectiveStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaIteratedSuspensionInjectiveStatement,
  TodaNuFamilyDefinitionStatement,
  TodaProp42ExactnessStatement,
  TodaProp44SuspensionInjectiveStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionSurjectiveStatement,
)


_BLOCK_ROLE_LABELS = {
  TodaGroupProofNarrativeMathematicalBlockRole.TARGET:
    "証明対象",
  TodaGroupProofNarrativeMathematicalBlockRole.REFERENCE:
    "参照結果",
  TodaGroupProofNarrativeMathematicalBlockRole.PRECONDITION:
    "適用条件",
  TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION:
    "定義",
  TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP:
    "所属",
  TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION:
    "計算",
  TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS:
    "完全性",
  TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY:
    "写像の性質",
  TodaGroupProofNarrativeMathematicalBlockRole.ORDER:
    "位数",
  TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE:
    "群構造",
  TodaGroupProofNarrativeMathematicalBlockRole.CONCLUSION:
    "結論",
  TodaGroupProofNarrativeMathematicalBlockRole.OTHER:
    "その他",
}


def _generic_eta_composition_factors(
  expression,
) -> tuple[HomotopyElement, ...] | None:
  if isinstance(expression, Composition):
    left = _generic_eta_composition_factors(expression.left)
    right = _generic_eta_composition_factors(expression.right)
    if left is None or right is None:
      return None
    return left + right

  if not isinstance(expression, HomotopyElement):
    return None

  generator = expression.generator
  if (
    generator is None
    or generator.family != "η"
    or not isinstance(generator.index, int)
    or isinstance(generator.index, bool)
    or generator.decoration is not None
  ):
    return None

  return (expression,)


def _render_generic_eta_composition_latex(
  expression,
) -> str | None:
  factors = _generic_eta_composition_factors(expression)
  if factors is None or len(factors) < 2:
    return None

  indices = tuple(
    factor.generator.index
    for factor in factors
  )
  start_index = indices[0]
  if indices != tuple(
    range(start_index, start_index + len(factors))
  ):
    return None

  return (
    r"\eta_{"
    + str(start_index)
    + r"}^{"
    + str(len(factors))
    + "}"
  )


def _render_generic_narrative_expression_latex(
  expression,
) -> str:
  compact = _render_generic_eta_composition_latex(expression)
  if compact is not None:
    return compact

  if isinstance(expression, Composition):
    return (
      _render_generic_narrative_expression_latex(expression.left)
      + _render_generic_narrative_expression_latex(expression.right)
    )

  return render_toda_expression_latex(expression)


def _try_render_generic_narrative_expression_latex(
  expression,
) -> str | None:
  try:
    return render_toda_expression_latex(
      expression
    )
  except TypeError:
    return None


def _normalize_generic_narrative_step_latex(
  proof_step: ProofStep,
  latex: str,
) -> str:
  statement = proof_step.conclusion

  if not hasattr(
    statement,
    "lhs",
  ):
    return latex

  if not hasattr(
    statement,
    "rhs",
  ):
    return latex

  normalized = latex

  for expression in (
    statement.lhs,
    statement.rhs,
  ):
    rendered_expression = (
      _try_render_generic_narrative_expression_latex(
        expression
      )
    )

    if rendered_expression is None:
      continue

    normalized_expression = (
      _render_generic_narrative_expression_latex(
        expression
      )
    )

    if (
      normalized_expression
      == rendered_expression
    ):
      continue

    normalized = normalized.replace(
      rendered_expression,
      normalized_expression,
    )

  return normalized


def _render_generic_narrative_group_map_latex(
  group_map,
) -> str | None:
  map_name = _generic_group_map_name(
    group_map
  )

  if map_name is None:
    return None

  source_group = getattr(
    group_map,
    "source_group",
    None,
  )
  target_group = getattr(
    group_map,
    "target_group",
    None,
  )

  if (
    source_group is None
    or target_group is None
  ):
    return None

  return (
    map_name
    + ": "
    + render_toda_primary_group_latex(
      source_group
    )
    + r" \to "
    + render_toda_primary_group_latex(
      target_group
    )
  )


def _render_generic_narrative_statement_prose(
  statement,
) -> str | None:
  if isinstance(
    statement,
    _GENERIC_INJECTIVE_STATEMENT_TYPES,
  ):
    map_latex = (
      _render_generic_narrative_group_map_latex(
        statement.map
      )
    )

    if map_latex is None:
      return None

    return (
      "$"
      + map_latex
      + "$ は単射である."
    )

  if isinstance(
    statement,
    _GENERIC_SURJECTIVE_STATEMENT_TYPES,
  ):
    map_latex = (
      _render_generic_narrative_group_map_latex(
        statement.map
      )
    )

    if map_latex is None:
      return None

    return (
      "$"
      + map_latex
      + "$ は全射である."
    )

  if isinstance(
    statement,
    TodaNuFamilyDefinitionStatement,
  ):
    return (
      "$"
      + render_toda_expression_latex(
        statement.element
      )
      + r"$ を \(\nu\)-family の元として定める."
    )

  return None


def _render_generic_narrative_step(
  proof_step: ProofStep,
) -> str:
  if not isinstance(
    proof_step,
    ProofStep,
  ):
    raise TypeError(
      "proof_step must be a ProofStep"
    )

  statement = proof_step.conclusion

  prose = (
    _render_generic_narrative_statement_prose(
      statement
    )
  )

  if prose is not None:
    return prose

  try:
    latex = (
      render_repository_conclusion_latex(
        statement
      )
    )
  except (
    TypeError,
    ValueError,
  ):
    latex = None

  if latex is None:
    latex = (
      render_toda_proof_statement_latex(
        statement
      )
    )

  if latex is not None:
    latex = _normalize_generic_narrative_step_latex(
      proof_step,
      latex,
    )
    return (
      "$"
      + latex
      + "$"
    )

  if proof_step.inference_rule is not None:
    return proof_step.inference_rule.name

  return (
    "`"
    + type(
      statement
    ).__name__
    + "`"
  )


def _validate_generic_narrative_blocks(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
) -> None:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    blocks,
    tuple,
  ):
    raise TypeError(
      "blocks must be a tuple"
    )

  selected_step_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }

  seen_step_ids = set()

  for block in blocks:
    if not isinstance(
      block,
      TodaGroupProofNarrativeBlock,
    ):
      raise TypeError(
        "blocks must contain only "
        "TodaGroupProofNarrativeBlock objects"
      )

    for proof_step in block.steps:
      step_id = id(
        proof_step
      )

      if step_id not in selected_step_ids:
        raise ValueError(
          "block proof steps must appear "
          "in presentation nodes"
        )

      if step_id in seen_step_ids:
        raise ValueError(
          "blocks must not contain duplicate "
          "ProofStep objects"
        )

      seen_step_ids.add(
        step_id
      )

  if seen_step_ids != selected_step_ids:
    raise ValueError(
      "blocks must cover presentation nodes "
      "exactly once"
    )


def _generic_narrative_dependency_indices(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  block_index: int,
  semantic_sidecar: (
    TodaGroupProofNarrativeSemanticSidecar
    | None
  ) = None,
) -> tuple[
  int,
  ...,
]:
  if (
    semantic_sidecar is not None
    and semantic_sidecar.presentation
    is not presentation
  ):
    raise ValueError(
      "semantic_sidecar must belong to presentation"
    )

  step_block_index = {
    id(
      proof_step
    ): index
    for index, block in enumerate(
      blocks
    )
    for proof_step in block.steps
  }

  block = blocks[
    block_index
  ]
  block_step_ids = {
    id(
      proof_step
    )
    for proof_step in block.steps
  }

  dependency_indices = []

  for edge in presentation.edges:
    if id(
      edge.parent_step
    ) not in block_step_ids:
      continue

    dependency_index = (
      step_block_index[
        id(
          edge.premise_step
        )
      ]
    )

    if dependency_index == block_index:
      continue

    if dependency_index in dependency_indices:
      continue

    dependency_indices.append(
      dependency_index
    )

  if semantic_sidecar is not None:
    for semantic in (
      semantic_sidecar.dependency_semantics
    ):
      if id(
        semantic.dependent_step
      ) not in block_step_ids:
        continue

      dependency_index = (
        step_block_index[
          id(
            semantic.prerequisite_step
          )
        ]
      )

      if dependency_index == block_index:
        continue

      if dependency_index in dependency_indices:
        continue

      dependency_indices.append(
        dependency_index
      )

  return tuple(
    dependency_indices
  )


def _generic_narrative_proof_order_indices(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  semantic_sidecar: (
    TodaGroupProofNarrativeSemanticSidecar
    | None
  ) = None,
) -> tuple[
  int,
  ...,
]:
  _validate_generic_narrative_blocks(
    presentation,
    blocks,
  )

  if semantic_sidecar is None:
    semantic_sidecar = (
      build_toda_group_proof_narrative_semantic_sidecar(
        presentation
      )
    )

  if (
    semantic_sidecar.presentation
    is not presentation
  ):
    raise ValueError(
      "semantic_sidecar must belong to presentation"
    )

  ordered_indices = []
  visited_indices = set()
  active_indices = set()

  def visit(
    block_index: int,
  ) -> None:
    if block_index in visited_indices:
      return

    if block_index in active_indices:
      return

    active_indices.add(
      block_index
    )

    for dependency_index in (
      _generic_narrative_dependency_indices(
        presentation,
        blocks,
        block_index,
        semantic_sidecar=semantic_sidecar,
      )
    ):
      visit(
        dependency_index
      )

    active_indices.remove(
      block_index
    )
    visited_indices.add(
      block_index
    )
    ordered_indices.append(
      block_index
    )

  target_indices = tuple(
    index
    for index, block in enumerate(
      blocks
    )
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole.TARGET
    )
  )
  non_target_indices = tuple(
    index
    for index, block in enumerate(
      blocks
    )
    if (
      block.role
      is not TodaGroupProofNarrativeMathematicalBlockRole.TARGET
    )
  )

  for block_index in non_target_indices:
    visit(
      block_index
    )

  for block_index in target_indices:
    visit(
      block_index
    )

  return tuple(
    ordered_indices
  )


_GENERIC_INJECTIVE_STATEMENT_TYPES = (
  TodaDeltaInjectiveStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaIteratedSuspensionInjectiveStatement,
  TodaProp44SuspensionInjectiveStatement,
  TodaSuspensionInjectiveStatement,
)

_GENERIC_SURJECTIVE_STATEMENT_TYPES = (
  TodaHopfInvariantSurjectiveStatement,
  TodaSuspensionSurjectiveStatement,
)


def _generic_group_map_name(
  group_map,
) -> str | None:
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

  return None


def _generic_short_exact_sequence_latex(
  presentation: TodaGroupProofPresentation,
  exactness_step: ProofStep,
) -> str | None:
  statement = (
    exactness_step.conclusion
  )

  if not isinstance(
    statement,
    TodaProp42ExactnessStatement,
  ):
    return None

  window = statement.window
  first_map_name = getattr(
    window.first_map,
    "name",
    None,
  )
  second_map_name = getattr(
    window.second_map,
    "name",
    None,
  )

  injective_step = next(
    (
      node.proof_step
      for node in presentation.nodes
      if (
        isinstance(
          node.proof_step.conclusion,
          _GENERIC_INJECTIVE_STATEMENT_TYPES,
        )
        and (
          node.proof_step.conclusion.map.source_group
          == window.source_term
        )
        and (
          node.proof_step.conclusion.map.target_group
          == window.middle_term
        )
        and (
          _generic_group_map_name(
            node.proof_step.conclusion.map
          )
          == first_map_name
        )
      )
    ),
    None,
  )

  surjective_step = next(
    (
      node.proof_step
      for node in presentation.nodes
      if (
        isinstance(
          node.proof_step.conclusion,
          _GENERIC_SURJECTIVE_STATEMENT_TYPES,
        )
        and (
          node.proof_step.conclusion.map.source_group
          == window.middle_term
        )
        and (
          node.proof_step.conclusion.map.target_group
          == window.target_term
        )
        and (
          _generic_group_map_name(
            node.proof_step.conclusion.map
          )
          == second_map_name
        )
      )
    ),
    None,
  )

  if (
    injective_step is None
    or surjective_step is None
    or first_map_name is None
    or second_map_name is None
  ):
    return None

  return (
    r"0\longrightarrow "
    + render_toda_primary_group_latex(
      window.source_term
    )
    + r"\xrightarrow{"
    + first_map_name
    + "} "
    + render_toda_primary_group_latex(
      window.middle_term
    )
    + r"\xrightarrow{"
    + second_map_name
    + "} "
    + render_toda_primary_group_latex(
      window.target_term
    )
    + r"\longrightarrow 0"
  )


def _generic_narrative_dependency_labels(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  block_index: int,
) -> tuple[
  str,
  ...,
]:
  return tuple(
    "[B"
    + f"{dependency_index + 1:02d}"
    + "]"
    for dependency_index
    in _generic_narrative_dependency_indices(
      presentation,
      blocks,
      block_index,
    )
  )


def _generic_narrative_sentence_lead(
  role: TodaGroupProofNarrativeMathematicalBlockRole,
  dependency_labels: tuple[
    str,
    ...,
  ],
) -> str:
  if not isinstance(
    role,
    TodaGroupProofNarrativeMathematicalBlockRole,
  ):
    raise TypeError(
      "role must be a "
      "TodaGroupProofNarrativeMathematicalBlockRole"
    )

  if not isinstance(
    dependency_labels,
    tuple,
  ):
    raise TypeError(
      "dependency_labels must be a tuple"
    )

  if not dependency_labels:
    if (
      role
      is TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
    ):
      return "次の完全列を考える."

    return ""

  dependency_text = ", ".join(
    dependency_labels
  )

  if (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION
  ):
    return (
      dependency_text
      + " の条件のもとで, 次の定義を用いる."
    )

  if (
    role
    is TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
  ):
    return (
      dependency_text
      + " を用いて, 次の完全列を考える."
    )

  return (
    dependency_text
    + " より,"
  )


def _render_generic_narrative_proof_block(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  block_index: int,
  show_dependency_labels: bool = True,
) -> tuple[
  str,
  ...,
]:
  if not isinstance(
    show_dependency_labels,
    bool,
  ):
    raise TypeError(
      "show_dependency_labels must be a bool"
    )

  block = blocks[
    block_index
  ]

  if show_dependency_labels:
    dependency_labels = (
      _generic_narrative_dependency_labels(
        presentation,
        blocks,
        block_index,
      )
    )
  else:
    dependency_labels = ()

  sentence_lead = (
    _generic_narrative_sentence_lead(
      block.role,
      dependency_labels,
    )
  )

  lines = []

  if sentence_lead:
    lines.append(
      sentence_lead
    )
    lines.append(
      ""
    )

  for proof_step in block.steps:
    lines.append(
      _render_generic_narrative_step(
        proof_step
      )
    )
    lines.append(
      ""
    )

    short_exact_sequence_latex = (
      _generic_short_exact_sequence_latex(
        presentation,
        proof_step,
      )
    )

    if short_exact_sequence_latex is not None:
      lines.append(
        "この完全性と両端の写像の性質より, "
        "次の短完全列を得る."
      )
      lines.append(
        ""
      )
      lines.append(
        "$"
        + short_exact_sequence_latex
        + "$"
      )
      lines.append(
        ""
      )

  return tuple(
    lines
  )


def render_toda_group_proof_generic_narrative_markdown(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
) -> str:
  _validate_generic_narrative_blocks(
    presentation,
    blocks,
  )

  lines = [
    "# Generic group proof narrative",
    "",
  ]

  for block_index, block in enumerate(
    blocks
  ):
    block_number = (
      block_index
      + 1
    )
    role_label = (
      _BLOCK_ROLE_LABELS[
        block.role
      ]
    )

    lines.append(
      "## [B"
      + f"{block_number:02d}"
      + "] "
      + role_label
    )
    lines.append(
      ""
    )

    dependency_indices = (
      _generic_narrative_dependency_indices(
        presentation,
        blocks,
        block_index,
      )
    )

    if dependency_indices:
      dependency_labels = ", ".join(
        "[B"
        + f"{dependency_index + 1:02d}"
        + "]"
        for dependency_index
        in dependency_indices
      )

      lines.append(
        "依存: "
        + dependency_labels
      )
      lines.append(
        ""
      )

    for proof_step in block.steps:
      lines.append(
        "- "
        + _render_generic_narrative_step(
          proof_step
        )
      )

    lines.append(
      ""
    )

  return (
    "\n".join(
      lines
    ).rstrip()
    + "\n"
  )


def render_toda_group_proof_generic_proof_markdown(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
) -> str:
  _validate_generic_narrative_blocks(
    presentation,
    blocks,
  )

  lines = [
    "# Generic group proof",
    "",
  ]

  for block_index in (
    _generic_narrative_proof_order_indices(
      presentation,
      blocks,
    )
  ):
    lines.extend(
      _render_generic_narrative_proof_block(
        presentation,
        blocks,
        block_index,
      )
    )

  return (
    "\n".join(
      lines
    ).rstrip()
    + "\n"
  )
