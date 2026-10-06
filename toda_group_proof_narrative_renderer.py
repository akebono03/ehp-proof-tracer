import re
from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from homotopy_groups import (
  HomotopyEHPExactnessWindow,
  HomotopyGroup,
  TodaDeltaMap,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
  TodaPrimaryGroupMembershipStatement,
  TodaProp44DecompositionMap,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionMap,
)
from proof import (
  ProofStep,
  Relation,
  RelationType,
  FoundationalReferenceIdentity,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
  _GENERIC_INJECTIVE_STATEMENT_TYPES,
  _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
  _GENERIC_SURJECTIVE_STATEMENT_TYPES,
  _render_generic_narrative_group_map_latex,
  _generic_group_map_name,
  _GENERIC_ZERO_MAP_STATEMENT_TYPES,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  build_toda_group_proof_narrative_reference_reuse_marker_by_step_id,
  link_toda_group_proof_narrative_reference_body_consumers,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
  suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry,
  suppress_toda_group_proof_narrative_reference_body_duplicates,
  suppress_toda_group_proof_narrative_reference_body_restatements,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_method_renderer import (
  render_toda_group_proof_narrative_exactness_method_component_latex,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
  TodaGroupProofNarrativeDependencySemanticRole,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  filter_toda_group_proof_narrative_reference_entries_by_body_usage,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
  render_toda_group_proof_narrative_reference_entries_markdown,
)
from toda_group_proof_narrative_provenance_catalog import (
  is_toda_group_proof_narrative_provenance_only_statement,
)
from toda_group_proof_narrative_helpers import (
  root_generator,
  root_target_group,
)
from toda_group_proof_narrative_classifier import (
  TodaGroupProofNarrativeBlockRole,
  TodaGroupProofNarrativeFactRole,
  classify_toda_group_proof_narrative_step,
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
  Toda48Pi16_9OrderAndE4InjectiveStatement,
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionIsomorphismStatement,
  Toda56Nu4DecompositionStatement,
  Toda58WhiteheadSquareUpToSignStatement,
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaKernelFreeCyclicStatement,
  TodaDeltaSurjectiveStatement,
  TodaDeltaZeroStatement,
  TodaEtaFamilyDefinitionStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaIteratedSuspensionInjectiveStatement,
  TodaLemma513Statement,
  TodaLemma514Sigma8Statement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma54Statement,
  TodaPi32Eta2DefinitionStatement,
  TodaPi32WhiteheadSquareUpToSignStatement,
  TodaProp27HopfInvariantUpToSignStatement,
  TodaProp42ExactnessStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp56FiniteDimensionalStatement,
  TodaProp56Pi8_5QuotientStatement,
  TodaSigmaFamilyDefinitionStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionKernelFreeCyclicStatement,
)

def _group_proof_narrative_statement_label(
  statement,
) -> str | None:
  if isinstance(
    statement,
    Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  ):
    return (
      "Theorem 3.6 と Lemma 5.14 を結ぶ σ″ の関係"
    )

  if isinstance(
    statement,
    Toda48Pi16_9OrderAndE4InjectiveStatement,
  ):
    return (
      "π₁₆⁹ の位数 16 と E⁴ の単射性"
    )

  if isinstance(
    statement,
    Toda52CompositionIsomorphismStatement,
  ):
    return "Toda (5.2) の η₂ 合成同型"

  if isinstance(
    statement,
    Toda53NuPrimeBracketSpecializationStatement,
  ):
    return (
      "ν′ に対する Lemma 5.2 の Toda bracket 特殊化"
    )

  if isinstance(
    statement,
    Toda55NuFamilyFiniteDimensionalStatement,
  ):
    return (
      "Toda (5.5) の ν-family 有限次元結果"
    )

  if isinstance(
    statement,
    Toda56Nu4DecompositionIsomorphismStatement,
  ):
    return "Toda (5.6) の ν₄ 分解同型"

  if isinstance(
    statement,
    Toda56Nu4DecompositionStatement,
  ):
    return "Toda (5.6) の ν₄ 分解"

  if isinstance(
    statement,
    TodaDeltaZeroStatement,
  ):
    return "Δ 写像が零写像であること"

  if isinstance(
    statement,
    TodaHopfInvariantInjectiveStatement,
  ):
    return "Hopf 写像の単射性"

  if isinstance(
    statement,
    TodaIteratedSuspensionInjectiveStatement,
  ):
    return "E²: π₆³ → π₈⁵ の単射性"

  if isinstance(
    statement,
    TodaLemma513Statement,
  ):
    return (
      "Toda Lemma 5.13 の σ‴ に関する結果"
    )

  if isinstance(
    statement,
    TodaLemma514Sigma8Statement,
  ):
    return (
      "Toda Lemma 5.14 の σ₈ に関する結果"
    )

  if isinstance(
    statement,
    TodaLemma514SigmaPrimeStatement,
  ):
    return "Toda Lemma 5.14 の σ′ に関する結果"

  if isinstance(
    statement,
    TodaLemma54Statement,
  ):
    return "Toda Lemma 5.4 の結果"

  if isinstance(
    statement,
    TodaProp51FiniteDimensionalStatement,
  ):
    return (
      "Toda Proposition 5.1 の有限次元結果"
    )

  if isinstance(
    statement,
    TodaProp511FiniteDimensionalStatement,
  ):
    return (
      "Toda Proposition 5.11 の有限次元結果"
    )

  if isinstance(
    statement,
    TodaProp515Pi12_5HopfIsomorphismStatement,
  ):
    return (
      "π₁₂⁵ の位数 2 の Hopf 像への同型"
    )

  if isinstance(
    statement,
    TodaProp56FiniteDimensionalStatement,
  ):
    return (
      "Toda Proposition 5.6 の有限次元結果"
    )

  if isinstance(
    statement,
    TodaProp56Pi8_5QuotientStatement,
  ):
    return (
      "π₈⁵ / E²π₆³ が位数 2 であること"
    )

  if isinstance(
    statement,
    TodaEtaFamilyDefinitionStatement,
  ):
    return "η-family の定義"

  if isinstance(
    statement,
    TodaSigmaFamilyDefinitionStatement,
  ):
    return "σ-family の定義"

  return None


def _render_finite_dimensional_aggregate_statement_latex(
  statement,
) -> str | None:
  target_names = {
    "TodaProp53FiniteDimensionalStatement",
    "TodaProp58FiniteDimensionalStatement",
    "TodaProp59FiniteDimensionalStatement",
    "TodaProp511NuSquaredFiniteDimensionalStatement",
  }

  if type(statement).__name__ not in target_names:
    return None

  parts = []
  range_latex = None

  for field_name in statement.__dataclass_fields__:
    value = getattr(
      statement,
      field_name,
    )

    if isinstance(
      value,
      Relation,
    ):
      if (
        value.relation_type
        != RelationType.EQUALITY
      ):
        return None

      parts.append(
        render_toda_primary_group_latex(
          value.lhs
        )
        + " = "
        + render_toda_raw_group_structure_latex(
          value.rhs
        )
      )
      continue

    if (
      type(value).__name__
      == "TodaPrimaryGroupZeroStatement"
    ):
      parts.append(
        render_toda_primary_group_latex(
          value.group
        )
        + " = 0"
      )
      continue

    if (
      type(value).__name__
      == "ScalarGreaterEqualStatement"
    ):
      range_latex = (
        _render_scalar_latex(
          value.left
        )
        + r" \ge "
        + _render_scalar_latex(
          value.right
        )
      )

  if not parts:
    return None

  latex = r",\quad ".join(parts)

  if range_latex is not None:
    latex += (
      r"\qquad ("
      + range_latex
      + ")"
    )

  return latex




def _render_prop44_suspension_injective_statement_latex(
  statement,
) -> str | None:
  if (
    type(statement).__name__
    != "TodaProp44SuspensionInjectiveStatement"
  ):
    return None

  suspension_map = statement.map

  return (
    "E: "
    + render_toda_primary_group_latex(
      suspension_map.source_group
    )
    + r" \hookrightarrow "
    + render_toda_primary_group_latex(
      suspension_map.target_group
    )
  )

def _render_group_proof_narrative_latex(
  proof_step: ProofStep,
) -> str | None:
  if not isinstance(
    proof_step,
    ProofStep,
  ):
    raise TypeError(
      "proof_step must be a ProofStep"
    )

  statement = proof_step.conclusion


  prop44_suspension_injective_latex = (
    _render_prop44_suspension_injective_statement_latex(
      statement
    )
  )

  if (
    prop44_suspension_injective_latex
    is not None
  ):
    return prop44_suspension_injective_latex


  finite_dimensional_latex = (
    _render_finite_dimensional_aggregate_statement_latex(
      statement
    )
  )

  if finite_dimensional_latex is not None:
    return finite_dimensional_latex

  if isinstance(
    statement,
    HomotopyGroup,
  ):
    return (
      r"\pi_{"
      + _render_scalar_latex(
        statement.group_dimension
      )
      + r"}^{"
      + _render_scalar_latex(
        statement.sphere_dimension
      )
      + "}"
    )

  if isinstance(
    statement,
    HomotopyEHPExactnessWindow,
  ):
    return (
      r"\pi_{"
      + _render_scalar_latex(
        statement.source_term.group_dimension
      )
      + r"}^{"
      + _render_scalar_latex(
        statement.source_term.sphere_dimension
      )
      + r"} \xrightarrow{"
      + statement.first_map.name
      + r"} \pi_{"
      + _render_scalar_latex(
        statement.middle_term.group_dimension
      )
      + r"}^{"
      + _render_scalar_latex(
        statement.middle_term.sphere_dimension
      )
      + r"} \xrightarrow{"
      + statement.second_map.name
      + r"} \pi_{"
      + _render_scalar_latex(
        statement.target_term.group_dimension
      )
      + r"}^{"
      + _render_scalar_latex(
        statement.target_term.sphere_dimension
      )
      + "}"
    )

  if isinstance(
    statement,
    TodaPi32Eta2DefinitionStatement,
  ):
    return (
      "H("
      + render_toda_expression_latex(
        statement.element
      )
      + ") = "
      + render_toda_expression_latex(
        statement.image
      )
    )

  if isinstance(
    statement,
    (
      TodaPi32WhiteheadSquareUpToSignStatement,
      Toda58WhiteheadSquareUpToSignStatement,
    ),
  ):
    return (
      render_toda_expression_latex(
        statement.whitehead_square
      )
      + r" = \pm "
      + render_toda_expression_latex(
        statement.positive_value
      )
    )

  if isinstance(
    statement,
    TodaProp27HopfInvariantUpToSignStatement,
  ):
    return (
      "H("
      + render_toda_expression_latex(
        statement.argument
      )
      + r") = \pm "
      + render_toda_expression_latex(
        statement.positive_value
      )
    )

  if isinstance(
    statement,
    TodaPrimaryGroupMembershipStatement,
  ):
    return (
      render_toda_expression_latex(
        statement.element
      )
      + r" \in "
      + render_toda_primary_group_latex(
        statement.group
      )
    )

  if isinstance(
    statement,
    TodaProp44IsomorphismStatement,
  ):
    return (
      r"\left("
      + render_toda_expression_latex(
        statement.map.beta
      )
      + r", "
      + render_toda_expression_latex(
        statement.map.gamma
      )
      + r"\right) \mapsto "
      + render_toda_expression_latex(
        statement.map.formula
      )
      + r"\quad\text{は同型写像}"
    )

  if isinstance(
    statement,
    TodaSuspensionIsomorphismStatement,
  ):
    return (
      r"E: "
      + render_toda_primary_group_latex(
        statement.map.source_group
      )
      + r" \xrightarrow{\cong} "
      + render_toda_primary_group_latex(
        statement.map.target_group
      )
    )

  if isinstance(
    statement,
    Toda45IsomorphismStatement,
  ):
    return (
      r"E^{"
      + _render_scalar_latex(
        statement.map.exponent
      )
      + r"}: "
      + render_toda_primary_group_latex(
        statement.map.source_group
      )
      + r" \xrightarrow{\cong} "
      + render_toda_primary_group_latex(
        statement.map.target_group
      )
    )

  if isinstance(
    statement,
    TodaHopfInvariantIsomorphismStatement,
  ):
    return (
      r"H: "
      + render_toda_primary_group_latex(
        statement.map.source_group
      )
      + r" \xrightarrow{\cong} "
      + render_toda_primary_group_latex(
        statement.map.target_group
      )
    )

  if isinstance(
    statement,
    TodaProp44SecondSummandRestrictionStatement,
  ):
    return (
      render_toda_expression_latex(
        statement.decomposition_map.gamma
      )
      + r" \mapsto "
      + render_toda_expression_latex(
        statement.composition
      )
    )

  if isinstance(
    statement,
    TodaSuspensionMap,
  ):
    return (
      "E: "
      + render_toda_primary_group_latex(
        statement.source_group
      )
      + r" \to "
      + render_toda_primary_group_latex(
        statement.target_group
      )
    )

  if isinstance(
    statement,
    TodaDeltaSurjectiveStatement,
  ):
    return (
      r"\Delta: "
      + render_toda_primary_group_latex(
        statement.map.source_group
      )
      + r" \twoheadrightarrow "
      + render_toda_primary_group_latex(
        statement.map.target_group
      )
    )

  if isinstance(
    statement,
    TodaSuspensionKernelFreeCyclicStatement,
  ):
    return (
      r"\ker\left(E: "
      + render_toda_primary_group_latex(
        statement.map.source_group
      )
      + r" \to "
      + render_toda_primary_group_latex(
        statement.map.target_group
      )
      + r"\right) = "
      + render_toda_raw_group_structure_latex(
        statement.kernel_group
      )
    )

  if isinstance(
    statement,
    TodaDeltaImageFreeCyclicStatement,
  ):
    return (
      r"\operatorname{Im}\left(\Delta: "
      + render_toda_primary_group_latex(
        statement.map.source_group
      )
      + r" \to "
      + render_toda_primary_group_latex(
        statement.map.target_group
      )
      + r"\right) = "
      + render_toda_raw_group_structure_latex(
        statement.image_group
      )
    )

  if isinstance(
    statement,
    TodaDeltaKernelFreeCyclicStatement,
  ):
    return (
      r"\ker\left(\Delta: "
      + render_toda_primary_group_latex(
        statement.map.source_group
      )
      + r" \to "
      + render_toda_primary_group_latex(
        statement.map.target_group
      )
      + r"\right) = "
      + render_toda_raw_group_structure_latex(
        statement.kernel_group
      )
    )

  if isinstance(
    statement,
    TodaIteratedSuspensionMap,
  ):
    return (
      r"E^{"
      + _render_scalar_latex(
        statement.exponent
      )
      + r"}: "
      + render_toda_primary_group_latex(
        statement.source_group
      )
      + r" \to "
      + render_toda_primary_group_latex(
        statement.target_group
      )
    )

  if isinstance(
    statement,
    TodaDeltaMap,
  ):
    return (
      r"\Delta: "
      + render_toda_primary_group_latex(
        statement.source_group
      )
      + r" \to "
      + render_toda_primary_group_latex(
        statement.target_group
      )
    )

  if isinstance(
    statement,
    TodaProp44DecompositionMap,
  ):
    return (
      r"("
      + render_toda_expression_latex(
        statement.beta
      )
      + r", "
      + render_toda_expression_latex(
        statement.gamma
      )
      + r") \mapsto "
      + render_toda_expression_latex(
        statement.formula
      )
    )

  if isinstance(
    statement,
    ScalarGreaterEqualStatement,
  ):
    return (
      _render_scalar_latex(
        statement.left
      )
      + r" \ge "
      + _render_scalar_latex(
        statement.right
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

  if latex is not None:
    return latex

  return (
    render_toda_proof_statement_latex(
      statement
    )
  )


def _render_group_proof_narrative_fact(
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

  generic_fact = (
    _render_generic_narrative_step(
      proof_step
    )
  )
  internal_fallbacks = {
    (
      proof_step.inference_rule.name
      if proof_step.inference_rule is not None
      else None
    ),
    (
      "`"
      + type(
        statement
      ).__name__
      + "`"
    ),
  }

  if (
    generic_fact
    and generic_fact not in internal_fallbacks
  ):
    return generic_fact

  latex = (
    _render_group_proof_narrative_latex(
      proof_step
    )
  )

  if latex is not None:
    return (
      "$"
      + latex
      + "$"
    )

  label = (
    _group_proof_narrative_statement_label(
      statement
    )
  )

  if label is not None:
    return label

  return "補助結果"

def _narrative_edges_for_parent(
  presentation: TodaGroupProofPresentation,
  parent_step: ProofStep,
):
  return tuple(
    sorted(
      (
        edge
        for edge in presentation.edges
        if edge.parent_step is parent_step
      ),
      key=lambda edge: edge.premise_index,
    )
  )


def _premise_lead(
  premise_number: int,
  premise_count: int,
) -> str:
  if premise_count <= 0:
    raise ValueError(
      "premise_count must be positive"
    )

  if (
    premise_number < 0
    or premise_number >= premise_count
  ):
    raise ValueError(
      "premise_number must be within "
      "the premise range"
    )

  if premise_number == 0:
    return "まず"

  if premise_number == premise_count - 1:
    return "さらに"

  return "また"


def _derivation_lead(
  premise_count: int,
) -> str:
  if premise_count <= 0:
    raise ValueError(
      "premise_count must be positive"
    )

  if premise_count == 1:
    return "このことから"

  return "これらから"


def _is_phase134_3_pi6_3_presentation(
  presentation: TodaGroupProofPresentation,
) -> bool:
  target = (
    presentation
    .source_replay
    .group_result
    .target
  )

  return (
    target.group_dimension == 6
    and target.sphere_dimension == 3
    and presentation.source_entry.theorem
    == "Toda Proposition 5.6"
  )


def _is_phase134_5_reference_step(
  proof_step: ProofStep,
) -> bool:
  return isinstance(
    proof_step.conclusion,
    (
      Toda52CompositionIsomorphismStatement,
      TodaProp51FiniteDimensionalStatement,
    ),
  )


def _phase134_5_pi6_3_ordered_steps(
  presentation: TodaGroupProofPresentation,
) -> tuple[
  ProofStep,
  ...,
]:
  ordered_steps = []
  visited_step_ids = set()
  active_step_ids = set()

  def visit(
    proof_step: ProofStep,
  ) -> None:
    step_id = id(
      proof_step
    )

    if step_id in visited_step_ids:
      return

    if step_id in active_step_ids:
      return

    active_step_ids.add(
      step_id
    )

    if not _is_phase134_5_reference_step(
      proof_step
    ):
      for edge in (
        _narrative_edges_for_parent(
          presentation,
          proof_step,
        )
      ):
        visit(
          edge.premise_step
        )

    active_step_ids.remove(
      step_id
    )

    visited_step_ids.add(
      step_id
    )

    ordered_steps.append(
      proof_step
    )

  visit(
    presentation.root_step
  )

  return tuple(
    ordered_steps
  )


def _phase134_5_pi6_3_reference_steps(
  presentation: TodaGroupProofPresentation,
) -> tuple[
  ProofStep,
  ...,
]:
  return _phase134_9_reference_steps(
    presentation
  )

def _phase134_5_reference_title(
  proof_step: ProofStep,
) -> str:
  statement = proof_step.conclusion

  if isinstance(
    statement,
    Toda52CompositionIsomorphismStatement,
  ):
    return "Toda (5.2) の η₂ 合成同型"

  if isinstance(
    statement,
    TodaProp51FiniteDimensionalStatement,
  ):
    return (
      "Toda Proposition 5.1 の有限次元結果"
    )

  raise ValueError(
    "unsupported Phase 134-5 reference step"
  )


def _phase134_5_reference_statement_lines(
  proof_step: ProofStep,
) -> tuple[
  str,
  ...,
]:
  statement = proof_step.conclusion

  if isinstance(
    statement,
    Toda52CompositionIsomorphismStatement,
  ):
    composition_element = (
      statement.composition.left
    )

    latex = (
      render_toda_expression_latex(
        composition_element
      )
      + r"\circ - : "
      + render_toda_primary_group_latex(
        statement.source_group
      )
      + r" \longrightarrow "
      + render_toda_primary_group_latex(
        statement.target_group
      )
      + "."
    )

    return (
      "次の合成写像は同型である.",
      "",
      r"\[",
      latex,
      r"\]",
    )

  if isinstance(
    statement,
    TodaProp51FiniteDimensionalStatement,
  ):
    latex = (
      render_repository_conclusion_latex(
        statement.higher_eta_group_relation
      )
      + r"\qquad (n \ge 3)."
    )

    return (
      "次の群構造を用いる.",
      "",
      r"\[",
      latex,
      r"\]",
    )

  raise ValueError(
    "unsupported Phase 134-5 reference step"
  )

def _phase134_5_dependency_text(
  presentation: TodaGroupProofPresentation,
  proof_step: ProofStep,
  number_by_step_id: dict[
    int,
    int,
  ],
  reference_by_step_id: dict[
    int,
    str,
  ],
) -> str:
  dependency_labels = []

  for edge in (
    _narrative_edges_for_parent(
      presentation,
      proof_step,
    )
  ):
    premise_id = id(
      edge.premise_step
    )

    reference_label = (
      reference_by_step_id.get(
        premise_id
      )
    )

    if reference_label is not None:
      dependency_labels.append(
        "["
        + reference_label
        + "]"
      )
      continue

    premise_number = (
      number_by_step_id.get(
        premise_id
      )
    )

    if premise_number is not None:
      dependency_labels.append(
        "("
        + str(
          premise_number
        )
        + ")"
      )

  return ", ".join(
    dependency_labels
  )


def _is_phase134_9_reference_step(
  presentation: TodaGroupProofPresentation,
  proof_step: ProofStep,
) -> bool:
  classification = (
    classify_toda_group_proof_narrative_step(
      presentation,
      proof_step,
    )
  )

  return (
    classification.fact_role
    is TodaGroupProofNarrativeFactRole.REFERENCE
  )


def _phase134_9_ordered_steps(
  presentation: TodaGroupProofPresentation,
) -> tuple[
  ProofStep,
  ...,
]:
  ordered_steps = []
  visited_step_ids = set()
  active_step_ids = set()

  def visit(
    proof_step: ProofStep,
  ) -> None:
    step_id = id(
      proof_step
    )

    if step_id in visited_step_ids:
      return

    if step_id in active_step_ids:
      return

    active_step_ids.add(
      step_id
    )

    if not _is_phase134_9_reference_step(
      presentation,
      proof_step,
    ):
      for edge in (
        _narrative_edges_for_parent(
          presentation,
          proof_step,
        )
      ):
        visit(
          edge.premise_step
        )

    active_step_ids.remove(
      step_id
    )

    visited_step_ids.add(
      step_id
    )

    ordered_steps.append(
      proof_step
    )

  visit(
    presentation.root_step
  )

  return tuple(
    ordered_steps
  )


def _phase134_9_numbered_steps(
  presentation: TodaGroupProofPresentation,
) -> tuple[
  ProofStep,
  ...,
]:
  return tuple(
    proof_step
    for proof_step in (
      _phase134_9_ordered_steps(
        presentation
      )
    )
    if not _is_phase134_9_reference_step(
      presentation,
      proof_step,
    )
  )


def _phase134_9_reference_steps(
  presentation: TodaGroupProofPresentation,
) -> tuple[
  ProofStep,
  ...,
]:
  return tuple(
    proof_step
    for proof_step in (
      _phase134_9_ordered_steps(
        presentation
      )
    )
    if _is_phase134_9_reference_step(
      presentation,
      proof_step,
    )
  )


def _phase134_3_pi6_3_numbered_steps(
  presentation: TodaGroupProofPresentation,
) -> tuple[
  ProofStep,
  ...,
]:
  return _phase134_9_numbered_steps(
    presentation
  )

def _phase134_6_boundary_fact_latex(
  statement,
) -> tuple[
  str | None,
  str | None,
]:
  if isinstance(
    statement,
    TodaDeltaZeroStatement,
  ):
    group_map = statement.map

    latex = (
      r"\Delta: "
      + render_toda_primary_group_latex(
        group_map.source_group
      )
      + r" \to "
      + render_toda_primary_group_latex(
        group_map.target_group
      )
    )

    return (
      latex,
      "は零写像である.",
    )

  if isinstance(
    statement,
    Toda53NuPrimeBracketSpecializationStatement,
  ):
    latex = (
      render_repository_conclusion_latex(
        statement.bracket_membership
      )
    )

    return (
      latex,
      None,
    )

  return (
    None,
    None,
  )


def _phase134_3_reference_text(
  premise_numbers: tuple[
    int,
    ...,
  ],
) -> str:
  return ", ".join(
    (
      "("
      + str(
        number
      )
      + ")"
    )
    for number in premise_numbers
  )


def _strip_phase134_3_latex_suffix(
  latex: str | None,
  suffix: str,
) -> str | None:
  if latex is None:
    return None

  if latex.endswith(
    suffix
  ):
    return latex[
      :-len(
        suffix
      )
    ]

  return latex


def _phase136_compact_eta_powers(
  latex: str,
) -> str:
  if not isinstance(
    latex,
    str,
  ):
    raise TypeError(
      "latex must be a str"
    )

  replacements = (
    (
      r"\eta_{2}\eta_{3}\eta_{4}",
      r"\eta_{2}^{3}",
    ),
    (
      r"\eta_{3}\eta_{4}\eta_{5}",
      r"\eta_{3}^{3}",
    ),
    (
      r"\eta_{2}\eta_{3}",
      r"\eta_{2}^{2}",
    ),
    (
      r"\eta_{3}\eta_{4}",
      r"\eta_{3}^{2}",
    ),
  )

  rendered = latex

  for old, new in replacements:
    rendered = rendered.replace(
      old,
      new,
    )

  return rendered


def _phase136_2_pi6_3_reference_blocks() -> tuple[
  tuple[
    str,
    tuple[str, ...],
  ],
  ...,
]:
  return (
    (
      "Toda Proposition 5.3",
      (
        r"\[",
        (
          r"\pi_{n + 2}^{n} = "
          r"\mathbb{Z}/2\{\eta_{n}^{2}\}"
          r"\qquad (n \ge 2)."
        ),
        r"\]",
        "",
        r"\[",
        (
          r"\pi_{5}^{3} = "
          r"\mathbb{Z}/2\{\eta_{3}^{2}\},"
          r"\qquad"
          r"\pi_{7}^{5} = "
          r"\mathbb{Z}/2\{\eta_{5}^{2}\}."
        ),
        r"\]",
      ),
    ),
    (
      "Toda Lemma 5.2",
      (
        "まず Lemma 5.2 の一般形を記す.",
        "",
        "$\\alpha\\in\\pi_i^3$, $2\\alpha=0$ であり,",
        "",
        r"\[",
        r"\beta \in \{\eta_{3},2\iota_{4},E\alpha\}_{1}",
        r"\]",
        "",
        "ならば,",
        "",
        r"\[",
        r"\beta\in\pi_{i+2}^{3},",
        r"\qquad",
        r"H(\beta)=E^{2}\alpha,",
        r"\qquad",
        r"2\beta=\eta_{3}\circ E\alpha\circ\eta_{i+1},",
        r"\qquad",
        r"\Delta(E^{2}\alpha)=0.",
        r"\]",
        "",
        (
          "この証明では $\\alpha=\\eta_{3}$, "
          "$i=4$ とする. まず $2\\eta_{3}=0$ "
          "を確認すると, Toda bracket"
        ),
        "",
        r"\[",
        r"\{\eta_{3},2\iota_{4},\eta_{4}\}_{1}",
        r"\]",
        "",
        (
          "が定義できる. この bracket のある元を "
          "$\\nu'$ と定める. すなわち,"
        ),
        "",
        r"\[",
        r"\nu' \in \{\eta_{3},2\iota_{4},\eta_{4}\}_{1}.",
        r"\]",
        "",
        "すると Lemma 5.2 より,",
        "",
        r"\[",
        r"\nu'\in\pi_{6}^{3},",
        r"\qquad",
        r"H(\nu')=E^{2}\eta_{3},",
        r"\qquad",
        r"2\nu'=\eta_{3}\circ E\eta_{3}\circ\eta_{5},",
        r"\qquad",
        r"\Delta(E^{2}\eta_{3})=0",
        r"\]",
        "",
        "を得る.",
      ),
    ),
    (
      "Toda Proposition 2.2 の右合成公式",
      (
        r"\[",
        r"H(\alpha\circ E\beta)=H(\alpha)\circ E\beta.",
        r"\]",
      ),
    ),
  )

def _phase136_2_is_pi6_5_group_step(
  proof_step: ProofStep,
) -> bool:
  statement = proof_step.conclusion

  if not isinstance(
    statement,
    Relation,
  ):
    return False

  lhs = statement.lhs

  return (
    isinstance(
      lhs,
      TodaPrimaryGroup,
    )
    and lhs.group_dimension == 6
    and lhs.sphere_dimension == 5
    and statement.relation_type
    is RelationType.EQUALITY
  )


def _phase136_2_pi6_3_ordered_numbered_steps(
  numbered_steps: tuple[
    ProofStep,
    ...,
  ],
) -> tuple[
  ProofStep,
  ...,
]:
  hopf_surjective_step = next(
    (
      proof_step
      for proof_step in numbered_steps
      if isinstance(
        proof_step.conclusion,
        TodaHopfInvariantSurjectiveStatement,
      )
    ),
    None,
  )

  pi6_5_step = next(
    (
      proof_step
      for proof_step in numbered_steps
      if _phase136_2_is_pi6_5_group_step(
        proof_step
      )
    ),
    None,
  )

  if (
    hopf_surjective_step is None
    or pi6_5_step is None
  ):
    return numbered_steps

  hopf_index = numbered_steps.index(
    hopf_surjective_step
  )
  pi6_5_index = numbered_steps.index(
    pi6_5_step
  )

  if pi6_5_index < hopf_index:
    return numbered_steps

  reordered = list(
    numbered_steps
  )
  reordered.pop(
    pi6_5_index
  )
  reordered.insert(
    hopf_index,
    pi6_5_step,
  )

  return tuple(
    reordered
  )


def _phase136_pi6_3_reason_lead(
  number: int,
) -> str | None:
  if not isinstance(
    number,
    int,
  ):
    raise TypeError(
      "number must be an int"
    )

  reasons = {
    1: "[R3] より,",
    4: "EHP 完全列より,",
    10: "[R2] の $n=3$ の場合より,",
    12: "EHP 完全列より,",
    14: "[R2] の $n=5$ の場合より,",
  }

  return reasons.get(
    number
  )

def _append_phase134_3_pi6_3_fact(
  lines: list[str],
  presentation: TodaGroupProofPresentation,
  proof_step: ProofStep,
  number_by_step_id: dict[
    int,
    int,
  ],
  reference_by_step_id: dict[
    int,
    str,
  ],
) -> None:
  number = number_by_step_id[
    id(
      proof_step
    )
  ]

  dependency_text = (
    _phase134_5_dependency_text(
      presentation,
      proof_step,
      number_by_step_id,
      reference_by_step_id,
    )
  )

  statement = proof_step.conclusion

  if number == 14:
    dependency_text = "[R2] の $n=5$ の場合より,"

  if (
    isinstance(
      statement,
      TodaHopfInvariantSurjectiveStatement,
    )
    and number == 15
  ):
    dependency_text = "(13), (14)"

  if proof_step is presentation.root_step:
    lines.append(
      "以上により,"
    )
  elif number == 3:
    lines.extend(
      (
        "まず, $\\Delta$ の直前を含む EHP 完全列",
        "",
        r"\[",
        (
          r"\pi_{7}^{3}\xrightarrow{H}"
          r"\pi_{7}^{5}\xrightarrow{\Delta}"
          r"\pi_{5}^{2}"
          r"\quad\text{は完全である.}"
        ),
        r"\]",
        "",
        (
          "[R4] の $\\nu'$ への適用から "
          "$H(\\nu')=E^{2}\\eta_{3}$ を得て, "
          "$E^{2}\\eta_{3}=\\eta_{5}$ だから"
        ),
        "",
        r"\[",
        r"H(\nu'\eta_{6})=\eta_{5}\eta_{6}=\eta_{5}^{2}.",
        r"\]",
        "",
        (
          "[R3] の $n=5$ の場合より "
          "$\\pi_{7}^{5}=\\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$ "
          "なので, $H:\\pi_{7}^{3}\\to\\pi_{7}^{5}$ は全射である."
        ),
        (
          "したがって完全性から "
          "$\\ker\\Delta=\\pi_{7}^{5}$ となり,"
        ),
        "",
      )
    )
  elif number == 7:
    lines.extend(
      (
        (
          "Lemma 5.2 に $\\alpha=\\eta_{3}$, "
          "$i=4$, $\\beta=\\nu'$ を代入すると,"
        ),
        "",
        r"\[",
        r"2\nu'=\eta_{3}\circ E\eta_{3}\circ\eta_{5}.",
        r"\]",
        "",
        (
          "ここで $E\\eta_{3}=\\eta_{4}$ なので, "
          "$\\eta_{3}\\circ E\\eta_{3}\\circ\\eta_{5}$ "
          "は $\\eta_{3}^{3}$ と書ける. よって,"
        ),
        "",
      )
    )
  elif number == 9:
    lines.extend(
      (
        (
          "次に Lemma 5.2 を $\\alpha=\\eta_{3}$, "
          "$i=4$, $\\beta=\\nu'$ として適用するための"
          "仮定を確認する."
        ),
        (
          "$E\\eta_{3}=\\eta_{4}$ であるから, "
          "Toda bracket に関する仮定は"
        ),
        "",
      )
    )
  elif number == 11:
    lines.extend(
      (
        (
          "(9), (10) により Lemma 5.2 の仮定が満たされる. "
          "したがって Lemma 5.2 の結論 "
          "$\\beta\\in\\pi_{i+2}^{3}$ に "
          "$i=4$, $\\beta=\\nu'$ を代入して,"
        ),
        "",
      )
    )
  elif number == 13:
    lines.extend(
      (
        (
          "同じ Lemma 5.2 の結論 "
          "$H(\\beta)=E^{2}\\alpha$ に "
          "$\\alpha=\\eta_{3}$, $\\beta=\\nu'$ を代入すると,"
        ),
        "",
        r"\[",
        r"H(\nu')=E^{2}\eta_{3}.",
        r"\]",
        "",
        "さらに $E^{2}\\eta_{3}=\\eta_{5}$ なので,",
        "",
      )
    )
  elif dependency_text:
    if number == 14:
      lines.append(
        dependency_text
      )
    else:
      lines.append(
        dependency_text
        + " より,"
      )
  else:
    reason_lead = (
      _phase136_pi6_3_reason_lead(
        number
      )
    )

    if reason_lead is not None:
      lines.append(
        reason_lead
      )

  boundary_latex, boundary_sentence = (
    _phase134_6_boundary_fact_latex(
      statement
    )
  )

  if boundary_latex is not None:
    rendered_latex = (
      _phase136_compact_eta_powers(
        boundary_latex
      )
    )

    if boundary_sentence is not None:
      rendered_latex = (
        rendered_latex
        + r"\quad\text{"
        + boundary_sentence
        + "}"
      )
    else:
      rendered_latex = (
        rendered_latex
        + "."
      )

    lines.extend(
      _phase134_30_display_math_lines(
        rendered_latex,
        number,
      )
    )
    return

  if isinstance(
    statement,
    TodaProp42ExactnessStatement,
  ):
    latex = (
      _strip_phase134_3_latex_suffix(
        render_toda_proof_statement_latex(
          statement
        ),
        r" \text{ is exact}",
      )
    )

    if latex is not None:
      lines.extend(
        _phase134_30_display_math_lines(
          (
            _phase136_compact_eta_powers(
              latex
            )
            + r"\quad\text{は完全である.}"
          ),
          number,
        )
      )
      return

  if isinstance(
    statement,
    TodaSuspensionInjectiveStatement,
  ):
    latex = (
      _strip_phase134_3_latex_suffix(
        render_toda_proof_statement_latex(
          statement
        ),
        r" \text{ is injective}",
      )
    )

    if latex is not None:
      lines.extend(
        _phase134_30_display_math_lines(
          (
            _phase136_compact_eta_powers(
              latex
            )
            + r"\quad\text{は単射である.}"
          ),
          number,
        )
      )
      return

  if isinstance(
    statement,
    TodaHopfInvariantSurjectiveStatement,
  ):
    latex = (
      _strip_phase134_3_latex_suffix(
        render_toda_proof_statement_latex(
          statement
        ),
        r" \text{ is surjective}",
      )
    )

    if latex is not None:
      lines.extend(
        _phase134_30_display_math_lines(
          (
            _phase136_compact_eta_powers(
              latex
            )
            + r"\quad\text{は全射である.}"
          ),
          number,
        )
      )
      return

  if (
    isinstance(
      statement,
      Relation,
    )
    and statement.relation_type
    is RelationType.ORDER
  ):
    lhs_latex = (
      _phase136_compact_eta_powers(
        render_toda_expression_latex(
          statement.lhs
        )
      )
    )

    lines.extend(
      _phase134_30_display_math_lines(
        (
          lhs_latex
          + r"\text{ の位数は }"
          + str(
            statement.rhs
          )
          + r"\text{ である.}"
        ),
        number,
      )
    )
    return

  latex = (
    _render_group_proof_narrative_latex(
      proof_step
    )
  )

  if latex is not None:
    rendered_latex = (
      _phase136_compact_eta_powers(
        latex
      )
    )

    if proof_step is presentation.root_step:
      lines.extend(
        _phase134_30_display_math_lines(
          rendered_latex,
          number,
        )
      )
      lines.extend(
        (
          "を得る.",
          "",
        )
      )
      return

    if isinstance(
      statement,
      HomotopyGroupMembershipStatement,
    ):
      lines.extend(
        _phase134_30_display_math_lines(
          rendered_latex + ".",
          number,
        )
      )
      return

    if (
      isinstance(
        statement,
        Relation,
      )
      and statement.relation_type
      in (
        RelationType.EQUALITY,
        RelationType.ZERO,
      )
    ):
      lines.extend(
        _phase134_30_display_math_lines(
          rendered_latex + ".",
          number,
        )
      )

      if number == 10:
        lines.extend(
          (
            (
              "この $2\\eta_{3}=0$ は, "
              "Lemma 5.2 を $\\alpha=\\eta_{3}$, "
              "$i=4$, $\\beta=\\nu'$ として適用するために"
              "必要な仮定である."
            ),
            "",
          )
        )

      return

    lines.extend(
      _phase134_30_display_math_lines(
        (
          rendered_latex
          + r"\quad\text{が成り立つ.}"
        ),
        number,
      )
    )
    return

  label = (
    _group_proof_narrative_statement_label(
      statement
    )
  )

  if label is None:
    label = (
      _render_group_proof_narrative_fact(
        proof_step
      )
    )

  if dependency_text:
    lines.extend(
      (
        (
          "**("
          + str(
            number
          )
          + ")** "
          + label
          + "を得る."
        ),
        "",
      )
    )
    return

  lines.extend(
    (
      (
        "**("
        + str(
          number
        )
        + ")** "
        + label
        + "を用いる."
      ),
      "",
    )
  )

def _phase134_7_block_lead(
  presentation: TodaGroupProofPresentation,
  proof_step: ProofStep,
  first_step: ProofStep,
) -> str | None:
  classification = (
    classify_toda_group_proof_narrative_step(
      presentation,
      proof_step,
    )
  )

  generator = root_generator(
    presentation
  )

  target = root_target_group(
    presentation
  )

  generator_latex = (
    render_toda_expression_latex(
      generator
    )
    if generator is not None
    else None
  )

  target_latex = (
    "\\pi_{"
    + str(
      target.group_dimension
    )
    + "}^{"
    + str(
      target.sphere_dimension
    )
    + "}"
  )

  if (
    proof_step is first_step
    and classification.block_role
    is TodaGroupProofNarrativeBlockRole.ORDER
    and generator_latex is not None
  ):
    return (
      "まず, $"
      + generator_latex
      + "$ の位数を求める."
    )

  if (
    classification.block_role
    is TodaGroupProofNarrativeBlockRole.MEMBERSHIP
    and isinstance(
      proof_step.conclusion,
      Toda53NuPrimeBracketSpecializationStatement,
    )
    and generator_latex is not None
  ):
    return (
      "次に, $"
      + generator_latex
      + " \\in "
      + target_latex
      + "$ であることを確認する."
    )

  if (
    classification.block_role
    is TodaGroupProofNarrativeBlockRole.GROUP_STRUCTURE
    and isinstance(
      proof_step.conclusion,
      TodaProp42ExactnessStatement,
    )
  ):
    return (
      "最後に, EHP 完全列を用いて $"
      + target_latex
      + "$ の群構造を決定する."
    )

  return None


def _phase134_26_narrative_section_header_lines(
  section_title: str,
) -> list[str]:
  if not isinstance(
    section_title,
    str,
  ):
    raise TypeError(
      "section_title must be a str"
    )

  if not section_title:
    raise ValueError(
      "section_title must not be empty"
    )

  return [
    "## " + section_title,
    "",
  ]


def _phase134_26_narrative_start_lines(
  target_lines: list[str],
) -> list[str]:
  if not isinstance(
    target_lines,
    list,
  ):
    raise TypeError(
      "target_lines must be a list"
    )

  return [
    "# Group proof narrative",
    "",
    *_phase134_26_narrative_section_header_lines(
      "証明対象"
    ),
    *target_lines,
    "",
  ]



def _phase134_28_reference_section_lines(
  reference_blocks: tuple[
    tuple[
      str,
      tuple[
        str,
        ...,
      ],
    ],
    ...,
  ],
) -> list[str]:
  if not isinstance(
    reference_blocks,
    tuple,
  ):
    raise TypeError(
      "reference_blocks must be a tuple"
    )

  if not reference_blocks:
    return []

  lines = (
    _phase134_26_narrative_section_header_lines(
      "使用する結果"
    )
  )

  for index, reference_block in enumerate(
    reference_blocks,
    start=1,
  ):
    if not (
      isinstance(
        reference_block,
        tuple,
      )
      and len(
        reference_block
      ) == 2
    ):
      raise TypeError(
        "each reference block must be "
        "a (title, statement_lines) tuple"
      )

    title, statement_lines = (
      reference_block
    )

    if not isinstance(
      title,
      str,
    ):
      raise TypeError(
        "reference title must be a str"
      )

    if not isinstance(
      statement_lines,
      tuple,
    ):
      raise TypeError(
        "reference statement_lines must be a tuple"
      )

    lines.extend(
      (
        (
          "**[R"
          + str(
            index
          )
          + "] "
          + title
          + ".**"
        ),
        "",
      )
    )

    if statement_lines:
      lines.extend(
        statement_lines
      )
      lines.append(
        ""
      )

  return lines



def _phase134_30_display_math_lines(
  latex: str,
  tag: int | None = None,
) -> list[str]:
  if not isinstance(
    latex,
    str,
  ):
    raise TypeError(
      "latex must be a str"
    )

  if tag is not None and not isinstance(
    tag,
    int,
  ):
    raise TypeError(
      "tag must be an int or None"
    )

  rendered_latex = latex

  if tag is not None:
    rendered_latex = (
      rendered_latex
      + r"\tag{"
      + str(
        tag
      )
      + "}"
    )

  return [
    "",
    r"\[",
    rendered_latex,
    r"\]",
    "",
  ]


def _phase134_30_completed_boundary_lines(
  latex: str,
  tag: int | None = None,
  closing_text: str | None = None,
) -> list[str]:
  if closing_text is not None and not isinstance(
    closing_text,
    str,
  ):
    raise TypeError(
      "closing_text must be a str or None"
    )

  lines = [
    "既に,",
    *_phase134_30_display_math_lines(
      latex,
      tag,
    ),
  ]

  if closing_text is not None:
    lines.extend(
      (
        closing_text,
        "",
      )
    )

  return lines


def _phase134_30_final_conclusion_lines(
  latex: str,
  tag: int | None = None,
) -> list[str]:
  return [
    "したがって,",
    *_phase134_30_display_math_lines(
      latex,
      tag,
    ),
    "を得る.",
    "",
  ]


def _render_phase134_3_pi6_3_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  reference_steps = (
    _phase134_5_pi6_3_reference_steps(
      presentation
    )
  )

  root_latex = (
    _render_group_proof_narrative_latex(
      presentation.root_step
    )
  )

  lines = (
    _phase134_26_narrative_start_lines(
      [
        "Toda Proposition 5.6 のうち,",
        "",
        r"\[",
        root_latex,
        r"\]",
        "",
        "を示す.",
      ]
    )
  )

  reference_blocks = tuple(
    (
      (
        "Toda Proposition 5.1"
        if isinstance(
          proof_step.conclusion,
          TodaProp51FiniteDimensionalStatement,
        )
        else _phase134_5_reference_title(
          proof_step
        )
      ),
      (
        (
          r"\[",
          (
            r"\pi_{n + 1}^{n} = "
            r"\mathbb{Z}/2\{\eta_{n}\}"
            r"\qquad (n \ge 3)."
          ),
          r"\]",
        )
        if isinstance(
          proof_step.conclusion,
          TodaProp51FiniteDimensionalStatement,
        )
        else _phase134_5_reference_statement_lines(
          proof_step
        )
      ),
    )
    for proof_step in reference_steps
  ) + _phase136_2_pi6_3_reference_blocks()

  if reference_blocks:
    lines.extend(
      _phase134_28_reference_section_lines(
        reference_blocks
      )
    )

  lines.extend(
    _phase134_26_narrative_section_header_lines(
      "証明"
    )
  )

  lines.extend(
    (
      (
        "まず, Lemma 5.2 を "
        "$\\alpha=\\eta_{3}$, $i=4$, "
        "$\\beta=\\nu'$ として適用するための仮定を確認する."
      ),
      "",
      "[R2] の $n=3$ の場合より,",
      "",
      r"\[",
      r"2\eta_{3}=0.\tag{1}",
      r"\]",
      "",
      (
        "したがって Toda bracket "
        "$\\{\\eta_{3},2\\iota_{4},\\eta_{4}\\}_{1}$ "
        "が定義できる. [R4] でこの bracket のある元を "
        "$\\nu'$ と定めたので,"
      ),
      "",
      r"\[",
      (
        r"\nu' \in "
        r"\{\eta_{3},2\iota_{4},\eta_{4}\}_{1}."
        r"\tag{2}"
      ),
      r"\]",
      "",
      (
        "(1), (2) により Lemma 5.2 の仮定が満たされる. "
        "したがって Lemma 5.2 の結論から,"
      ),
      "",
      r"\[",
      r"\nu'\in\pi_{6}^{3}.\tag{3}",
      r"\]",
      "",
      (
        "さらに $H(\\beta)=E^{2}\\alpha$ と "
        "$E^{2}\\eta_{3}=\\eta_{5}$ から,"
      ),
      "",
      r"\[",
      r"H(\nu')=\eta_{5}.\tag{4}",
      r"\]",
      "",
      (
        "また $2\\beta="
        "\\eta_{3}\\circ E\\alpha\\circ\\eta_{i+1}$ と "
        "$E\\eta_{3}=\\eta_{4}$ から,"
      ),
      "",
      r"\[",
      (
        r"2\nu'="
        r"\eta_{3}\circ E\eta_{3}\circ\eta_{5}"
        r"=\eta_{3}^{3}."
        r"\tag{5}"
      ),
      r"\]",
      "",
      "[R3] の $n=3$ の場合より,",
      "",
      r"\[",
      (
        r"\pi_{5}^{3}="
        r"\mathbb{Z}/2\{\eta_{3}^{2}\}."
        r"\tag{6}"
      ),
      r"\]",
      "",
      "(6), [R1] より,",
      "",
      r"\[",
      (
        r"\pi_{5}^{2}="
        r"\mathbb{Z}/2\{\eta_{2}^{3}\}."
        r"\tag{7}"
      ),
      r"\]",
      "",
      (
        "$\\nu'$ の位数を決定するために, "
        "次の EHP 完全列を考える."
      ),
      "",
      r"\[",
      (
        r"\pi_{7}^{3}"
        r"\xrightarrow{H}"
        r"\pi_{7}^{5}"
        r"\xrightarrow{\Delta}"
        r"\pi_{5}^{2}"
        r"\xrightarrow{E}"
        r"\pi_{6}^{3}"
        r"\xrightarrow{H}"
        r"\pi_{6}^{5}"
        r"\quad\text{は完全である.}"
        r"\tag{8}"
      ),
      r"\]",
      "",
      (
        "[R2] の $n=6$ の場合より "
        "$\\eta_{6}\\in\\pi_{7}^{6}$ であり, "
        "(3) と合成して,"
      ),
      "",
      r"\[",
      r"\nu'\eta_{6}\in\pi_{7}^{3}.\tag{9}",
      r"\]",
      "",
      (
        "また η-family の suspension relation "
        "$\\eta_{6}=E\\eta_{5}$ を用いる. "
        "[R5] の Toda Proposition 2.2 に "
        "$\\alpha=\\nu'$, $\\beta=\\eta_{5}$ "
        "を代入すると,"
      ),
      "",
      r"\[",
      (
        r"H(\nu'\eta_{6})"
        r"=H(\nu'\circ E\eta_{5})"
        r"=H(\nu')\circ E\eta_{5}"
        r"=\eta_{5}\eta_{6}"
        r"=\eta_{5}^{2}."
        r"\tag{10}"
      ),
      r"\]",
      "",
      "[R3] の $n=5$ の場合より,",
      "",
      r"\[",
      (
        r"\pi_{7}^{5}="
        r"\mathbb{Z}/2\{\eta_{5}^{2}\}."
        r"\tag{11}"
      ),
      r"\]",
      "",
      (
        "(9), (10), (11) より, "
        "$H:\\pi_{7}^{3}\\to\\pi_{7}^{5}$ は"
        "生成元 $\\eta_{5}^{2}$ を像に持つ. "
        "したがって,"
      ),
      "",
      r"\[",
      (
        r"H:\pi_{7}^{3}\to\pi_{7}^{5}"
        r"\quad\text{は全射である.}"
        r"\tag{12}"
      ),
      r"\]",
      "",
      (
        "(8), (12) の完全性より "
        "$\\operatorname{Im}H=\\ker\\Delta"
        "=\\pi_{7}^{5}$ である. よって,"
      ),
      "",
      r"\[",
      (
        r"\Delta:\pi_{7}^{5}\to\pi_{5}^{2}"
        r"\quad\text{は零写像である.}"
        r"\tag{13}"
      ),
      r"\]",
      "",
      (
        "さらに (8), (13) より "
        "$\\operatorname{Im}\\Delta=\\ker E=0$ "
        "なので,"
      ),
      "",
      r"\[",
      (
        r"E:\pi_{5}^{2}\to\pi_{6}^{3}"
        r"\quad\text{は単射である.}"
        r"\tag{14}"
      ),
      r"\]",
      "",
      (
        "(7), (14) と η-family の suspension "
        "relation $E(\\eta_{2}^{3})="
        "\\eta_{3}^{3}$ より,"
      ),
      "",
      r"\[",
      (
        r"\eta_{3}^{3}"
        r"\text{ の位数は }2"
        r"\text{ である.}"
        r"\tag{15}"
      ),
      r"\]",
      "",
      "(5), (15) より,",
      "",
      r"\[",
      (
        r"\nu'"
        r"\text{ の位数は }4"
        r"\text{ である.}"
        r"\tag{16}"
      ),
      r"\]",
      "",
      "最後に, $\\pi_{6}^{3}$ の群構造を決定する.",
      "",
      "[R2] の $n=5$ の場合より,",
      "",
      r"\[",
      (
        r"\pi_{6}^{5}="
        r"\mathbb{Z}/2\{\eta_{5}\}."
        r"\tag{17}"
      ),
      r"\]",
      "",
      "(4), (17) より,",
      "",
      r"\[",
      (
        r"H:\pi_{6}^{3}\to\pi_{6}^{5}"
        r"\quad\text{は全射である.}"
        r"\tag{18}"
      ),
      r"\]",
      "",
      (
        "(8), (14), (18) より, "
        "$E$ は単射, $H$ は全射なので, "
        "次の短完全列を得る."
      ),
      "",
      r"\[",
      (
        r"0\longrightarrow\pi_{5}^{2}"
        r"\xrightarrow{E}"
        r"\pi_{6}^{3}"
        r"\xrightarrow{H}"
        r"\pi_{6}^{5}"
        r"\longrightarrow 0."
        r"\tag{19}"
      ),
      r"\]",
      "",
      (
        "(7), (17), (19) より $\\pi_{6}^{3}$ の位数は 4 "
        "である. 一方, (3), (16) より "
        "$\\nu'\\in\\pi_{6}^{3}$ は位数 4 の元なので, "
        "$\\nu'$ が群全体を生成する."
      ),
      "",
      "以上により,",
      "",
      r"\[",
      (
        r"\pi_{6}^{3}="
        r"\mathbb{Z}/4\{\nu'\}"
        r"\tag{20}"
      ),
      r"\]",
      "",
      "を得る.",
      "",
    )
  )

  return (
    "\n".join(
      lines
    )
    + "\n"
  )

def _append_narrative_for_step(
  lines: list[str],
  presentation: TodaGroupProofPresentation,
  parent_step: ProofStep,
  active_step_ids: set[int],
  expanded_step_ids: set[int],
  reference_marker_by_step_id: dict[int, str] | None = None,
  reference_reuse_marker_by_step_id: dict[int, str] | None = None,
) -> None:
  parent_id = id(
    parent_step
  )

  if parent_id in active_step_ids:
    return

  active_step_ids.add(
    parent_id
  )

  edges = (
    _narrative_edges_for_parent(
      presentation,
      parent_step,
    )
  )

  for index, edge in enumerate(
    edges
  ):
    premise_step = edge.premise_step
    premise_id = id(
      premise_step
    )
    premise_fact = (
      _render_group_proof_narrative_fact(
        premise_step
      )
    )
    premise_reference_marker = (
      None
      if (
        reference_marker_by_step_id is None
        or isinstance(
          premise_step.conclusion,
          TodaProp42ExactnessStatement,
        )
      )
      else reference_marker_by_step_id.get(
        premise_id
      )
    )
    premise_reference_reuse_marker = (
      None
      if (
        reference_reuse_marker_by_step_id is None
        or isinstance(
          premise_step.conclusion,
          TodaProp42ExactnessStatement,
        )
      )
      else reference_reuse_marker_by_step_id.get(
        premise_id
      )
    )
    lead = (
      _premise_lead(
        index,
        len(
          edges
        ),
      )
    )

    if premise_id in expanded_step_ids:
      if parent_step is presentation.root_step:
        lines.append(
          (
            lead
            + ", すでに得た"
            + premise_fact
            + "を用いる."
          )
        )
      continue

    premise_edges = (
      _narrative_edges_for_parent(
        presentation,
        premise_step,
      )
    )

    if (
      premise_edges
      and premise_reference_reuse_marker is not None
    ):
      lines.append(
        (
          lead
          + ", "
          + premise_reference_reuse_marker
          + "を用いる."
        )
      )
    elif premise_edges:
      _append_narrative_for_step(
        lines,
        presentation,
        premise_step,
        active_step_ids,
        expanded_step_ids,
        reference_marker_by_step_id,
        reference_reuse_marker_by_step_id,
      )

      generic_premise_fact = (
        _render_generic_narrative_step(
          premise_step
        )
      )
      if (
        generic_premise_fact.endswith(".")
        or generic_premise_fact.endswith("。")
      ):
        lines.append(
          (
            _derivation_lead(
              len(
                premise_edges
              )
            )
            + ", "
            + generic_premise_fact
          )
        )
      else:
        lines.append(
          (
            _derivation_lead(
              len(
                premise_edges
              )
            )
            + ", "
            + premise_fact
            + "を得る."
          )
        )
    else:
      generic_premise_fact = (
        _render_generic_narrative_step(
          premise_step
        )
      )
      inference_rule = (
        premise_step.inference_rule
      )
      generic_fact_is_fallback = (
        (
          inference_rule is not None
          and generic_premise_fact == inference_rule.name
        )
        or generic_premise_fact
        == (
          "`"
          + type(
            premise_step.conclusion
          ).__name__
          + "`"
        )
        or generic_premise_fact == repr(
          premise_step.conclusion
        )
        or generic_premise_fact == str(
          premise_step.conclusion
        )
      )
      reference_plus_semantic_fact = (
        premise_reference_marker is not None
        and not (
          is_toda_group_proof_narrative_provenance_only_statement(
            premise_step.conclusion
          )
        )
        and not generic_fact_is_fallback
      )

      if reference_plus_semantic_fact:
        if (
          generic_premise_fact.startswith("$")
          and generic_premise_fact.endswith("$")
        ):
          lines.append(
            (
              lead
              + ", "
              + premise_reference_marker
              + " により, "
              + generic_premise_fact
              + "を得る."
            )
          )
        else:
          lines.append(
            (
              lead
              + ", "
              + premise_reference_marker
              + " により, "
              + generic_premise_fact
            )
          )
      elif (
        not generic_fact_is_fallback
        and (
          generic_premise_fact.endswith(".")
          or generic_premise_fact.endswith("。")
        )
      ):
        lines.append(
          (
            lead
            + ", "
            + generic_premise_fact
          )
        )
      else:
        lines.append(
          (
            lead
            + ", "
            + (
              premise_reference_marker
              if premise_reference_marker is not None
              else premise_fact
            )
            + "を用いる."
          )
        )

    expanded_step_ids.add(
      premise_id
    )

  active_step_ids.remove(
    parent_id
  )

def _is_phase134_9_pi8_5_presentation(
  presentation: TodaGroupProofPresentation,
) -> bool:
  root = presentation.root_step.conclusion

  if not isinstance(
    root,
    Relation,
  ):
    return False

  if not isinstance(
    root.lhs,
    TodaPrimaryGroup,
  ):
    return False

  return (
    root.lhs.group_dimension == 8
    and root.lhs.sphere_dimension == 5
  )


def _phase134_9_reference_title(
  proof_step: ProofStep,
) -> str:
  statement = proof_step.conclusion

  if isinstance(
    statement,
    Toda55NuFamilyFiniteDimensionalStatement,
  ):
    return (
      "Toda (5.5) の ν-family 有限次元結果"
    )

  if isinstance(
    statement,
    Toda56Nu4DecompositionStatement,
  ):
    return "Toda (5.6) の ν₄ 分解"

  return _phase134_5_reference_title(
    proof_step
  )


def _phase134_9_pi8_5_block_lead(
  presentation: TodaGroupProofPresentation,
  proof_step: ProofStep,
  previous_block_role,
) -> str | None:
  classification = (
    classify_toda_group_proof_narrative_step(
      presentation,
      proof_step,
    )
  )

  if (
    classification.block_role
    is previous_block_role
  ):
    return None

  generator = root_generator(
    presentation
  )

  target = root_target_group(
    presentation
  )

  generator_latex = (
    render_toda_expression_latex(
      generator
    )
    if generator is not None
    else None
  )

  target_latex = (
    "\\pi_{"
    + str(
      target.group_dimension
    )
    + "}^{"
    + str(
      target.sphere_dimension
    )
    + "}"
  )

  if (
    classification.block_role
    is TodaGroupProofNarrativeBlockRole.ORDER
    and generator_latex is not None
  ):
    return (
      "まず, $"
      + generator_latex
      + "$ の位数を求める."
    )

  if (
    classification.block_role
    is TodaGroupProofNarrativeBlockRole.GROUP_STRUCTURE
  ):
    return (
      "最後に, これらの結果から $"
      + target_latex
      + "$ の群構造を決定する."
    )

  return None

def _is_phase134_11_pi8_5_boundary_step(
  presentation: TodaGroupProofPresentation,
  proof_step: ProofStep,
) -> bool:
  classification = (
    classify_toda_group_proof_narrative_step(
      presentation,
      proof_step,
    )
  )

  return (
    classification.fact_role
    is TodaGroupProofNarrativeFactRole.BOUNDARY
    and isinstance(
      proof_step.conclusion,
      Relation,
    )
    and isinstance(
      proof_step.conclusion.lhs,
      TodaPrimaryGroup,
    )
    and (
      proof_step.conclusion
      .lhs
      .group_dimension
      == 6
    )
    and (
      proof_step.conclusion
      .lhs
      .sphere_dimension
      == 3
    )
  )


def _phase134_11_pi8_5_numbered_steps(
  presentation: TodaGroupProofPresentation,
) -> tuple[
  ProofStep,
  ...,
]:
  ordered_steps = []
  visited_step_ids = set()
  active_step_ids = set()

  def visit(
    proof_step: ProofStep,
  ) -> None:
    step_id = id(
      proof_step
    )

    if step_id in visited_step_ids:
      return

    if step_id in active_step_ids:
      return

    active_step_ids.add(
      step_id
    )

    classification = (
      classify_toda_group_proof_narrative_step(
        presentation,
        proof_step,
      )
    )

    stop_here = (
      classification.fact_role
      is TodaGroupProofNarrativeFactRole.REFERENCE
      or _is_phase134_11_pi8_5_boundary_step(
        presentation,
        proof_step,
      )
    )

    if not stop_here:
      for edge in (
        _narrative_edges_for_parent(
          presentation,
          proof_step,
        )
      ):
        visit(
          edge.premise_step
        )

    active_step_ids.remove(
      step_id
    )
    visited_step_ids.add(
      step_id
    )

    if (
      classification.fact_role
      is not TodaGroupProofNarrativeFactRole.REFERENCE
    ):
      ordered_steps.append(
        proof_step
      )

  visit(
    presentation.root_step
  )

  return tuple(
    ordered_steps
  )


def _phase134_11_pi8_5_reference_steps(
  presentation: TodaGroupProofPresentation,
  numbered_steps: tuple[
    ProofStep,
    ...,
  ],
) -> tuple[
  ProofStep,
  ...,
]:
  references = []
  seen_ids = set()

  for proof_step in numbered_steps:
    for premise_step in proof_step.premises:
      classification = (
        classify_toda_group_proof_narrative_step(
          presentation,
          premise_step,
        )
      )

      if (
        classification.fact_role
        is not TodaGroupProofNarrativeFactRole.REFERENCE
      ):
        continue

      premise_id = id(
        premise_step
      )

      if premise_id in seen_ids:
        continue

      seen_ids.add(
        premise_id
      )
      references.append(
        premise_step
      )

  return tuple(
    references
  )


def _phase134_11_pi8_5_dependency_text(
  proof_step: ProofStep,
  number_by_step_id: dict[
    int,
    int,
  ],
  reference_by_step_id: dict[
    int,
    str,
  ],
) -> str:
  parts = []
  seen = set()

  for premise_step in proof_step.premises:
    premise_id = id(
      premise_step
    )

    if premise_id in reference_by_step_id:
      part = (
        "["
        + reference_by_step_id[
          premise_id
        ]
        + "]"
      )
    elif premise_id in number_by_step_id:
      part = (
        "("
        + str(
          number_by_step_id[
            premise_id
          ]
        )
        + ")"
      )
    else:
      continue

    if part in seen:
      continue

    seen.add(
      part
    )
    parts.append(
      part
    )

  return ", ".join(
    parts
  )


def _append_phase134_11_pi8_5_fact(
  lines: list[str],
  presentation: TodaGroupProofPresentation,
  proof_step: ProofStep,
  number_by_step_id: dict[
    int,
    int,
  ],
  reference_by_step_id: dict[
    int,
    str,
  ],
) -> None:
  number = number_by_step_id[
    id(
      proof_step
    )
  ]

  classification = (
    classify_toda_group_proof_narrative_step(
      presentation,
      proof_step,
    )
  )

  statement = proof_step.conclusion

  dependency_text = (
    _phase134_11_pi8_5_dependency_text(
      proof_step,
      number_by_step_id,
      reference_by_step_id,
    )
  )

  if proof_step is presentation.root_step:
    lines.append(
      "したがって,"
    )
  elif dependency_text:
    lines.append(
      dependency_text
      + " より,"
    )
  elif (
    classification.fact_role
    is TodaGroupProofNarrativeFactRole.BOUNDARY
  ):
    lines.append(
      "既に,"
    )

  if (
    classification.fact_role
    is TodaGroupProofNarrativeFactRole.DEFINITION
  ):
    element_latex = (
      render_toda_expression_latex(
        statement.element
      )
    )

    lines.extend(
      (
        (
          "**("
          + str(
            number
          )
          + ")** "
          + "$"
          + element_latex
          + "$"
          + " を "
          + "$\\nu$-family"
          + " の定義により取る."
        ),
        "",
      )
    )
    return

  if isinstance(
    statement,
    TodaIteratedSuspensionInjectiveStatement,
  ):
    label = (
      _group_proof_narrative_statement_label(
        statement
      )
    )

    lines.extend(
      (
        (
          "**("
          + str(
            number
          )
          + ")** "
          + label
          + "."
        ),
        "",
      )
    )
    return

  if isinstance(
    statement,
    TodaProp56Pi8_5QuotientStatement,
  ):
    label = (
      _group_proof_narrative_statement_label(
        statement
      )
    )

    lines.extend(
      (
        (
          "**("
          + str(
            number
          )
          + ")** "
          + label
          + "."
        ),
        "",
      )
    )
    return

  if (
    isinstance(
      statement,
      Relation,
    )
    and statement.relation_type
    is RelationType.ORDER
  ):
    lhs_latex = (
      render_toda_expression_latex(
        statement.lhs
      )
    )

    lines.extend(
      (
        (
          "**("
          + str(
            number
          )
          + ")** "
          + "$"
          + lhs_latex
          + "$"
          + " の位数は "
          + "$"
          + str(
            statement.rhs
          )
          + "$"
          + " である."
        ),
        "",
      )
    )
    return

  latex = (
    _render_group_proof_narrative_latex(
      proof_step
    )
  )

  if latex is not None:
    lines.extend(
      _phase134_30_display_math_lines(
        latex,
        number,
      )
    )

    if proof_step is presentation.root_step:
      lines.extend(
        (
          "を得る.",
          "",
        )
      )

    return

  label = (
    _group_proof_narrative_statement_label(
      statement
    )
  )

  if label is None:
    label = (
      _render_group_proof_narrative_fact(
        proof_step
      )
    )

  lines.extend(
    (
      (
        "**("
        + str(
          number
        )
        + ")** "
        + label
        + "."
      ),
      "",
    )
  )

def _render_phase134_9_pi8_5_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  numbered_steps = (
    _phase134_11_pi8_5_numbered_steps(
      presentation
    )
  )

  reference_steps = (
    _phase134_11_pi8_5_reference_steps(
      presentation,
      numbered_steps,
    )
  )

  number_by_step_id = {
    id(
      proof_step
    ): number
    for number, proof_step in enumerate(
      numbered_steps,
      start=1,
    )
  }

  reference_by_step_id = {
    id(
      proof_step
    ): (
      "R"
      + str(
        number
      )
    )
    for number, proof_step in enumerate(
      reference_steps,
      start=1,
    )
  }

  root_latex = (
    _render_group_proof_narrative_latex(
      presentation.root_step
    )
  )

  lines = (
    _phase134_26_narrative_start_lines(
      [
        "Toda Proposition 5.6 のうち,",
        "",
        r"\[",
        root_latex,
        r"\]",
        "",
        "を示す.",
      ]
    )
  )

  if reference_steps:
    reference_blocks = tuple(
      (
        _phase134_9_reference_title(
          proof_step
        ),
        (),
      )
      for proof_step in reference_steps
    )

    lines.extend(
      _phase134_28_reference_section_lines(
        reference_blocks
      )
    )

  lines.extend(
    _phase134_26_narrative_section_header_lines(
      "証明"
    )
  )

  previous_block_role = None

  for proof_step in numbered_steps:
    classification = (
      classify_toda_group_proof_narrative_step(
        presentation,
        proof_step,
      )
    )

    lead = (
      _phase134_9_pi8_5_block_lead(
        presentation,
        proof_step,
        previous_block_role,
      )
    )

    if lead is not None:
      lines.extend(
        (
          lead,
          "",
        )
      )

    if proof_step is presentation.root_step:
      lines.extend(
        (
          (
            "(3), (4), (7) より, "
            "$E^{2}\\pi_{6}^{3}$ は位数 $4$ の部分群であり, "
            "その商が位数 $2$ なので, "
            "$\\pi_{8}^{5}$ の位数は $8$ である."
          ),
          "",
          (
            "(6) より $\\nu_{5}$ も位数 $8$ であるから, "
            "$\\nu_{5}$ は $\\pi_{8}^{5}$ を生成する."
          ),
          "",
        )
      )

    _append_phase134_11_pi8_5_fact(
      lines,
      presentation,
      proof_step,
      number_by_step_id,
      reference_by_step_id,
    )

    if (
      classification.block_role
      is not TodaGroupProofNarrativeBlockRole.OTHER
    ):
      previous_block_role = (
        classification.block_role
      )

  return (
    "\n".join(
      lines
    )
    + "\n"
  )

def _phase134_24_render_pi15_8_narrative(
  presentation: TodaGroupProofPresentation,
) -> str | None:
  from toda_human_readable_renderer import (
    render_toda_expression_latex,
  )
  from toda_proof_narrative_renderer import (
    render_toda_primary_group_latex,
    render_toda_raw_group_structure_latex,
  )
  from toda_rules import (
    Toda515Sigma8TransportedDecompositionStatement,
  )

  if presentation.max_depth < 2:
    return None

  if _phase158_r5_5b_has_ordered_root_argument(
    presentation
  ):
    return None

  target = (
    presentation
    .source_replay
    .group_result
    .target
  )

  if (
    target.group_dimension != 15
    or target.sphere_dimension != 8
  ):
    return None

  transported_step = next(
    (
      node.proof_step
      for node in presentation.nodes
      if isinstance(
        node.proof_step.conclusion,
        Toda515Sigma8TransportedDecompositionStatement,
      )
    ),
    None,
  )

  if transported_step is None:
    return None

  statement = transported_step.conclusion
  decomposition_map = (
    statement
    .prop44_isomorphism
    .map
  )

  source_summands = (
    decomposition_map
    .source_group
    .summands
  )

  if len(
    source_summands
  ) != 2:
    return None

  pi14_7_latex = (
    render_repository_conclusion_latex(
      statement.pi14_7_group_relation
    )
  )

  pi15_15_latex = (
    render_repository_conclusion_latex(
      statement.pi15_15_group_relation
    )
  )

  source_left_latex = (
    render_toda_primary_group_latex(
      source_summands[0]
    )
  )

  source_right_latex = (
    render_toda_primary_group_latex(
      source_summands[1]
    )
  )

  target_latex = (
    render_toda_primary_group_latex(
      decomposition_map.target_group
    )
  )

  first_variable_latex = (
    render_toda_expression_latex(
      decomposition_map.beta
    )
  )

  second_variable_latex = (
    render_toda_expression_latex(
      decomposition_map.gamma
    )
  )

  formula_latex = (
    render_toda_expression_latex(
      decomposition_map.formula
    )
  )

  first_source_generator_latex = (
    render_toda_expression_latex(
      statement
      .pi14_7_group_relation
      .rhs
      .generator
    )
  )

  second_source_generator_latex = (
    render_toda_expression_latex(
      statement
      .pi15_15_group_relation
      .rhs
      .generator
    )
  )

  first_image_latex = (
    render_toda_expression_latex(
      statement.first_generator_image
    )
  )

  second_image_latex = (
    render_toda_expression_latex(
      statement.second_generator_image
    )
  )

  transported_group_latex = (
    render_toda_raw_group_structure_latex(
      statement.transported_group
    )
  )

  final_relation_latex = (
    render_repository_conclusion_latex(
      presentation.root_step.conclusion
    )
  )

  lines = [
    *_phase134_26_narrative_start_lines(
      [
        "Toda Proposition 5.15 のうち,",
        "",
        "\\[",
        final_relation_latex,
        "\\]",
        "",
        "を示す.",
      ]
    ),
    *_phase134_28_reference_section_lines(
      (
        (
          "Toda Proposition 4.4 の分解同型",
          (
            "次の写像は同型である.",
            "",
            "\\[",
            (
              source_left_latex
              + r" \oplus "
              + source_right_latex
              + r" \longrightarrow "
              + target_latex
            ),
            "\\]",
            "",
            "\\[",
            (
              "("
              + first_variable_latex
              + ", "
              + second_variable_latex
              + r") \longmapsto "
              + formula_latex
            ),
            "\\]",
          ),
        ),
      )
    ),
    *_phase134_26_narrative_section_header_lines(
      "証明"
    ),
    *_phase134_30_completed_boundary_lines(
      pi14_7_latex,
      closing_text="である.",
    ),
    "また,",
    "",
    "\\[",
    pi15_15_latex,
    "\\]",
    "",
    "である.",
    "",
    "[R1] より, これらの生成元はそれぞれ",
    "",
    "\\[",
    (
      first_source_generator_latex
      + r" \longmapsto "
      + first_image_latex
      + ","
    ),
    "\\qquad",
    (
      second_source_generator_latex
      + r" \longmapsto "
      + second_image_latex
    ),
    "\\]",
    "",
    "と写る.",
    "",
    *_phase134_30_final_conclusion_lines(
      (
        target_latex
        + r" \cong "
        + transported_group_latex
      )
    ),
    "直和因子の順序を入れ替えると,",
    "",
    "\\[",
    final_relation_latex,
    "\\]",
    "",
    "を得る.",
  ]

  return (
    "\n".join(
      lines
    )
    + "\n"
  )

def _phase153_r3_10_connect_public_reference_section(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  if presentation.max_depth < 2:
    return rendered

  lines = rendered.splitlines()
  reference_header = "## 使用する結果"
  proof_header = "## 証明"

  try:
    reference_index = lines.index(
      reference_header
    )
    proof_index = lines.index(
      proof_header
    )
  except ValueError:
    return rendered

  if reference_index >= proof_index:
    return rendered

  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  reference_entries = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      reference_entries,
      presentation.root_step,
    )
  )

  if not reference_entries:
    return rendered

  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
  )

  proof_body = "\n".join(
    lines[
      proof_index
      + 1:
    ]
  ).lstrip()

  target = (
    presentation
    .source_replay
    .group_result
    .target
  )

  if (
    target.group_dimension == 15
    and target.sphere_dimension == 8
  ):
    prop515_entry = next(
      (
        entry
        for entry in reference_entries
        if entry.reference.locator
        == "Proposition 5.15"
      ),
      None,
    )
    prop44_reference_number = next(
      (
        entry.number
        for entry in reference_entries
        if entry.reference.locator
        == "Proposition 4.4"
      ),
      None,
    )

    if prop515_entry is not None:
      pi14_7_step = next(
        (
          proof_step
          for proof_step in prop515_entry.proof_steps
          if (
            proof_step.inference_rule is not None
            and "pi_14^7 finite cyclic"
            in proof_step.inference_rule.name
          )
        ),
        None,
      )

      if pi14_7_step is not None:
        pi14_7_latex = (
          render_repository_conclusion_latex(
            pi14_7_step.conclusion
          )
        )
        legacy_pi14_7_block = (
          "既に,\n\n"
          "\\[\n"
          + pi14_7_latex
          + "\n\\]"
        )

        if legacy_pi14_7_block in proof_body:
          proof_body = proof_body.replace(
            legacy_pi14_7_block,
            (
              "[R"
              + str(
                prop515_entry.number
              )
              + "] より,\n\n"
              "\\[\n"
              + pi14_7_latex
              + "\n\\]"
            ),
            1,
          )

    if (
      prop44_reference_number is not None
      and "[R1] より, これらの生成元はそれぞれ"
      in proof_body
    ):
      proof_body = proof_body.replace(
        "[R1] より, これらの生成元はそれぞれ",
        (
          "[R"
          + str(
            prop44_reference_number
          )
          + "] より, これらの生成元はそれぞれ"
        ),
        1,
      )

  (
    used_reference_entries,
    used_statement_lines,
    filtered_proof_body,
  ) = (
    filter_toda_group_proof_narrative_reference_entries_by_body_usage(
      reference_entries,
      statement_lines_by_reference_number,
      proof_body,
    )
  )

  (
    filtered_reference_entries,
    filtered_statement_lines,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      used_reference_entries,
      used_statement_lines,
      presentation.root_step,
    )
  )

  if (
    len(
      filtered_reference_entries
    )
    != len(
      used_reference_entries
    )
  ):
    return rendered

  filtered_statement_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      filtered_reference_entries,
    )
  )

  filtered_proof_body = (
    suppress_toda_group_proof_narrative_reference_body_restatements(
      filtered_proof_body,
      filtered_statement_lines,
    )
  )

  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      filtered_reference_entries,
      filtered_statement_lines,
    )
  )

  if not reference_section:
    return rendered

  prefix_lines = lines[
    :reference_index
  ]

  while (
    prefix_lines
    and not prefix_lines[
      -1
    ].strip()
  ):
    prefix_lines.pop()

  return (
    "\n".join(
      (
        *prefix_lines,
        "",
        reference_header,
        "",
        reference_section,
        "",
        "---",
        "",
        proof_header,
        "",
        filtered_proof_body,
      )
    ).rstrip()
    + "\n"
  )


def _wrap_phase150_rc4_generic_public_narrative(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  reference_entries = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      reference_entries,
      presentation.root_step,
    )
  )
  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
  )
  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )

  if not reference_section:
    return rendered

  reference_prefixes = (
    (
      reference_section
      + "\n\n"
    ),
    (
      "使用する結果を先にまとめる.\n\n"
      + reference_section
      + "\n\n"
    ),
  )
  reference_prefix = next(
    (
      prefix
      for prefix in reference_prefixes
      if rendered.startswith(
        prefix
      )
    ),
    None,
  )

  if reference_prefix is None:
    return rendered

  proof = rendered[
    len(
      reference_prefix
    ):
  ].lstrip()
  proof = (
    suppress_toda_group_proof_narrative_reference_body_restatements(
      proof,
      statement_lines_by_reference_number,
    )
  )

  return (
    "# Group proof narrative\n\n"
    "## 使用する結果\n\n"
    + reference_section
    + "\n\n"
    "---\n\n"
    "## 証明\n\n"
    + proof.rstrip()
    + "\n"
  )


def _phase157_r11_r17_normalize_public_connectors(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  paragraphs = rendered.split(
    "\n\n"
  )
  connectors = {
    "以上より,",
    "したがって,",
    "これより,",
  }
  index = 0

  while index < len(
    paragraphs
  ) - 1:
    stripped = paragraphs[
      index
    ].strip()

    if stripped not in connectors:
      index += 1
      continue

    next_paragraph = paragraphs[
      index + 1
    ]
    separator = (
      "\n"
      if next_paragraph.lstrip().startswith(
        r"\["
      )
      else " "
    )

    paragraphs[
      index:
      index + 2
    ] = [
      stripped
      + separator
      + next_paragraph,
    ]

  return "\n\n".join(
    paragraphs
  )


def _phase157_r11_r17_normalize_public_numeric_equalities(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  characters = []
  index = 0

  while index < len(
    rendered
  ):
    if rendered[
      index
    ] != "=":
      characters.append(
        rendered[
          index
        ]
      )
      index += 1
      continue

    first_number_start = index + 1

    while (
      first_number_start < len(
        rendered
      )
      and rendered[
        first_number_start
      ].isspace()
    ):
      first_number_start += 1

    first_number_end = first_number_start

    while (
      first_number_end < len(
        rendered
      )
      and rendered[
        first_number_end
      ].isdigit()
    ):
      first_number_end += 1

    if first_number_end == first_number_start:
      characters.append(
        rendered[
          index
        ]
      )
      index += 1
      continue

    second_equals_index = first_number_end

    while (
      second_equals_index < len(
        rendered
      )
      and rendered[
        second_equals_index
      ].isspace()
    ):
      second_equals_index += 1

    if (
      second_equals_index >= len(
        rendered
      )
      or rendered[
        second_equals_index
      ] != "="
    ):
      characters.append(
        rendered[
          index
        ]
      )
      index += 1
      continue

    second_number_start = second_equals_index + 1

    while (
      second_number_start < len(
        rendered
      )
      and rendered[
        second_number_start
      ].isspace()
    ):
      second_number_start += 1

    second_number_end = second_number_start

    while (
      second_number_end < len(
        rendered
      )
      and rendered[
        second_number_end
      ].isdigit()
    ):
      second_number_end += 1

    first_number = rendered[
      first_number_start:
      first_number_end
    ]
    second_number = rendered[
      second_number_start:
      second_number_end
    ]

    if (
      not second_number
      or first_number != second_number
    ):
      characters.append(
        rendered[
          index
        ]
      )
      index += 1
      continue

    characters.append(
      rendered[
        index:
        first_number_end
      ]
    )
    index = second_number_end

  return "".join(
    characters
  )



def _normalize_toda_group_proof_narrative_display_closing_fragments(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  lines = rendered.splitlines()
  normalized = []
  closing_fragments = {
    "である.",
    "を得る.",
    "を用いる.",
    "となる.",
  }

  for line in lines:
    stripped = line.strip()

    if (
      stripped
      in closing_fragments
      and normalized
    ):
      previous_index = (
        len(
          normalized
        )
        - 1
      )

      while (
        previous_index >= 0
        and not normalized[
          previous_index
        ].strip()
      ):
        previous_index -= 1

      if (
        previous_index >= 0
        and normalized[
          previous_index
        ].strip()
        == r"\]"
      ):
        del normalized[
          previous_index + 1:
        ]

    normalized.append(
      line
    )

  return "\n".join(
    normalized
  )

def _finalize_toda_group_proof_narrative_markdown(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  rendered = (
    _phase157_r11_r17_normalize_public_connectors(
      rendered
    )
  )
  rendered = (
    _phase157_r11_r17_normalize_public_numeric_equalities(
      rendered
    )
  )
  rendered = (
    _normalize_toda_group_proof_narrative_display_closing_fragments(
      rendered
    )
  )
  lines = rendered.rstrip().splitlines()

  reference_header = "## 使用する結果"
  proof_header = "## 証明"

  if (
    reference_header in lines
    and proof_header in lines
  ):
    reference_index = lines.index(
      reference_header
    )
    proof_index = lines.index(
      proof_header
    )

    if reference_index < proof_index:
      before_proof = lines[
        :proof_index
      ]
      proof_and_after = lines[
        proof_index:
      ]

      while (
        before_proof
        and not before_proof[-1].strip()
      ):
        before_proof.pop()

      if (
        before_proof
        and before_proof[-1].strip()
        == "---"
      ):
        before_proof.pop()

        while (
          before_proof
          and not before_proof[-1].strip()
        ):
          before_proof.pop()

      lines = [
        *before_proof,
        "",
        "---",
        "",
        *proof_and_after,
      ]

  while (
    lines
    and not lines[-1].strip()
  ):
    lines.pop()

  if (
    not lines
    or lines[-1].strip()
    != r"$\square$"
  ):
    lines.extend(
      (
        "",
        r"$\square$",
      )
    )

  return (
    "\n".join(
      lines
    ).rstrip()
    + "\n"
  )


def _phase158_r5_5b_has_ordered_root_argument(
  presentation: TodaGroupProofPresentation,
) -> bool:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if presentation.max_depth < 2:
    return False

  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=semantic_sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=semantic_sidecar,
    )
  )

  return any(
    (
      argument.supporting_blocks
      and presentation.root_step
      in argument.conclusion_block.steps
    )
    for argument in arguments
  )

def _is_phase150_rc4_generic_route_target(
  presentation: TodaGroupProofPresentation,
) -> bool:
  if presentation.max_depth < 2:
    return False

  if _is_phase134_9_pi8_5_presentation(
    presentation
  ):
    return False

  if _phase158_r5_5b_has_ordered_root_argument(
    presentation
  ):
    return True

  target = (
    presentation
    .source_replay
    .group_result
    .target
  )

  return (
    (
      target.group_dimension == 10
      and target.sphere_dimension == 4
    )
    or (
      target.group_dimension == 12
      and target.sphere_dimension == 5
    )
    or (
      target.group_dimension == 16
      and target.sphere_dimension == 9
    )
  )

def _phase158_baseline_render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  if presentation.max_depth >= 2:
    semantic_sidecar = (
      build_toda_group_proof_narrative_semantic_sidecar(
        presentation
      )
    )
    blocks = (
      build_toda_group_proof_narrative_blocks(
        presentation,
        semantic_sidecar=semantic_sidecar,
      )
    )
    arguments = (
      build_toda_group_proof_narrative_arguments(
        presentation,
        blocks,
        semantic_sidecar=semantic_sidecar,
      )
    )

    rendered = (
      render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
      )
    )

    public_rendered = (
      _wrap_phase150_rc4_generic_public_narrative(
        presentation,
        rendered,
      )
    )

    return (
      _finalize_toda_group_proof_narrative_markdown(
        public_rendered
      )
    )

  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
    if presentation.max_depth >= 2
    else ()
  )
  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
    if reference_entries
    else {}
  )
  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      reference_entries,
      statement_lines_by_reference_number,
      presentation.root_step,
    )
  )
  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
  reference_marker_by_step_id = {
    id(proof_step): f"[R{entry.number}]"
    for entry in reference_entries
    for proof_step in entry.proof_steps
  }
  reference_reuse_marker_by_step_id = (
    build_toda_group_proof_narrative_reference_reuse_marker_by_step_id(
      presentation,
      reference_entries,
    )
  )

  lines = [
    "# Group proof narrative",
    "",
  ]

  if reference_section:
    lines.extend(
      (
        "## 使用する結果",
        "",
        reference_section,
        "",
        "## 証明",
        "",
      )
    )

  root_edges = (
    _narrative_edges_for_parent(
      presentation,
      presentation.root_step,
    )
  )

  if root_edges:
    target = (
      presentation
      .source_replay
      .group_result
      .target
    )

    if (
      target.group_dimension == 16
      and target.sphere_dimension == 9
    ):
      lines.extend(
        (
          (
            "$\\sigma_{9}$ の位数を確認し, "
            "これが $\\pi_{16}^{9}$ を生成することを示す。"
          ),
          "",
        )
      )

    _append_narrative_for_step(
      lines,
      presentation,
      presentation.root_step,
      set(),
      set(),
      reference_marker_by_step_id,
      reference_reuse_marker_by_step_id,
    )

    lines.extend(
      (
        "",
        (
          "したがって, "
          + _render_group_proof_narrative_fact(
            presentation.root_step
          )
          + "を得る."
        ),
      )
    )
  else:
    lines.append(
      (
        "したがって, "
        + _render_group_proof_narrative_fact(
          presentation.root_step
        )
        + "である."
      )
    )

  rendered = (
    "\n".join(
      lines
    )
    + "\n"
  )

  if reference_section:
    proof_section_marker = "## 証明\n\n"
    proof_section_index = rendered.find(
      proof_section_marker
    )

    if proof_section_index >= 0:
      body_start = (
        proof_section_index
        + len(
          proof_section_marker
        )
      )
      body = rendered[
        body_start:
      ]
      suppressed_body = (
        suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(
          presentation,
          body,
          reference_entries,
        )
      )
      suppressed_body = (
        suppress_toda_group_proof_narrative_reference_body_duplicates(
          suppressed_body,
          statement_lines_by_reference_number,
        )
      )
      suppressed_body = (
        link_toda_group_proof_narrative_reference_body_consumers(
          presentation,
          suppressed_body,
          reference_entries,
        )
      )
      (
        filtered_reference_entries,
        filtered_statement_lines,
        suppressed_body,
      ) = (
        filter_toda_group_proof_narrative_reference_entries_by_body_usage(
          reference_entries,
          statement_lines_by_reference_number,
          suppressed_body,
        )
      )
      filtered_reference_section = (
        render_toda_group_proof_narrative_reference_entries_markdown(
          filtered_reference_entries,
          filtered_statement_lines,
        )
      )
      prefix_lines = [
        "# Group proof narrative",
        "",
      ]

      if filtered_reference_section:
        prefix_lines.extend(
          (
            "## 使用する結果",
            "",
            filtered_reference_section,
            "",
            "## 証明",
            "",
          )
        )

      rendered = (
        "\n".join(
          prefix_lines
        )
        + "\n"
        + suppressed_body
        + "\n"
      )

  return (
    _finalize_toda_group_proof_narrative_markdown(
      rendered
    )
  )

def _phase158_public_narrative_target_lines(
  presentation: TodaGroupProofPresentation,
) -> list[str]:
  root_latex = (
    _render_group_proof_narrative_latex(
      presentation.root_step
    )
  )

  if root_latex is not None:
    return [
      r"\[",
      root_latex + ".",
      r"\]",
    ]

  return [
    _render_group_proof_narrative_fact(
      presentation.root_step
    )
  ]

def _phase158_strip_terminal_qed_lines(
  lines: list[str],
) -> list[str]:
  result = lines[:]

  while (
    result
    and not result[-1].strip()
  ):
    result.pop()

  qed_markers = {
    "□",
    r"$\square$",
    r"\(\square\)",
    r"\square",
  }

  if (
    result
    and result[-1].strip()
    in qed_markers
  ):
    result.pop()

  while (
    result
    and not result[-1].strip()
  ):
    result.pop()

  return result


def _phase158_public_equation_tag_number(
  line: str,
) -> int | None:
  marker = r"\tag{"
  marker_index = line.find(
    marker
  )

  if marker_index < 0:
    return None

  number_start = (
    marker_index
    + len(
      marker
    )
  )
  number_end = line.find(
    "}",
    number_start,
  )

  if number_end < 0:
    return None

  number_text = line[
    number_start:
    number_end
  ]

  if not number_text.isdigit():
    return None

  return int(
    number_text
  )


def _phase158_public_equation_connector_numbers(
  line: str,
) -> tuple[
  int,
  ...,
] | None:
  stripped = line.strip()
  suffix = "より,"

  if not stripped.endswith(
    suffix
  ):
    return None

  reference_text = stripped[
    :-len(
      suffix
    )
  ].strip()

  if not reference_text:
    return None

  if " と " in reference_text:
    left, right = reference_text.rsplit(
      " と ",
      1,
    )
    pieces = tuple(
      (
        *(
          piece.strip()
          for piece in left.split(
            ","
          )
          if piece.strip()
        ),
        right.strip(),
      )
    )
  else:
    pieces = (
      reference_text,
    )

  numbers = []

  for piece in pieces:
    if (
      not piece.startswith(
        "("
      )
      or not piece.endswith(
        ")"
      )
    ):
      return None

    number_text = piece[
      1:-1
    ]

    if not number_text.isdigit():
      return None

    numbers.append(
      int(
        number_text
      )
    )

  return tuple(
    numbers
  )


def _phase158_render_public_equation_connector(
  numbers: tuple[
    int,
    ...,
  ],
) -> str:
  references = tuple(
    "("
    + str(
      number
    )
    + ")"
    for number in numbers
  )

  if len(
    references
  ) == 1:
    return (
      references[
        0
      ]
      + " より,"
    )

  return (
    ", ".join(
      references[
        :-1
      ]
    )
    + " と "
    + references[
      -1
    ]
    + " より,"
  )


def _phase158_normalize_public_equation_numbers(
  proof_body: list[
    str
  ],
) -> list[
  str
]:
  connector_numbers_by_index = {}
  referenced_numbers = set()

  for index, line in enumerate(
    proof_body
  ):
    numbers = (
      _phase158_public_equation_connector_numbers(
        line
      )
    )

    if numbers is None:
      continue

    connector_numbers_by_index[
      index
    ] = numbers
    referenced_numbers.update(
      numbers
    )

  derivation_target_numbers = set()

  for connector_index in connector_numbers_by_index:
    target_index = next(
      (
        index
        for index in range(
          connector_index + 1,
          len(
            proof_body
          ),
        )
        if proof_body[
          index
        ].strip()
      ),
      None,
    )

    if target_index is None:
      continue

    target_number = (
      _phase158_public_equation_tag_number(
        proof_body[
          target_index
        ]
      )
    )

    if target_number is not None:
      derivation_target_numbers.add(
        target_number
      )

  retained_numbers = (
    referenced_numbers
    | derivation_target_numbers
  )
  retained_old_numbers = []
  seen_old_numbers = set()

  for line in proof_body:
    number = (
      _phase158_public_equation_tag_number(
        line
      )
    )

    if (
      number is None
      or number not in retained_numbers
      or number in seen_old_numbers
    ):
      continue

    retained_old_numbers.append(
      number
    )
    seen_old_numbers.add(
      number
    )

  number_map = {
    old_number: new_number
    for new_number, old_number in enumerate(
      retained_old_numbers,
      start=1,
    )
  }

  result = []
  emitted_old_numbers = set()

  for index, source_line in enumerate(
    proof_body
  ):
    line = source_line
    tag_number = (
      _phase158_public_equation_tag_number(
        line
      )
    )
    public_number = None

    if tag_number is not None:
      old_marker = (
        r"	ag{"
        + str(
          tag_number
        )
        + "}"
      )

      if (
        tag_number not in number_map
        or tag_number in emitted_old_numbers
      ):
        line = line.replace(
          old_marker,
          "",
          1,
        )
      else:
        public_number = number_map[
          tag_number
        ]
        line = line.replace(
          old_marker,
          "",
          1,
        )
        emitted_old_numbers.add(
          tag_number
        )

    connector_numbers = (
      connector_numbers_by_index.get(
        index
      )
    )

    if connector_numbers is not None:
      if all(
        number in number_map
        for number in connector_numbers
      ):
        line = (
          _phase158_render_public_equation_connector(
            tuple(
              number_map[
                number
              ]
              for number in connector_numbers
            )
          )
        )
      else:
        line = (
          "これより,"
          if len(
            connector_numbers
          ) == 1
          else "これらより,"
        )

    line = line.replace(
      "は零写像である.",
      "は零写像.",
    )

    numbered_map_properties = (
      (
        " は単射.",
        "は単射",
      ),
      (
        " は全射.",
        "は全射",
      ),
      (
        " は同型.",
        "は同型",
      ),
    )

    normalized_map_property = False

    if public_number is not None:
      stripped = line.strip()

      for suffix, property_text in numbered_map_properties:
        if (
          not stripped.startswith(
            "$"
          )
          or not stripped.endswith(
            suffix
          )
        ):
          continue

        math_and_suffix = stripped[
          : -len(
            suffix
          )
        ]

        if not math_and_suffix.endswith(
          "$"
        ):
          continue

        math_content = math_and_suffix[
          1:-1
        ].rstrip()

        result.extend(
          (
            r"\[",
            (
              math_content
              + r"\quad	ext{"
              + property_text
              + r"}. \qquad ("
              + str(
                public_number
              )
              + ")"
            ),
            r"\]",
          )
        )
        normalized_map_property = True
        break

    if normalized_map_property:
      continue

    result.append(
      line
    )

  return result




def _phase159_restore_isomorphism_to_injective_dependency_visibility(
  presentation: TodaGroupProofPresentation,
  proof_body: list[str],
) -> list[str]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    proof_body,
    list,
  ):
    raise TypeError(
      "proof_body must be a list"
    )

  dependency_pairs = []
  visited_step_ids = set()

  def visit(
    proof_step: ProofStep,
  ) -> None:
    step_id = id(
      proof_step
    )

    if step_id in visited_step_ids:
      return

    visited_step_ids.add(
      step_id
    )

    if isinstance(
      proof_step.conclusion,
      TodaSuspensionInjectiveStatement,
    ):
      injective_map = (
        proof_step.conclusion.map
      )
      isomorphism_step = next(
        (
          premise_step
          for premise_step in proof_step.premises
          if (
            isinstance(
              premise_step.conclusion,
              TodaSuspensionIsomorphismStatement,
            )
            and premise_step.conclusion.map
            == injective_map
          )
        ),
        None,
      )

      if isomorphism_step is not None:
        dependency_pairs.append(
          (
            isomorphism_step,
            proof_step,
          )
        )

    for premise_step in proof_step.premises:
      visit(
        premise_step
      )

  visit(
    presentation.root_step
  )

  rendered = "\n".join(
    proof_body
  )

  for (
    isomorphism_step,
    injective_step,
  ) in dependency_pairs:
    isomorphism_prose = (
      _render_generic_narrative_step(
        isomorphism_step
      )
    )
    injective_prose = (
      _render_generic_narrative_step(
        injective_step
      )
    )

    if (
      not isomorphism_prose
      or not injective_prose
    ):
      continue

    has_isomorphism = (
      isomorphism_prose in rendered
    )
    has_injectivity = (
      injective_prose in rendered
    )

    if (
      has_isomorphism
      and has_injectivity
    ):
      continue

    if has_injectivity:
      rendered = rendered.replace(
        injective_prose,
        (
          isomorphism_prose
          + "\n\n"
          + "したがって, "
          + injective_prose
        ),
        1,
      )
      continue

    if has_isomorphism:
      rendered = rendered.replace(
        isomorphism_prose,
        (
          isomorphism_prose
          + "\n\n"
          + "したがって, "
          + injective_prose
        ),
        1,
      )
      continue

    dependency_prose = (
      isomorphism_prose
      + "\n\n"
      + "したがって, "
      + injective_prose
    )

    if rendered:
      rendered = (
        dependency_prose
        + "\n\n"
        + rendered
      )
    else:
      rendered = dependency_prose

  return rendered.splitlines()

def _phase159_public_semantic_projection_context(
  presentation: TodaGroupProofPresentation,
):
  semantic_presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      semantic_presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      semantic_presentation,
      semantic_sidecar=semantic_sidecar,
    )
  )
  exactness_blocks = tuple(
    block
    for block in blocks
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    )
  )
  components = (
    build_toda_group_proof_narrative_exactness_method_components(
      exactness_blocks
    )
  )
  target = (
    semantic_presentation
    .source_replay
    .group_result
    .target
  )
  matching_components = tuple(
    component
    for component in components
    if any(
      target
      in (
        window.source_term,
        window.middle_term,
        window.target_term,
      )
      for window in component.windows
    )
  )
  primary_component = (
    matching_components[0]
    if len(matching_components) == 1
    else None
  )

  return (
    semantic_presentation,
    semantic_sidecar,
    primary_component,
  )


def _phase159_matching_map_property_step(
  presentation: TodaGroupProofPresentation,
  statement_types: tuple,
  group_map,
) -> ProofStep | None:
  return next(
    (
      node.proof_step
      for node in presentation.nodes
      if (
        isinstance(
          node.proof_step.conclusion,
          statement_types,
        )
        and getattr(
          node.proof_step.conclusion,
          "map",
          None,
        )
        == group_map
      )
    ),
    None,
  )


def _phase159_public_map_property_triples(
  presentation: TodaGroupProofPresentation,
) -> tuple[
  tuple[
    ProofStep,
    ProofStep,
    ProofStep,
  ],
  ...,
]:
  triples = []

  for node in presentation.nodes:
    isomorphism_step = node.proof_step
    statement = isomorphism_step.conclusion

    if not isinstance(
      statement,
      _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
    ):
      continue

    group_map = getattr(
      statement,
      "map",
      None,
    )

    if group_map is None:
      continue

    injective_step = _phase159_matching_map_property_step(
      presentation,
      _GENERIC_INJECTIVE_STATEMENT_TYPES,
      group_map,
    )
    surjective_step = _phase159_matching_map_property_step(
      presentation,
      _GENERIC_SURJECTIVE_STATEMENT_TYPES,
      group_map,
    )

    if injective_step is None or surjective_step is None:
      continue

    triples.append(
      (
        injective_step,
        surjective_step,
        isomorphism_step,
      )
    )

  return tuple(triples)


def _phase159_numbered_map_property_line(
  proof_step: ProofStep,
  number: int,
  predicate: str,
) -> str | None:
  group_map = getattr(
    proof_step.conclusion,
    "map",
    None,
  )
  if group_map is None:
    return None

  map_latex = _render_generic_narrative_group_map_latex(
    group_map
  )
  if map_latex is None:
    return None

  return (
    "$"
    + map_latex
    + r"\tag{"
    + str(number)
    + "}$ は"
    + predicate
    + "."
  )


def _phase159_plain_map_property_line(
  proof_step: ProofStep,
  predicate: str,
) -> str | None:
  group_map = getattr(
    proof_step.conclusion,
    "map",
    None,
  )
  if group_map is None:
    return None

  map_latex = _render_generic_narrative_group_map_latex(
    group_map
  )
  if map_latex is None:
    return None

  return (
    "$"
    + map_latex
    + "$ は"
    + predicate
    + "."
  )


def _phase159_unique_preimage_definition_line(
  proof_step: ProofStep,
) -> str | None:
  statement = proof_step.conclusion
  group_map = getattr(
    statement,
    "map",
    None,
  )
  element = getattr(
    statement,
    "element",
    None,
  )
  image = getattr(
    statement,
    "image",
    None,
  )

  if (
    group_map is None
    or element is None
    or image is None
  ):
    return None

  isomorphism_premise = next(
    (
      premise_step
      for premise_step in proof_step.premises
      if (
        isinstance(
          premise_step,
          ProofStep,
        )
        and isinstance(
          premise_step.conclusion,
          _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
        )
        and getattr(
          premise_step.conclusion,
          "map",
          None,
        )
        == group_map
      )
    ),
    None,
  )

  if isomorphism_premise is None:
    return None

  map_name = _generic_group_map_name(
    group_map
  )

  if map_name is None:
    return None

  return (
    "この同型写像により, $"
    + map_name
    + "("
    + render_toda_expression_latex(
      element
    )
    + ") = "
    + render_toda_expression_latex(
      image
    )
    + "$ となる $"
    + render_toda_expression_latex(
      element
    )
    + r" \in "
    + render_toda_primary_group_latex(
      group_map.source_group
    )
    + "$ が一意に存在する."
  )

def _phase159_public_exactness_latex(
  line: str,
) -> str | None:
  stripped = line.strip()

  if (
    not stripped.startswith("$")
    or r"\xrightarrow{" not in stripped
  ):
    return None

  closing_math = stripped.rfind(
    "$"
  )

  if closing_math <= 0:
    return None

  latex = stripped[
    1:closing_math
  ]

  return latex.replace(
    "Δ",
    r"\Delta",
  )


def _phase159_consolidate_public_exactness_lines(
  lines: list[str],
) -> list[str]:
  exactness_by_index = {
    index: latex
    for index, line in enumerate(
      lines
    )
    if (
      latex := _phase159_public_exactness_latex(
        line
      )
    )
    is not None
  }

  if not exactness_by_index:
    return lines

  maximal_indices = []

  for index, latex in exactness_by_index.items():
    is_strict_subsequence = any(
      (
        latex != other_latex
        and latex in other_latex
      )
      for (
        other_index,
        other_latex,
      ) in exactness_by_index.items()
      if other_index != index
    )

    if not is_strict_subsequence:
      maximal_indices.append(
        index
      )

  canonical_index_by_latex = {}

  for index in maximal_indices:
    latex = exactness_by_index[
      index
    ]
    canonical_index_by_latex.setdefault(
      latex,
      index,
    )

  canonical_latex_by_index = {
    index: latex
    for (
      latex,
      index,
    ) in canonical_index_by_latex.items()
  }

  result = []

  for index, line in enumerate(
    lines
  ):
    latex = exactness_by_index.get(
      index
    )

    if latex is None:
      result.append(
        line
      )
      continue

    owner_index = next(
      (
        canonical_index
        for (
          canonical_index,
          canonical_latex,
        ) in canonical_latex_by_index.items()
        if latex in canonical_latex
      ),
      None,
    )

    if owner_index is None:
      result.append(
        line
      )
      continue

    if index != owner_index:
      continue

    result.append(
      "$"
      + canonical_latex_by_index[
        owner_index
      ]
      + "$ は完全である."
    )

  return result


def _phase159_project_generic_semantics_to_public_proof(
  presentation: TodaGroupProofPresentation,
  proof_body: list[str],
) -> list[str]:
  (
    semantic_presentation,
    semantic_sidecar,
    primary_component,
  ) = _phase159_public_semantic_projection_context(
    presentation
  )

  lines = list(proof_body)

  if primary_component is not None:
    component_latex = (
      render_toda_group_proof_narrative_exactness_method_component_latex(
        primary_component
      )
    )
    long_exact_sequence = (
      "$"
      + component_latex
      + "$ は完全である."
    )
    projected_lines = []
    inserted = False

    for line in lines:
      stripped = line.strip()
      exactness_latex = None

      if (
        stripped.startswith("$")
        and r"\\xrightarrow{" in stripped
      ):
        closing_math = stripped.rfind(
          "$"
        )

        if closing_math > 0:
          exactness_latex = stripped[
            1:closing_math
          ]

      if (
        exactness_latex is not None
        and exactness_latex in component_latex
      ):
        if not inserted:
          projected_lines.append(
            long_exact_sequence
          )
          inserted = True
        continue

      projected_lines.append(
        line
      )

    lines = projected_lines

  next_equation_number = 1
  for line in lines:
    number = _phase158_public_equation_tag_number(line)
    if (
      number is not None
      and number >= next_equation_number
    ):
      next_equation_number = number + 1

  for (
    injective_step,
    surjective_step,
    isomorphism_step,
  ) in _phase159_public_map_property_triples(
    semantic_presentation
  ):
    injective_rendered = _render_generic_narrative_step(
      injective_step
    )
    surjective_rendered = _render_generic_narrative_step(
      surjective_step
    )
    isomorphism_rendered = _render_generic_narrative_step(
      isomorphism_step
    )

    injective_index = next(
      (
        index
        for index, line in enumerate(lines)
        if injective_rendered in line
      ),
      None,
    )
    surjective_index = next(
      (
        index
        for index, line in enumerate(lines)
        if surjective_rendered in line
      ),
      None,
    )
    isomorphism_index = next(
      (
        index
        for index, line in enumerate(lines)
        if isomorphism_rendered in line
      ),
      None,
    )

    if (
      injective_index is None
      or surjective_index is None
      or isomorphism_index is None
    ):
      continue

    injective_number = next_equation_number
    surjective_number = next_equation_number + 1
    next_equation_number += 2

    injective_line = _phase159_numbered_map_property_line(
      injective_step,
      injective_number,
      "単射",
    )
    surjective_line = _phase159_numbered_map_property_line(
      surjective_step,
      surjective_number,
      "全射",
    )
    isomorphism_line = _phase159_plain_map_property_line(
      isomorphism_step,
      "同型",
    )

    if (
      injective_line is None
      or surjective_line is None
      or isomorphism_line is None
    ):
      continue

    lines[injective_index] = lines[injective_index].replace(
      injective_rendered,
      injective_line,
      1,
    )
    lines[surjective_index] = lines[surjective_index].replace(
      surjective_rendered,
      surjective_line,
      1,
    )

    source_line = lines[isomorphism_index]
    marker_index = source_line.find(isomorphism_rendered)
    prefix = (
      source_line[:marker_index]
      if marker_index >= 0
      else ""
    )
    derivation_prefixes = (
      "これらから, ",
      "これらより, ",
      "このことから, ",
      "したがって, ",
    )
    if prefix in derivation_prefixes:
      prefix = ""

    lines[isomorphism_index] = (
      prefix
      + "("
      + str(injective_number)
      + "), ("
      + str(surjective_number)
      + ") より, "
      + isomorphism_line
    )

  for node in semantic_presentation.nodes:
    proof_step = node.proof_step
    original = _render_generic_narrative_step(
      proof_step
    )
    replacement = (
      _phase159_unique_preimage_definition_line(
        proof_step,
      )
    )

    if replacement is None:
      continue

    for index, line in enumerate(
      lines
    ):
      if original not in line:
        continue

      prefix = line[
        :line.find(
          original
        )
      ]

      if prefix in (
        "これらから, ",
        "これらより, ",
        "このことから, ",
        "したがって, ",
      ):
        prefix = ""

      lines[
        index
      ] = (
        prefix
        + replacement
      )
      break

  lines = (
    _phase159_consolidate_public_exactness_lines(
      lines
    )
  )

  punctuated_lines = []

  for line in lines:
    stripped = line.rstrip()

    if (
      stripped
      and stripped.endswith("$")
    ):
      line = stripped + "."

    punctuated_lines.append(
      line
    )

  lines = punctuated_lines

  compacted = []
  previous_blank = False

  for line in lines:
    is_blank = not line.strip()
    if is_blank and previous_blank:
      continue
    compacted.append(line)
    previous_blank = is_blank

  return compacted

def _phase159_r1_7b_exactness_step_latex(
  proof_step: ProofStep,
) -> str | None:
  statement = proof_step.conclusion

  if not isinstance(
    statement,
    TodaProp42ExactnessStatement,
  ):
    return None

  rendered = (
    render_toda_proof_statement_latex(
      statement
    )
  )

  if rendered is None:
    return None

  suffix = (
    r" \text{ is exact}"
  )

  if not rendered.endswith(
    suffix
  ):
    return None

  return rendered[
    :-len(
      suffix
    )
  ]




def _phase159_r1_7b_inline_exactness_latex(
  line: str,
) -> str | None:
  stripped = line.strip()
  verbose_suffix = "$ は完全である."

  if (
    stripped.startswith(
      "$"
    )
    and stripped.endswith(
      verbose_suffix
    )
  ):
    latex = stripped[
      1:-len(
        verbose_suffix
      )
    ]
  elif (
    stripped.startswith(
      "$"
    )
    and stripped.endswith(
      "$."
    )
  ):
    latex = stripped[
      1:-2
    ]
  elif (
    stripped.startswith(
      "$"
    )
    and stripped.endswith(
      "$"
    )
  ):
    latex = stripped[
      1:-1
    ]
  else:
    return None

  if latex.count(
    r"\xrightarrow{"
  ) < 2:
    return None

  if not latex.startswith(
    r"\pi_{"
  ):
    return None

  return latex



def _phase159_r1_7b_inline_short_exact_latex(
  line: str,
) -> str | None:
  stripped = line.strip()

  if not stripped.startswith(
    r"$0\longrightarrow "
  ):
    return None

  if stripped.endswith(
    "$."
  ):
    latex = stripped[
      1:-2
    ]
  elif stripped.endswith(
    "$"
  ):
    latex = stripped[
      1:-1
    ]
  else:
    return None

  if not latex.endswith(
    r"\longrightarrow 0"
  ):
    return None

  return latex


def _phase159_r1_7b_display_math_lines(
  latex: str,
) -> tuple[
  str,
  ...,
]:
  return (
    r"\[",
    latex.rstrip(
      "."
    )
    + ".",
    r"\]",
    "",
  )


def _phase159_r1_7b_map_property_signature(
  line: str,
) -> tuple[
  str,
  str,
  str,
] | None:
  stripped = line.strip()

  if not stripped.startswith(
    "$"
  ):
    return None

  math_end = stripped.find(
    "$",
    1,
  )

  if math_end < 0:
    return None

  suffix = stripped[
    math_end + 1:
  ].strip()

  if not (
    suffix.startswith(
      "は単射"
    )
    or suffix.startswith(
      "は全射"
    )
    or suffix.startswith(
      "は零写像"
    )
    or suffix.startswith(
      "は同型"
    )
  ):
    return None

  math = stripped[
    1:math_end
  ]

  if ": " not in math:
    return None

  map_name, map_expression = math.split(
    ": ",
    1,
  )

  arrow = r" \to "

  if arrow not in map_expression:
    return None

  source, target = map_expression.split(
    arrow,
    1,
  )

  if (
    not source.startswith(
      r"\pi_{"
    )
    or not target.startswith(
      r"\pi_{"
    )
  ):
    return None

  return (
    map_name,
    source,
    target,
  )


def _phase159_r1_7b_exactness_matches_map_property(
  exactness_latex: str,
  signature: tuple[
    str,
    str,
    str,
  ],
) -> bool:
  map_name, source, target = signature
  map_segment = (
    source
    + r" \xrightarrow{"
    + map_name
    + "} "
    + target
  )

  return (
    map_segment
    in exactness_latex
  )


def _phase159_r1_7b_find_display_math_span(
  lines: list[
    str
  ],
  latex: str,
) -> tuple[
  int,
  int,
] | None:
  normalized_target = latex.rstrip(
    "."
  )
  index = 0

  while index < len(
    lines
  ):
    if lines[
      index
    ].strip() != r"\[":
      index += 1
      continue

    end_index = index + 1
    inner_lines = []

    while (
      end_index < len(
        lines
      )
      and lines[
        end_index
      ].strip() != r"\]"
    ):
      if lines[
        end_index
      ].strip():
        inner_lines.append(
          lines[
            end_index
          ].strip()
        )
      end_index += 1

    if end_index >= len(
      lines
    ):
      return None

    normalized_inner = " ".join(
      inner_lines
    ).rstrip(
      "."
    )

    if (
      normalized_inner
      == normalized_target
    ):
      span_end = end_index + 1

      if (
        span_end < len(
          lines
        )
        and not lines[
          span_end
        ].strip()
      ):
        span_end += 1

      return (
        index,
        span_end,
      )

    index = end_index + 1

  return None


def _phase159_r1_7b_next_nonblank_index(
  lines: list[
    str
  ],
  start: int,
) -> int | None:
  return next(
    (
      index
      for index in range(
        start,
        len(
          lines
        ),
      )
      if lines[
        index
      ].strip()
    ),
    None,
  )


def _phase159_r1_7b_normalize_public_exact_sequences(
  presentation: TodaGroupProofPresentation,
  proof_body: list[
    str
  ],
) -> list[
  str
]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    proof_body,
    list,
  ):
    raise TypeError(
      "proof_body must be a list"
    )

  semantic_presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  exactness_latex = tuple(
    latex
    for latex in (
      _phase159_r1_7b_exactness_step_latex(
        node.proof_step
      )
      for node in semantic_presentation.nodes
    )
    if latex is not None
  )

  def canonical_exactness(
    latex: str,
  ) -> str:
    return (
      latex
      .replace(
        r"\xrightarrow{Δ}",
        r"\xrightarrow{\Delta}",
      )
      .strip()
      .removesuffix(
        "."
      )
      .strip()
    )

  canonical_exactness_latex = tuple(
    canonical_exactness(
      latex
    )
    for latex in exactness_latex
  )

  def canonical_typed_exactness(
    latex: str,
  ) -> str:
    canonical = canonical_exactness(
      latex
    )

    for (
      typed_latex,
      typed_canonical,
    ) in zip(
      exactness_latex,
      canonical_exactness_latex,
    ):
      if canonical == typed_canonical:
        return typed_latex

    return canonical

  def prior_display_covers(
    lines: list[
      str
    ],
    latex: str,
    before_index: int,
  ) -> bool:
    target = canonical_exactness(
      latex
    )
    index = 0

    while index < min(
      before_index,
      len(
        lines
      ),
    ):
      if (
        lines[
          index
        ].strip()
        == r"\["
        and index + 2
        < len(
          lines
        )
        and lines[
          index + 2
        ].strip()
        == r"\]"
      ):
        displayed = (
          canonical_exactness(
            lines[
              index + 1
            ]
          )
        )

        if target in displayed:
          return True

        index += 3
        continue

      index += 1

    return False

  lines = []

  for line in proof_body:
    inline_exactness = (
      _phase159_r1_7b_inline_exactness_latex(
        line
      )
    )

    if inline_exactness is not None:
      lines.extend(
        _phase159_r1_7b_display_math_lines(
          canonical_typed_exactness(
            inline_exactness
          )
        )
      )
      continue

    inline_short_exact = (
      _phase159_r1_7b_inline_short_exact_latex(
        line
      )
    )

    if inline_short_exact is not None:
      lines.extend(
        _phase159_r1_7b_display_math_lines(
          inline_short_exact
        )
      )
      continue

    lines.append(
      line
    )

  line_index = 0

  while line_index < len(
    lines
  ):
    signature = (
      _phase159_r1_7b_map_property_signature(
        lines[
          line_index
        ]
      )
    )

    if signature is None:
      line_index += 1
      continue

    matching_latex = next(
      (
        latex
        for latex in exactness_latex
        if (
          _phase159_r1_7b_exactness_matches_map_property(
            latex,
            signature,
          )
        )
      ),
      None,
    )

    if matching_latex is None:
      line_index += 1
      continue

    if prior_display_covers(
      lines,
      matching_latex,
      line_index,
    ):
      line_index += 1
      continue

    existing_span = (
      _phase159_r1_7b_find_display_math_span(
        lines,
        matching_latex,
      )
    )

    if (
      existing_span is not None
      and existing_span[
        0
      ] < line_index
    ):
      line_index += 1
      continue

    if existing_span is not None:
      span_start, span_end = existing_span

      del lines[
        span_start:span_end
      ]

      if span_start < line_index:
        line_index -= (
          span_end
          - span_start
        )

    display_lines = list(
      _phase159_r1_7b_display_math_lines(
        matching_latex
      )
    )

    lines[
      line_index:line_index
    ] = display_lines

    line_index += (
      len(
        display_lines
      )
      + 1
    )

  result = []
  displayed_exactness = []
  line_index = 0

  while line_index < len(
    lines
  ):
    if (
      lines[
        line_index
      ].strip()
      == r"\["
      and line_index + 2
      < len(
        lines
      )
      and lines[
        line_index + 2
      ].strip()
      == r"\]"
    ):
      content = canonical_exactness(
        lines[
          line_index + 1
        ]
      )

      is_typed_exactness = (
        content
        in canonical_exactness_latex
      )

      if (
        is_typed_exactness
        and any(
          content in earlier
          for earlier in displayed_exactness
        )
      ):
        line_index += 3
        continue

      displayed_exactness.append(
        content
      )

      result.extend(
        lines[
          line_index:line_index + 3
        ]
      )
      line_index += 3
      continue

    result.append(
      lines[
        line_index
      ]
    )
    line_index += 1

  return result








def _phase159_r1_7c_r4_normalize_proof_body_prose(
  proof_body: list[str],
) -> list[str]:
  if not isinstance(
    proof_body,
    list,
  ):
    raise TypeError(
      "proof_body must be a list"
    )

  normalized = []

  for source_line in proof_body:
    if not isinstance(
      source_line,
      str,
    ):
      raise TypeError(
        "proof_body must contain only strings"
      )

    line = source_line
    stripped = line.strip()

    if (
      stripped.startswith(
        "$"
      )
      and stripped.endswith(
        "$ である."
      )
    ):
      leading = line[
        :len(line)
        - len(line.lstrip())
      ]
      trailing = line[
        len(line.rstrip()):
      ]
      stripped = (
        stripped[
          :-len(
            " である."
          )
        ]
        + "."
      )
      line = (
        leading
        + stripped
        + trailing
      )

    for redundant_prefix in (
      "以上より, この完全性と ",
      "したがって, この完全性と ",
    ):
      stripped = line.strip()

      if not stripped.startswith(
        redundant_prefix
      ):
        continue

      leading = line[
        :len(line)
        - len(line.lstrip())
      ]
      trailing = line[
        len(line.rstrip()):
      ]
      stripped = (
        "この完全性と "
        + stripped[
          len(
            redundant_prefix
          ):
        ]
      )
      line = (
        leading
        + stripped
        + trailing
      )
      break

    normalized.append(
      line
    )

  return normalized


def _phase158_normalize_public_narrative_contract(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  if presentation.max_depth < 2:
    return rendered

  title = "# Group proof narrative"
  target_header = "## 証明対象"
  reference_header = "## 使用する結果"
  separator = "---"
  proof_header = "## 証明"
  qed = "□"

  source_lines = rendered.rstrip().splitlines()

  if source_lines and source_lines[0] == title:
    content_lines = source_lines[1:]
  else:
    content_lines = source_lines[:]

  while content_lines and not content_lines[0].strip():
    content_lines.pop(0)

  def exact_index(
    marker: str,
  ) -> int | None:
    try:
      return content_lines.index(marker)
    except ValueError:
      return None

  target_index = exact_index(target_header)
  reference_index = exact_index(reference_header)
  proof_index = exact_index(proof_header)

  target_body = _phase158_public_narrative_target_lines(
    presentation
  )

  reference_body: list[str] = []

  if (
    reference_index is not None
    and proof_index is not None
    and reference_index < proof_index
  ):
    reference_body = content_lines[
      reference_index + 1:
      proof_index
    ]

  while reference_body and not reference_body[0].strip():
    reference_body.pop(0)

  while reference_body and not reference_body[-1].strip():
    reference_body.pop()

  if (
    reference_body
    and reference_body[-1].strip() == separator
  ):
    reference_body.pop()
    while reference_body and not reference_body[-1].strip():
      reference_body.pop()

  if proof_index is not None:
    proof_body = content_lines[proof_index + 1:]
  elif target_index is None and reference_index is None:
    proof_body = content_lines[:]
  else:
    proof_body = []

  while proof_body and not proof_body[0].strip():
    proof_body.pop(0)

  proof_body = _phase158_strip_terminal_qed_lines(
    proof_body
  )
  proof_body = _phase158_normalize_public_equation_numbers(
    proof_body
  )
  proof_body = (
    _phase159_r1_7b_normalize_public_exact_sequences(
      presentation,
      proof_body,
    )
  )
  proof_body = _phase159_project_generic_semantics_to_public_proof(
    presentation,
    proof_body,
  )

  proof_body = (
    _phase159_r1_7c_r4_normalize_proof_body_prose(
      proof_body
    )
  )

  lines = [
    title,
    "",
    target_header,
    "",
    *target_body,
    "",
    reference_header,
    "",
  ]

  if reference_body:
    lines.extend(
      (
        *reference_body,
        "",
      )
    )

  lines.extend(
    (
      separator,
      "",
      proof_header,
      "",
      *proof_body,
      "",
      qed,
    )
  )

  return "\n".join(lines).rstrip() + "\n"

def _phase159_public_formula_map_property_line(
  proof_step: ProofStep,
) -> str | None:
  statement = proof_step.conclusion

  if isinstance(
    statement,
    _GENERIC_INJECTIVE_STATEMENT_TYPES,
  ):
    property_label = "単射"
  elif isinstance(
    statement,
    _GENERIC_SURJECTIVE_STATEMENT_TYPES,
  ):
    property_label = "全射"
  elif isinstance(
    statement,
    _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
  ):
    property_label = "同型"
  elif isinstance(
    statement,
    _GENERIC_ZERO_MAP_STATEMENT_TYPES,
  ):
    property_label = "零写像"
  else:
    return None

  group_map = getattr(
    statement,
    "map",
    None,
  )

  if group_map is None:
    return None

  map_latex = (
    _render_generic_narrative_group_map_latex(
      group_map
    )
  )

  if map_latex is None:
    return None

  return (
    "$"
    + map_latex
    + "$ は"
    + property_label
    + "."
  )


def _phase159_normalize_public_map_property_wording(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  proof_marker = "## 証明\n\n"
  proof_index = rendered.find(
    proof_marker
  )

  if proof_index < 0:
    return rendered

  body_start = (
    proof_index
    + len(
      proof_marker
    )
  )
  prefix = rendered[
    :body_start
  ]
  proof_body = rendered[
    body_start:
  ]

  semantic_presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  for node in semantic_presentation.nodes:
    proof_step = node.proof_step
    original = (
      _render_generic_narrative_step(
        proof_step
      )
    )
    replacement = (
      _phase159_public_formula_map_property_line(
        proof_step
      )
    )

    if replacement is None:
      continue

    proof_body = proof_body.replace(
      original,
      replacement,
    )

  return (
    prefix
    + proof_body
  )


def _phase159_foundational_reference_statement(
  proof_step: ProofStep,
) -> str:
  map_property = (
    _phase159_public_formula_map_property_line(
      proof_step
    )
  )

  if map_property is not None:
    return map_property

  rendered = (
    _render_generic_narrative_step(
      proof_step
    )
  )

  if rendered.endswith("$"):
    return (
      rendered
      + "."
    )

  return rendered


def _phase159_render_foundational_reference_section(
  presentation: TodaGroupProofPresentation,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  entries = []
  index_by_key = {}
  seen_step_ids = set()

  def visit(
    proof_step: ProofStep,
  ) -> None:
    step_id = id(
      proof_step
    )

    if step_id in seen_step_ids:
      return

    seen_step_ids.add(
      step_id
    )

    identity = (
      proof_step.foundational_reference
    )

    if identity is not None:
      if not isinstance(
        identity,
        FoundationalReferenceIdentity,
      ):
        raise TypeError(
          "foundational_reference must be a "
          "FoundationalReferenceIdentity or None"
        )

      existing_index = (
        index_by_key.get(
          identity.key
        )
      )

      if existing_index is None:
        index_by_key[
          identity.key
        ] = len(
          entries
        )
        entries.append(
          [
            identity,
            [
              proof_step,
            ],
          ]
        )
      else:
        entries[
          existing_index
        ][
          1
        ].append(
          proof_step
        )

    for premise in proof_step.premises:
      if isinstance(
        premise,
        ProofStep,
      ):
        visit(
          premise
        )

  visit(
    presentation.root_step
  )

  if not entries:
    return ""

  lines = []

  for number, (
    identity,
    proof_steps,
  ) in enumerate(
    entries,
    start=1,
  ):
    lines.append(
      "**[F"
      + str(
        number
      )
      + "] "
      + identity.label
      + ".**"
    )

    seen_statements = set()

    for proof_step in proof_steps:
      statement = (
        _phase159_foundational_reference_statement(
          proof_step
        )
      )

      if statement in seen_statements:
        continue

      seen_statements.add(
        statement
      )
      lines.append(
        statement
      )

  return "\n".join(
    lines
  )

def _phase159_inject_foundational_reference_section(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  foundational = (
    _phase159_render_foundational_reference_section(
      presentation
    )
  )

  if not foundational:
    return rendered

  reference_marker = (
    "## 使用する結果\n\n"
  )
  proof_boundary = (
    "---\n\n## 証明"
  )
  reference_start = rendered.find(
    reference_marker
  )

  if reference_start < 0:
    return rendered

  content_start = (
    reference_start
    + len(
      reference_marker
    )
  )
  boundary_index = rendered.find(
    proof_boundary,
    content_start,
  )

  if boundary_index < 0:
    return rendered

  existing = rendered[
    content_start:
    boundary_index
  ].strip()

  if existing:
    replacement = (
      existing
      + "\n\n"
      + foundational
    )
  else:
    replacement = foundational

  return (
    rendered[
      :content_start
    ]
    + replacement
    + "\n\n"
    + rendered[
      boundary_index:
    ]
  )

def _phase159_normalize_public_reference_map_property_wording(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  reference_marker = (
    "## 使用する結果\n\n"
  )
  proof_boundary = (
    "\n---\n\n## 証明"
  )
  reference_start = rendered.find(
    reference_marker
  )

  if reference_start < 0:
    return rendered

  content_start = (
    reference_start
    + len(
      reference_marker
    )
  )
  boundary_index = rendered.find(
    proof_boundary,
    content_start,
  )

  if boundary_index < 0:
    return rendered

  reference_body = rendered[
    content_start:
    boundary_index
  ]

  pattern = re.compile(
    r"^(?P<prefix>\$.*\$\s+は)"
    r"(?P<property>"
    r"単射である"
    r"|全射である"
    r"|同型写像である"
    r"|零写像である"
    r")\.$"
  )

  normalized_lines = []

  replacement_by_property = {
    "単射である": "単射",
    "全射である": "全射",
    "同型写像である": "同型",
    "零写像である": "零写像",
  }

  for line in reference_body.splitlines():
    match = pattern.match(
      line.strip()
    )

    if match is None:
      normalized_lines.append(
        line
      )
      continue

    leading = line[
      :len(
        line
      )
      - len(
        line.lstrip()
      )
    ]

    normalized_lines.append(
      leading
      + match.group(
        "prefix"
      )
      + replacement_by_property[
        match.group(
          "property"
        )
      ]
      + "."
    )

  normalized_reference = "\n".join(
    normalized_lines
  )

  return (
    rendered[
      :content_start
    ]
    + normalized_reference
    + rendered[
      boundary_index:
    ]
  )


def _phase159_number_public_map_property_statement(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  pattern = re.compile(
    r"^\$(?P<map>.+?)"
    r"\\tag\{(?P<number>[0-9]+)\}"
    r"\$ は"
    r"(?P<property>単射|全射|同型|零写像)"
    r"\.$"
  )

  lines = []

  for line in rendered.splitlines():
    match = pattern.match(
      line.strip()
    )

    if match is None:
      lines.append(
        line
      )
      continue

    leading = line[
      :len(
        line
      )
      - len(
        line.lstrip()
      )
    ]

    lines.append(
      leading
      + "$"
      + match.group(
        "map"
      )
      + r" \text{ は"
      + match.group(
        "property"
      )
      + r"}. \tag{"
      + match.group(
        "number"
      )
      + "}$"
    )

  return "\n".join(
    lines
  )


def _phase159_r1_6c_recursive_proof_steps(
  root_step: ProofStep,
) -> tuple[ProofStep, ...]:
  if not isinstance(
    root_step,
    ProofStep,
  ):
    raise TypeError(
      "root_step must be a ProofStep"
    )

  steps = []
  seen_step_ids = set()

  def visit(
    proof_step: ProofStep,
  ) -> None:
    step_id = id(
      proof_step
    )

    if step_id in seen_step_ids:
      return

    seen_step_ids.add(
      step_id
    )
    steps.append(
      proof_step
    )

    for premise in proof_step.premises:
      if isinstance(
        premise,
        ProofStep,
      ):
        visit(
          premise
        )

  visit(
    root_step
  )

  return tuple(
    steps
  )


def _phase159_r1_6c_step_reference_locator(
  proof_step: ProofStep,
) -> str | None:
  if not isinstance(
    proof_step,
    ProofStep,
  ):
    raise TypeError(
      "proof_step must be a ProofStep"
    )

  inference_rule = (
    proof_step.inference_rule
  )

  if inference_rule is None:
    return None

  reference = (
    inference_rule.literature_reference
  )

  if reference is None:
    return None

  return reference.locator


def _phase159_r1_6c_compact_map_property_line(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  replacements = (
    (
      " は単射である.",
      " は単射.",
    ),
    (
      " は全射である.",
      " は全射.",
    ),
    (
      " は同型写像である.",
      " は同型.",
    ),
    (
      " は零写像である.",
      " は零写像.",
    ),
  )

  normalized = rendered.strip()

  for old, new in replacements:
    if normalized.endswith(
      old
    ):
      return (
        normalized[
          :-len(
            old
          )
        ]
        + new
      )

  return normalized


def _phase159_r1_6c_statement_match_key(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  normalized = rendered.strip()

  normalized = re.sub(
    r"\\tag\{[0-9]+\}",
    "",
    normalized,
  )
  normalized = re.sub(
    r"\s+",
    " ",
    normalized,
  )

  return normalized


def _phase159_r1_6c_reference_number(
  rendered: str,
  locator: str,
) -> int | None:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  if not isinstance(
    locator,
    str,
  ):
    raise TypeError(
      "locator must be a str"
    )

  match = re.search(
    r"^\*\*\[R([0-9]+)\] "
    + re.escape(
      locator
    )
    + r"\.\*\*$",
    rendered,
    flags=re.MULTILINE,
  )

  if match is None:
    return None

  return int(
    match.group(
      1
    )
  )


def _phase159_r1_6c_canonicalize_toda_51_reference(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  reference_marker = (
    "## 使用する結果\n\n"
  )
  proof_boundary = (
    "\n---\n\n## 証明"
  )
  reference_start = rendered.find(
    reference_marker
  )

  if reference_start < 0:
    return rendered

  content_start = (
    reference_start
    + len(
      reference_marker
    )
  )
  boundary_index = rendered.find(
    proof_boundary,
    content_start,
  )

  if boundary_index < 0:
    return rendered

  reference_body = rendered[
    content_start:
    boundary_index
  ]
  lines = reference_body.splitlines()
  output = []
  index = 0

  while index < len(
    lines
  ):
    match = re.match(
      r"^\*\*\[R([0-9]+)\] "
      r"\(5\.1\)\.\*\*$",
      lines[
        index
      ].strip(),
    )

    if match is None:
      output.append(
        lines[
          index
        ]
      )
      index += 1
      continue

    output.append(
      lines[
        index
      ]
    )
    output.append(
      (
        r"$\pi_{i}^{1} = 0\ (i > 1),"
        r"\qquad "
        r"\pi_{i}^{n} = 0\ (i < n)$."
      )
    )
    output.append(
      (
        r"$\pi_{n}^{n} = "
        r"\langle \iota_{n} \rangle "
        r"\cong \mathbb{Z}$."
      )
    )

    index += 1

    while (
      index < len(
        lines
      )
      and not lines[
        index
      ].strip().startswith(
        "**[R"
      )
    ):
      index += 1

  normalized_reference = "\n".join(
    output
  ).rstrip()

  return (
    rendered[
      :content_start
    ]
    + normalized_reference
    + rendered[
      boundary_index:
    ]
  )


def _phase159_r1_6c_remove_redundant_exactness_sentence(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  lines = rendered.splitlines()
  result = []

  for index, line in enumerate(
    lines
  ):
    stripped = line.strip()

    if not (
      stripped.startswith(
        "$"
      )
      and stripped.endswith(
        "$ は完全である."
      )
    ):
      result.append(
        line
      )
      continue

    previous_nonblank = next(
      (
        lines[
          previous_index
        ].strip()
        for previous_index in range(
          index - 1,
          -1,
          -1,
        )
        if lines[
          previous_index
        ].strip()
      ),
      "",
    )

    if not previous_nonblank.endswith(
      "次の完全列を考える."
    ):
      result.append(
        line
      )
      continue

    result.append(
      line.replace(
        "$ は完全である.",
        "$.",
        1,
      )
    )

  return "\n".join(
    result
  )


def _phase159_r1_6c_link_proof_reasons(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  proof_marker = (
    "## 証明\n\n"
  )
  proof_start = rendered.find(
    proof_marker
  )

  if proof_start < 0:
    return rendered

  body_start = (
    proof_start
    + len(
      proof_marker
    )
  )
  body = rendered[
    body_start:
  ]
  body_lines = body.splitlines()

  all_steps = (
    _phase159_r1_6c_recursive_proof_steps(
      presentation.root_step
    )
  )

  exactness_derived_keys = set()

  for proof_step in all_steps:
    if not any(
      (
        isinstance(
          premise,
          ProofStep,
        )
        and isinstance(
          premise.conclusion,
          TodaProp42ExactnessStatement,
        )
      )
      for premise in proof_step.premises
    ):
      continue

    rendered_step = (
      _phase159_r1_6c_compact_map_property_line(
        _render_generic_narrative_step(
          proof_step
        )
      )
    )

    exactness_derived_keys.add(
      _phase159_r1_6c_statement_match_key(
        rendered_step
      )
    )

  suspension_pairs = []

  for proof_step in all_steps:
    if not isinstance(
      proof_step.conclusion,
      TodaSuspensionInjectiveStatement,
    ):
      continue

    source_step = next(
      (
        premise
        for premise in proof_step.premises
        if (
          isinstance(
            premise,
            ProofStep,
          )
          and isinstance(
            premise.conclusion,
            TodaSuspensionIsomorphismStatement,
          )
          and (
            _phase159_r1_6c_step_reference_locator(
              premise
            )
            == "(5.1)"
          )
        )
      ),
      None,
    )

    if source_step is None:
      continue

    source_line = (
      _phase159_r1_6c_compact_map_property_line(
        _render_generic_narrative_step(
          source_step
        )
      )
    )
    target_line = (
      _phase159_r1_6c_compact_map_property_line(
        _render_generic_narrative_step(
          proof_step
        )
      )
    )

    suspension_pairs.append(
      (
        _phase159_r1_6c_statement_match_key(
          target_line
        ),
        source_line,
      )
    )

  reference_number = (
    _phase159_r1_6c_reference_number(
      rendered,
      "(5.1)",
    )
  )

  linked_lines = []
  inserted_source_keys = set()

  for line in body_lines:
    stripped = line.strip()
    key = (
      _phase159_r1_6c_statement_match_key(
        stripped
      )
    )

    suspension_pair = next(
      (
        pair
        for pair in suspension_pairs
        if pair[
          0
        ] == key
      ),
      None,
    )

    if (
      suspension_pair is not None
      and reference_number is not None
    ):
      source_line = (
        suspension_pair[
          1
        ]
      )
      source_key = (
        _phase159_r1_6c_statement_match_key(
          source_line
        )
      )

      if source_key not in inserted_source_keys:
        if (
          linked_lines
          and linked_lines[
            -1
          ].strip()
        ):
          linked_lines.append(
            ""
          )

        linked_lines.append(
          (
            "[R"
            + str(
              reference_number
            )
            + "]より, "
            + source_line
          )
        )
        linked_lines.append(
          ""
        )
        inserted_source_keys.add(
          source_key
        )

      linked_lines.append(
        (
          "したがって, "
          + stripped
        )
      )
      continue

    if (
      key in exactness_derived_keys
      and not stripped.startswith(
        "完全性より,"
      )
    ):
      linked_lines.append(
        (
          "完全性より, "
          + stripped
        )
      )
      continue

    linked_lines.append(
      line
    )

  return (
    rendered[
      :body_start
    ]
    + "\n".join(
      linked_lines
    )
  )


def _phase159_r1_6c_render_statement_numbers(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  pattern = re.compile(
    r"^(?P<prefix>.*)"
    r"\$(?P<map>.+?)"
    r"\\tag\{(?P<number>[0-9]+)\}"
    r"\$ は"
    r"(?P<property>単射|全射|同型|零写像)"
    r"\.$"
  )

  result = []

  for line in rendered.splitlines():
    match = pattern.match(
      line
    )

    if match is None:
      result.append(
        line
      )
      continue

    result.append(
      (
        match.group(
          "prefix"
        )
        + "$"
        + match.group(
          "map"
        )
        + "$ は"
        + match.group(
          "property"
        )
        + ". ("
        + match.group(
          "number"
        )
        + ")"
      )
    )

  return "\n".join(
    result
  )


def _phase159_r1_6d_toda_51_diagonal_specialization_lines(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> tuple[
  str,
  str,
  str,
] | None:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  reference_number = (
    _phase159_r1_6c_reference_number(
      rendered,
      "(5.1)",
    )
  )

  if reference_number is None:
    return None

  suspension_step = next(
    (
      proof_step
      for proof_step in (
        _phase159_r1_6c_recursive_proof_steps(
          presentation.root_step
        )
      )
      if (
        isinstance(
          proof_step.conclusion,
          TodaSuspensionIsomorphismStatement,
        )
        and (
          _phase159_r1_6c_step_reference_locator(
            proof_step
          )
          == "(5.1)"
        )
      )
    ),
    None,
  )

  if suspension_step is None:
    return None

  suspension_map = (
    suspension_step.conclusion.map
  )
  source_group = (
    suspension_map.source_group
  )
  target_group = (
    suspension_map.target_group
  )

  source_dimension = getattr(
    source_group,
    "sphere_dimension",
    None,
  )
  target_dimension = getattr(
    target_group,
    "sphere_dimension",
    None,
  )

  if (
    not isinstance(
      source_dimension,
      int,
    )
    or not isinstance(
      target_dimension,
      int,
    )
  ):
    return None

  source_group_latex = (
    render_toda_primary_group_latex(
      source_group
    )
  )
  target_group_latex = (
    render_toda_primary_group_latex(
      target_group
    )
  )

  isomorphism_line = (
    _phase159_r1_6c_compact_map_property_line(
      _render_generic_narrative_step(
        suspension_step
      )
    )
  )

  specialization_line = (
    "[R"
    + str(
      reference_number
    )
    + "] より, $"
    + source_group_latex
    + r" = \mathbb{Z}\{\iota_{"
    + str(
      source_dimension
    )
    + r"}\}$, $"
    + target_group_latex
    + r" = \mathbb{Z}\{\iota_{"
    + str(
      target_dimension
    )
    + r"}\}$."
  )

  generator_line = (
    "$E(\\iota_{"
    + str(
      source_dimension
    )
    + r"}) = \iota_{"
    + str(
      target_dimension
    )
    + r"}$ であるから, "
    + isomorphism_line
  )

  old_line = (
    "[R"
    + str(
      reference_number
    )
    + "]より, "
    + isomorphism_line
  )

  return (
    old_line,
    specialization_line,
    generator_line,
  )


def _phase159_r1_6d_finalize_reference_and_linkage(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  rendered = rendered.replace(
    (
      r"$\pi_{n}^{n} = "
      r"\langle \iota_{n} \rangle "
      r"\cong \mathbb{Z}$."
    ),
    (
      r"$\pi_{n}^{n} = "
      r"\mathbb{Z}\{\iota_{n}\}$."
    ),
  )

  rendered = re.sub(
    r"(\[R[0-9]+\])より,",
    r"\1 より,",
    rendered,
  )

  specialization = (
    _phase159_r1_6d_toda_51_diagonal_specialization_lines(
      presentation,
      rendered,
    )
  )

  if specialization is None:
    return rendered

  (
    old_line,
    specialization_line,
    generator_line,
  ) = specialization

  normalized_old_line = re.sub(
    r"^(\[R[0-9]+\])より,",
    r"\1 より,",
    old_line,
  )

  if normalized_old_line not in rendered:
    return rendered

  return rendered.replace(
    normalized_old_line,
    (
      specialization_line
      + "\n\n"
      + generator_line
    ),
    1,
  )


def _phase159_r1_6d_center_structural_formulas(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  lines = rendered.splitlines()
  output = []

  numbered_map_property = re.compile(
    r"^(?P<lead>.*?), "
    r"\$(?P<math>.+)\$ は"
    r"(?P<property>単射|全射|同型|零写像)"
    r"\. \((?P<number>[0-9]+)\)$"
  )

  standalone_exact_sequence = re.compile(
    r"^\$(?P<math>.+\\xrightarrow\{.+)\$\.$"
  )

  for line in lines:
    stripped = line.strip()

    exact_match = (
      standalone_exact_sequence.match(
        stripped
      )
    )

    if exact_match is not None:
      if (
        output
        and output[
          -1
        ].strip()
      ):
        output.append(
          ""
        )

      output.extend(
        (
          r"\[",
          exact_match.group(
            "math"
          )
          + ".",
          r"\]",
        )
      )
      continue

    numbered_match = (
      numbered_map_property.match(
        stripped
      )
    )

    if numbered_match is not None:
      lead = numbered_match.group(
        "lead"
      )

      if lead:
        output.append(
          lead + ","
        )
        output.append(
          ""
        )

      output.extend(
        (
          r"\[",
          (
            numbered_match.group(
              "math"
            )
            + r"\quad\text{は"
            + numbered_match.group(
              "property"
            )
            + r"}. \qquad ("
            + numbered_match.group(
              "number"
            )
            + ")"
          ),
          r"\]",
        )
      )
      continue

    output.append(
      line
    )

  compacted = []
  previous_blank = False

  for line in output:
    is_blank = not line.strip()

    if (
      is_blank
      and previous_blank
    ):
      continue

    compacted.append(
      line
    )
    previous_blank = is_blank

  return "\n".join(
    compacted
  )


def _phase159_r1_6d_reorder_target_group_fact_after_surjectivity(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  all_steps = (
    _phase159_r1_6c_recursive_proof_steps(
      presentation.root_step
    )
  )

  for surjective_step in all_steps:
    if not isinstance(
      surjective_step.conclusion,
      TodaHopfInvariantSurjectiveStatement,
    ):
      continue

    target_group = (
      surjective_step.conclusion.map.target_group
    )
    target_group_latex = (
      render_toda_primary_group_latex(
        target_group
      )
    )

    rendered_surjective = (
      _phase159_r1_6c_compact_map_property_line(
        _render_generic_narrative_step(
          surjective_step
        )
      )
    )

    surjective_match = re.match(
      r"^\$(?P<math>.+)\$ は全射\.$",
      rendered_surjective,
    )

    if surjective_match is None:
      continue

    display_prefix = (
      "\\[\n"
      + surjective_match.group(
        "math"
      )
      + r"\quad\text{は全射}. \qquad ("
    )

    display_start = rendered.find(
      display_prefix
    )

    if display_start < 0:
      continue

    display_end = rendered.find(
      "\n\\]",
      display_start,
    )

    if display_end < 0:
      continue

    display_end += len(
      "\n\\]"
    )

    target_group_pattern = re.compile(
      r"^\[R[0-9]+\] より, \$"
      + re.escape(
        target_group_latex
      )
      + r" = .+\$\.$",
      flags=re.MULTILINE,
    )

    target_group_match = (
      target_group_pattern.search(
        rendered
      )
    )

    if target_group_match is None:
      continue

    target_group_line = (
      target_group_match.group(
        0
      )
    )

    if (
      target_group_match.start()
      > display_end
    ):
      continue

    source_start = (
      target_group_match.start()
    )
    source_end = (
      target_group_match.end()
    )

    while (
      source_end < len(
        rendered
      )
      and rendered[
        source_end
      ]
      == "\n"
    ):
      source_end += 1

    without_source = (
      rendered[
        :source_start
      ]
      + rendered[
        source_end:
      ]
    )

    display_start = without_source.find(
      display_prefix
    )

    if display_start < 0:
      continue

    display_end = without_source.find(
      "\n\\]",
      display_start,
    )

    if display_end < 0:
      continue

    display_end += len(
      "\n\\]"
    )

    return (
      without_source[
        :display_end
      ]
      + "\n\n"
      + target_group_line
      + without_source[
        display_end:
      ]
    )

  return rendered




























def _phase159_r1_7c_preexisting_render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  rendered = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  rendered = (
    _phase158_normalize_public_narrative_contract(
      presentation,
      rendered,
    )
  )
  rendered = (
    _phase159_normalize_public_map_property_wording(
      presentation,
      rendered,
    )
  )
  rendered = (
    _phase159_normalize_public_reference_map_property_wording(
      rendered
    )
  )
  rendered = (
    _phase159_r1_6c_canonicalize_toda_51_reference(
      rendered
    )
  )
  rendered = (
    _phase159_r1_6c_remove_redundant_exactness_sentence(
      rendered
    )
  )
  rendered = (
    _phase159_r1_6c_link_proof_reasons(
      presentation,
      rendered,
    )
  )
  rendered = (
    _phase159_r1_6c_render_statement_numbers(
      rendered
    )
  )
  rendered = (
    _phase159_r1_6d_finalize_reference_and_linkage(
      presentation,
      rendered,
    )
  )
  rendered = (
    _phase159_r1_6d_center_structural_formulas(
      rendered
    )
  )
  rendered = (
    _phase159_r1_6d_reorder_target_group_fact_after_surjectivity(
      presentation,
      rendered,
    )
  )

  return (
    _phase159_inject_foundational_reference_section(
      presentation,
      rendered,
    )
  )

def _phase159_r1_7c_inline_math_content(
  line: str,
) -> str | None:
  if line.count(
    "$"
  ) != 2:
    return None

  math_start = line.find(
    "$"
  )
  math_end = line.find(
    "$",
    math_start + 1,
  )

  if (
    math_start < 0
    or math_end < 0
  ):
    return None

  content = line[
    math_start + 1:
    math_end
  ]

  tag_number = (
    _phase158_public_equation_tag_number(
      content
    )
  )

  if tag_number is not None:
    content = content.replace(
      (
        r"\tag{"
        + str(
          tag_number
        )
        + "}"
      ),
      "",
      1,
    )

  return content.strip()


def _phase159_r1_7c_rendered_step_math_content(
  proof_step: ProofStep,
) -> str | None:
  rendered = (
    _render_generic_narrative_step(
      proof_step
    )
  )

  if (
    not rendered
    or rendered.count(
      "$"
    )
    != 2
  ):
    return None

  math_start = rendered.find(
    "$"
  )
  math_end = rendered.find(
    "$",
    math_start + 1,
  )

  if (
    math_start < 0
    or math_end < 0
  ):
    return None

  return rendered[
    math_start + 1:
    math_end
  ].strip()


def _phase159_r1_7c_exact_step_line_indices(
  proof_body: list[
    str
  ],
  proof_step: ProofStep,
) -> tuple[
  int,
  ...,
]:
  expected = (
    _phase159_r1_7c_rendered_step_math_content(
      proof_step
    )
  )

  if expected is None:
    return ()

  return tuple(
    index
    for index, line in enumerate(
      proof_body
    )
    if (
      _phase159_r1_7c_inline_math_content(
        line
      )
      == expected
    )
  )


def _phase159_r1_7c_rendered_equality_parts(
  proof_step: ProofStep,
) -> tuple[
  str,
  str,
] | None:
  content = (
    _phase159_r1_7c_rendered_step_math_content(
      proof_step
    )
  )

  if (
    content is None
    or content.count(
      " = "
    )
    != 1
  ):
    return None

  left, right = content.split(
    " = ",
    1,
  )

  if (
    not left
    or not right
  ):
    return None

  return (
    left,
    right,
  )

def _phase159_r1_7c_equality_transitivity_chain_latex(
  proof_step: ProofStep,
) -> str | None:
  conclusion = proof_step.conclusion
  inference_rule = proof_step.inference_rule

  if (
    inference_rule is None
    or inference_rule.name
    != "equality transitivity"
    or not isinstance(
      conclusion,
      Relation,
    )
    or conclusion.relation_type
    is not RelationType.EQUALITY
    or len(
      proof_step.premises
    )
    != 2
  ):
    return None

  first_step, second_step = (
    proof_step.premises
  )
  first = first_step.conclusion
  second = second_step.conclusion

  if (
    not isinstance(
      first,
      Relation,
    )
    or first.relation_type
    is not RelationType.EQUALITY
    or not isinstance(
      second,
      Relation,
    )
    or second.relation_type
    is not RelationType.EQUALITY
  ):
    return None

  first_parts = (
    _phase159_r1_7c_rendered_equality_parts(
      first_step
    )
  )
  second_parts = (
    _phase159_r1_7c_rendered_equality_parts(
      second_step
    )
  )
  conclusion_parts = (
    _phase159_r1_7c_rendered_equality_parts(
      proof_step
    )
  )

  if (
    first_parts is None
    or second_parts is None
    or conclusion_parts is None
  ):
    return None

  first_left, first_right = (
    first_parts
  )
  second_left, second_right = (
    second_parts
  )
  conclusion_left, conclusion_right = (
    conclusion_parts
  )

  if (
    first_left == conclusion_left
    and first_right == second_left
    and second_right == conclusion_right
  ):
    middle = first_right
  elif (
    second_left == conclusion_left
    and second_right == first_left
    and first_right == conclusion_right
  ):
    middle = second_right
  else:
    return None

  if middle == conclusion_right:
    return None

  return (
    conclusion_left
    + " = "
    + middle
    + " = "
    + conclusion_right
  )



def _phase159_r1_7c_reference_prefix(
  line: str,
) -> str:
  math_start = line.find(
    "$"
  )

  if math_start < 0:
    return ""

  prefix = line[
    :math_start
  ]

  if (
    prefix.endswith(
      "より, "
    )
    or prefix.endswith(
      "より,"
    )
  ):
    return prefix

  return ""


def _phase159_r1_7c_equation_number_reused(
  proof_body: list[
    str
  ],
  number: int,
  ignored_indices: frozenset[
    int
  ],
) -> bool:
  marker = (
    "("
    + str(
      number
    )
    + ")"
  )

  return any(
    marker in line
    for index, line in enumerate(
      proof_body
    )
    if index not in ignored_indices
  )


def _phase159_r1_7c_collapse_equality_transitivity_chains(
  presentation: TodaGroupProofPresentation,
  proof_body: list[
    str
  ],
) -> list[
  str
]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    proof_body,
    list,
  ):
    raise TypeError(
      "proof_body must be a list"
    )

  semantic_presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )
  result = list(
    proof_body
  )

  for node in semantic_presentation.nodes:
    proof_step = node.proof_step
    chain_latex = (
      _phase159_r1_7c_equality_transitivity_chain_latex(
        proof_step
      )
    )

    if chain_latex is None:
      continue

    first_step, second_step = (
      proof_step.premises
    )

    first_parts = (
      _phase159_r1_7c_rendered_equality_parts(
        first_step
      )
    )
    second_parts = (
      _phase159_r1_7c_rendered_equality_parts(
        second_step
      )
    )
    conclusion_parts = (
      _phase159_r1_7c_rendered_equality_parts(
        proof_step
      )
    )

    if (
      first_parts is None
      or second_parts is None
      or conclusion_parts is None
    ):
      continue

    first_left, first_right = (
      first_parts
    )
    second_left, second_right = (
      second_parts
    )
    conclusion_left, conclusion_right = (
      conclusion_parts
    )

    if (
      first_left == conclusion_left
      and first_right == second_left
      and second_right == conclusion_right
    ):
      ordered_steps = (
        first_step,
        second_step,
      )
      middle = first_right
    elif (
      second_left == conclusion_left
      and second_right == first_left
      and first_right == conclusion_right
    ):
      ordered_steps = (
        second_step,
        first_step,
      )
      middle = second_right
    else:
      continue

    first_indices = (
      _phase159_r1_7c_exact_step_line_indices(
        result,
        ordered_steps[
          0
        ],
      )
    )
    second_indices = (
      _phase159_r1_7c_exact_step_line_indices(
        result,
        ordered_steps[
          1
        ],
      )
    )
    conclusion_indices = (
      _phase159_r1_7c_exact_step_line_indices(
        result,
        proof_step,
      )
    )

    if (
      len(
        first_indices
      )
      == 1
      and len(
        second_indices
      )
      == 1
      and len(
        conclusion_indices
      )
      == 1
    ):
      first_index = first_indices[
        0
      ]
      second_index = second_indices[
        0
      ]
      conclusion_index = (
        conclusion_indices[
          0
        ]
      )

      if not (
        first_index
        < second_index
        < conclusion_index
      ):
        continue

      first_number = (
        _phase158_public_equation_tag_number(
          result[
            first_index
          ]
        )
      )
      second_number = (
        _phase158_public_equation_tag_number(
          result[
            second_index
          ]
        )
      )

      if (
        first_number is None
        or second_number is None
      ):
        continue

      connector_indices = tuple(
        index
        for index in range(
          second_index + 1,
          conclusion_index,
        )
        if (
          _phase158_public_equation_connector_numbers(
            result[
              index
            ]
          )
          == (
            first_number,
            second_number,
          )
        )
      )

      if len(
        connector_indices
      ) != 1:
        continue

      connector_index = (
        connector_indices[
          0
        ]
      )
      local_indices = frozenset(
        (
          first_index,
          second_index,
          connector_index,
          conclusion_index,
        )
      )

      if (
        _phase159_r1_7c_equation_number_reused(
          result,
          first_number,
          local_indices,
        )
        or _phase159_r1_7c_equation_number_reused(
          result,
          second_number,
          local_indices,
        )
      ):
        continue

      allowed_nonblank_indices = {
        first_index,
        second_index,
        connector_index,
        conclusion_index,
      }

      if any(
        result[
          index
        ].strip()
        and index
        not in allowed_nonblank_indices
        for index in range(
          first_index,
          conclusion_index + 1,
        )
      ):
        continue

      prefix = (
        _phase159_r1_7c_reference_prefix(
          result[
            first_index
          ]
        )
      )
      replacement = (
        prefix
        + "$"
        + chain_latex
        + "$."
      )

      result[
        first_index:
        conclusion_index + 1
      ] = [
        replacement,
      ]
      continue

    projected_indices = []

    for index, line in enumerate(
      result
    ):
      content = (
        _phase159_r1_7c_inline_math_content(
          line
        )
      )

      if content is None:
        continue

      if (
        content.startswith(
          conclusion_left
          + " = "
        )
        and content.endswith(
          " = "
          + middle
        )
      ):
        projected_indices.append(
          index
        )
        continue

      if content == (
        conclusion_left
        + " = "
        + middle
      ):
        projected_indices.append(
          index
        )

    if len(
      projected_indices
    ) != 1:
      continue

    projected_index = (
      projected_indices[
        0
      ]
    )
    line = result[
      projected_index
    ]
    math_start = line.find(
      "$"
    )
    math_end = line.find(
      "$",
      math_start + 1,
    )

    if (
      math_start < 0
      or math_end < 0
    ):
      continue

    result[
      projected_index
    ] = (
      line[
        :math_start + 1
      ]
      + chain_latex
      + line[
        math_end:
      ]
    )

  return (
    _phase158_normalize_public_equation_numbers(
      result
    )
  )




def _phase159_r1_7c_normalize_public_equality_chains(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  proof_marker = "\n## 証明\n"

  if proof_marker not in rendered:
    return rendered

  prefix, proof = rendered.split(
    proof_marker,
    1,
  )
  proof_lines = proof.rstrip().splitlines()

  normalized_lines = (
    _phase159_r1_7c_collapse_equality_transitivity_chains(
      presentation,
      proof_lines,
    )
  )

  return (
    prefix
    + proof_marker
    + "\n".join(
      normalized_lines
    ).rstrip()
    + "\n"
  )

def _phase159_r1_7c_r4_normalize_public_map_property_prose(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  replacements = (
    (
      "は単射である.",
      "は単射.",
    ),
    (
      "は全射である.",
      "は全射.",
    ),
    (
      "は同型写像である.",
      "は同型.",
    ),
    (
      "は同型である.",
      "は同型.",
    ),
    (
      "は零写像である.",
      "は零写像.",
    ),
  )

  normalized = rendered

  for old, new in replacements:
    normalized = normalized.replace(
      old,
      new,
    )

  return normalized



def _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  proof_marker = "## 証明\n\n"
  marker_index = rendered.find(
    proof_marker
  )

  if marker_index < 0:
    return rendered

  proof_start = (
    marker_index
    + len(
      proof_marker
    )
  )
  prefix = rendered[
    :proof_start
  ]
  proof_body = rendered[
    proof_start:
  ]
  lines = proof_body.splitlines()

  reference_prefix = re.compile(
    r"^\[R\d+\]より,\s*"
  )
  connector_prefix = re.compile(
    r"^\((\d+)\),\s*\((\d+)\)\s+より,\s*"
  )
  tag_pattern = re.compile(
    r"\\tag\{(\d+)\}"
  )

  def map_property(
    line: str,
    suffix: str,
  ) -> tuple[
    str,
    int | None,
  ] | None:
    stripped = line.strip()
    stripped = reference_prefix.sub(
      "",
      stripped,
    )

    if not stripped.endswith(
      suffix
    ):
      return None

    map_text = stripped[
      :-len(
        suffix
      )
    ].strip()

    tag_match = tag_pattern.search(
      map_text
    )
    tag_number = (
      int(
        tag_match.group(
          1
        )
      )
      if tag_match is not None
      else None
    )
    map_text = tag_pattern.sub(
      "",
      map_text,
    ).strip()

    return (
      map_text,
      tag_number,
    )

  def isomorphism_map(
    line: str,
  ) -> tuple[
    str,
    bool,
  ] | None:
    stripped = line.strip()

    if reference_prefix.match(
      stripped
    ):
      return None

    had_connector = (
      connector_prefix.match(
        stripped
      )
      is not None
    )
    stripped = connector_prefix.sub(
      "",
      stripped,
    )

    for suffix in (
      " は同型.",
      " は同型写像.",
      " は同型である.",
      " は同型写像である.",
    ):
      if stripped.endswith(
        suffix
      ):
        return (
          tag_pattern.sub(
            "",
            stripped[
              :-len(
                suffix
              )
            ].strip(),
          ),
          had_connector,
        )

    return None

  injective_by_map = {}
  surjective_by_map = {}
  isomorphism_by_map = {}

  for index, line in enumerate(
    lines
  ):
    injective = map_property(
      line,
      " は単射.",
    )

    if injective is not None:
      injective_by_map.setdefault(
        injective[0],
        [],
      ).append(
        (
          index,
          injective[1],
        )
      )

    surjective = map_property(
      line,
      " は全射.",
    )

    if surjective is not None:
      surjective_by_map.setdefault(
        surjective[0],
        [],
      ).append(
        (
          index,
          surjective[1],
        )
      )

    isomorphism = isomorphism_map(
      line
    )

    if isomorphism is not None:
      isomorphism_by_map.setdefault(
        isomorphism[0],
        [],
      ).append(
        (
          index,
          isomorphism[1],
        )
      )

  existing_numbers = tuple(
    int(
      match.group(
        1
      )
    )
    for line in lines
    for match in tag_pattern.finditer(
      line
    )
  )
  next_number = (
    max(
      existing_numbers,
      default=0,
    )
    + 1
  )

  numbered_map_properties = {}

  for map_text in tuple(
    isomorphism_by_map
  ):
    injective_rows = injective_by_map.get(
      map_text,
      (),
    )
    surjective_rows = surjective_by_map.get(
      map_text,
      (),
    )

    if (
      not injective_rows
      or not surjective_rows
    ):
      continue

    injective_index, injective_number = (
      injective_rows[
        0
      ]
    )
    surjective_index, surjective_number = (
      surjective_rows[
        0
      ]
    )

    if injective_number is None:
      injective_number = next_number
      next_number += 1

    if surjective_number is None:
      surjective_number = next_number
      next_number += 1

    numbered_map_properties[
      injective_index
    ] = (
      map_text,
      "は単射",
      injective_number,
    )
    numbered_map_properties[
      surjective_index
    ] = (
      map_text,
      "は全射",
      surjective_number,
    )

    isomorphism_index, _had_connector = (
      isomorphism_by_map[
        map_text
      ][
        0
      ]
    )
    lines[
      isomorphism_index
    ] = (
      "("
      + str(
        injective_number
      )
      + "), ("
      + str(
        surjective_number
      )
      + ") より, "
      + map_text
      + " は同型."
    )

  output_lines = []

  for index, line in enumerate(
    lines
  ):
    numbered = numbered_map_properties.get(
      index
    )

    if numbered is None:
      output_lines.append(
        line
      )
      continue

    map_text, property_text, number = numbered

    if (
      map_text.startswith(
        "$"
      )
      and map_text.endswith(
        "$"
      )
    ):
      map_text = map_text[
        1:-1
      ]

    output_lines.extend(
      (
        r"\[",
        (
          map_text
          + r"\quad\text{"
          + property_text
          + r"}. \qquad ("
          + str(
            number
          )
          + ")"
        ),
        r"\]",
      )
    )

  return (
    prefix
    + "\n".join(
      output_lines
    )
    + (
      "\n"
      if rendered.endswith(
        "\n"
      )
      else ""
    )
  )



def _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  proof_marker = "## 証明\n\n"
  marker_index = rendered.find(
    proof_marker
  )

  if marker_index < 0:
    return rendered

  proof_start = (
    marker_index
    + len(
      proof_marker
    )
  )
  prefix = rendered[
    :proof_start
  ]
  proof_body = rendered[
    proof_start:
  ]

  had_trailing_newline = (
    rendered.endswith(
      "\n"
    )
  )
  paragraphs = proof_body.rstrip(
    "\n"
  ).split(
    "\n\n"
  )

  tag_pattern = re.compile(
    r"\\tag\{(\d+)\}"
  )
  reference_pattern = re.compile(
    (
      r"^"
      r"((?:\(\d+\)"
      r"(?:,\s*|\s+と\s+)?)+)"
      r"\s*より,"
    )
  )
  parenthesized_number_pattern = re.compile(
    r"\((\d+)\)"
  )

  changed = True

  while changed:
    changed = False
    tag_paragraph_by_number = {}

    for paragraph_index, paragraph in enumerate(
      paragraphs
    ):
      for match in tag_pattern.finditer(
        paragraph
      ):
        number = int(
          match.group(
            1
          )
        )
        tag_paragraph_by_number.setdefault(
          number,
          paragraph_index,
        )

    for conclusion_index, paragraph in enumerate(
      paragraphs
    ):
      stripped = paragraph.strip()
      reference_match = reference_pattern.match(
        stripped
      )

      if reference_match is None:
        continue

      reference_numbers = tuple(
        int(
          number
        )
        for number in parenthesized_number_pattern.findall(
          reference_match.group(
            1
          )
        )
      )

      if not reference_numbers:
        continue

      referenced_indices = tuple(
        tag_paragraph_by_number.get(
          number
        )
        for number in reference_numbers
      )

      if any(
        index is None
        for index in referenced_indices
      ):
        continue

      target_index = max(
        index
        for index in referenced_indices
        if index is not None
      )

      if target_index < conclusion_index:
        continue

      conclusion = paragraphs.pop(
        conclusion_index
      )

      if conclusion_index < target_index:
        target_index -= 1

      paragraphs.insert(
        target_index + 1,
        conclusion,
      )
      changed = True
      break

  result = (
    prefix
    + "\n\n".join(
      paragraphs
    )
  )

  if had_trailing_newline:
    result += "\n"

  return result

def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  rendered = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  rendered = (
    _phase158_normalize_public_narrative_contract(
      presentation,
      rendered,
    )
  )
  rendered = (
    _phase159_r1_7c_r4_normalize_public_map_property_prose(
      rendered
    )
  )
  rendered = (
    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
      rendered
    )
  )

  return (
    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(
      rendered
    )
  )

