from proof import (
  ProofStep,
  Relation,
  RelationType,
)
from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda48Pi16_9OrderAndE4InjectiveStatement,
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionIsomorphismStatement,
  Toda56Nu4DecompositionStatement,
  TodaDeltaZeroStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaIteratedSuspensionInjectiveStatement,
  TodaLemma513Statement,
  TodaLemma514Sigma8Statement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma54Statement,
  TodaProp42ExactnessStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp56FiniteDimensionalStatement,
  TodaProp56Pi8_5QuotientStatement,
  TodaSigmaFamilyDefinitionStatement,
  TodaSuspensionInjectiveStatement,
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


def _phase134_3_pi6_3_numbered_steps(
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


def _append_phase134_3_pi6_3_fact(
  lines: list[str],
  presentation: TodaGroupProofPresentation,
  proof_step: ProofStep,
  number_by_step_id: dict[
    int,
    int,
  ],
) -> None:
  number = number_by_step_id[
    id(
      proof_step
    )
  ]

  edges = (
    _narrative_edges_for_parent(
      presentation,
      proof_step,
    )
  )

  premise_numbers = tuple(
    number_by_step_id[
      id(
        edge.premise_step
      )
    ]
    for edge in edges
  )

  reference_text = (
    _phase134_3_reference_text(
      premise_numbers
    )
  )

  statement = proof_step.conclusion

  if proof_step is presentation.root_step:
    lines.append(
      "以上から,"
    )
  elif reference_text:
    lines.append(
      reference_text
      + " より,"
    )

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
        (
          "",
          r"\[",
          latex
          + r"\tag{"
          + str(
            number
          )
          + "}",
          r"\]",
          "",
          "は完全である.",
          "",
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
        (
          "",
          r"\[",
          latex
          + r"\tag{"
          + str(
            number
          )
          + "}",
          r"\]",
          "",
          "は単射である.",
          "",
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
        (
          "",
          r"\[",
          latex
          + r"\tag{"
          + str(
            number
          )
          + "}",
          r"\]",
          "",
          "は全射である.",
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
      (
        "",
        r"\[",
        latex
        + r"\tag{"
        + str(
          number
        )
        + "}",
        r"\]",
        "",
      )
    )

    if (
      isinstance(
        statement,
        Relation,
      )
      and statement.relation_type
      is RelationType.ORDER
    ):
      lines.extend(
        (
          "が成り立つ.",
          "",
        )
      )
      return

    if proof_step is presentation.root_step:
      lines.extend(
        (
          "を得る.",
          "",
        )
      )
      return

    lines.extend(
      (
        "が成り立つ.",
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

  if reference_text:
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


def _render_phase134_3_pi6_3_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  numbered_steps = (
    _phase134_3_pi6_3_numbered_steps(
      presentation
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

  root_latex = (
    _render_group_proof_narrative_latex(
      presentation.root_step
    )
  )

  lines = [
    "# Group proof narrative",
    "",
    "## 参照",
    "",
    "**[R1] Toda Proposition 5.6.**",
    "",
    "本証明では, Proposition 5.6 のうち次の主張を示す.",
    "",
    r"\[",
    root_latex,
    r"\]",
    "",
    "## 証明",
    "",
    (
      "[R1] の該当する主張を, "
      "既存の ProofStep graph から再構成する."
    ),
    "",
  ]

  for proof_step in numbered_steps:
    _append_phase134_3_pi6_3_fact(
      lines,
      presentation,
      proof_step,
      number_by_step_id,
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
