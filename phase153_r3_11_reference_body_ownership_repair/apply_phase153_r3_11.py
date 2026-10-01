from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent


def _replace_once(
    path: Path,
    old: str,
    new: str,
    label: str,
) -> None:
    text = path.read_text(
        encoding="utf-8",
    )
    count = text.count(
        old
    )

    if count != 1:
        raise RuntimeError(
            label
            + ": expected exactly one replacement target, found "
            + str(count)
        )

    path.write_text(
        text.replace(
            old,
            new,
            1,
        ),
        encoding="utf-8",
    )


def main() -> int:
    renderer_path = (
        REPO_ROOT
        / "toda_group_proof_narrative_contribution_renderer.py"
    )
    test_path = (
        REPO_ROOT
        / "tests"
        / "test_phase153_r3_11_reference_body_ownership_repair.py"
    )

    _replace_once(
        renderer_path,
        'def suppress_toda_group_proof_narrative_reference_body_duplicates(\n  body_markdown: str,\n  statement_lines_by_reference_number: dict[\n    int,\n    tuple[\n      str,\n      ...,\n    ],\n  ],\n) -> str:\n  if not isinstance(\n    body_markdown,\n    str,\n  ):\n    raise TypeError(\n      "body_markdown must be a str"\n    )\n\n  if not isinstance(\n    statement_lines_by_reference_number,\n    dict,\n  ):\n    raise TypeError(\n      "statement_lines_by_reference_number must be a dict"\n    )\n\n  lines = body_markdown.splitlines()\n\n  for reference_number, statement_lines in (\n    statement_lines_by_reference_number.items()\n  ):\n    if (\n      isinstance(\n        reference_number,\n        bool,\n      )\n      or not isinstance(\n        reference_number,\n        int,\n      )\n    ):\n      raise TypeError(\n        "statement_lines_by_reference_number keys "\n        "must be integers"\n      )\n\n    if not isinstance(\n      statement_lines,\n      tuple,\n    ):\n      raise TypeError(\n        "statement_lines_by_reference_number values "\n        "must be tuples"\n      )\n\n    marker = (\n      "[R"\n      + str(\n        reference_number\n      )\n      + "]"\n    )\n\n    for statement_line in statement_lines:\n      if not isinstance(\n        statement_line,\n        str,\n      ):\n        raise TypeError(\n          "statement_lines_by_reference_number values "\n          "must contain only strings"\n        )\n\n      if not statement_line:\n        continue\n\n      updated_lines = []\n\n      for line in lines:\n        if statement_line not in line:\n          updated_lines.append(\n            line\n          )\n          continue\n\n        if line.strip() == statement_line:\n          continue\n\n        if marker not in line:\n          updated_lines.append(\n            line\n          )\n          continue\n\n        prefix = line.split(\n          marker,\n          1,\n        )[0]\n\n        updated_lines.append(\n          prefix\n          + marker\n          + "を用いる。"\n        )\n\n      lines = updated_lines\n\n  compacted_lines = []\n  previous_blank = False\n\n  for line in lines:\n    is_blank = not line.strip()\n\n    if is_blank and previous_blank:\n      continue\n\n    compacted_lines.append(\n      line\n    )\n    previous_blank = is_blank\n\n  return "\\n".join(\n    compacted_lines\n  ).strip()\n',
        'def suppress_toda_group_proof_narrative_reference_body_duplicates(\n  body_markdown: str,\n  statement_lines_by_reference_number: dict[\n    int,\n    tuple[\n      str,\n      ...,\n    ],\n  ],\n) -> str:\n  if not isinstance(\n    body_markdown,\n    str,\n  ):\n    raise TypeError(\n      "body_markdown must be a str"\n    )\n\n  if not isinstance(\n    statement_lines_by_reference_number,\n    dict,\n  ):\n    raise TypeError(\n      "statement_lines_by_reference_number must be a dict"\n    )\n\n  lines = body_markdown.splitlines()\n\n  for reference_number, statement_lines in (\n    statement_lines_by_reference_number.items()\n  ):\n    if (\n      isinstance(\n        reference_number,\n        bool,\n      )\n      or not isinstance(\n        reference_number,\n        int,\n      )\n    ):\n      raise TypeError(\n        "statement_lines_by_reference_number keys "\n        "must be integers"\n      )\n\n    if not isinstance(\n      statement_lines,\n      tuple,\n    ):\n      raise TypeError(\n        "statement_lines_by_reference_number values "\n        "must be tuples"\n      )\n\n    marker = (\n      "[R"\n      + str(\n        reference_number\n      )\n      + "]"\n    )\n\n    for statement_line in statement_lines:\n      if not isinstance(\n        statement_line,\n        str,\n      ):\n        raise TypeError(\n          "statement_lines_by_reference_number values "\n          "must contain only strings"\n        )\n\n      if not statement_line:\n        continue\n\n      updated_lines = []\n\n      for line in lines:\n        if statement_line not in line:\n          updated_lines.append(\n            line\n          )\n          continue\n\n        if line.strip() == statement_line:\n          continue\n\n        if marker in line:\n          prefix = line.split(\n            marker,\n            1,\n          )[0]\n\n          updated_lines.append(\n            prefix\n            + marker\n            + "を用いる。"\n          )\n          continue\n\n        updated_lines.append(\n          line.replace(\n            statement_line,\n            marker,\n          )\n        )\n\n      lines = updated_lines\n\n  compacted_lines = []\n  previous_blank = False\n\n  for line in lines:\n    is_blank = not line.strip()\n\n    if is_blank and previous_blank:\n      continue\n\n    compacted_lines.append(\n      line\n    )\n    previous_blank = is_blank\n\n  return "\\n".join(\n    compacted_lines\n  ).strip()\n',
        "Reference/body ownership suppression",
    )

    test_path.write_text(
        'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  _toda_group_proof_narrative_reference_statement_lines_by_number,\n  suppress_toda_group_proof_narrative_reference_body_duplicates,\n)\nfrom toda_group_proof_narrative_references import (\n  build_toda_group_proof_narrative_reference_entries,\n  render_toda_group_proof_narrative_reference_entries_markdown,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _phase153_r3_11_presentations():\n  for n in range(\n    2,\n    16,\n  ):\n    for k in range(\n      0,\n      8,\n    ):\n      report = build_standard_toda_report(\n        n=n,\n        k=k,\n      )\n\n      if not report.candidates:\n        continue\n\n      group_result = (\n        report.candidates[\n          0\n        ].source_candidate.group_result\n      )\n      replay = build_toda_group_result_proof_replay(\n        group_result,\n        max_depth=2,\n      )\n      raw_presentation = (\n        build_toda_group_proof_presentation(\n          replay\n        )\n      )\n      presentation = (\n        build_toda_group_proof_narrative_semantic_closure_presentation(\n          raw_presentation\n        )\n      )\n\n      yield (\n        n,\n        k,\n        raw_presentation,\n        presentation,\n      )\n\n\ndef _phase153_r3_11_public_body(\n  rendered: str,\n  canonical_reference_section: str,\n) -> str:\n  lines = rendered.splitlines()\n\n  if "## 証明" in lines:\n    proof_index = lines.index(\n      "## 証明"\n    )\n\n    return "\\n".join(\n      lines[\n        proof_index + 1:\n      ]\n    )\n\n  if rendered.startswith(\n    canonical_reference_section\n  ):\n    return rendered[\n      len(\n        canonical_reference_section\n      ):\n    ].lstrip()\n\n  return rendered\n\n\ndef test_phase153_r3_11_replaces_embedded_unmarked_selected_statement_with_reference_marker():\n  statement = "$E: A \\\\xrightarrow{\\\\cong} B$"\n  body = (\n    "この結果として、"\n    + statement\n    + "を得る。"\n  )\n\n  suppressed = (\n    suppress_toda_group_proof_narrative_reference_body_duplicates(\n      body,\n      {\n        2: (\n          statement,\n        ),\n      },\n    )\n  )\n\n  assert statement not in suppressed\n  assert suppressed == "この結果として、[R2]を得る。"\n\n\ndef test_phase153_r3_11_preserves_surrounding_prose_when_replacing_embedded_statement():\n  statement = "$E: A \\\\xrightarrow{\\\\cong} B$"\n  body = (\n    "まず、"\n    + statement\n    + "を確認し、次の計算へ進む。"\n  )\n\n  suppressed = (\n    suppress_toda_group_proof_narrative_reference_body_duplicates(\n      body,\n      {\n        2: (\n          statement,\n        ),\n      },\n    )\n  )\n\n  assert suppressed == (\n    "まず、[R2]を確認し、次の計算へ進む。"\n  )\n\n\ndef test_phase153_r3_11_keeps_nonidentical_body_statement():\n  selected = "$E: A \\\\xrightarrow{\\\\cong} B$"\n  different = "$E^2: A \\\\xrightarrow{\\\\cong} B$"\n  body = (\n    "この結果として、"\n    + different\n    + "を得る。"\n  )\n\n  suppressed = (\n    suppress_toda_group_proof_narrative_reference_body_duplicates(\n      body,\n      {\n        2: (\n          selected,\n        ),\n      },\n    )\n  )\n\n  assert suppressed == body\n\n\ndef test_phase153_r3_11_all_112_groups_have_no_exact_selected_statement_body_duplicates():\n  duplicates = []\n\n  for (\n    n,\n    k,\n    raw_presentation,\n    presentation,\n  ) in _phase153_r3_11_presentations():\n    entries = (\n      build_toda_group_proof_narrative_reference_entries(\n        presentation\n      )\n    )\n\n    if not entries:\n      continue\n\n    selected_by_number = (\n      _toda_group_proof_narrative_reference_statement_lines_by_number(\n        presentation,\n        entries,\n      )\n    )\n    canonical_reference_section = (\n      render_toda_group_proof_narrative_reference_entries_markdown(\n        entries,\n        selected_by_number,\n      )\n    )\n    rendered = (\n      render_toda_group_proof_narrative_markdown(\n        raw_presentation\n      )\n    )\n    body = (\n      _phase153_r3_11_public_body(\n        rendered,\n        canonical_reference_section,\n      )\n    )\n\n    for reference_number, statement_lines in (\n      selected_by_number.items()\n    ):\n      for statement_line in statement_lines:\n        if statement_line not in body:\n          continue\n\n        duplicates.append(\n          (\n            n,\n            k,\n            reference_number,\n            statement_line,\n          )\n        )\n\n  assert duplicates == []\n',
        encoding="utf-8",
    )

    print(
        "updated: "
        "toda_group_proof_narrative_contribution_renderer.py"
    )
    print(
        "added: "
        "tests\\test_phase153_r3_11_reference_body_ownership_repair.py"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
