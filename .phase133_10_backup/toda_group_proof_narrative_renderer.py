from proof import ProofStep
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
  TodaIteratedSuspensionInjectiveStatement,
  TodaLemma513Statement,
  TodaLemma514Sigma8Statement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma54Statement,
  TodaProp51FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp56FiniteDimensionalStatement,
  TodaProp56Pi8_5QuotientStatement,
  TodaSigmaFamilyDefinitionStatement,
)


def _group_proof_narrative_statement_label(
  statement,
) -> str | None:
  if isinstance(
    statement,
    Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  ):
    return (
      "Theorem 3.6 から Lemma 5.14 への σ″ bridge"
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
    return "Toda Lemma 5.14 の σ′ branch"

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
    latex = (
      render_toda_proof_statement_latex(
        statement
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
