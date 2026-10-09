def build_standard_web_group_proof_view(
  n: int,
  k: int,
  max_depth: int = 2,
  mode: str = "narrative",
) -> WebGroupProofView:
  if (
    mode == "narrative"
    and k == 1
    and n in (4, 5)
  ):
    from phase162_r4_b3_web_common_display import (
      build_phase162_r4_b3_web_common_display_view,
    )
    return build_phase162_r4_b3_web_common_display_view(
      n=n, k=k, max_depth=max_depth,
    )

  query = TodaGroupQuery(
    n=n,
    k=k,
  )

  domain = (
    classify_toda_group_query_domain(
      query
    )
  )

  if (
    domain.kind
    is not (
      TodaGroupQueryDomainKind
      .POSITIVE_DIMENSION
    )
  ):
    raise ValueError(
      "group proof is available only for "
      "repository-backed group results"
    )

  if (
    isinstance(
      max_depth,
      bool,
    )
    or not isinstance(
      max_depth,
      int,
    )
  ):
    raise TypeError(
      "max_depth must be an int"
    )

  if max_depth < 0:
    raise ValueError(
      "max_depth must be nonnegative"
    )

  if mode not in (
    "trace",
    "outline",
    "narrative",
  ):
    raise ValueError(
      "mode must be trace, outline, or narrative"
    )

  report = (
    build_standard_toda_report(
      n=n,
      k=k,
    )
  )

  if (
    report.status
    is TodaCalculationStatus.NOT_FOUND
  ):
    raise ValueError(
      "no proof-backed group result found"
    )

  if (
    report.status
    is TodaCalculationStatus.MULTIPLE_RESULTS
  ):
    raise ValueError(
      "group proof requires exactly one result"
    )

  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )

  if n == 3 and k == 2 and mode == "narrative":
    from phase162_pi5_3_web_replay import (
      build_phase162_pi5_3_web_replay,
    )
    replay = build_phase162_pi5_3_web_replay(
      max_depth=max(max_depth, 40),
    )
  else:
    replay = (
      build_toda_group_result_proof_replay(
        group_result,
        max_depth=max_depth,
      )
    )

  (
    conclusion_latex,
    conclusion_fallback,
  ) = _group_proof_statement_latex(
    replay.root_step.conclusion
  )

  if conclusion_latex is None:
    raise ValueError(
      "group conclusion is not renderable as LaTeX: "
      f"{conclusion_fallback}"
    )

  steps = []

  for replay_step in replay.steps:
    (
      statement_latex,
      fallback_type_name,
    ) = _group_proof_statement_latex(
      replay_step.proof_step.conclusion
    )

    steps.append(
      WebGroupProofStepView(
        depth=replay_step.depth,
        statement_latex=statement_latex,
        fallback_type_name=fallback_type_name,
        rule_name=(
          _group_proof_rule_name(
            replay_step.proof_step
          )
        ),
        role_name=replay_step.role.value,
      )
    )

  rendered_lines = ()

  if mode != "trace":
    presentation = (
      build_toda_group_proof_presentation(
        replay
      )
    )

    if mode == "outline":
      markdown = (
        render_toda_group_proof_outline_markdown(
          presentation
        )
      )
    else:
      markdown = (
        render_toda_group_proof_narrative_markdown(
          presentation
        )
      )

    rendered_lines = (
      _build_group_proof_rendered_lines(
        markdown
      )
    )

  return WebGroupProofView(
    n=n,
    k=k,
    conclusion_latex=conclusion_latex,
    theorem=replay.source_entry.theorem,
    phase=replay.source_entry.phase,
    key=replay.source_entry.key,
    steps=tuple(
      steps
    ),
    max_depth=replay.max_depth,
    mode=mode,
    rendered_lines=rendered_lines,
  )
