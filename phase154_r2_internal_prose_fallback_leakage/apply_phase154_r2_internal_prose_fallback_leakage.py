from pathlib import Path
import shutil

REPO_ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = {
    "toda_group_proof_generic_narrative_renderer.py": {
        "_render_generic_narrative_statement_prose": 'def _render_generic_narrative_statement_prose(\n  statement,\n) -> str | None:\n  reference_prose = (\n    _render_phase153_r3_9_reference_statement_prose(\n      statement\n    )\n  )\n\n  if reference_prose is not None:\n    return reference_prose\n\n  reference_prose = (\n    _render_phase153_r3_6_reference_statement_prose(\n      statement\n    )\n  )\n\n  if reference_prose is not None:\n    return reference_prose\n\n  aggregate_prose = (\n    render_toda_group_proof_aggregate_statement_prose(\n      statement\n    )\n  )\n\n  if aggregate_prose is not None:\n    return aggregate_prose\n\n  if isinstance(\n    statement,\n    TodaProp42ExactnessStatement,\n  ):\n    window = statement.window\n    return (\n      "$"\n      + render_toda_primary_group_latex(\n        window.source_term\n      )\n      + r" \\xrightarrow{"\n      + window.first_map.name\n      + r"} "\n      + render_toda_primary_group_latex(\n        window.middle_term\n      )\n      + r" \\xrightarrow{"\n      + window.second_map.name\n      + r"} "\n      + render_toda_primary_group_latex(\n        window.target_term\n      )\n      + "$ は完全である."\n    )\n\n  if isinstance(\n    statement,\n    _GENERIC_INJECTIVE_STATEMENT_TYPES,\n  ):\n    map_latex = (\n      _render_generic_narrative_group_map_latex(\n        statement.map\n      )\n    )\n\n    if map_latex is None:\n      return None\n\n    return (\n      "$"\n      + map_latex\n      + "$ は単射である."\n    )\n\n  if isinstance(\n    statement,\n    _GENERIC_SURJECTIVE_STATEMENT_TYPES,\n  ):\n    map_latex = (\n      _render_generic_narrative_group_map_latex(\n        statement.map\n      )\n    )\n\n    if map_latex is None:\n      return None\n\n    return (\n      "$"\n      + map_latex\n      + "$ は全射である."\n    )\n\n  if isinstance(\n    statement,\n    _GENERIC_ISOMORPHISM_STATEMENT_TYPES,\n  ):\n    map_latex = (\n      _render_generic_narrative_group_map_latex(\n        statement.map\n      )\n    )\n\n    if map_latex is None:\n      return None\n\n    return (\n      "$"\n      + map_latex\n      + "$ は同型写像である."\n    )\n\n  if isinstance(\n    statement,\n    _GENERIC_ZERO_MAP_STATEMENT_TYPES,\n  ):\n    map_latex = (\n      _render_generic_narrative_group_map_latex(\n        statement.map\n      )\n    )\n\n    if map_latex is None:\n      return None\n\n    return (\n      "$"\n      + map_latex\n      + "$ は零写像である."\n    )\n\n  if isinstance(\n    statement,\n    TodaNuFamilyDefinitionStatement,\n  ):\n    return (\n      "$"\n      + render_toda_expression_latex(\n        statement.element\n      )\n      + r"$ を \\(\\nu\\)-family の元として定める."\n    )\n\n  if isinstance(\n    statement,\n    TodaSigmaFamilyDefinitionStatement,\n  ):\n    return (\n      "$"\n      + render_toda_expression_latex(\n        statement.element\n      )\n      + r"$ を \\(\\sigma\\)-family の元として定める."\n    )\n\n  return None\n',
    },
    "toda_group_proof_narrative_contribution_renderer.py": {
        "_insert_toda_group_proof_narrative_argument_contributions": 'def _insert_toda_group_proof_narrative_argument_contributions(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n  blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  arguments: tuple[\n    TodaGroupProofNarrativeArgument,\n    ...,\n  ],\n  ordered_contributions,\n) -> str:\n  insertion_indices = (\n    _contribution_insertion_indices(\n      markdown,\n      blocks,\n      arguments,\n      ordered_contributions,\n    )\n  )\n  connector_by_target_step_id = (\n    _contribution_connector_lines(\n      presentation,\n      ordered_contributions,\n    )\n  )\n  insertions_by_index = {}\n\n  for argument_index, contributions in enumerate(\n    ordered_contributions\n  ):\n    for contribution_index, contribution in enumerate(\n      contributions\n    ):\n      contribution_line = (\n        _render_generic_narrative_step(\n          contribution.proof_step\n        )\n      )\n      if not contribution_line:\n        continue\n      if not (\n        _is_toda_group_proof_narrative_reference_statement_candidate(\n          contribution.proof_step,\n          contribution_line,\n        )\n      ):\n        continue\n      if contribution_line in markdown:\n        continue\n\n      insertion_index = insertion_indices[\n        argument_index\n      ][\n        contribution_index\n      ]\n      if insertion_index is None:\n        continue\n\n      connector = (\n        connector_by_target_step_id.get(\n          id(\n            contribution.proof_step\n          )\n        )\n      )\n      lines = []\n      if connector is not None:\n        lines.append(\n          connector\n        )\n      lines.append(\n        contribution_line\n      )\n\n      insertions_by_index.setdefault(\n        insertion_index,\n        [],\n      ).append(\n        "\\n\\n".join(\n          lines\n        )\n      )\n\n  rendered = markdown\n\n  for insertion_index in sorted(\n    insertions_by_index,\n    reverse=True,\n  ):\n    contribution_fragments = insertions_by_index[\n      insertion_index\n    ]\n    insertion = (\n      "\\n\\n"\n      + "\\n\\n".join(\n        contribution_fragments\n      )\n    )\n\n    if (\n      insertion_index < len(markdown)\n      and not markdown[\n        insertion_index:\n      ].startswith(\n        "\\n\\n"\n      )\n    ):\n      insertion += "\\n\\n"\n\n    rendered = (\n      rendered[\n        :insertion_index\n      ]\n      + insertion\n      + rendered[\n        insertion_index:\n      ]\n    )\n\n  return rendered\n',
    },
    "toda_group_proof_narrative_renderer.py": {
        "_render_group_proof_narrative_fact": 'def _render_group_proof_narrative_fact(\n  proof_step: ProofStep,\n) -> str:\n  if not isinstance(\n    proof_step,\n    ProofStep,\n  ):\n    raise TypeError(\n      "proof_step must be a ProofStep"\n    )\n\n  statement = proof_step.conclusion\n\n  generic_fact = (\n    _render_generic_narrative_step(\n      proof_step\n    )\n  )\n  internal_fallbacks = {\n    (\n      proof_step.inference_rule.name\n      if proof_step.inference_rule is not None\n      else None\n    ),\n    (\n      "`"\n      + type(\n        statement\n      ).__name__\n      + "`"\n    ),\n  }\n\n  if (\n    generic_fact\n    and generic_fact not in internal_fallbacks\n  ):\n    return generic_fact\n\n  latex = (\n    _render_group_proof_narrative_latex(\n      proof_step\n    )\n  )\n\n  if latex is not None:\n    return (\n      "$"\n      + latex\n      + "$"\n    )\n\n  label = (\n    _group_proof_narrative_statement_label(\n      statement\n    )\n  )\n\n  if label is not None:\n    return label\n\n  return "補助結果"\n',
    },
}

def replace_function(source: str, name: str, replacement: str) -> str:
    marker = "def " + name + "("
    start = source.find(marker)
    if start < 0:
        raise RuntimeError(f"function not found: {name}")
    next_def = source.find("\ndef ", start + len(marker))
    if next_def < 0:
        end = len(source)
        suffix = ""
    else:
        end = next_def + 1
        suffix = source[end:]
    prefix = source[:start]
    return prefix + replacement.rstrip() + "\n\n" + suffix

def main():
    backup_dir = REPO_ROOT / "phase154_r2_internal_prose_fallback_leakage" / "backup_before_r2"
    backup_dir.mkdir(parents=True, exist_ok=True)

    for relative_path, functions in REPLACEMENTS.items():
        path = REPO_ROOT / relative_path
        if not path.exists():
            raise RuntimeError(f"missing production file: {relative_path}")

        backup = backup_dir / relative_path
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)

        source = path.read_text(encoding="utf-8")
        for name, replacement in functions.items():
            source = replace_function(
                source,
                name,
                replacement,
            )
        path.write_text(
            source,
            encoding="utf-8",
        )
        print("updated:", relative_path)

    test_source = (
        Path(__file__).resolve().parent
        / "tests"
        / "test_phase154_r2_internal_prose_fallback_leakage.py"
    )
    test_target = (
        REPO_ROOT
        / "tests"
        / "test_phase154_r2_internal_prose_fallback_leakage.py"
    )
    shutil.copy2(
        test_source,
        test_target,
    )
    print("added:", test_target.relative_to(REPO_ROOT))

if __name__ == "__main__":
    main()
