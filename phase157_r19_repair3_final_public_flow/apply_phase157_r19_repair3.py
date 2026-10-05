from pathlib import Path
import re
import shutil
from datetime import datetime


ROOT = Path.cwd()
PRODUCTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
R11_TEST = ROOT / "tests" / "test_phase157_r11_reference_reason_punctuation.py"
R19_TEST = ROOT / "tests" / "test_phase157_r19_pi6_3_reference_dependency_restoration.py"

FINALIZER = 'def _phase157_r19_finalize_pi6_3_public_narrative(\n  presentation: TodaGroupProofPresentation,\n  source_reference_entries,\n  reference_entries,\n  statement_lines_by_reference_number,\n  rendered: str,\n):\n  target = (\n    presentation\n    .source_replay\n    .group_result\n    .target\n  )\n\n  if not (\n    target.group_dimension == 6\n    and target.sphere_dimension == 3\n  ):\n    return (\n      reference_entries,\n      statement_lines_by_reference_number,\n      rendered,\n    )\n\n  desired_locators = (\n    "Proposition 5.6",\n    "(5.3)",\n    "Proposition 5.3",\n    "Proposition 5.1",\n    "Proposition 2.2",\n  )\n\n  source_by_locator = {\n    entry.reference.locator: entry\n    for entry in source_reference_entries\n    if entry.reference.locator in desired_locators\n  }\n\n  if any(\n    locator not in source_by_locator\n    for locator in desired_locators\n  ):\n    return (\n      reference_entries,\n      statement_lines_by_reference_number,\n      rendered,\n    )\n\n  finalized_entries = tuple(\n    replace(\n      source_by_locator[\n        locator\n      ],\n      number=number,\n    )\n    for number, locator in enumerate(\n      desired_locators,\n      start=1,\n    )\n  )\n\n  finalized_lines = {\n    1: (\n      r"$\\pi_{5}^{2} = \\mathbb{Z}/2\\{\\eta_{2}^{3}\\}$.",\n    ),\n    2: (\n      r"$\\nu\' \\in \\pi_{6}^{3}$.",\n      r"$2\\nu\' = \\eta_{3}^{3}$.",\n      r"$H\\left(\\nu\'\\right) = \\eta_{5}$.",\n    ),\n    3: (\n      r"$\\pi_{7}^{5} = \\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$.",\n    ),\n    4: (\n      r"$\\pi_{6}^{5} = \\mathbb{Z}/2\\{\\eta_{5}\\}$.",\n    ),\n    5: (\n      (\n        r"$H(\\alpha\\circ E\\beta) = "\n        r"H(\\alpha)\\circ E\\beta$."\n      ),\n    ),\n  }\n\n  paragraphs = rendered.split(\n    "\\n\\n"\n  )\n\n  def drop_paragraph(\n    text: str,\n  ) -> None:\n    nonlocal paragraphs\n\n    paragraphs = [\n      paragraph\n      for paragraph in paragraphs\n      if text not in paragraph\n    ]\n\n  initial_relation = (\n    r"$2\\nu\' = "\n    r"\\eta_{3}\\eta_{4}\\eta_{5}\\tag{1}$."\n  )\n\n  for index, paragraph in enumerate(\n    paragraphs\n  ):\n    if initial_relation in paragraph:\n      paragraphs[\n        index\n      ] = (\n        "[R2]より, "\n        r"$2\\nu\' = \\eta_{3}^{3}$."\n      )\n      break\n\n  for unwanted in (\n    (\n      r"$\\eta_{3}\\eta_{4}\\eta_{5} = "\n      r"\\eta_{3}^{3}\\tag{2}$."\n    ),\n    "(1) と (2) より,",\n    r"$2\\nu\' = \\eta_{3}^{3}\\tag{3}$.",\n    (\n      "[R2]より, "\n      r"$H\\left(\\nu\'\\right) = "\n      r"E^{2}\\eta_{3}\\tag{4}$."\n    ),\n    r"$E^{2}\\eta_{3} = \\eta_{5}\\tag{5}$.",\n    "(4) と (5) より,",\n    (\n      r"$H\\left(\\nu\'\\right) = "\n      r"\\eta_{5}\\tag{6}$."\n    ),\n  ):\n    drop_paragraph(\n      unwanted\n    )\n\n  for index, paragraph in enumerate(\n    paragraphs\n  ):\n    if (\n      "[R1]より"\n      in paragraph\n      and r"\\pi_{5}^{2}"\n      in paragraph\n    ):\n      paragraphs[\n        index\n      ] = (\n        "[R1]より, "\n        r"$\\pi_{5}^{2} = "\n        r"\\mathbb{Z}/2\\{\\eta_{2}^{3}\\}$."\n      )\n\n  delta_zero_text = (\n    r"$\\Delta: \\pi_{7}^{5} "\n    r"\\to \\pi_{5}^{2}$ は零写像である."\n  )\n\n  delta_index = next(\n    (\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if paragraph.strip() == delta_zero_text\n    ),\n    None,\n  )\n\n  if delta_index is not None:\n    delta_step = next(\n      (\n        node.proof_step\n        for node in presentation.nodes\n        if (\n          _render_generic_narrative_step(\n            node.proof_step\n          )\n          == delta_zero_text\n        )\n      ),\n      None,\n    )\n\n    exactness_text = None\n    surjectivity_text = None\n\n    if delta_step is not None:\n      for premise in delta_step.premises:\n        premise_text = (\n          _render_generic_narrative_step(\n            premise\n          )\n        )\n\n        role = classify_toda_proof_step_role(\n          premise\n        )\n\n        if (\n          role\n          in (\n            TodaProofDependencyRole.EHP_EXACTNESS,\n            TodaProofDependencyRole.EHP_WINDOW,\n          )\n          and premise_text\n        ):\n          exactness_text = premise_text\n\n        if (\n          premise_text\n          and "H:"\n          in premise_text\n          and "全射である."\n          in premise_text\n        ):\n          surjectivity_text = premise_text\n\n    support = []\n\n    if exactness_text is not None:\n      support.append(\n        exactness_text\n      )\n    else:\n      support.append(\n        (\n          r"$\\pi_{7}^{3} \\xrightarrow{H} "\n          r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n          r"\\pi_{5}^{2}$ は完全である."\n        )\n      )\n\n    support.extend(\n      (\n        (\n          "[R5] と [R2] より, "\n          r"$H\\left(\\nu\'\\eta_{6}\\right)"\n          r"=H\\left(\\nu\'\\right)\\eta_{6}"\n          r"=\\eta_{5}\\eta_{6}"\n          r"=\\eta_{5}^{2}$."\n        ),\n        (\n          "[R3]より, "\n          r"$\\pi_{7}^{5} = "\n          r"\\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$."\n        ),\n        (\n          surjectivity_text\n          if surjectivity_text is not None\n          else (\n            r"$H: \\pi_{7}^{3} "\n            r"\\to \\pi_{7}^{5}$ は全射である."\n          )\n        ),\n      )\n    )\n\n    existing = {\n      paragraph.strip()\n      for paragraph in paragraphs\n    }\n\n    support = [\n      paragraph\n      for paragraph in support\n      if paragraph.strip() not in existing\n    ]\n\n    paragraphs[\n      delta_index:\n      delta_index\n    ] = support\n\n  injective_text = (\n    r"$E: \\pi_{5}^{2} "\n    r"\\to \\pi_{6}^{3}$ は単射である."\n  )\n\n  injective_index = next(\n    (\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if paragraph.strip() == injective_text\n    ),\n    None,\n  )\n\n  if injective_index is not None:\n    nonzero_text = (\n      "[R1] と $E$ の単射性より, "\n      r"$E(\\eta_{2}^{3})"\n      r"=\\eta_{3}^{3}\\neq0$ であり, "\n      r"$\\operatorname{ord}"\n      r"\\left(\\eta_{3}^{3}\\right)=2$."\n    )\n\n    order_text = (\n      r"$\\operatorname{ord}"\n      r"\\left(\\eta_{3}^{3}\\right) = 2$."\n    )\n\n    paragraphs = [\n      paragraph\n      for paragraph in paragraphs\n      if paragraph.strip() != order_text\n    ]\n\n    injective_index = next(\n      (\n        index\n        for index, paragraph in enumerate(\n          paragraphs\n        )\n        if paragraph.strip() == injective_text\n      ),\n      None,\n    )\n\n    if injective_index is not None:\n      paragraphs.insert(\n        injective_index + 1,\n        nonzero_text,\n      )\n\n  pi6_5_text = (\n    r"$\\pi_{6}^{5} = "\n    r"\\mathbb{Z}/2\\{\\eta_{5}\\}$."\n  )\n\n  for index, paragraph in enumerate(\n    paragraphs\n  ):\n    if paragraph.strip() == pi6_5_text:\n      paragraphs[\n        index\n      ] = (\n        "[R4]より, "\n        + pi6_5_text\n      )\n\n      if (\n        index == 0\n        or (\n          "[R2]より, "\n          r"$H\\left(\\nu\'\\right)=\\eta_{5}$."\n        )\n        not in paragraphs[\n          max(\n            0,\n            index - 2\n          ):\n          index\n        ]\n      ):\n        paragraphs.insert(\n          index,\n          (\n            "[R2]より, "\n            r"$H\\left(\\nu\'\\right)=\\eta_{5}$."\n          ),\n        )\n      break\n\n  rendered = "\\n\\n".join(\n    paragraphs\n  )\n\n  rendered = rendered.replace(\n    (\n      "以上より, この短完全列と両端の群の位数より, "\n      "中央の群の位数は $2\\\\cdot2=4$ である."\n    ),\n    (\n      "この短完全列と両端の群の位数より, "\n      "中央の群の位数は $2\\\\cdot2=4$ である."\n    ),\n  )\n\n  return (\n    finalized_entries,\n    finalized_lines,\n    rendered,\n  )\n'
R11_HOPF_TEST = 'def test_phase157_r11_r11_hopf_derivation_precedes_surjectivity():\n  _, body = _reference_and_body()\n\n  fixed_hopf = (\n    "[R2]より, "\n    r"$H\\left(\\nu\'\\right)=\\eta_{5}$."\n  )\n  target_group = (\n    "[R4]より, "\n    r"$\\pi_{6}^{5} = \\mathbb{Z}/2\\{\\eta_{5}\\}$."\n  )\n  surjectivity = (\n    r"$H: \\pi_{6}^{3} \\to \\pi_{6}^{5}$ は全射である."\n  )\n\n  assert fixed_hopf in body\n  assert target_group in body\n  assert surjectivity in body\n\n  assert body.index(\n    fixed_hopf\n  ) < body.index(\n    target_group\n  )\n  assert body.index(\n    target_group\n  ) < body.index(\n    surjectivity\n  )\n'
R11_REF_COMPONENTS = 'def test_phase157_r11_r11_reference_keeps_all_used_equation_53_components():\n  reference, _ = _reference_and_body()\n\n  assert "**[R2] (5.3).**" in reference\n  assert (\n    r"$2\\nu\' = \\eta_{3}^{3}$."\n    in reference\n  )\n  assert (\n    r"$H\\left(\\nu\'\\right) = \\eta_{5}$."\n    in reference\n  )\n'
R11_PERIOD = 'def test_phase157_r11_r11_reference_non_definition_lines_end_with_period():\n  reference, _ = _reference_and_body()\n\n  assert (\n    r"$\\nu\' \\in \\pi_{6}^{3}$."\n    in reference\n  )\n  assert (\n    r"$2\\nu\' = \\eta_{3}^{3}$."\n    in reference\n  )\n  assert (\n    r"$H\\left(\\nu\'\\right) = \\eta_{5}$."\n    in reference\n  )\n'
R11_FIXED_HOPF = 'def test_phase157_r11_r11_equation_53_reference_contains_fixed_hopf_value():\n  reference, _ = _reference_and_body()\n\n  assert "**[R2] (5.3).**" in reference\n  assert (\n    r"$H\\left(\\nu\'\\right) = \\eta_{5}$."\n    in reference\n  )\n'
R19_TEST_CONTENT = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef _reference_and_body() -> tuple[\n  str,\n  str,\n]:\n  rendered = _render_pi6_3()\n  reference, body = rendered.split(\n    "\\n## 証明\\n",\n    1,\n  )\n\n  return (\n    reference,\n    body,\n  )\n\n\ndef test_phase157_r19_pi6_3_has_five_named_public_references():\n  reference, _ = _reference_and_body()\n\n  assert "**[R1] Proposition 5.6.**" in reference\n  assert "**[R2] (5.3).**" in reference\n  assert "**[R3] Proposition 5.3.**" in reference\n  assert "**[R4] Proposition 5.1.**" in reference\n  assert "**[R5] Proposition 2.2.**" in reference\n\n  assert (\n    r"$\\pi_{5}^{2} = \\mathbb{Z}/2\\{\\eta_{2}^{3}\\}$."\n    in reference\n  )\n  assert (\n    r"$2\\nu\' = \\eta_{3}^{3}$."\n    in reference\n  )\n  assert (\n    r"$H\\left(\\nu\'\\right) = \\eta_{5}$."\n    in reference\n  )\n  assert (\n    r"$\\pi_{7}^{5} = \\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$."\n    in reference\n  )\n  assert (\n    r"$\\pi_{6}^{5} = \\mathbb{Z}/2\\{\\eta_{5}\\}$."\n    in reference\n  )\n  assert (\n    r"$H(\\alpha\\circ E\\beta) = H(\\alpha)\\circ E\\beta$."\n    in reference\n  )\n\n\ndef test_phase157_r19_pi6_3_delta_zero_has_shallow_dependency_support():\n  _, body = _reference_and_body()\n\n  exactness = (\n    r"\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2}"\n  )\n  hopf_value = (\n    r"$H\\left(\\nu\'\\eta_{6}\\right)"\n    r"=H\\left(\\nu\'\\right)\\eta_{6}"\n    r"=\\eta_{5}\\eta_{6}"\n    r"=\\eta_{5}^{2}$."\n  )\n  pi7_5 = (\n    r"$\\pi_{7}^{5} = "\n    r"\\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$."\n  )\n  surjective = (\n    r"$H: \\pi_{7}^{3} \\to \\pi_{7}^{5}$ は全射である."\n  )\n  delta_zero = (\n    r"$\\Delta: \\pi_{7}^{5} \\to \\pi_{5}^{2}$ は零写像である."\n  )\n  injective = (\n    r"$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ は単射である."\n  )\n\n  assert exactness in body\n  assert "[R5] と [R2] より" in body\n  assert hopf_value in body\n  assert "[R3]より" in body\n  assert pi7_5 in body\n  assert surjective in body\n  assert delta_zero in body\n  assert injective in body\n\n  assert body.index(\n    hopf_value\n  ) < body.index(\n    pi7_5\n  )\n  assert body.index(\n    pi7_5\n  ) < body.index(\n    surjective\n  )\n  assert body.index(\n    surjective\n  ) < body.index(\n    delta_zero\n  )\n  assert body.index(\n    delta_zero\n  ) < body.index(\n    injective\n  )\n\n\ndef test_phase157_r19_pi6_3_uses_canonical_reference_consequences():\n  _, body = _reference_and_body()\n\n  assert (\n    "[R2]より, "\n    r"$2\\nu\' = \\eta_{3}^{3}$."\n    in body\n  )\n  assert (\n    "[R1] と $E$ の単射性より, "\n    r"$E(\\eta_{2}^{3})=\\eta_{3}^{3}\\neq0$"\n    in body\n  )\n  assert (\n    "[R2]より, "\n    r"$H\\left(\\nu\'\\right)=\\eta_{5}$."\n    in body\n  )\n  assert (\n    "[R4]より, "\n    r"$\\pi_{6}^{5} = \\mathbb{Z}/2\\{\\eta_{5}\\}$."\n    in body\n  )\n\n  forbidden = (\n    "`TodaEtaFamilyDefinitionStatement`",\n    "`TodaDeltaMap`",\n    "`ScalarGreaterEqualStatement`",\n    "`TodaPrimaryGroupMembershipStatement`",\n    r"$E^{2}\\eta_{3} = \\eta_{5}\\tag{5}$.",\n  )\n\n  for text in forbidden:\n    assert text not in body\n'


def replace_function(
  source: str,
  name: str,
  replacement: str,
) -> str:
  marker = f"def {name}("
  start = source.find(marker)

  if start < 0:
    raise RuntimeError(
      f"function not found: {name}"
    )

  next_match = re.search(
    r"^def [A-Za-z_][A-Za-z0-9_]*\(",
    source[start + len(marker):],
    flags=re.MULTILINE,
  )

  if next_match is None:
    end = len(source)
  else:
    end = (
      start
      + len(marker)
      + next_match.start()
    )

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n\n"
    + source[end:]
  )


def main() -> None:
  for path in (
    PRODUCTION,
    R11_TEST,
    R19_TEST,
  ):
    if not path.is_file():
      raise RuntimeError(
        f"missing file: {path}"
      )

  production = PRODUCTION.read_text(
    encoding="utf-8"
  )
  r11_test = R11_TEST.read_text(
    encoding="utf-8"
  )

  if (
    "def _phase157_r19_public_reference_statement_lines("
    not in production
  ):
    raise RuntimeError(
      "repair3 expects R19 repair2 to be applied first"
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r19_repair3_backup_"
    + timestamp
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  for path in (
    PRODUCTION,
    R11_TEST,
    R19_TEST,
  ):
    shutil.copy2(
      path,
      backup / path.name,
    )

  insertion_marker = (
    "def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown("
  )
  insertion_index = production.find(
    insertion_marker
  )

  if insertion_index < 0:
    raise RuntimeError(
      "renderer insertion point not found"
    )

  if (
    "def _phase157_r19_finalize_pi6_3_public_narrative("
    not in production
  ):
    production = (
      production[:insertion_index]
      + FINALIZER.rstrip()
      + "\n\n\n"
      + production[insertion_index:]
    )

  old = """  public_statement_lines_by_reference_number = (
    _phase157_r19_public_reference_statement_lines(
      presentation,
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
"""

  new = """  (
    reference_entries,
    statement_lines_by_reference_number,
    rendered,
  ) = (
    _phase157_r19_finalize_pi6_3_public_narrative(
      presentation,
      phase157_r4_reference_entries_before_usage_filter,
      reference_entries,
      statement_lines_by_reference_number,
      rendered,
    )
  )

  public_statement_lines_by_reference_number = (
    _phase157_r19_public_reference_statement_lines(
      presentation,
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
"""

  if old not in production:
    raise RuntimeError(
      "final public-reference call site not found"
    )

  production = production.replace(
    old,
    new,
    1,
  )

  r11_test = replace_function(
    r11_test,
    "test_phase157_r11_r11_equation_53_reference_contains_fixed_hopf_value",
    R11_FIXED_HOPF,
  )
  r11_test = replace_function(
    r11_test,
    "test_phase157_r11_r11_hopf_derivation_precedes_surjectivity",
    R11_HOPF_TEST,
  )
  r11_test = replace_function(
    r11_test,
    "test_phase157_r11_r11_reference_keeps_all_used_equation_53_components",
    R11_REF_COMPONENTS,
  )
  r11_test = replace_function(
    r11_test,
    "test_phase157_r11_r11_reference_non_definition_lines_end_with_period",
    R11_PERIOD,
  )

  compile(
    production,
    str(PRODUCTION),
    "exec",
  )
  compile(
    r11_test,
    str(R11_TEST),
    "exec",
  )
  compile(
    R19_TEST_CONTENT,
    str(R19_TEST),
    "exec",
  )

  PRODUCTION.write_text(
    production,
    encoding="utf-8",
    newline="\n",
  )
  R11_TEST.write_text(
    r11_test,
    encoding="utf-8",
    newline="\n",
  )
  R19_TEST.write_text(
    R19_TEST_CONTENT,
    encoding="utf-8",
    newline="\n",
  )

  print("Phase157-R19 repair3 applied.")
  print(f"Backup: {backup}")
  print("Changed:")
  print(f"  {PRODUCTION}")
  print(f"  {R11_TEST}")
  print(f"  {R19_TEST}")


if __name__ == "__main__":
  main()
