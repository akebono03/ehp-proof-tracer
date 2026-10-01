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
        / "toda_group_proof_narrative_renderer.py"
    )
    test_path = (
        REPO_ROOT
        / "tests"
        / "test_phase153_r3_10_public_reference_connection_repair.py"
    )

    marker = 'def _wrap_phase150_rc4_generic_public_narrative(\n  rendered: str,\n) -> str:\n  if not isinstance(rendered, str):\n    raise TypeError("rendered must be a str")\n\n  lines = rendered.splitlines()\n  reference_line_indices = [\n    index\n    for index, line in enumerate(lines)\n    if line.startswith("**[R")\n  ]\n\n  if not reference_line_indices:\n    return rendered\n\n  last_reference_index = reference_line_indices[-1]\n  reference_lines = lines[\n    :last_reference_index + 1\n  ]\n  proof_lines = lines[\n    last_reference_index + 1:\n  ]\n\n  while proof_lines and not proof_lines[0]:\n    proof_lines.pop(0)\n\n  wrapped_lines = [\n    "# Group proof narrative",\n    "",\n    "## 使用する結果",\n    "",\n    *reference_lines,\n    "",\n    "## 証明",\n    "",\n    *proof_lines,\n  ]\n\n  return "\\n".join(wrapped_lines).rstrip() + "\\n"\n'
    text = renderer_path.read_text(
        encoding="utf-8",
    )

    if text.count(
        marker
    ) != 1:
        raise RuntimeError(
            "Phase150 generic wrapper marker "
            "not found exactly once"
        )

    renderer_path.write_text(
        text.replace(
            marker,
            'def _phase153_r3_10_connect_public_reference_section(\n  presentation: TodaGroupProofPresentation,\n  rendered: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  if presentation.max_depth < 2:\n    return rendered\n\n  reference_entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n\n  if not reference_entries:\n    return rendered\n\n  statement_lines_by_reference_number = (\n    _toda_group_proof_narrative_reference_statement_lines_by_number(\n      presentation,\n      reference_entries,\n    )\n  )\n  reference_section = (\n    render_toda_group_proof_narrative_reference_entries_markdown(\n      reference_entries,\n      statement_lines_by_reference_number,\n    )\n  )\n\n  if not reference_section:\n    return rendered\n\n  reference_header = "## 使用する結果"\n  proof_header = "## 証明"\n  reference_index = rendered.find(\n    reference_header\n  )\n  proof_index = rendered.find(\n    proof_header\n  )\n\n  if (\n    reference_index < 0\n    or proof_index < 0\n    or reference_index >= proof_index\n  ):\n    return rendered\n\n  prefix = rendered[\n    :reference_index\n  ].rstrip()\n  proof = rendered[\n    proof_index:\n  ].lstrip()\n\n  return (\n    prefix\n    + "\\n\\n"\n    + reference_header\n    + "\\n\\n"\n    + reference_section\n    + "\\n\\n"\n    + proof\n    + (\n      ""\n      if proof.endswith(\n        "\\n"\n      )\n      else "\\n"\n    )\n  )\n\n\n'
            + 'def _wrap_phase150_rc4_generic_public_narrative(\n  presentation: TodaGroupProofPresentation,\n  rendered: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  reference_entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n  )\n  statement_lines_by_reference_number = (\n    _toda_group_proof_narrative_reference_statement_lines_by_number(\n      presentation,\n      reference_entries,\n    )\n  )\n  reference_section = (\n    render_toda_group_proof_narrative_reference_entries_markdown(\n      reference_entries,\n      statement_lines_by_reference_number,\n    )\n  )\n\n  if not reference_section:\n    return rendered\n\n  reference_prefix = (\n    reference_section\n    + "\\n\\n"\n  )\n\n  if not rendered.startswith(\n    reference_prefix\n  ):\n    return rendered\n\n  proof = rendered[\n    len(\n      reference_prefix\n    ):\n  ].lstrip()\n\n  return (\n    "# Group proof narrative\\n\\n"\n    "## 使用する結果\\n\\n"\n    + reference_section\n    + "\\n\\n"\n    "## 証明\\n\\n"\n    + proof.rstrip()\n    + "\\n"\n  )\n',
            1,
        ),
        encoding="utf-8",
    )

    _replace_once(
        renderer_path,
        '  if phase134_24_pi15_8 is not None:\n    return phase134_24_pi15_8\n',
        '  if phase134_24_pi15_8 is not None:\n    return (\n      _phase153_r3_10_connect_public_reference_section(\n        presentation,\n        phase134_24_pi15_8,\n      )\n    )\n',
        "pi15_8 custom route connection",
    )

    _replace_once(
        renderer_path,
        '      return _wrap_phase150_rc4_generic_public_narrative(\n        rendered\n      )\n',
        '      return _wrap_phase150_rc4_generic_public_narrative(\n        presentation,\n        rendered,\n      )\n',
        "generic public wrapper call",
    )

    _replace_once(
        renderer_path,
        '  if _is_phase134_9_pi8_5_presentation(\n    presentation\n  ):\n    return (\n      _render_phase134_9_pi8_5_narrative_markdown(\n        presentation\n      )\n    )\n',
        '  if _is_phase134_9_pi8_5_presentation(\n    presentation\n  ):\n    rendered = (\n      _render_phase134_9_pi8_5_narrative_markdown(\n        presentation\n      )\n    )\n\n    return (\n      _phase153_r3_10_connect_public_reference_section(\n        presentation,\n        rendered,\n      )\n    )\n',
        "pi8_5 custom route connection",
    )

    test_path.write_text(
        'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  _toda_group_proof_narrative_reference_statement_lines_by_number,\n)\nfrom toda_group_proof_narrative_references import (\n  build_toda_group_proof_narrative_reference_entries,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _phase153_r3_10_presentations():\n  for n in range(\n    2,\n    16,\n  ):\n    for k in range(\n      0,\n      8,\n    ):\n      report = build_standard_toda_report(\n        n=n,\n        k=k,\n      )\n\n      if not report.candidates:\n        continue\n\n      group_result = (\n        report.candidates[\n          0\n        ].source_candidate.group_result\n      )\n      replay = build_toda_group_result_proof_replay(\n        group_result,\n        max_depth=2,\n      )\n      raw_presentation = (\n        build_toda_group_proof_presentation(\n          replay\n        )\n      )\n      presentation = (\n        build_toda_group_proof_narrative_semantic_closure_presentation(\n          raw_presentation\n        )\n      )\n\n      yield (\n        n,\n        k,\n        raw_presentation,\n        presentation,\n      )\n\n\ndef test_phase153_r3_10_all_selected_statements_are_publicly_visible():\n  missing = []\n\n  for (\n    n,\n    k,\n    raw_presentation,\n    presentation,\n  ) in _phase153_r3_10_presentations():\n    entries = (\n      build_toda_group_proof_narrative_reference_entries(\n        presentation\n      )\n    )\n    selected_by_number = (\n      _toda_group_proof_narrative_reference_statement_lines_by_number(\n        presentation,\n        entries,\n      )\n    )\n    rendered = (\n      render_toda_group_proof_narrative_markdown(\n        raw_presentation\n      )\n    )\n\n    assert "## 証明" in rendered, (\n      n,\n      k,\n    )\n\n    reference_section = rendered.split(\n      "## 証明",\n      1,\n    )[0]\n\n    for entry in entries:\n      for statement_line in selected_by_number.get(\n        entry.number,\n        (),\n      ):\n        if statement_line in reference_section:\n          continue\n\n        missing.append(\n          (\n            n,\n            k,\n            entry.number,\n            entry.reference.locator\n            or entry.reference.label,\n            statement_line,\n          )\n        )\n\n  assert missing == []\n\n\ndef test_phase153_r3_10_public_reference_markers_cover_structured_entries():\n  missing_markers = []\n\n  for (\n    n,\n    k,\n    raw_presentation,\n    presentation,\n  ) in _phase153_r3_10_presentations():\n    entries = (\n      build_toda_group_proof_narrative_reference_entries(\n        presentation\n      )\n    )\n    rendered = (\n      render_toda_group_proof_narrative_markdown(\n        raw_presentation\n      )\n    )\n\n    reference_section = rendered.split(\n      "## 証明",\n      1,\n    )[0]\n\n    for entry in entries:\n      marker = (\n        "[R"\n        + str(\n          entry.number\n        )\n        + "]"\n      )\n\n      if marker in reference_section:\n        continue\n\n      missing_markers.append(\n        (\n          n,\n          k,\n          entry.number,\n          entry.reference.locator\n          or entry.reference.label,\n        )\n      )\n\n  assert missing_markers == []\n',
        encoding="utf-8",
    )

    print(
        "updated: toda_group_proof_narrative_renderer.py"
    )
    print(
        "added: "
        "tests\\test_phase153_r3_10_public_reference_connection_repair.py"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
