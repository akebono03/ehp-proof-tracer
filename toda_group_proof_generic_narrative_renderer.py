import re
from expression import (
  Composition,
  HomotopyElement,
  Suspension,
  IteratedSuspension,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaDeltaMap,
  TodaHopfInvariantMap,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
  TodaSuspensionMap,
)
from proof import (
  ProofStep,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from toda_group_proof_aggregate_statement_renderer import (
  render_toda_group_proof_aggregate_statement_prose,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_provenance_catalog import (
  is_toda_group_proof_narrative_provenance_only_statement,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeSemanticSidecar,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_human_readable_renderer import (
  _render_scalar_latex,
  render_toda_expression_latex,
)
from toda_proof_narrative_renderer import (
  render_toda_primary_group_latex,
  render_toda_proof_statement_latex,
  render_toda_raw_group_structure_latex,
)
from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda45IsomorphismStatement,
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionIsomorphismStatement,
  Toda56Nu4DecompositionStatement,
  TodaDeltaInjectiveStatement,
  TodaDeltaKernelFreeCyclicStatement,
  TodaDeltaSurjectiveStatement,
  TodaDeltaZeroStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaIteratedSuspensionInjectiveStatement,
  TodaLemma513Statement,
  TodaLemma514Sigma8Statement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma54Statement,
  TodaNuFamilyDefinitionStatement,
  TodaProp27HopfInvariantUpToSignStatement,
  TodaProp42ExactnessStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  TodaProp44SuspensionInjectiveStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaProp53FiniteDimensionalStatement,
  TodaProp58FiniteDimensionalStatement,
  TodaProp59FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp511NuSquaredFiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp56FiniteDimensionalStatement,
  TodaSigmaFamilyDefinitionStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionIsomorphismStatement,
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


def _normalize_generic_eta_family_latex(
  latex: str,
) -> str:
  if not isinstance(
    latex,
    str,
  ):
    raise TypeError(
      "latex must be a str"
    )

  suspension_pattern = re.compile(
    r"E(?:\^\{(?P<exponent>[0-9]+)\})?"
    r"\\eta_\{(?P<index>[0-9]+)\}"
  )

  def replace_suspension(
    match,
  ):
    exponent_text = match.group(
      "exponent"
    )
    exponent = (
      1
      if exponent_text is None
      else int(
        exponent_text
      )
    )
    index = int(
      match.group(
        "index"
      )
    )

    return (
      r"\eta_{"
      + str(
        index + exponent
      )
      + "}"
    )

  normalized = suspension_pattern.sub(
    replace_suspension,
    latex,
  )

  factor_pattern = re.compile(
    r"\\eta_\{([0-9]+)\}"
  )
  matches = tuple(
    factor_pattern.finditer(
      normalized
    )
  )

  if not matches:
    return normalized

  replacements = []
  run_start = 0

  while run_start < len(
    matches
  ):
    run_end = run_start + 1
    first_index = int(
      matches[
        run_start
      ].group(
        1
      )
    )

    while run_end < len(
      matches
    ):
      previous = matches[
        run_end - 1
      ]
      current = matches[
        run_end
      ]

      between = normalized[
        previous.end():
        current.start()
      ]

      if between:
        break

      current_index = int(
        current.group(
          1
        )
      )

      if (
        current_index
        != first_index
        + (
          run_end
          - run_start
        )
      ):
        break

      run_end += 1

    run_length = (
      run_end
      - run_start
    )

    if run_length >= 2:
      replacements.append(
        (
          matches[
            run_start
          ].start(),
          matches[
            run_end - 1
          ].end(),
          (
            r"\eta_{"
            + str(
              first_index
            )
            + r"}^{"
            + str(
              run_length
            )
            + "}"
          ),
        )
      )

    run_start = run_end

  for start, end, replacement in reversed(
    replacements
  ):
    normalized = (
      normalized[
        :start
      ]
      + replacement
      + normalized[
        end:
      ]
    )

  return normalized


def _render_generic_narrative_expression_latex(
  expression,
) -> str:
  compact = _render_generic_eta_composition_latex(
    expression
  )
  if compact is not None:
    return compact

  if isinstance(
    expression,
    Suspension,
  ):
    suspended = expression.expression

    if isinstance(
      suspended,
      HomotopyElement,
    ):
      generator = suspended.generator

      if (
        generator is not None
        and generator.family == "η"
        and isinstance(
          generator.index,
          int,
        )
        and not isinstance(
          generator.index,
          bool,
        )
        and generator.decoration is None
      ):
        return (
          r"\eta_{"
          + str(
            generator.index + 1
          )
          + "}"
        )

  if isinstance(
    expression,
    IteratedSuspension,
  ):
    suspended = expression.expression
    exponent = expression.exponent

    if (
      isinstance(
        suspended,
        HomotopyElement,
      )
      and isinstance(
        exponent,
        int,
      )
      and not isinstance(
        exponent,
        bool,
      )
    ):
      generator = suspended.generator

      if (
        generator is not None
        and generator.family == "η"
        and isinstance(
          generator.index,
          int,
        )
        and not isinstance(
          generator.index,
          bool,
        )
        and generator.decoration is None
      ):
        return (
          r"\eta_{"
          + str(
            generator.index
            + exponent
          )
          + "}"
        )

  if isinstance(
    expression,
    Composition,
  ):
    return (
      _render_generic_narrative_expression_latex(
        expression.left
      )
      + _render_generic_narrative_expression_latex(
        expression.right
      )
    )

  return (
    _normalize_generic_eta_family_latex(
      render_toda_expression_latex(
        expression
      )
    )
  )


def _try_render_generic_narrative_expression_latex(
  expression,
) -> str | None:
  try:
    return render_toda_expression_latex(
      expression
    )
  except TypeError:
    return None


def _normalize_generic_narrative_statement_latex(
  statement,
  latex: str,
) -> str:
  if not isinstance(
    latex,
    str,
  ):
    raise TypeError(
      "latex must be a str"
    )

  normalized = (
    _normalize_generic_eta_family_latex(
      latex
    )
  )

  if not hasattr(
    statement,
    "lhs",
  ):
    return normalized

  if not hasattr(
    statement,
    "rhs",
  ):
    return normalized

  replacements = []
  search_start = 0

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

    expression_start = normalized.find(
      rendered_expression,
      search_start,
    )

    if expression_start < 0:
      continue

    expression_end = (
      expression_start
      + len(
        rendered_expression
      )
    )
    search_start = expression_end

    if (
      normalized_expression
      == rendered_expression
    ):
      continue

    replacements.append(
      (
        expression_start,
        expression_end,
        normalized_expression,
      )
    )

  for (
    expression_start,
    expression_end,
    normalized_expression,
  ) in reversed(
    replacements
  ):
    normalized = (
      normalized[
        :expression_start
      ]
      + normalized_expression
      + normalized[
        expression_end:
      ]
    )

  return (
    _normalize_generic_eta_family_latex(
      normalized
    )
  )


def _normalize_generic_narrative_step_latex(
  proof_step: ProofStep,
  latex: str,
) -> str:
  return (
    _normalize_generic_narrative_statement_latex(
      proof_step.conclusion,
      latex,
    )
  )


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


def _render_phase153_r3_6_component_latex(
  component,
) -> str | None:
  if isinstance(
    component,
    ScalarGreaterEqualStatement,
  ):
    return (
      _render_scalar_latex(
        component.left
      )
      + r" \ge "
      + _render_scalar_latex(
        component.right
      )
    )

  try:
    latex = (
      render_repository_conclusion_latex(
        component
      )
    )
  except (
    TypeError,
    ValueError,
  ):
    latex = None

  if latex is not None:
    return (
      _normalize_generic_narrative_statement_latex(
        component,
        latex,
      )
    )

  try:
    latex = (
      render_toda_proof_statement_latex(
        component
      )
    )
  except (
    TypeError,
    ValueError,
  ):
    return None

  return (
    _normalize_generic_narrative_statement_latex(
      component,
      latex,
    )
  )


def _render_phase153_r3_6_component_list_prose(
  components: tuple[
    object,
    ...,
  ],
) -> str | None:
  rendered = tuple(
    latex
    for latex in (
      _render_phase153_r3_6_component_latex(
        component
      )
      for component in components
    )
    if latex is not None
  )

  if not rendered:
    return None

  return (
    ", ".join(
      "$"
      + latex
      + "$"
      for latex in rendered
    )
    + " が成り立つ."
  )


def _render_phase153_r3_9_group_term_latex(
  group,
) -> str | None:
  if isinstance(
    group,
    TodaPrimaryGroup,
  ):
    return (
      render_toda_primary_group_latex(
        group
      )
    )

  if isinstance(
    group,
    DirectSumGroup,
  ):
    rendered_summands = tuple(
      _render_phase153_r3_9_group_term_latex(
        summand
      )
      for summand in group.summands
    )

    if any(
      rendered is None
      for rendered in rendered_summands
    ):
      return None

    return r" \oplus ".join(
      rendered
      for rendered in rendered_summands
      if rendered is not None
    )

  return None


def _render_phase153_r3_9_reference_statement_prose(
  statement,
) -> str | None:
  if isinstance(
    statement,
    TodaProp44IsomorphismStatement,
  ):
    decomposition_map = (
      statement.map
    )
    source_latex = (
      _render_phase153_r3_9_group_term_latex(
        decomposition_map.source_group
      )
    )
    target_latex = (
      _render_phase153_r3_9_group_term_latex(
        decomposition_map.target_group
      )
    )

    if (
      source_latex is None
      or target_latex is None
    ):
      return None

    return (
      "$("
      + render_toda_expression_latex(
        decomposition_map.beta
      )
      + ", "
      + render_toda_expression_latex(
        decomposition_map.gamma
      )
      + r") \mapsto "
      + render_toda_expression_latex(
        decomposition_map.formula
      )
      + ": "
      + source_latex
      + r" \to "
      + target_latex
      + "$ は同型写像である."
    )

  if isinstance(
    statement,
    TodaProp44SecondSummandRestrictionStatement,
  ):
    return (
      "分解写像の第二成分は $"
      + render_toda_expression_latex(
        statement.composition
      )
      + "$ で与えられる."
    )

  if isinstance(
    statement,
    TodaProp53FiniteDimensionalStatement,
  ):
    return (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.pi4_2_group_relation,
          statement.pi5_3_group_relation,
          statement.pi6_4_group_relation,
          statement.higher_eta_squared_group_relation,
          statement.higher_range,
        )
      )
    )

  if isinstance(
    statement,
    TodaProp58FiniteDimensionalStatement,
  ):
    return (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.pi6_2_group_relation,
          statement.pi7_3_group_relation,
          statement.pi8_4_group_relation,
          statement.pi9_5_group_relation,
          statement.higher_four_stem_zero,
          statement.higher_range,
        )
      )
    )

  if isinstance(
    statement,
    TodaProp59FiniteDimensionalStatement,
  ):
    return (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.pi7_2_group_relation,
          statement.pi8_3_group_relation,
          statement.pi9_4_group_relation,
          statement.pi10_5_group_relation,
          statement.pi11_6_group_relation,
          statement.higher_five_stem_zero,
          statement.higher_range,
        )
      )
    )

  if isinstance(
    statement,
    TodaProp511NuSquaredFiniteDimensionalStatement,
  ):
    return (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.pi11_5_group_relation,
          statement.pi12_6_group_relation,
          statement.pi13_7_group_relation,
          statement.pi14_8_group_relation,
          statement.higher_six_stem_group_relation,
          statement.higher_range,
        )
      )
    )

  if isinstance(
    statement,
    TodaDeltaKernelFreeCyclicStatement,
  ):
    map_latex = (
      _render_generic_narrative_group_map_latex(
        statement.map
      )
    )

    if map_latex is None:
      return None

    return (
      r"$\ker\Delta = "
      + render_toda_raw_group_structure_latex(
        statement.kernel_group
      )
      + "$ が成り立つ."
    )

  if isinstance(
    statement,
    TodaProp27HopfInvariantUpToSignStatement,
  ):
    return (
      "$H("
      + render_toda_expression_latex(
        statement.argument
      )
      + r") = \pm "
      + render_toda_expression_latex(
        statement.positive_value
      )
      + "$ が成り立つ."
    )

  return None


def _render_phase153_r3_6_reference_statement_prose(
  statement,
) -> str | None:
  if isinstance(
    statement,
    Toda52CompositionIsomorphismStatement,
  ):
    return (
      "$"
      + render_toda_expression_latex(
        statement.composition.left
      )
      + r"\circ -: "
      + render_toda_primary_group_latex(
        statement.source_group
      )
      + r" \to "
      + render_toda_primary_group_latex(
        statement.target_group
      )
      + "$ は同型写像である."
    )

  if isinstance(
    statement,
    Toda53NuPrimeBracketSpecializationStatement,
  ):
    return (
      "$"
      + render_toda_expression_latex(
        statement.nu_prime
      )
      + r" \in "
      + render_toda_expression_latex(
        statement
        .bracket_membership
        .bracket
      )
      + "$ が成り立つ."
    )

  if isinstance(
    statement,
    TodaLemma54Statement,
  ):
    membership = (
      statement.membership
    )
    membership_latex = (
      render_toda_expression_latex(
        membership.element
      )
      + r" \in \pi_{"
      + _render_scalar_latex(
        membership.group_dimension
      )
      + r"}^{"
      + _render_scalar_latex(
        membership.sphere_dimension
      )
      + "}"
    )
    relations = (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.hopf_relation,
          statement.double_suspension_relation,
        )
      )
    )

    if relations is None:
      return (
        "$"
        + membership_latex
        + "$."
      )

    return (
      "$"
      + membership_latex
      + "$, "
      + relations
    )

  if isinstance(
    statement,
    TodaProp51FiniteDimensionalStatement,
  ):
    return (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.pi3_2_group_relation,
          statement.eta2_hopf_relation,
          statement.delta_iota5_relation,
          statement.higher_eta_group_relation,
        )
      )
    )

  if isinstance(
    statement,
    TodaProp56FiniteDimensionalStatement,
  ):
    return (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.pi5_2_group_relation,
          statement.pi6_3_group_relation,
          statement.pi7_4_group_relation,
          statement.pi8_5_group_relation,
          statement.higher_nu_group_relation,
          statement.higher_range,
        )
      )
    )

  if isinstance(
    statement,
    Toda55NuFamilyFiniteDimensionalStatement,
  ):
    definition = (
      statement.nu_family_definition
    )
    definition_latex = (
      render_toda_expression_latex(
        definition.element
      )
      + " = "
      + render_toda_expression_latex(
        definition.iterated_suspension
      )
    )
    relations = (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.n_range,
          statement.double_nu_relation,
          statement.quadruple_nu_relation,
        )
      )
    )

    if relations is None:
      return (
        "$"
        + definition_latex
        + "$."
      )

    return (
      "$"
      + definition_latex
      + "$, "
      + relations
    )

  if isinstance(
    statement,
    TodaProp511FiniteDimensionalStatement,
  ):
    six_stem = (
      statement.nu_squared_finite_dimensional
    )

    return (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.pi8_2_group_relation,
          statement.pi9_3_zero,
          statement.pi10_4_group_relation,
          six_stem.pi11_5_group_relation,
          six_stem.pi12_6_group_relation,
          six_stem.pi13_7_group_relation,
          six_stem.pi14_8_group_relation,
          six_stem.higher_six_stem_group_relation,
          six_stem.higher_range,
        )
      )
    )

  if isinstance(
    statement,
    TodaProp515Pi12_5HopfIsomorphismStatement,
  ):
    return (
      "$H: "
      + render_toda_primary_group_latex(
        statement.map.source_group
      )
      + r" \xrightarrow{\cong} "
      + render_toda_raw_group_structure_latex(
        statement.image_group
      )
      + "$, $H("
      + render_toda_expression_latex(
        statement.source_generator
      )
      + ") = "
      + render_toda_expression_latex(
        statement.image_generator
      )
      + "$ が成り立つ."
    )

  if isinstance(
    statement,
    TodaLemma513Statement,
  ):
    return (
      "$"
      + render_toda_expression_latex(
        statement.sigma_triple_prime
      )
      + r" \in "
      + render_toda_expression_latex(
        statement.bracket
      )
      + "$, $H("
      + render_toda_expression_latex(
        statement.sigma_triple_prime
      )
      + ") = "
      + render_toda_expression_latex(
        statement.hopf_image
      )
      + "$ が成り立つ."
    )

  if isinstance(
    statement,
    Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  ):
    return (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.odd_parameter_statement,
          statement.bridge_relation,
        )
      )
    )

  if isinstance(
    statement,
    TodaLemma514SigmaPrimeStatement,
  ):
    return (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.double_relation,
          statement.hopf_relation,
        )
      )
    )

  if isinstance(
    statement,
    TodaLemma514Sigma8Statement,
  ):
    return (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.definition_relation,
          statement.hopf_relation,
          statement.suspension_relation,
          statement.double_suspension_relation,
        )
      )
    )

  return None


def _render_generic_narrative_statement_prose(
  statement,
) -> str | None:
  reference_prose = (
    _render_phase153_r3_9_reference_statement_prose(
      statement
    )
  )

  if reference_prose is not None:
    return reference_prose

  reference_prose = (
    _render_phase153_r3_6_reference_statement_prose(
      statement
    )
  )

  if reference_prose is not None:
    return reference_prose

  aggregate_prose = (
    render_toda_group_proof_aggregate_statement_prose(
      statement
    )
  )

  if aggregate_prose is not None:
    return aggregate_prose

  if isinstance(
    statement,
    Toda56Nu4DecompositionStatement,
  ):
    return (
      r"$\nu_{4}$ の分解を用いる."
    )

  if isinstance(
    statement,
    Toda56Nu4DecompositionIsomorphismStatement,
  ):
    return (
      r"$\nu_{4}$ の分解写像は同型写像である."
    )

  if isinstance(
    statement,
    TodaProp42ExactnessStatement,
  ):
    window = statement.window
    return (
      "$"
      + render_toda_primary_group_latex(
        window.source_term
      )
      + r" \xrightarrow{"
      + window.first_map.name
      + r"} "
      + render_toda_primary_group_latex(
        window.middle_term
      )
      + r" \xrightarrow{"
      + window.second_map.name
      + r"} "
      + render_toda_primary_group_latex(
        window.target_term
      )
      + "$ は完全である."
    )

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
    _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
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
      + "$ は同型写像である."
    )

  if isinstance(
    statement,
    _GENERIC_ZERO_MAP_STATEMENT_TYPES,
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
      + "$ は零写像である."
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

  if isinstance(
    statement,
    TodaSigmaFamilyDefinitionStatement,
  ):
    return (
      "$"
      + render_toda_expression_latex(
        statement.element
      )
      + r"$ を \(\sigma\)-family の元として定める."
    )

  return None

def _normalize_toda_group_proof_narrative_sentence_endings(
  prose: str,
) -> str:
  if not isinstance(
    prose,
    str,
  ):
    raise TypeError(
      "prose must be a str"
    )

  normalized_lines = []

  for line in prose.splitlines():
    stripped = line.rstrip()
    trailing = line[
      len(
        stripped
      ):
    ]
    has_japanese = any(
      (
        "\u3040" <= character <= "\u30ff"
        or "\u3400" <= character <= "\u9fff"
      )
      for character in stripped
    )

    if (
      has_japanese
      and stripped.endswith(
        "。"
      )
    ):
      stripped = (
        stripped[
          :-1
        ]
        + "."
      )

    normalized_lines.append(
      stripped
      + trailing
    )

  return "\n".join(
    normalized_lines
  )


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
    return (
      _normalize_toda_group_proof_narrative_sentence_endings(
        prose
      )
    )

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
  TodaDeltaSurjectiveStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaSuspensionSurjectiveStatement,
)


_GENERIC_ISOMORPHISM_STATEMENT_TYPES = (
  Toda45IsomorphismStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaSuspensionIsomorphismStatement,
)


_GENERIC_ZERO_MAP_STATEMENT_TYPES = (
  TodaDeltaZeroStatement,
  TodaHopfInvariantZeroStatement,
)


def _is_generic_narrative_provenance_only_statement(
  statement,
) -> bool:
  return (
    is_toda_group_proof_narrative_provenance_only_statement(
      statement
    )
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
    TodaIteratedSuspensionMap,
  ):
    exponent = group_map.exponent

    if isinstance(
      exponent,
      bool,
    ):
      return None

    if isinstance(
      exponent,
      int,
    ):
      if exponent < 1:
        return None

      if exponent == 1:
        return "E"

      exponent_latex = str(
        exponent
      )
    else:
      try:
        exponent_latex = (
          _render_scalar_latex(
            exponent
          )
        )
      except TypeError:
        return None

    return (
      r"E^{"
      + exponent_latex
      + "}"
    )

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


def _generic_short_exact_sequence_reason_prose(
  presentation: TodaGroupProofPresentation,
  exactness_step: ProofStep,
) -> str | None:
  short_exact_sequence_latex = (
    _generic_short_exact_sequence_latex(
      presentation,
      exactness_step,
    )
  )

  if short_exact_sequence_latex is None:
    return None

  return (
    "この完全性と, 左の写像が単射, "
    "右の写像が全射であることより, "
    "次の短完全列を得る."
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
  suppress_provenance_only: bool = False,
  preserve_provenance_step_ids: (
    frozenset[int]
    | None
  ) = None,
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

  if not isinstance(
    suppress_provenance_only,
    bool,
  ):
    raise TypeError(
      "suppress_provenance_only must be a bool"
    )

  if (
    preserve_provenance_step_ids is not None
    and not isinstance(
      preserve_provenance_step_ids,
      frozenset,
    )
  ):
    raise TypeError(
      "preserve_provenance_step_ids must be "
      "a frozenset or None"
    )

  if preserve_provenance_step_ids is None:
    preserve_provenance_step_ids = frozenset()

  for step_id in preserve_provenance_step_ids:
    if (
      not isinstance(
        step_id,
        int,
      )
      or isinstance(
        step_id,
        bool,
      )
    ):
      raise TypeError(
        "preserve_provenance_step_ids must "
        "contain only integers"
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
    if (
      suppress_provenance_only
      and id(
        proof_step
      ) not in preserve_provenance_step_ids
      and _is_generic_narrative_provenance_only_statement(
        proof_step.conclusion
      )
    ):
      continue

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
      reason_prose = (
        _generic_short_exact_sequence_reason_prose(
          presentation,
          proof_step,
        )
      )

      if reason_prose is None:
        raise ValueError(
          "short exact sequence reason prose "
          "must exist when the sequence exists"
        )

      lines.append(
        reason_prose
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
