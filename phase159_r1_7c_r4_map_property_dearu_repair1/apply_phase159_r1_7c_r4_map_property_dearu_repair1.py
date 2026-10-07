from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"

PRODUCTION = (
  ROOT
  / "toda_group_proof_narrative_renderer.py"
)
TEST = (
  ROOT
  / "tests"
  / "test_phase159_r1_7c_r4_map_property_dearu_public_normalization.py"
)

HELPER = 'def _phase159_r1_7c_r4_normalize_public_map_property_prose(\n  rendered: str,\n) -> str:\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  proof_marker = (\n    "## 証明\\n\\n"\n  )\n  marker_index = rendered.find(\n    proof_marker\n  )\n\n  if marker_index < 0:\n    return rendered\n\n  proof_start = (\n    marker_index\n    + len(\n      proof_marker\n    )\n  )\n  proof_body = rendered[\n    proof_start:\n  ]\n  proof_body = proof_body.replace(\n    "は単射である.",\n    "は単射.",\n  )\n  proof_body = proof_body.replace(\n    "は全射である.",\n    "は全射.",\n  )\n\n  return (\n    rendered[\n      :proof_start\n    ]\n    + proof_body\n  )\n'
RENDER_FUNCTION = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  rendered = (\n    _phase158_baseline_render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n  rendered = (\n    _phase158_normalize_public_narrative_contract(\n      presentation,\n      rendered,\n    )\n  )\n\n  return (\n    _phase159_r1_7c_r4_normalize_public_map_property_prose(\n      rendered\n    )\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _public_narrative(\n  n: int,\n  k: int,\n) -> str:\n  report = build_standard_toda_report(\n    n=n,\n    k=k,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase159_r1_7c_r4_public_map_property_prose_removes_dearu():\n  targets = (\n    (\n      6,\n      5,\n    ),\n    (\n      6,\n      6,\n    ),\n    (\n      7,\n      6,\n    ),\n    (\n      9,\n      7,\n    ),\n  )\n\n  for n, k in targets:\n    rendered = _public_narrative(\n      n,\n      k,\n    )\n    proof_body = rendered.split(\n      "## 証明\\n\\n",\n      1,\n    )[\n      1\n    ]\n\n    assert "は単射である." not in proof_body\n    assert "は全射である." not in proof_body\n\n\ndef test_phase159_r1_7c_r4_pi11_6_uses_concise_map_property_prose():\n  rendered = _public_narrative(\n    6,\n    5,\n  )\n\n  assert (\n    r"$\\Delta: \\pi_{10}^{9} \\to \\pi_{8}^{4}$ は単射."\n    in rendered\n  )\n  assert (\n    r"$E: \\pi_{9}^{4} \\to \\pi_{10}^{5}$ は全射."\n    in rendered\n  )\n  assert (\n    r"[R1] より, $H: \\pi_{7}^{3} \\to \\pi_{7}^{5}$ は単射."\n    in rendered\n  )\n  assert (\n    r"$H: \\pi_{7}^{3} \\to \\pi_{7}^{5}$ は全射."\n    in rendered\n  )\n\n\ndef test_phase159_r1_7c_r4_pi16_9_aggregate_line_is_concise():\n  rendered = _public_narrative(\n    9,\n    7,\n  )\n\n  assert (\n    r"$|\\pi_{16}^{9}| = 16$ であり, "\n    r"$E^{4}: \\pi_{12}^{5} \\to \\pi_{16}^{9}$ は単射."\n    in rendered\n  )\n\n\ndef test_phase159_r1_7c_r4_reference_section_is_not_normalized():\n  rendered = (\n    "# Group proof narrative\\n\\n"\n    "## 証明対象\\n\\n"\n    "target\\n\\n"\n    "## 使用する結果\\n\\n"\n    "Reference map は単射である.\\n\\n"\n    "---\\n\\n"\n    "## 証明\\n\\n"\n    "Proof map は単射である.\\n"\n  )\n\n  from toda_group_proof_narrative_renderer import (\n    _phase159_r1_7c_r4_normalize_public_map_property_prose,\n  )\n\n  normalized = (\n    _phase159_r1_7c_r4_normalize_public_map_property_prose(\n      rendered\n    )\n  )\n\n  assert (\n    "Reference map は単射である."\n    in normalized\n  )\n  assert (\n    "Proof map は単射."\n    in normalized\n  )\n  assert (\n    "Proof map は単射である."\n    not in normalized\n  )\n'


def replace_function(
  source: str,
  function_name: str,
  new_source: str,
) -> str:
  marker = (
    "def "
    + function_name
    + "("
  )
  start = source.find(
    marker
  )

  if start < 0:
    raise SystemExit(
      f"function not found: {function_name}"
    )

  next_start = source.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  if next_start < 0:
    end = len(
      source
    )
  else:
    end = next_start + 1

  return (
    source[:start]
    + new_source.rstrip()
    + "\n\n"
    + source[end:]
  )


def main() -> None:
  BACKUP.mkdir(
    parents=True,
    exist_ok=True,
  )

  shutil.copy2(
    PRODUCTION,
    BACKUP / PRODUCTION.name,
  )

  source = PRODUCTION.read_text(
    encoding="utf-8"
  )

  helper_marker = (
    "def _phase159_r1_7c_r4_normalize_public_map_property_prose("
  )

  if helper_marker not in source:
    render_marker = (
      "def render_toda_group_proof_narrative_markdown("
    )
    render_index = source.find(
      render_marker
    )

    if render_index < 0:
      raise SystemExit(
        "public narrative render function anchor not found"
      )

    source = (
      source[:render_index]
      + HELPER.rstrip()
      + "\n\n"
      + source[render_index:]
    )

  source = replace_function(
    source,
    "render_toda_group_proof_narrative_markdown",
    RENDER_FUNCTION,
  )

  PRODUCTION.write_text(
    source,
    encoding="utf-8",
  )

  TEST.write_text(
    TEST_SOURCE,
    encoding="utf-8",
  )

  print(
    "Phase 159 R1-7c R4 map-property dearu repair1 applied."
  )
  print(
    "Internal renderer matching contracts were left unchanged."
  )
  print(
    "Only the final public proof body is normalized."
  )


if __name__ == "__main__":
  main()
