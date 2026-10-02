from pathlib import Path

CONTRIBUTION = Path("toda_group_proof_narrative_contribution_renderer.py")
RENDERER = Path("toda_group_proof_narrative_renderer.py")

NEW_HELPER = 'def suppress_toda_group_proof_narrative_reference_body_restatements(\n  body_markdown: str,\n  statement_lines_by_reference_number: dict[\n    int,\n    tuple[\n      str,\n      ...,\n    ],\n  ],\n) -> str:\n  if not isinstance(\n    body_markdown,\n    str,\n  ):\n    raise TypeError(\n      "body_markdown must be a str"\n    )\n\n  if not isinstance(\n    statement_lines_by_reference_number,\n    dict,\n  ):\n    raise TypeError(\n      "statement_lines_by_reference_number must be a dict"\n    )\n\n  derivation_tokens = (\n    "これらから",\n    "このことから",\n    "したがって",\n    "従って",\n    "よって",\n    "ゆえに",\n    "以上より",\n    "ここから",\n    "計算",\n    "導く",\n    "導か",\n    "得る",\n    "従う",\n    "分かる",\n    "わかる",\n    "示す",\n    "確認",\n  )\n\n  lines = body_markdown.splitlines()\n\n  for reference_number, statement_lines in (\n    statement_lines_by_reference_number.items()\n  ):\n    if (\n      isinstance(\n        reference_number,\n        bool,\n      )\n      or not isinstance(\n        reference_number,\n        int,\n      )\n    ):\n      raise TypeError(\n        "statement_lines_by_reference_number keys "\n        "must be integers"\n      )\n\n    if not isinstance(\n      statement_lines,\n      tuple,\n    ):\n      raise TypeError(\n        "statement_lines_by_reference_number values "\n        "must be tuples"\n      )\n\n    marker = (\n      "[R"\n      + str(\n        reference_number\n      )\n      + "]"\n    )\n\n    for statement_line in statement_lines:\n      if not isinstance(\n        statement_line,\n        str,\n      ):\n        raise TypeError(\n          "statement_lines_by_reference_number values "\n          "must contain only strings"\n        )\n\n      if not statement_line:\n        continue\n\n      updated_lines = []\n\n      for line in lines:\n        if statement_line not in line:\n          updated_lines.append(\n            line\n          )\n          continue\n\n        stripped = line.strip()\n\n        if stripped == statement_line:\n          continue\n\n        if any(\n          token in line\n          for token in derivation_tokens\n        ):\n          updated_lines.append(\n            line\n          )\n          continue\n\n        if marker in line:\n          updated_lines.append(\n            marker\n            + "を用いる."\n          )\n          continue\n\n        replaced_line = line.replace(\n          statement_line,\n          marker,\n        )\n\n        if replaced_line.rstrip().endswith(\n          marker\n        ):\n          replaced_line = (\n            replaced_line.rstrip()\n            + "を用いる."\n          )\n\n        updated_lines.append(\n          replaced_line\n        )\n\n      lines = updated_lines\n\n  compacted_lines = []\n  previous_blank = False\n\n  for line in lines:\n    is_blank = not line.strip()\n\n    if is_blank and previous_blank:\n      continue\n\n    compacted_lines.append(\n      line\n    )\n    previous_blank = is_blank\n\n  return "\\n".join(\n    compacted_lines\n  ).strip()\n'
CONNECT_FUNCTION = 'def _phase153_r3_10_connect_public_reference_section(\n  presentation: TodaGroupProofPresentation,\n  rendered: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  if presentation.max_depth < 2:\n    return rendered\n\n  lines = rendered.splitlines()\n  reference_header = "## 使用する結果"\n  proof_header = "## 証明"\n\n  try:\n    reference_index = lines.index(\n      reference_header\n    )\n    proof_index = lines.index(\n      proof_header\n    )\n  except ValueError:\n    return rendered\n\n  if reference_index >= proof_index:\n    return rendered\n\n  reference_entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n\n  if not reference_entries:\n    return rendered\n\n  statement_lines_by_reference_number = (\n    _toda_group_proof_narrative_reference_statement_lines_by_number(\n      presentation,\n      reference_entries,\n    )\n  )\n\n  proof_body = "\\n".join(\n    lines[\n      proof_index\n      + 1:\n    ]\n  ).lstrip()\n\n  (\n    used_reference_entries,\n    used_statement_lines,\n    filtered_proof_body,\n  ) = (\n    filter_toda_group_proof_narrative_reference_entries_by_body_usage(\n      reference_entries,\n      statement_lines_by_reference_number,\n      proof_body,\n    )\n  )\n\n  (\n    filtered_reference_entries,\n    filtered_statement_lines,\n  ) = (\n    exclude_toda_group_proof_narrative_root_reference(\n      used_reference_entries,\n      used_statement_lines,\n      presentation.root_step,\n    )\n  )\n\n  if (\n    len(\n      filtered_reference_entries\n    )\n    != len(\n      used_reference_entries\n    )\n  ):\n    return rendered\n\n  filtered_proof_body = (\n    suppress_toda_group_proof_narrative_reference_body_restatements(\n      filtered_proof_body,\n      filtered_statement_lines,\n    )\n  )\n\n  reference_section = (\n    render_toda_group_proof_narrative_reference_entries_markdown(\n      filtered_reference_entries,\n      filtered_statement_lines,\n    )\n  )\n\n  if not reference_section:\n    return rendered\n\n  prefix_lines = lines[\n    :reference_index\n  ]\n\n  while (\n    prefix_lines\n    and not prefix_lines[\n      -1\n    ].strip()\n  ):\n    prefix_lines.pop()\n\n  return (\n    "\\n".join(\n      (\n        *prefix_lines,\n        "",\n        reference_header,\n        "",\n        reference_section,\n        "",\n        proof_header,\n        "",\n        filtered_proof_body,\n      )\n    ).rstrip()\n    + "\\n"\n  )\n'
WRAP_FUNCTION = 'def _wrap_phase150_rc4_generic_public_narrative(\n  presentation: TodaGroupProofPresentation,\n  rendered: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  reference_entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n  statement_lines_by_reference_number = (\n    _toda_group_proof_narrative_reference_statement_lines_by_number(\n      presentation,\n      reference_entries,\n    )\n  )\n  reference_section = (\n    render_toda_group_proof_narrative_reference_entries_markdown(\n      reference_entries,\n      statement_lines_by_reference_number,\n    )\n  )\n\n  if not reference_section:\n    return rendered\n\n  reference_prefix = (\n    reference_section\n    + "\\n\\n"\n  )\n\n  if not rendered.startswith(\n    reference_prefix\n  ):\n    return rendered\n\n  proof = rendered[\n    len(\n      reference_prefix\n    ):\n  ].lstrip()\n  proof = (\n    suppress_toda_group_proof_narrative_reference_body_restatements(\n      proof,\n      statement_lines_by_reference_number,\n    )\n  )\n\n  return (\n    "# Group proof narrative\\n\\n"\n    "## 使用する結果\\n\\n"\n    + reference_section\n    + "\\n\\n"\n    "## 証明\\n\\n"\n    + proof.rstrip()\n    + "\\n"\n  )\n'


def replace_function(
    text: str,
    start_marker: str,
    end_marker: str,
    replacement: str,
) -> str:
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    return text[:start] + replacement + "\n" + text[end:]


def main() -> None:
    contribution_text = CONTRIBUTION.read_text(
        encoding="utf-8"
    )
    insertion_marker = (
        "def suppress_toda_group_proof_narrative_reference_body_duplicates("
    )
    insertion_index = contribution_text.index(
        insertion_marker
    )
    contribution_text = (
        contribution_text[:insertion_index]
        + NEW_HELPER
        + "\n"
        + contribution_text[insertion_index:]
    )
    CONTRIBUTION.write_text(
        contribution_text,
        encoding="utf-8",
    )

    renderer_text = RENDERER.read_text(
        encoding="utf-8"
    )

    old_import = (
        "  suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry,\n"
        "  suppress_toda_group_proof_narrative_reference_body_duplicates,\n"
    )
    new_import = (
        "  suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry,\n"
        "  suppress_toda_group_proof_narrative_reference_body_duplicates,\n"
        "  suppress_toda_group_proof_narrative_reference_body_restatements,\n"
    )

    if old_import not in renderer_text:
        raise RuntimeError(
            "renderer import target not found"
        )

    renderer_text = renderer_text.replace(
        old_import,
        new_import,
        1,
    )

    renderer_text = replace_function(
        renderer_text,
        "def _phase153_r3_10_connect_public_reference_section(",
        "\ndef _wrap_phase150_rc4_generic_public_narrative(",
        CONNECT_FUNCTION,
    )
    renderer_text = replace_function(
        renderer_text,
        "def _wrap_phase150_rc4_generic_public_narrative(",
        "\ndef _is_phase150_rc4_generic_route_target(",
        WRAP_FUNCTION,
    )

    RENDERER.write_text(
        renderer_text,
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
