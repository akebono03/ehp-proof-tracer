from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent


def main() -> int:
    test_path = (
        REPO_ROOT
        / "tests"
        / "test_phase153_r3_10_public_reference_connection_repair.py"
    )

    test_path.write_text(
        'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  _toda_group_proof_narrative_reference_statement_lines_by_number,\n)\nfrom toda_group_proof_narrative_references import (\n  build_toda_group_proof_narrative_reference_entries,\n  render_toda_group_proof_narrative_reference_entries_markdown,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _phase153_r3_10_presentations():\n  for n in range(\n    2,\n    16,\n  ):\n    for k in range(\n      0,\n      8,\n    ):\n      report = build_standard_toda_report(\n        n=n,\n        k=k,\n      )\n\n      if not report.candidates:\n        continue\n\n      group_result = (\n        report.candidates[\n          0\n        ].source_candidate.group_result\n      )\n      replay = build_toda_group_result_proof_replay(\n        group_result,\n        max_depth=2,\n      )\n      raw_presentation = (\n        build_toda_group_proof_presentation(\n          replay\n        )\n      )\n      presentation = (\n        build_toda_group_proof_narrative_semantic_closure_presentation(\n          raw_presentation\n        )\n      )\n\n      yield (\n        n,\n        k,\n        raw_presentation,\n        presentation,\n      )\n\n\ndef _phase153_r3_10_public_reference_section(\n  rendered: str,\n  canonical_reference_section: str,\n) -> str:\n  lines = rendered.splitlines()\n\n  if "## 証明" in lines:\n    proof_index = lines.index(\n      "## 証明"\n    )\n\n    return "\\n".join(\n      lines[\n        :proof_index\n      ]\n    )\n\n  if rendered.startswith(\n    canonical_reference_section\n  ):\n    return canonical_reference_section\n\n  return ""\n\n\ndef test_phase153_r3_10_all_selected_statements_are_publicly_visible():\n  missing = []\n\n  for (\n    n,\n    k,\n    raw_presentation,\n    presentation,\n  ) in _phase153_r3_10_presentations():\n    entries = (\n      build_toda_group_proof_narrative_reference_entries(\n        presentation\n      )\n    )\n\n    if not entries:\n      continue\n\n    selected_by_number = (\n      _toda_group_proof_narrative_reference_statement_lines_by_number(\n        presentation,\n        entries,\n      )\n    )\n    canonical_reference_section = (\n      render_toda_group_proof_narrative_reference_entries_markdown(\n        entries,\n        selected_by_number,\n      )\n    )\n    rendered = (\n      render_toda_group_proof_narrative_markdown(\n        raw_presentation\n      )\n    )\n    public_reference_section = (\n      _phase153_r3_10_public_reference_section(\n        rendered,\n        canonical_reference_section,\n      )\n    )\n\n    assert public_reference_section, (\n      n,\n      k,\n      rendered,\n    )\n\n    for entry in entries:\n      for statement_line in selected_by_number.get(\n        entry.number,\n        (),\n      ):\n        if statement_line in public_reference_section:\n          continue\n\n        missing.append(\n          (\n            n,\n            k,\n            entry.number,\n            entry.reference.locator\n            or entry.reference.label,\n            statement_line,\n          )\n        )\n\n  assert missing == []\n\n\ndef test_phase153_r3_10_public_reference_markers_cover_structured_entries():\n  missing_markers = []\n\n  for (\n    n,\n    k,\n    raw_presentation,\n    presentation,\n  ) in _phase153_r3_10_presentations():\n    entries = (\n      build_toda_group_proof_narrative_reference_entries(\n        presentation\n      )\n    )\n\n    if not entries:\n      continue\n\n    selected_by_number = (\n      _toda_group_proof_narrative_reference_statement_lines_by_number(\n        presentation,\n        entries,\n      )\n    )\n    canonical_reference_section = (\n      render_toda_group_proof_narrative_reference_entries_markdown(\n        entries,\n        selected_by_number,\n      )\n    )\n    rendered = (\n      render_toda_group_proof_narrative_markdown(\n        raw_presentation\n      )\n    )\n    public_reference_section = (\n      _phase153_r3_10_public_reference_section(\n        rendered,\n        canonical_reference_section,\n      )\n    )\n\n    assert public_reference_section, (\n      n,\n      k,\n      rendered,\n    )\n\n    for entry in entries:\n      marker = (\n        "[R"\n        + str(\n          entry.number\n        )\n        + "]"\n      )\n\n      if marker in public_reference_section:\n        continue\n\n      missing_markers.append(\n        (\n          n,\n          k,\n          entry.number,\n          entry.reference.locator\n          or entry.reference.label,\n        )\n      )\n\n  assert missing_markers == []\n',
        encoding="utf-8",
    )

    print(
        "updated: "
        "tests\\test_phase153_r3_10_public_reference_connection_repair.py"
    )
    print(
        "production files: unchanged"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
