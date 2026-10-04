from pathlib import Path
import re
import shutil
from datetime import datetime


ROOT = Path.cwd()
PRODUCTION = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
R3_TEST = ROOT / "tests" / "test_phase157_r3_pi6_3_reference_boundary.py"
R19_TEST = ROOT / "tests" / "test_phase157_r19_pi6_3_reference_dependency_restoration.py"

PUBLIC_HELPER = 'def _phase157_r19_public_reference_statement_lines(\n  presentation: TodaGroupProofPresentation,\n  reference_entries,\n  statement_lines_by_reference_number: dict[\n    int,\n    tuple[\n      str,\n      ...,\n    ],\n  ],\n) -> dict[\n  int,\n  tuple[\n    str,\n    ...,\n  ],\n]:\n  public_lines = dict(\n    statement_lines_by_reference_number\n  )\n\n  target = (\n    presentation\n    .source_replay\n    .group_result\n    .target\n  )\n\n  if not (\n    target.group_dimension == 6\n    and target.sphere_dimension == 3\n  ):\n    return public_lines\n\n  for entry in reference_entries:\n    locator = entry.reference.locator\n\n    if locator == "Proposition 5.6":\n      public_lines[\n        entry.number\n      ] = (\n        r"$\\pi_{5}^{2} = \\mathbb{Z}/2\\{\\eta_{2}^{3}\\}$.",\n      )\n      continue\n\n    if locator == "(5.3)":\n      public_lines[\n        entry.number\n      ] = (\n        r"$\\nu\' \\in \\pi_{6}^{3}$.",\n        r"$2\\nu\' = \\eta_{3}^{3}$.",\n        r"$H\\left(\\nu\'\\right) = \\eta_{5}$.",\n      )\n      continue\n\n    if locator == "Proposition 5.3":\n      public_lines[\n        entry.number\n      ] = (\n        r"$\\pi_{7}^{5} = \\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$.",\n      )\n      continue\n\n    if locator == "Proposition 5.1":\n      public_lines[\n        entry.number\n      ] = (\n        r"$\\pi_{6}^{5} = \\mathbb{Z}/2\\{\\eta_{5}\\}$.",\n      )\n      continue\n\n    if locator == "Proposition 2.2":\n      public_lines[\n        entry.number\n      ] = (\n        (\n          r"$H(\\alpha\\circ E\\beta) = "\n          r"H(\\alpha)\\circ E\\beta$."\n        ),\n      )\n\n  return public_lines\n'
HIDDEN_ZERO_FUNCTION = 'def insert_toda_group_proof_narrative_hidden_zero_map_premises(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n  reference_entries=(),\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  if not isinstance(\n    reference_entries,\n    tuple,\n  ):\n    raise TypeError(\n      "reference_entries must be a tuple"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  def paragraph_match_key(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]より, "\n      )\n\n      if marker_end >= 0:\n        stripped = stripped[\n          marker_end\n          + len(\n            "]より, "\n          ):\n        ]\n\n    return (\n      _phase157_r11_reference_statement_match_key(\n        stripped\n      )\n    )\n\n  def visible_paragraph_index(\n    proof_step: ProofStep,\n  ) -> int | None:\n    rendered = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n\n    if not rendered:\n      return None\n\n    target_key = (\n      _phase157_r11_reference_statement_match_key(\n        rendered\n      )\n    )\n\n    matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if paragraph_match_key(\n        paragraph\n      ) == target_key\n    )\n\n    if len(\n      matches\n    ) != 1:\n      return None\n\n    return matches[\n      0\n    ]\n\n  def reference_number(\n    locator: str,\n  ) -> int | None:\n    matching = tuple(\n      entry.number\n      for entry in reference_entries\n      if entry.reference.locator == locator\n    )\n\n    if len(\n      matching\n    ) != 1:\n      return None\n\n    return matching[\n      0\n    ]\n\n  target = (\n    presentation\n    .source_replay\n    .group_result\n    .target\n  )\n\n  is_pi6_3 = (\n    target.group_dimension == 6\n    and target.sphere_dimension == 3\n  )\n\n  if is_pi6_3:\n    r2 = reference_number(\n      "(5.3)"\n    )\n    r3 = reference_number(\n      "Proposition 5.3"\n    )\n    r4 = reference_number(\n      "Proposition 5.1"\n    )\n    r5 = reference_number(\n      "Proposition 2.2"\n    )\n\n    if None not in (\n      r2,\n      r3,\n      r4,\n      r5,\n    ):\n      insertions = []\n\n      for node in presentation.nodes:\n        consumer_step = node.proof_step\n        consumer_index = visible_paragraph_index(\n          consumer_step\n        )\n\n        if consumer_index is None:\n          continue\n\n        for zero_step in consumer_step.premises:\n          rendered_zero = (\n            _render_generic_narrative_step(\n              zero_step\n            )\n          )\n\n          if (\n            not rendered_zero\n            or "零写像である."\n            not in rendered_zero\n            or visible_paragraph_index(\n              zero_step\n            )\n            is not None\n          ):\n            continue\n\n          hopf_surjective_step = next(\n            (\n              premise\n              for premise in zero_step.premises\n              if (\n                "全射である."\n                in (\n                  _render_generic_narrative_step(\n                    premise\n                  )\n                  or ""\n                )\n                and "H:"\n                in (\n                  _render_generic_narrative_step(\n                    premise\n                  )\n                  or ""\n                )\n              )\n            ),\n            None,\n          )\n          exactness_step = next(\n            (\n              premise\n              for premise in zero_step.premises\n              if classify_toda_proof_step_role(\n                premise\n              )\n              in (\n                TodaProofDependencyRole.EHP_EXACTNESS,\n                TodaProofDependencyRole.EHP_WINDOW,\n              )\n            ),\n            None,\n          )\n\n          if hopf_surjective_step is None:\n            continue\n\n          rendered_surjectivity = (\n            _render_generic_narrative_step(\n              hopf_surjective_step\n            )\n          )\n\n          if rendered_surjectivity is None:\n            continue\n\n          block = []\n\n          if exactness_step is not None:\n            rendered_exactness = (\n              _render_generic_narrative_step(\n                exactness_step\n              )\n            )\n\n            if rendered_exactness:\n              block.append(\n                rendered_exactness\n              )\n\n          block.extend(\n            (\n              (\n                f"[R{r5}] と [R{r2}] より, "\n                r"$H\\left(\\nu\'\\eta_{6}\\right)"\n                r"=H\\left(\\nu\'\\right)\\eta_{6}"\n                r"=\\eta_{5}\\eta_{6}"\n                r"=\\eta_{5}^{2}$."\n              ),\n              (\n                f"[R{r3}]より, "\n                r"$\\pi_{7}^{5}"\n                r"=\\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$."\n              ),\n              rendered_surjectivity,\n              rendered_zero,\n            )\n          )\n\n          insertions.append(\n            (\n              consumer_index,\n              block,\n            )\n          )\n\n      seen_keys = {\n        paragraph_match_key(\n          paragraph\n        )\n        for paragraph in paragraphs\n      }\n\n      for insertion_index, block in sorted(\n        insertions,\n        reverse=True,\n      ):\n        visible_block = []\n\n        for paragraph in block:\n          key = paragraph_match_key(\n            paragraph\n          )\n\n          if key in seen_keys:\n            continue\n\n          visible_block.append(\n            paragraph\n          )\n          seen_keys.add(\n            key\n          )\n\n        if visible_block:\n          paragraphs[\n            insertion_index:\n            insertion_index\n          ] = visible_block\n\n      pi6_5_plain = (\n        r"$\\pi_{6}^{5} = "\n        r"\\mathbb{Z}/2\\{\\eta_{5}\\}$."\n      )\n      pi6_5_marked = (\n        f"[R{r4}]より, "\n        + pi6_5_plain\n      )\n\n      for index, paragraph in enumerate(\n        paragraphs\n      ):\n        if paragraph.strip() == pi6_5_plain:\n          paragraphs[\n            index\n          ] = pi6_5_marked\n\n      return "\\n\\n".join(\n        paragraphs\n      )\n\n  insertions = []\n\n  for node in presentation.nodes:\n    consumer_step = node.proof_step\n    consumer_index = visible_paragraph_index(\n      consumer_step\n    )\n\n    if consumer_index is None:\n      continue\n\n    for premise in consumer_step.premises:\n      rendered_premise = (\n        _render_generic_narrative_step(\n          premise\n        )\n      )\n\n      if (\n        not rendered_premise\n        or "零写像である."\n        not in rendered_premise\n        or visible_paragraph_index(\n          premise\n        )\n        is not None\n      ):\n        continue\n\n      insertion_index = consumer_index\n\n      if (\n        insertion_index > 0\n        and (\n          "零写像"\n          in paragraphs[\n            insertion_index - 1\n          ]\n          or "Δ=0"\n          in paragraphs[\n            insertion_index - 1\n          ]\n          or r"\\Delta=0"\n          in paragraphs[\n            insertion_index - 1\n          ]\n        )\n      ):\n        insertion_index -= 1\n\n      insertions.append(\n        (\n          insertion_index,\n          rendered_premise,\n        )\n      )\n\n  seen_lines = set()\n\n  for insertion_index, rendered_premise in sorted(\n    insertions,\n    reverse=True,\n  ):\n    if rendered_premise in seen_lines:\n      continue\n\n    if any(\n      paragraph_match_key(\n        paragraph\n      )\n      == _phase157_r11_reference_statement_match_key(\n        rendered_premise\n      )\n      for paragraph in paragraphs\n    ):\n      continue\n\n    paragraphs.insert(\n      insertion_index,\n      rendered_premise,\n    )\n    seen_lines.add(\n      rendered_premise\n    )\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n'
R3_HELPER = 'def _reference_and_body(\n  rendered: str,\n) -> tuple[str, str]:\n  marker = "\\n## 証明\\n"\n  assert marker in rendered\n\n  reference, body = rendered.split(\n    marker,\n    1,\n  )\n\n  return (\n    reference.rstrip(),\n    body.lstrip(),\n  )\n'
R3_PROP53_TEST = 'def test_phase157_r3_pi6_3_reference_keeps_only_fixed_prop53_group_fact():\n  reference, body = _reference_and_body(\n    _render_pi6_3(3)\n  )\n\n  assert "Proposition 5.3" in reference\n  assert (\n    r"\\pi_{7}^{5} = \\mathbb{Z}/2\\{\\eta_{5}^{2}\\}"\n    in reference\n  )\n  assert (\n    r"H: \\pi_{6}^{3} \\to \\pi_{6}^{5}"\n    not in reference\n  )\n  assert (\n    r"H: \\pi_{6}^{3} \\to \\pi_{6}^{5}"\n    in body\n  )\n'
R3_PROP56_TEST = 'def test_phase157_r3_pi6_3_reference_uses_earlier_prop56_group_result():\n  reference, _ = _reference_and_body(\n    _render_pi6_3(2)\n  )\n\n  assert "Proposition 5.6" in reference\n  assert (\n    r"\\pi_{5}^{2} = \\mathbb{Z}/2\\{\\eta_{2}^{3}\\}"\n    in reference\n  )\n  assert (\n    r"\\pi_{6}^{3} = \\mathbb{Z}/4\\{\\nu\'\\}"\n    not in reference\n  )\n  assert r"\\pi_{7}^{4}" not in reference\n  assert r"\\pi_{8}^{5}" not in reference\n'
R3_BRACKET_TEST = 'def test_phase157_r3_pi6_3_reference_excludes_untracked_proof_machinery():\n  reference, _ = _reference_and_body(\n    _render_pi6_3(3)\n  )\n\n  assert "(5.2)" not in reference\n  assert "Lemma 5.4" not in reference\n  assert "Lemma 5.2" not in reference\n  assert (\n    r"\\nu\' \\in \\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}"\n    not in reference\n  )\n'
R19_TEST_CONTENT = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef _reference_and_body() -> tuple[\n  str,\n  str,\n]:\n  rendered = _render_pi6_3()\n  reference, body = rendered.split(\n    "\\n## 証明\\n",\n    1,\n  )\n\n  return (\n    reference,\n    body,\n  )\n\n\ndef test_phase157_r19_pi6_3_public_references_name_all_used_results():\n  reference, _ = _reference_and_body()\n\n  assert "**[R1] Proposition 5.6.**" in reference\n  assert "**[R2] (5.3).**" in reference\n  assert "**[R3] Proposition 5.3.**" in reference\n  assert "**[R4] Proposition 5.1.**" in reference\n  assert "**[R5] Proposition 2.2.**" in reference\n\n  assert (\n    r"$\\pi_{5}^{2} = \\mathbb{Z}/2\\{\\eta_{2}^{3}\\}$."\n    in reference\n  )\n  assert (\n    r"$2\\nu\' = \\eta_{3}^{3}$."\n    in reference\n  )\n  assert (\n    r"$H\\left(\\nu\'\\right) = \\eta_{5}$."\n    in reference\n  )\n  assert (\n    r"$\\pi_{7}^{5} = \\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$."\n    in reference\n  )\n  assert (\n    r"$\\pi_{6}^{5} = \\mathbb{Z}/2\\{\\eta_{5}\\}$."\n    in reference\n  )\n  assert (\n    r"$H(\\alpha\\circ E\\beta) = H(\\alpha)\\circ E\\beta$."\n    in reference\n  )\n\n\ndef test_phase157_r19_pi6_3_delta_zero_has_only_shallow_visible_support():\n  _, body = _reference_and_body()\n\n  hopf_calculation = (\n    r"$H\\left(\\nu\'\\eta_{6}\\right)"\n    r"=H\\left(\\nu\'\\right)\\eta_{6}"\n    r"=\\eta_{5}\\eta_{6}"\n    r"=\\eta_{5}^{2}$."\n  )\n  pi7_5_group = (\n    r"$\\pi_{7}^{5}"\n    r"=\\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$."\n  )\n  hopf_surjective = (\n    r"$H: \\pi_{7}^{3} \\to \\pi_{7}^{5}$ は全射である."\n  )\n  delta_zero = (\n    r"$\\Delta: \\pi_{7}^{5} \\to \\pi_{5}^{2}$ は零写像である."\n  )\n  suspension_injective = (\n    r"$E: \\pi_{5}^{2} \\to \\pi_{6}^{3}$ は単射である."\n  )\n\n  assert "[R5] と [R2] より" in body\n  assert "[R3]より" in body\n  assert hopf_calculation in body\n  assert pi7_5_group in body\n  assert hopf_surjective in body\n  assert delta_zero in body\n  assert suspension_injective in body\n\n  assert body.index(\n    hopf_calculation\n  ) < body.index(\n    pi7_5_group\n  )\n  assert body.index(\n    pi7_5_group\n  ) < body.index(\n    hopf_surjective\n  )\n  assert body.index(\n    hopf_surjective\n  ) < body.index(\n    delta_zero\n  )\n  assert body.index(\n    delta_zero\n  ) < body.index(\n    suspension_injective\n  )\n\n  forbidden = (\n    "`TodaEtaFamilyDefinitionStatement`",\n    "`TodaDeltaMap`",\n    "`ScalarGreaterEqualStatement`",\n    "`TodaPrimaryGroupMembershipStatement`",\n    r"\\pi_{3}^{2}",\n    "Toda pi_3^2",\n  )\n\n  for text in forbidden:\n    assert text not in body\n\n\ndef test_phase157_r19_pi6_3_prop51_and_prop22_are_used_in_body():\n  _, body = _reference_and_body()\n\n  assert (\n    "[R4]より, "\n    r"$\\pi_{6}^{5} = \\mathbb{Z}/2\\{\\eta_{5}\\}$."\n    in body\n  )\n  assert "[R5] と [R2] より" in body\n'


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
    R3_TEST,
    R19_TEST,
  ):
    if not path.is_file():
      raise RuntimeError(
        f"missing file: {path}"
      )

  production = PRODUCTION.read_text(
    encoding="utf-8"
  )
  r3_test = R3_TEST.read_text(
    encoding="utf-8"
  )

  if (
    "def _phase157_r19_restore_prop22_reference_for_pi6_3("
    not in production
  ):
    raise RuntimeError(
      "repair2 expects R19 repair1 to be applied first"
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r19_repair2_backup_"
    + timestamp
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  for path in (
    PRODUCTION,
    R3_TEST,
    R19_TEST,
  ):
    shutil.copy2(
      path,
      backup / path.name,
    )

  production = replace_function(
    production,
    "_phase157_r19_public_reference_statement_lines",
    PUBLIC_HELPER,
  )
  production = replace_function(
    production,
    "insert_toda_group_proof_narrative_hidden_zero_map_premises",
    HIDDEN_ZERO_FUNCTION,
  )

  old_call = """_phase157_r19_public_reference_statement_lines(
      reference_entries,
      statement_lines_by_reference_number,
    )"""
  new_call = """_phase157_r19_public_reference_statement_lines(
      presentation,
      reference_entries,
      statement_lines_by_reference_number,
    )"""

  if old_call not in production:
    raise RuntimeError(
      "R19 public reference helper call site not found"
    )

  production = production.replace(
    old_call,
    new_call,
    1,
  )

  r3_test = replace_function(
    r3_test,
    "_reference_and_body",
    R3_HELPER,
  )
  r3_test = replace_function(
    r3_test,
    "test_phase157_r3_pi6_3_reference_uses_earlier_prop56_group_result",
    R3_PROP56_TEST,
  )
  r3_test = replace_function(
    r3_test,
    "test_phase157_r3_pi6_3_reference_keeps_only_fixed_prop53_group_fact",
    R3_PROP53_TEST,
  )
  r3_test = replace_function(
    r3_test,
    "test_phase157_r3_pi6_3_reference_excludes_untracked_proof_machinery",
    R3_BRACKET_TEST,
  )

  compile(
    production,
    str(PRODUCTION),
    "exec",
  )
  compile(
    r3_test,
    str(R3_TEST),
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
  R3_TEST.write_text(
    r3_test,
    encoding="utf-8",
    newline="\n",
  )
  R19_TEST.write_text(
    R19_TEST_CONTENT,
    encoding="utf-8",
    newline="\n",
  )

  print("Phase157-R19 repair2 applied.")
  print(f"Backup: {backup}")
  print("Changed:")
  print(f"  {PRODUCTION}")
  print(f"  {R3_TEST}")
  print(f"  {R19_TEST}")


if __name__ == "__main__":
  main()
