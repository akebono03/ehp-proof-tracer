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

  if proof_step.inference_rule is not None:
    return proof_step.inference_rule.name

  return (
    "`"
    + type(
      statement
    ).__name__
    + "`"
  )


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
            + "、すでに得た"
            + premise_fact
            + "を用いる。"
          )
        )
      continue

    premise_edges = (
      _narrative_edges_for_parent(
        presentation,
        premise_step,
      )
    )

    if premise_edges:
      _append_narrative_for_step(
        lines,
        presentation,
        premise_step,
        active_step_ids,
        expanded_step_ids,
      )

      lines.append(
        (
          _derivation_lead(
            len(
              premise_edges
            )
          )
          + "、"
          + premise_fact
          + "を得る。"
        )
      )
    else:
      lines.append(
        (
          lead
          + "、"
          + premise_fact
          + "を用いる。"
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

def render_toda_group_proof_narrative_markdown(
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

  phase134_24_pi15_8 = (
    _phase134_24_render_pi15_8_narrative(
      presentation
    )
  )

  if phase134_24_pi15_8 is not None:
    return phase134_24_pi15_8

  if (
    _is_phase134_3_pi6_3_presentation(
      presentation
    )
  ):
    return (
      _render_phase134_3_pi6_3_narrative_markdown(
        presentation
      )
    )

  if _is_phase134_9_pi8_5_presentation(
    presentation
  ):
    return (
      _render_phase134_9_pi8_5_narrative_markdown(
        presentation
      )
    )

  source_entry = presentation.source_entry

  theorem = (
    source_entry.theorem
    if source_entry.theorem is not None
    else "出典不明の結果"
  )

  lines = [
    "# Group proof narrative",
    "",
    theorem + "を用いる。",
    "",
  ]

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
            "$\\sigma_{9}$ の位数を確認し、"
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
    )

    lines.extend(
      (
        "",
        (
          "したがって、"
          + _render_group_proof_narrative_fact(
            presentation.root_step
          )
          + "を得る。"
        ),
      )
    )
  else:
    lines.append(
      (
        "したがって、"
        + _render_group_proof_narrative_fact(
          presentation.root_step
        )
        + "である。"
      )
    )

  return (
    "\n".join(
      lines
    )
    + "\n"
  )
