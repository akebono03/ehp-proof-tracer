from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
R12_TEST = (
  ROOT
  / "tests"
  / "test_phase159_r1_2_pi3_2_narrative_repair.py"
)
R16B_TEST = (
  ROOT
  / "tests"
  / "test_phase159_r1_6b_toda51_attribution.py"
)
R16C_TEST = (
  ROOT
  / "tests"
  / "test_phase159_r1_6c_source_faithful_reference_linkage.py"
)

HELPERS = 'def _phase159_r1_6c_recursive_proof_steps(\n  root_step: ProofStep,\n) -> tuple[ProofStep, ...]:\n  if not isinstance(\n    root_step,\n    ProofStep,\n  ):\n    raise TypeError(\n      "root_step must be a ProofStep"\n    )\n\n  steps = []\n  seen_step_ids = set()\n\n  def visit(\n    proof_step: ProofStep,\n  ) -> None:\n    step_id = id(\n      proof_step\n    )\n\n    if step_id in seen_step_ids:\n      return\n\n    seen_step_ids.add(\n      step_id\n    )\n    steps.append(\n      proof_step\n    )\n\n    for premise in proof_step.premises:\n      if isinstance(\n        premise,\n        ProofStep,\n      ):\n        visit(\n          premise\n        )\n\n  visit(\n    root_step\n  )\n\n  return tuple(\n    steps\n  )\n\n\ndef _phase159_r1_6c_step_reference_locator(\n  proof_step: ProofStep,\n) -> str | None:\n  if not isinstance(\n    proof_step,\n    ProofStep,\n  ):\n    raise TypeError(\n      "proof_step must be a ProofStep"\n    )\n\n  inference_rule = (\n    proof_step.inference_rule\n  )\n\n  if inference_rule is None:\n    return None\n\n  reference = (\n    inference_rule.literature_reference\n  )\n\n  if reference is None:\n    return None\n\n  return reference.locator\n\n\ndef _phase159_r1_6c_compact_map_property_line(\n  rendered: str,\n) -> str:\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  replacements = (\n    (\n      " は単射である.",\n      " は単射.",\n    ),\n    (\n      " は全射である.",\n      " は全射.",\n    ),\n    (\n      " は同型写像である.",\n      " は同型.",\n    ),\n    (\n      " は零写像である.",\n      " は零写像.",\n    ),\n  )\n\n  normalized = rendered.strip()\n\n  for old, new in replacements:\n    if normalized.endswith(\n      old\n    ):\n      return (\n        normalized[\n          :-len(\n            old\n          )\n        ]\n        + new\n      )\n\n  return normalized\n\n\ndef _phase159_r1_6c_statement_match_key(\n  rendered: str,\n) -> str:\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  normalized = rendered.strip()\n\n  normalized = re.sub(\n    r"\\\\tag\\{[0-9]+\\}",\n    "",\n    normalized,\n  )\n  normalized = re.sub(\n    r"\\s+",\n    " ",\n    normalized,\n  )\n\n  return normalized\n\n\ndef _phase159_r1_6c_reference_number(\n  rendered: str,\n  locator: str,\n) -> int | None:\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  if not isinstance(\n    locator,\n    str,\n  ):\n    raise TypeError(\n      "locator must be a str"\n    )\n\n  match = re.search(\n    r"^\\*\\*\\[R([0-9]+)\\] "\n    + re.escape(\n      locator\n    )\n    + r"\\.\\*\\*$",\n    rendered,\n    flags=re.MULTILINE,\n  )\n\n  if match is None:\n    return None\n\n  return int(\n    match.group(\n      1\n    )\n  )\n\n\ndef _phase159_r1_6c_canonicalize_toda_51_reference(\n  rendered: str,\n) -> str:\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  reference_marker = (\n    "## 使用する結果\\n\\n"\n  )\n  proof_boundary = (\n    "\\n---\\n\\n## 証明"\n  )\n  reference_start = rendered.find(\n    reference_marker\n  )\n\n  if reference_start < 0:\n    return rendered\n\n  content_start = (\n    reference_start\n    + len(\n      reference_marker\n    )\n  )\n  boundary_index = rendered.find(\n    proof_boundary,\n    content_start,\n  )\n\n  if boundary_index < 0:\n    return rendered\n\n  reference_body = rendered[\n    content_start:\n    boundary_index\n  ]\n  lines = reference_body.splitlines()\n  output = []\n  index = 0\n\n  while index < len(\n    lines\n  ):\n    match = re.match(\n      r"^\\*\\*\\[R([0-9]+)\\] "\n      r"\\(5\\.1\\)\\.\\*\\*$",\n      lines[\n        index\n      ].strip(),\n    )\n\n    if match is None:\n      output.append(\n        lines[\n          index\n        ]\n      )\n      index += 1\n      continue\n\n    output.append(\n      lines[\n        index\n      ]\n    )\n    output.append(\n      (\n        r"$\\pi_{i}^{1} = 0\\ (i > 1),"\n        r"\\qquad "\n        r"\\pi_{i}^{n} = 0\\ (i < n)$."\n      )\n    )\n    output.append(\n      (\n        r"$\\pi_{n}^{n} = "\n        r"\\langle \\iota_{n} \\rangle "\n        r"\\cong \\mathbb{Z}$."\n      )\n    )\n\n    index += 1\n\n    while (\n      index < len(\n        lines\n      )\n      and not lines[\n        index\n      ].strip().startswith(\n        "**[R"\n      )\n    ):\n      index += 1\n\n  normalized_reference = "\\n".join(\n    output\n  ).rstrip()\n\n  return (\n    rendered[\n      :content_start\n    ]\n    + normalized_reference\n    + rendered[\n      boundary_index:\n    ]\n  )\n\n\ndef _phase159_r1_6c_remove_redundant_exactness_sentence(\n  rendered: str,\n) -> str:\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  lines = rendered.splitlines()\n  result = []\n\n  for index, line in enumerate(\n    lines\n  ):\n    stripped = line.strip()\n\n    if not (\n      stripped.startswith(\n        "$"\n      )\n      and stripped.endswith(\n        "$ は完全である."\n      )\n    ):\n      result.append(\n        line\n      )\n      continue\n\n    previous_nonblank = next(\n      (\n        lines[\n          previous_index\n        ].strip()\n        for previous_index in range(\n          index - 1,\n          -1,\n          -1,\n        )\n        if lines[\n          previous_index\n        ].strip()\n      ),\n      "",\n    )\n\n    if not previous_nonblank.endswith(\n      "次の完全列を考える."\n    ):\n      result.append(\n        line\n      )\n      continue\n\n    result.append(\n      line.replace(\n        "$ は完全である.",\n        "$.",\n        1,\n      )\n    )\n\n  return "\\n".join(\n    result\n  )\n\n\ndef _phase159_r1_6c_link_proof_reasons(\n  presentation: TodaGroupProofPresentation,\n  rendered: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  proof_marker = (\n    "## 証明\\n\\n"\n  )\n  proof_start = rendered.find(\n    proof_marker\n  )\n\n  if proof_start < 0:\n    return rendered\n\n  body_start = (\n    proof_start\n    + len(\n      proof_marker\n    )\n  )\n  body = rendered[\n    body_start:\n  ]\n  body_lines = body.splitlines()\n\n  all_steps = (\n    _phase159_r1_6c_recursive_proof_steps(\n      presentation.root_step\n    )\n  )\n\n  exactness_derived_keys = set()\n\n  for proof_step in all_steps:\n    if not any(\n      (\n        isinstance(\n          premise,\n          ProofStep,\n        )\n        and isinstance(\n          premise.conclusion,\n          TodaProp42ExactnessStatement,\n        )\n      )\n      for premise in proof_step.premises\n    ):\n      continue\n\n    rendered_step = (\n      _phase159_r1_6c_compact_map_property_line(\n        _render_generic_narrative_step(\n          proof_step\n        )\n      )\n    )\n\n    exactness_derived_keys.add(\n      _phase159_r1_6c_statement_match_key(\n        rendered_step\n      )\n    )\n\n  suspension_pairs = []\n\n  for proof_step in all_steps:\n    if not isinstance(\n      proof_step.conclusion,\n      TodaSuspensionInjectiveStatement,\n    ):\n      continue\n\n    source_step = next(\n      (\n        premise\n        for premise in proof_step.premises\n        if (\n          isinstance(\n            premise,\n            ProofStep,\n          )\n          and isinstance(\n            premise.conclusion,\n            TodaSuspensionIsomorphismStatement,\n          )\n          and (\n            _phase159_r1_6c_step_reference_locator(\n              premise\n            )\n            == "(5.1)"\n          )\n        )\n      ),\n      None,\n    )\n\n    if source_step is None:\n      continue\n\n    source_line = (\n      _phase159_r1_6c_compact_map_property_line(\n        _render_generic_narrative_step(\n          source_step\n        )\n      )\n    )\n    target_line = (\n      _phase159_r1_6c_compact_map_property_line(\n        _render_generic_narrative_step(\n          proof_step\n        )\n      )\n    )\n\n    suspension_pairs.append(\n      (\n        _phase159_r1_6c_statement_match_key(\n          target_line\n        ),\n        source_line,\n      )\n    )\n\n  reference_number = (\n    _phase159_r1_6c_reference_number(\n      rendered,\n      "(5.1)",\n    )\n  )\n\n  linked_lines = []\n  inserted_source_keys = set()\n\n  for line in body_lines:\n    stripped = line.strip()\n    key = (\n      _phase159_r1_6c_statement_match_key(\n        stripped\n      )\n    )\n\n    suspension_pair = next(\n      (\n        pair\n        for pair in suspension_pairs\n        if pair[\n          0\n        ] == key\n      ),\n      None,\n    )\n\n    if (\n      suspension_pair is not None\n      and reference_number is not None\n    ):\n      source_line = (\n        suspension_pair[\n          1\n        ]\n      )\n      source_key = (\n        _phase159_r1_6c_statement_match_key(\n          source_line\n        )\n      )\n\n      if source_key not in inserted_source_keys:\n        if (\n          linked_lines\n          and linked_lines[\n            -1\n          ].strip()\n        ):\n          linked_lines.append(\n            ""\n          )\n\n        linked_lines.append(\n          (\n            "[R"\n            + str(\n              reference_number\n            )\n            + "]より, "\n            + source_line\n          )\n        )\n        linked_lines.append(\n          ""\n        )\n        inserted_source_keys.add(\n          source_key\n        )\n\n      linked_lines.append(\n        (\n          "したがって, "\n          + stripped\n        )\n      )\n      continue\n\n    if (\n      key in exactness_derived_keys\n      and not stripped.startswith(\n        "完全性より,"\n      )\n    ):\n      linked_lines.append(\n        (\n          "完全性より, "\n          + stripped\n        )\n      )\n      continue\n\n    linked_lines.append(\n      line\n    )\n\n  return (\n    rendered[\n      :body_start\n    ]\n    + "\\n".join(\n      linked_lines\n    )\n  )\n\n\ndef _phase159_r1_6c_render_statement_numbers(\n  rendered: str,\n) -> str:\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  pattern = re.compile(\n    r"^(?P<prefix>.*)"\n    r"\\$(?P<map>.+?)"\n    r"\\\\tag\\{(?P<number>[0-9]+)\\}"\n    r"\\$ は"\n    r"(?P<property>単射|全射|同型|零写像)"\n    r"\\.$"\n  )\n\n  result = []\n\n  for line in rendered.splitlines():\n    match = pattern.match(\n      line\n    )\n\n    if match is None:\n      result.append(\n        line\n      )\n      continue\n\n    result.append(\n      (\n        match.group(\n          "prefix"\n        )\n        + "$"\n        + match.group(\n          "map"\n        )\n        + "$ は"\n        + match.group(\n          "property"\n        )\n        + ". ("\n        + match.group(\n          "number"\n        )\n        + ")"\n      )\n    )\n\n  return "\\n".join(\n    result\n  )\n'
NEW_RENDER = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  rendered = (\n    _phase158_baseline_render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n  rendered = (\n    _phase158_normalize_public_narrative_contract(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_normalize_public_map_property_wording(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_normalize_public_reference_map_property_wording(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_6c_canonicalize_toda_51_reference(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_6c_remove_redundant_exactness_sentence(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_6c_link_proof_reasons(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_r1_6c_render_statement_numbers(\n      rendered\n    )\n  )\n\n  return (\n    _phase159_inject_foundational_reference_section(\n      presentation,\n      rendered,\n    )\n  )\n'
TEST_R14 = 'def test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically():\n  presentation = _phase159_r1_2_pi3_2_presentation()\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  injective = (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ "\n    "は単射. (1)"\n  )\n  surjective = (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ "\n    "は全射. (2)"\n  )\n  isomorphism = (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ "\n    "は同型."\n  )\n\n  assert injective in rendered\n  assert surjective in rendered\n  assert isomorphism in rendered\n\n  assert rendered.index(\n    injective\n  ) < rendered.index(\n    isomorphism\n  )\n  assert rendered.index(\n    surjective\n  ) < rendered.index(\n    isomorphism\n  )\n\n  assert r"\\tag{1}" not in rendered\n  assert r"\\tag{2}" not in rendered\n  assert r"\\text{ は単射}" not in rendered\n  assert r"\\text{ は全射}" not in rendered\n\n  assert (\n    "(1), (2) より, "\n    + isomorphism\n    in rendered\n  )\n'
TEST_R16B_NUMBER = 'def test_phase159_r1_6b_pi3_2_number_tags_include_map_property_statement():\n  presentation = (\n    _phase159_r1_6b_pi3_2_presentation()\n  )\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n\n  assert (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ "\n    "は単射. (1)"\n    in rendered\n  )\n  assert (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ "\n    "は全射. (2)"\n    in rendered\n  )\n\n  assert r"\\tag{1}" not in rendered\n  assert r"\\tag{2}" not in rendered\n\n  assert (\n    "(1), (2) より, "\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型."\n    in rendered\n  )\n'
NEW_TEST = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _phase159_r1_6c_pi3_2_presentation():\n  report = build_standard_toda_report(\n    n=2,\n    k=1,\n  )\n  group_result = (\n    report.candidates[\n      0\n    ].source_candidate.group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n\n  return build_toda_group_proof_presentation(\n    replay\n  )\n\n\ndef test_phase159_r1_6c_toda_51_reference_is_source_faithful():\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      _phase159_r1_6c_pi3_2_presentation()\n    )\n  )\n  reference = (\n    rendered.split(\n      "## 使用する結果\\n\\n",\n      1,\n    )[1].split(\n      "\\n---\\n",\n      1,\n    )[0]\n  )\n\n  assert "**[R1] (5.1).**" in reference\n  assert (\n    r"$\\pi_{i}^{1} = 0\\ (i > 1),"\n    r"\\qquad "\n    r"\\pi_{i}^{n} = 0\\ (i < n)$."\n    in reference\n  )\n  assert (\n    r"$\\pi_{n}^{n} = "\n    r"\\langle \\iota_{n} \\rangle "\n    r"\\cong \\mathbb{Z}$."\n    in reference\n  )\n\n  assert r"\\pi_{2}^{1} = 0" not in reference\n  assert r"\\pi_{3}^{3}" not in reference\n  assert (\n    r"$E: \\pi_{1}^{1} \\to \\pi_{2}^{2}$"\n    not in reference\n  )\n\n\ndef test_phase159_r1_6c_exact_sequence_intro_does_not_repeat_exactness():\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      _phase159_r1_6c_pi3_2_presentation()\n    )\n  )\n\n  assert (\n    "$\\\\pi_{3}^{2}$ の群構造を決定するために, "\n    "次の完全列を考える."\n    in rendered\n  )\n  assert (\n    r"$\\pi_{2}^{1} \\xrightarrow{E} "\n    r"\\pi_{3}^{2} \\xrightarrow{H} "\n    r"\\pi_{3}^{3} \\xrightarrow{\\Delta} "\n    r"\\pi_{1}^{1} \\xrightarrow{E} "\n    r"\\pi_{2}^{2}$."\n    in rendered\n  )\n  assert "は完全である." not in rendered\n\n\ndef test_phase159_r1_6c_proof_body_links_reference_and_exactness():\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      _phase159_r1_6c_pi3_2_presentation()\n    )\n  )\n\n  assert (\n    r"[R1]より, $\\pi_{2}^{1} = 0$."\n    in rendered\n  )\n  assert (\n    r"完全性より, $H: \\pi_{3}^{2} "\n    r"\\to \\pi_{3}^{3}$ は単射. (1)"\n    in rendered\n  )\n  assert (\n    r"[R1]より, $E: \\pi_{1}^{1} "\n    r"\\to \\pi_{2}^{2}$ は同型."\n    in rendered\n  )\n  assert (\n    r"したがって, $E: \\pi_{1}^{1} "\n    r"\\to \\pi_{2}^{2}$ は単射."\n    in rendered\n  )\n  assert (\n    r"完全性より, $\\Delta: \\pi_{3}^{3} "\n    r"\\to \\pi_{1}^{1}$ は零写像."\n    in rendered\n  )\n  assert (\n    r"[R1]より, $\\pi_{3}^{3} = "\n    r"\\mathbb{Z}\\{\\iota_{3}\\}$."\n    in rendered\n  )\n  assert (\n    r"完全性より, $H: \\pi_{3}^{2} "\n    r"\\to \\pi_{3}^{3}$ は全射. (2)"\n    in rendered\n  )\n\n\ndef test_phase159_r1_6c_statement_numbers_are_outside_math():\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      _phase159_r1_6c_pi3_2_presentation()\n    )\n  )\n\n  assert r"\\tag{1}" not in rendered\n  assert r"\\tag{2}" not in rendered\n  assert r"\\text{ は単射}" not in rendered\n  assert r"\\text{ は全射}" not in rendered\n\n  assert (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ "\n    "は単射. (1)"\n    in rendered\n  )\n  assert (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ "\n    "は全射. (2)"\n    in rendered\n  )\n'


def replace_function(
  source: str,
  function_name: str,
  replacement: str,
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
    raise RuntimeError(
      "function not found: "
      + function_name
    )

  next_function = source.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  end = (
    len(
      source
    )
    if next_function < 0
    else next_function + 1
  )

  return (
    source[
      :start
    ]
    + replacement.rstrip()
    + "\n\n"
    + source[
      end:
    ]
  )


def main() -> None:
  for path in (
    RENDERER,
    R12_TEST,
    R16B_TEST,
  ):
    if not path.exists():
      raise FileNotFoundError(
        path
      )

  stamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase159_r1_6c_backup_"
      + stamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )

  for path in (
    RENDERER,
    R12_TEST,
    R16B_TEST,
  ):
    shutil.copy2(
      path,
      backup_dir / path.name,
    )

  renderer = RENDERER.read_text(
    encoding="utf-8-sig"
  )

  anchor = (
    "def render_toda_group_proof_narrative_markdown("
  )
  anchor_index = renderer.find(
    anchor
  )

  if anchor_index < 0:
    raise RuntimeError(
      "public render function not found"
    )

  if (
    "def _phase159_r1_6c_recursive_proof_steps("
    not in renderer
  ):
    renderer = (
      renderer[
        :anchor_index
      ]
      + HELPERS.rstrip()
      + "\n\n\n"
      + renderer[
        anchor_index:
      ]
    )

  renderer = replace_function(
    renderer,
    "render_toda_group_proof_narrative_markdown",
    NEW_RENDER,
  )

  RENDERER.write_text(
    renderer,
    encoding="utf-8",
    newline="\n",
  )

  r12_test = R12_TEST.read_text(
    encoding="utf-8-sig"
  )
  r12_test = replace_function(
    r12_test,
    "test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically",
    TEST_R14,
  )
  R12_TEST.write_text(
    r12_test,
    encoding="utf-8",
    newline="\n",
  )

  r16b_test = R16B_TEST.read_text(
    encoding="utf-8-sig"
  )
  r16b_test = replace_function(
    r16b_test,
    "test_phase159_r1_6b_pi3_2_number_tags_include_map_property_statement",
    TEST_R16B_NUMBER,
  )
  R16B_TEST.write_text(
    r16b_test,
    encoding="utf-8",
    newline="\n",
  )

  R16C_TEST.write_text(
    NEW_TEST,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159-R1-6c applied."
  )
  print(
    "Backup:",
    backup_dir,
  )
  print(
    "Implemented source-faithful Toda (5.1) Reference, "
    "proof-body linkage, exactness deduplication, "
    "and prose statement numbering."
  )


if __name__ == "__main__":
  main()
