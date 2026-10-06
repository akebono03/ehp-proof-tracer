from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
R12_TEST = ROOT / "tests" / "test_phase159_r1_2_pi3_2_narrative_repair.py"
R16B_TEST = ROOT / "tests" / "test_phase159_r1_6b_toda51_attribution.py"
R16C_TEST = ROOT / "tests" / "test_phase159_r1_6c_source_faithful_reference_linkage.py"
R16D_TEST = ROOT / "tests" / "test_phase159_r1_6d_specialization_reference_linkage_finalization.py"

HELPERS = 'def _phase159_r1_6d_toda_51_diagonal_specialization_lines(\n  presentation: TodaGroupProofPresentation,\n  rendered: str,\n) -> tuple[\n  str,\n  str,\n  str,\n] | None:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  reference_number = (\n    _phase159_r1_6c_reference_number(\n      rendered,\n      "(5.1)",\n    )\n  )\n\n  if reference_number is None:\n    return None\n\n  suspension_step = next(\n    (\n      proof_step\n      for proof_step in (\n        _phase159_r1_6c_recursive_proof_steps(\n          presentation.root_step\n        )\n      )\n      if (\n        isinstance(\n          proof_step.conclusion,\n          TodaSuspensionIsomorphismStatement,\n        )\n        and (\n          _phase159_r1_6c_step_reference_locator(\n            proof_step\n          )\n          == "(5.1)"\n        )\n      )\n    ),\n    None,\n  )\n\n  if suspension_step is None:\n    return None\n\n  suspension_map = (\n    suspension_step.conclusion.map\n  )\n  source_group = (\n    suspension_map.source_group\n  )\n  target_group = (\n    suspension_map.target_group\n  )\n\n  source_dimension = getattr(\n    source_group,\n    "sphere_dimension",\n    None,\n  )\n  target_dimension = getattr(\n    target_group,\n    "sphere_dimension",\n    None,\n  )\n\n  if (\n    not isinstance(\n      source_dimension,\n      int,\n    )\n    or not isinstance(\n      target_dimension,\n      int,\n    )\n  ):\n    return None\n\n  source_group_latex = (\n    render_toda_primary_group_latex(\n      source_group\n    )\n  )\n  target_group_latex = (\n    render_toda_primary_group_latex(\n      target_group\n    )\n  )\n\n  isomorphism_line = (\n    _phase159_r1_6c_compact_map_property_line(\n      _render_generic_narrative_step(\n        suspension_step\n      )\n    )\n  )\n\n  specialization_line = (\n    "[R"\n    + str(\n      reference_number\n    )\n    + "] より, $"\n    + source_group_latex\n    + r" = \\mathbb{Z}\\{\\iota_{"\n    + str(\n      source_dimension\n    )\n    + r"}\\}$, $"\n    + target_group_latex\n    + r" = \\mathbb{Z}\\{\\iota_{"\n    + str(\n      target_dimension\n    )\n    + r"}\\}$."\n  )\n\n  generator_line = (\n    "$E(\\\\iota_{"\n    + str(\n      source_dimension\n    )\n    + r"}) = \\iota_{"\n    + str(\n      target_dimension\n    )\n    + r"}$ であるから, "\n    + isomorphism_line\n  )\n\n  old_line = (\n    "[R"\n    + str(\n      reference_number\n    )\n    + "]より, "\n    + isomorphism_line\n  )\n\n  return (\n    old_line,\n    specialization_line,\n    generator_line,\n  )\n\n\ndef _phase159_r1_6d_finalize_reference_and_linkage(\n  presentation: TodaGroupProofPresentation,\n  rendered: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  rendered = rendered.replace(\n    (\n      r"$\\pi_{n}^{n} = "\n      r"\\langle \\iota_{n} \\rangle "\n      r"\\cong \\mathbb{Z}$."\n    ),\n    (\n      r"$\\pi_{n}^{n} = "\n      r"\\mathbb{Z}\\{\\iota_{n}\\}$."\n    ),\n  )\n\n  rendered = re.sub(\n    r"(\\[R[0-9]+\\])より,",\n    r"\\1 より,",\n    rendered,\n  )\n\n  specialization = (\n    _phase159_r1_6d_toda_51_diagonal_specialization_lines(\n      presentation,\n      rendered,\n    )\n  )\n\n  if specialization is None:\n    return rendered\n\n  (\n    old_line,\n    specialization_line,\n    generator_line,\n  ) = specialization\n\n  normalized_old_line = re.sub(\n    r"^(\\[R[0-9]+\\])より,",\n    r"\\1 より,",\n    old_line,\n  )\n\n  if normalized_old_line not in rendered:\n    return rendered\n\n  return rendered.replace(\n    normalized_old_line,\n    (\n      specialization_line\n      + "\\n\\n"\n      + generator_line\n    ),\n    1,\n  )\n\n\ndef _phase159_r1_6d_center_structural_formulas(\n  rendered: str,\n) -> str:\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  lines = rendered.splitlines()\n  output = []\n\n  numbered_map_property = re.compile(\n    r"^(?P<lead>.*?), "\n    r"\\$(?P<math>.+)\\$ は"\n    r"(?P<property>単射|全射|同型|零写像)"\n    r"\\. \\((?P<number>[0-9]+)\\)$"\n  )\n\n  standalone_exact_sequence = re.compile(\n    r"^\\$(?P<math>.+\\\\xrightarrow\\{.+)\\$\\.$"\n  )\n\n  for line in lines:\n    stripped = line.strip()\n\n    exact_match = (\n      standalone_exact_sequence.match(\n        stripped\n      )\n    )\n\n    if exact_match is not None:\n      if (\n        output\n        and output[\n          -1\n        ].strip()\n      ):\n        output.append(\n          ""\n        )\n\n      output.extend(\n        (\n          r"\\[",\n          exact_match.group(\n            "math"\n          )\n          + ".",\n          r"\\]",\n        )\n      )\n      continue\n\n    numbered_match = (\n      numbered_map_property.match(\n        stripped\n      )\n    )\n\n    if numbered_match is not None:\n      lead = numbered_match.group(\n        "lead"\n      )\n\n      if lead:\n        output.append(\n          lead + ","\n        )\n        output.append(\n          ""\n        )\n\n      output.extend(\n        (\n          r"\\[",\n          (\n            numbered_match.group(\n              "math"\n            )\n            + r"\\quad\\text{は"\n            + numbered_match.group(\n              "property"\n            )\n            + r"}. \\qquad ("\n            + numbered_match.group(\n              "number"\n            )\n            + ")"\n          ),\n          r"\\]",\n        )\n      )\n      continue\n\n    output.append(\n      line\n    )\n\n  compacted = []\n  previous_blank = False\n\n  for line in output:\n    is_blank = not line.strip()\n\n    if (\n      is_blank\n      and previous_blank\n    ):\n      continue\n\n    compacted.append(\n      line\n    )\n    previous_blank = is_blank\n\n  return "\\n".join(\n    compacted\n  )\n'
NEW_RENDER = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  rendered = (\n    _phase158_baseline_render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n  rendered = (\n    _phase158_normalize_public_narrative_contract(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_normalize_public_map_property_wording(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_normalize_public_reference_map_property_wording(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_6c_canonicalize_toda_51_reference(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_6c_remove_redundant_exactness_sentence(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_6c_link_proof_reasons(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_r1_6c_render_statement_numbers(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_6d_finalize_reference_and_linkage(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_r1_6d_center_structural_formulas(\n      rendered\n    )\n  )\n\n  return (\n    _phase159_inject_foundational_reference_section(\n      presentation,\n      rendered,\n    )\n  )\n'
TEST_R14_EXACT = 'def test_phase159_r1_4_pi3_2_public_uses_exactly_one_exact_sequence():\n  presentation = _phase159_r1_2_pi3_2_presentation()\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  long_exact = (\n    r"\\pi_{2}^{1} \\xrightarrow{E} "\n    r"\\pi_{3}^{2} \\xrightarrow{H} "\n    r"\\pi_{3}^{3} \\xrightarrow{\\Delta} "\n    r"\\pi_{1}^{1} \\xrightarrow{E} "\n    r"\\pi_{2}^{2}."\n  )\n\n  proof_body = rendered.split(\n    "## 証明\\n\\n",\n    1,\n  )[1]\n\n  exactness_lines = tuple(\n    line\n    for line in proof_body.splitlines()\n    if r"\\xrightarrow{" in line\n  )\n\n  assert exactness_lines == (\n    long_exact,\n  )\n  assert (\n    "\\\\[\\n"\n    + long_exact\n    + "\\n\\\\]"\n    in proof_body\n  )\n  assert "は完全である." not in proof_body\n'
TEST_R14_NUMBER = 'def test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically():\n  presentation = _phase159_r1_2_pi3_2_presentation()\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  injective = (\n    r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"\n    r"\\quad\\text{は単射}. \\qquad (1)"\n  )\n  surjective = (\n    r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"\n    r"\\quad\\text{は全射}. \\qquad (2)"\n  )\n  isomorphism = (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ "\n    "は同型."\n  )\n\n  assert (\n    "\\\\[\\n"\n    + injective\n    + "\\n\\\\]"\n    in rendered\n  )\n  assert (\n    "\\\\[\\n"\n    + surjective\n    + "\\n\\\\]"\n    in rendered\n  )\n  assert isomorphism in rendered\n\n  assert rendered.index(\n    injective\n  ) < rendered.index(\n    isomorphism\n  )\n  assert rendered.index(\n    surjective\n  ) < rendered.index(\n    isomorphism\n  )\n\n  assert r"\\tag{1}" not in rendered\n  assert r"\\tag{2}" not in rendered\n\n  assert (\n    "(1), (2) より, "\n    + isomorphism\n    in rendered\n  )\n'
TEST_R16B_NUMBER = 'def test_phase159_r1_6b_pi3_2_number_tags_include_map_property_statement():\n  presentation = (\n    _phase159_r1_6b_pi3_2_presentation()\n  )\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n\n  assert (\n    "\\\\[\\n"\n    r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"\n    r"\\quad\\text{は単射}. \\qquad (1)"\n    "\\n\\\\]"\n    in rendered\n  )\n  assert (\n    "\\\\[\\n"\n    r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"\n    r"\\quad\\text{は全射}. \\qquad (2)"\n    "\\n\\\\]"\n    in rendered\n  )\n\n  assert r"\\tag{1}" not in rendered\n  assert r"\\tag{2}" not in rendered\n\n  assert (\n    "(1), (2) より, "\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型."\n    in rendered\n  )\n'
TEST_R16C_REFERENCE = 'def test_phase159_r1_6c_toda_51_reference_is_source_faithful():\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      _phase159_r1_6c_pi3_2_presentation()\n    )\n  )\n  reference = (\n    rendered.split(\n      "## 使用する結果\\n\\n",\n      1,\n    )[1].split(\n      "\\n---\\n",\n      1,\n    )[0]\n  )\n\n  assert "**[R1] (5.1).**" in reference\n  assert (\n    r"$\\pi_{i}^{1} = 0\\ (i > 1),"\n    r"\\qquad "\n    r"\\pi_{i}^{n} = 0\\ (i < n)$."\n    in reference\n  )\n  assert (\n    r"$\\pi_{n}^{n} = "\n    r"\\mathbb{Z}\\{\\iota_{n}\\}$."\n    in reference\n  )\n\n  assert r"\\langle" not in reference\n  assert r"\\rangle" not in reference\n  assert r"\\pi_{2}^{1} = 0" not in reference\n  assert r"\\pi_{3}^{3}" not in reference\n  assert (\n    r"$E: \\pi_{1}^{1} \\to \\pi_{2}^{2}$"\n    not in reference\n  )\n'
TEST_R16C_EXACT = 'def test_phase159_r1_6c_exact_sequence_intro_does_not_repeat_exactness():\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      _phase159_r1_6c_pi3_2_presentation()\n    )\n  )\n\n  assert (\n    "$\\\\pi_{3}^{2}$ の群構造を決定するために, "\n    "次の完全列を考える."\n    in rendered\n  )\n  assert (\n    "\\\\[\\n"\n    r"\\pi_{2}^{1} \\xrightarrow{E} "\n    r"\\pi_{3}^{2} \\xrightarrow{H} "\n    r"\\pi_{3}^{3} \\xrightarrow{\\Delta} "\n    r"\\pi_{1}^{1} \\xrightarrow{E} "\n    r"\\pi_{2}^{2}."\n    "\\n\\\\]"\n    in rendered\n  )\n  assert "は完全である." not in rendered\n'
TEST_R16C_BODY = 'def test_phase159_r1_6c_proof_body_links_reference_and_exactness():\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      _phase159_r1_6c_pi3_2_presentation()\n    )\n  )\n\n  assert (\n    r"[R1] より, $\\pi_{2}^{1} = 0$."\n    in rendered\n  )\n  assert (\n    "完全性より,\\n\\n"\n    "\\\\[\\n"\n    r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"\n    r"\\quad\\text{は単射}. \\qquad (1)"\n    "\\n\\\\]"\n    in rendered\n  )\n  assert (\n    r"[R1] より, $\\pi_{1}^{1} = "\n    r"\\mathbb{Z}\\{\\iota_{1}\\}$, "\n    r"$\\pi_{2}^{2} = "\n    r"\\mathbb{Z}\\{\\iota_{2}\\}$."\n    in rendered\n  )\n  assert (\n    r"$E(\\iota_{1}) = \\iota_{2}$ であるから, "\n    r"$E: \\pi_{1}^{1} \\to \\pi_{2}^{2}$ は同型."\n    in rendered\n  )\n  assert (\n    r"したがって, $E: \\pi_{1}^{1} "\n    r"\\to \\pi_{2}^{2}$ は単射."\n    in rendered\n  )\n  assert (\n    r"完全性より, $\\Delta: \\pi_{3}^{3} "\n    r"\\to \\pi_{1}^{1}$ は零写像."\n    in rendered\n  )\n  assert (\n    r"[R1] より, $\\pi_{3}^{3} = "\n    r"\\mathbb{Z}\\{\\iota_{3}\\}$."\n    in rendered\n  )\n  assert (\n    "完全性より,\\n\\n"\n    "\\\\[\\n"\n    r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"\n    r"\\quad\\text{は全射}. \\qquad (2)"\n    "\\n\\\\]"\n    in rendered\n  )\n'
TEST_R16C_NUMBERS = 'def test_phase159_r1_6c_statement_numbers_are_outside_math():\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      _phase159_r1_6c_pi3_2_presentation()\n    )\n  )\n\n  assert r"\\tag{1}" not in rendered\n  assert r"\\tag{2}" not in rendered\n\n  assert (\n    "\\\\[\\n"\n    r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"\n    r"\\quad\\text{は単射}. \\qquad (1)"\n    "\\n\\\\]"\n    in rendered\n  )\n  assert (\n    "\\\\[\\n"\n    r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"\n    r"\\quad\\text{は全射}. \\qquad (2)"\n    "\\n\\\\]"\n    in rendered\n  )\n'
NEW_TEST = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _phase159_r1_6d_pi3_2_presentation():\n  report = build_standard_toda_report(\n    n=2,\n    k=1,\n  )\n  group_result = (\n    report.candidates[\n      0\n    ].source_candidate.group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n\n  return build_toda_group_proof_presentation(\n    replay\n  )\n\n\ndef test_phase159_r1_6d_diagonal_group_notation_uses_braces():\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      _phase159_r1_6d_pi3_2_presentation()\n    )\n  )\n  reference = (\n    rendered.split(\n      "## 使用する結果\\n\\n",\n      1,\n    )[1].split(\n      "\\n---\\n",\n      1,\n    )[0]\n  )\n\n  assert (\n    r"$\\pi_{n}^{n} = "\n    r"\\mathbb{Z}\\{\\iota_{n}\\}$."\n    in reference\n  )\n  assert r"\\langle" not in reference\n  assert r"\\rangle" not in reference\n\n\ndef test_phase159_r1_6d_suspension_isomorphism_is_derived_in_body():\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      _phase159_r1_6d_pi3_2_presentation()\n    )\n  )\n\n  assert (\n    r"[R1] より, $\\pi_{1}^{1} = "\n    r"\\mathbb{Z}\\{\\iota_{1}\\}$, "\n    r"$\\pi_{2}^{2} = "\n    r"\\mathbb{Z}\\{\\iota_{2}\\}$."\n    in rendered\n  )\n  assert (\n    r"$E(\\iota_{1}) = \\iota_{2}$ であるから, "\n    r"$E: \\pi_{1}^{1} \\to \\pi_{2}^{2}$ は同型."\n    in rendered\n  )\n\n\ndef test_phase159_r1_6d_reference_marker_spacing_is_normalized():\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      _phase159_r1_6d_pi3_2_presentation()\n    )\n  )\n\n  assert "[R1]より," not in rendered\n  assert "[R1] より," in rendered\n\n\ndef test_phase159_r1_6d_structural_formulas_are_centered():\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      _phase159_r1_6d_pi3_2_presentation()\n    )\n  )\n\n  assert (\n    "\\\\[\\n"\n    r"\\pi_{2}^{1} \\xrightarrow{E} "\n    r"\\pi_{3}^{2} \\xrightarrow{H} "\n    r"\\pi_{3}^{3} \\xrightarrow{\\Delta} "\n    r"\\pi_{1}^{1} \\xrightarrow{E} "\n    r"\\pi_{2}^{2}."\n    "\\n\\\\]"\n    in rendered\n  )\n  assert (\n    "\\\\[\\n"\n    r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"\n    r"\\quad\\text{は単射}. \\qquad (1)"\n    "\\n\\\\]"\n    in rendered\n  )\n  assert (\n    "\\\\[\\n"\n    r"H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"\n    r"\\quad\\text{は全射}. \\qquad (2)"\n    "\\n\\\\]"\n    in rendered\n  )\n'


def replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  marker = "def " + function_name + "("
  start = source.find(marker)

  if start < 0:
    raise RuntimeError(
      "function not found: "
      + function_name
    )

  next_function = source.find(
    "\ndef ",
    start + len(marker),
  )
  end = len(source) if next_function < 0 else next_function + 1

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n"
    + source[end:]
  )


def main() -> None:
  required = (
    RENDERER,
    R12_TEST,
    R16B_TEST,
    R16C_TEST,
  )

  for path in required:
    if not path.exists():
      raise FileNotFoundError(path)

  stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  backup_dir = ROOT / ("phase159_r1_6d_backup_" + stamp)
  backup_dir.mkdir(parents=True, exist_ok=False)

  for path in required:
    shutil.copy2(path, backup_dir / path.name)

  renderer = RENDERER.read_text(encoding="utf-8-sig")
  anchor = "def render_toda_group_proof_narrative_markdown("
  anchor_index = renderer.find(anchor)

  if anchor_index < 0:
    raise RuntimeError("public render function not found")

  if "def _phase159_r1_6d_toda_51_diagonal_specialization_lines(" not in renderer:
    renderer = (
      renderer[:anchor_index]
      + HELPERS.rstrip()
      + "\n\n\n"
      + renderer[anchor_index:]
    )

  renderer = replace_function(
    renderer,
    "render_toda_group_proof_narrative_markdown",
    NEW_RENDER,
  )
  RENDERER.write_text(renderer, encoding="utf-8", newline="\n")

  r12 = R12_TEST.read_text(encoding="utf-8-sig")
  r12 = replace_function(
    r12,
    "test_phase159_r1_4_pi3_2_public_uses_exactly_one_exact_sequence",
    TEST_R14_EXACT,
  )
  r12 = replace_function(
    r12,
    "test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically",
    TEST_R14_NUMBER,
  )
  R12_TEST.write_text(r12, encoding="utf-8", newline="\n")

  r16b = R16B_TEST.read_text(encoding="utf-8-sig")
  r16b = replace_function(
    r16b,
    "test_phase159_r1_6b_pi3_2_number_tags_include_map_property_statement",
    TEST_R16B_NUMBER,
  )
  R16B_TEST.write_text(r16b, encoding="utf-8", newline="\n")

  r16c = R16C_TEST.read_text(encoding="utf-8-sig")
  r16c = replace_function(
    r16c,
    "test_phase159_r1_6c_toda_51_reference_is_source_faithful",
    TEST_R16C_REFERENCE,
  )
  r16c = replace_function(
    r16c,
    "test_phase159_r1_6c_exact_sequence_intro_does_not_repeat_exactness",
    TEST_R16C_EXACT,
  )
  r16c = replace_function(
    r16c,
    "test_phase159_r1_6c_proof_body_links_reference_and_exactness",
    TEST_R16C_BODY,
  )
  r16c = replace_function(
    r16c,
    "test_phase159_r1_6c_statement_numbers_are_outside_math",
    TEST_R16C_NUMBERS,
  )
  R16C_TEST.write_text(r16c, encoding="utf-8", newline="\n")

  R16D_TEST.write_text(NEW_TEST, encoding="utf-8", newline="\n")

  print("Phase 159-R1-6d applied.")
  print("Backup:", backup_dir)
  print("Production:")
  print("- finalize Toda (5.1) diagonal specialization prose")
  print("- normalize [R] より spacing")
  print("- center exact sequence and numbered map-property formulas")
  print("- use Z-brace-iota notation in public Toda (5.1) Reference")


if __name__ == "__main__":
  main()
