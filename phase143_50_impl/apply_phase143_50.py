from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def replace_once(
  path: Path,
  old: str,
  new: str,
) -> None:
  text = path.read_text(
    encoding="utf-8",
  )

  if old not in text:
    raise RuntimeError(
      f"expected source block not found in {path}"
    )

  path.write_text(
    text.replace(
      old,
      new,
      1,
    ),
    encoding="utf-8",
  )
  print(
    f"updated {path}"
  )


def main() -> None:
  generic_path = (
    ROOT
    / "toda_group_proof_generic_narrative_renderer.py"
  )
  body_path = (
    ROOT
    / "toda_group_proof_narrative_argument_body_renderer.py"
  )

  old_import = '''from toda_rules import (
  TodaDeltaInjectiveStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaIteratedSuspensionInjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaProp44SuspensionInjectiveStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionSurjectiveStatement,
)
'''

  new_import = '''from toda_rules import (
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
'''

  replace_once(
    generic_path,
    old_import,
    new_import,
  )

  anchor = '''def _render_generic_narrative_step(
  proof_step: ProofStep,
) -> str:
'''

  helper = r'''def _render_generic_narrative_group_map_latex(
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


'''

  text = generic_path.read_text(
    encoding="utf-8",
  )
  if anchor not in text:
    raise RuntimeError(
      f"expected insertion anchor not found in {generic_path}"
    )
  generic_path.write_text(
    text.replace(
      anchor,
      helper + anchor,
      1,
    ),
    encoding="utf-8",
  )
  print(
    f"updated {generic_path}"
  )

  old_step_start = '''  statement = proof_step.conclusion

  try:
    latex = (
      render_repository_conclusion_latex(
        statement
      )
    )
'''

  new_step_start = '''  statement = proof_step.conclusion

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
'''

  replace_once(
    generic_path,
    old_step_start,
    new_step_start,
  )

  old_exactness_render = '''    if (
      contribution.kind
      is TodaGroupProofNarrativeExactnessDisplayContributionKind
      .EXACTNESS_WINDOW
    ):
      lines.append(
        "$"
        + contribution.latex
        + "$"
      )
      lines.append(
        ""
      )
      continue
'''

  new_exactness_render = r'''    if (
      contribution.kind
      is TodaGroupProofNarrativeExactnessDisplayContributionKind
      .EXACTNESS_WINDOW
    ):
      exactness_latex = (
        contribution.latex
      )
      english_suffix = (
        r" \text{ is exact}"
      )

      if exactness_latex.endswith(
        english_suffix
      ):
        exactness_latex = (
          exactness_latex[
            :-len(
              english_suffix
            )
          ]
        )

      lines.append(
        "$"
        + exactness_latex
        + "$ は完全である."
      )
      lines.append(
        ""
      )
      continue
'''

  replace_once(
    body_path,
    old_exactness_render,
    new_exactness_render,
  )

  test_source = (
    Path(__file__).resolve().parent
    / "tests"
    / "test_phase143_50_generic_statement_prose_renderer.py"
  )
  test_destination = (
    ROOT
    / "tests"
    / "test_phase143_50_generic_statement_prose_renderer.py"
  )
  test_destination.write_text(
    test_source.read_text(
      encoding="utf-8",
    ),
    encoding="utf-8",
  )
  print(
    f"copied {test_source} -> {test_destination}"
  )


if __name__ == "__main__":
  main()
