from pathlib import Path
from datetime import datetime
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
BOUNDARY = ROOT / "toda_literature_statement_boundary.py"
BOOTSTRAP = ROOT / "toda_upstream_bootstrap.py"
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
OLD_R16A_TEST = (
  ROOT
  / "tests"
  / "test_phase159_r1_6a_foundational_reference_identity.py"
)
NEW_TEST = (
  ROOT
  / "tests"
  / "test_phase159_r1_6b_toda51_attribution.py"
)

EQUATION51_COMPONENTS = '_EQUATION_51_COMPONENTS = (\n  TodaFixedStatementComponent(\n    reference_locator="(5.1)",\n    component_key="circle_higher_homotopy_zero",\n    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,\n    order=None,\n    range_text="i > 1",\n    range_is_explicit_in_current_aggregate=True,\n  ),\n  TodaFixedStatementComponent(\n    reference_locator="(5.1)",\n    component_key="sphere_connectivity_zero",\n    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,\n    order=None,\n    range_text="i < n",\n    range_is_explicit_in_current_aggregate=True,\n  ),\n  TodaFixedStatementComponent(\n    reference_locator="(5.1)",\n    component_key="stable_negative_zero",\n    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,\n    order=None,\n    range_text="k < 0",\n    range_is_explicit_in_current_aggregate=True,\n  ),\n  TodaFixedStatementComponent(\n    reference_locator="(5.1)",\n    component_key="diagonal_identity_group",\n    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,\n    order=None,\n    range_text=None,\n    range_is_explicit_in_current_aggregate=True,\n  ),\n  TodaFixedStatementComponent(\n    reference_locator="(5.1)",\n    component_key="stable_zero_stem",\n    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,\n    order=None,\n    range_text=None,\n    range_is_explicit_in_current_aggregate=True,\n  ),\n  TodaFixedStatementComponent(\n    reference_locator="(5.1)",\n    component_key="diagonal_suspension_isomorphism",\n    statement_role=TodaLiteratureStatementRole.OTHER,\n    order=None,\n    range_text=None,\n    range_is_explicit_in_current_aggregate=False,\n  ),\n)\n\n\n'
NEW_FIRST_THREE = '    ProofStep(\n      conclusion=pi_2_1_zero_fact(),\n      premises=(),\n      rule=ProofRule.GIVEN,\n      inference_rule=InferenceRule(\n        name=(\n          "Toda (5.1) circle higher homotopy zero"\n        ),\n        literature_reference=LiteratureReference(\n          label="Toda (5.1)",\n          locator="(5.1)",\n        ),\n      ),\n    ),\n    ProofStep(\n      conclusion=pi_3_3_free_cyclic_fact(),\n      premises=(),\n      rule=ProofRule.GIVEN,\n      inference_rule=InferenceRule(\n        name=(\n          "Toda (5.1) diagonal identity group"\n        ),\n        literature_reference=LiteratureReference(\n          label="Toda (5.1)",\n          locator="(5.1)",\n        ),\n      ),\n    ),\n    ProofStep(\n      conclusion=e_pi_1_1_to_pi_2_2_isomorphism_fact(),\n      premises=(),\n      rule=ProofRule.GIVEN,\n      inference_rule=InferenceRule(\n        name=(\n          "Toda (5.1) low-dimensional "\n          "suspension isomorphism"\n        ),\n        literature_reference=LiteratureReference(\n          label="Toda (5.1)",\n          locator="(5.1)",\n        ),\n      ),\n    ),\n'
NUMBERING_HELPER = 'def _phase159_number_public_map_property_statement(\n  rendered: str,\n) -> str:\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  pattern = re.compile(\n    r"^\\$(?P<map>.+?)"\n    r"\\\\tag\\{(?P<number>[0-9]+)\\}"\n    r"\\$ は"\n    r"(?P<property>単射|全射|同型|零写像)"\n    r"\\.$"\n  )\n\n  lines = []\n\n  for line in rendered.splitlines():\n    match = pattern.match(\n      line.strip()\n    )\n\n    if match is None:\n      lines.append(\n        line\n      )\n      continue\n\n    leading = line[\n      :len(\n        line\n      )\n      - len(\n        line.lstrip()\n      )\n    ]\n\n    lines.append(\n      leading\n      + "$"\n      + match.group(\n        "map"\n      )\n      + r" \\text{ は"\n      + match.group(\n        "property"\n      )\n      + r"}. \\tag{"\n      + match.group(\n        "number"\n      )\n      + "}$"\n    )\n\n  return "\\n".join(\n    lines\n  )\n'
NEW_RENDER = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  rendered = (\n    _phase158_baseline_render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n  rendered = (\n    _phase158_normalize_public_narrative_contract(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_normalize_public_map_property_wording(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_number_public_map_property_statement(\n      rendered\n    )\n  )\n\n  return (\n    _phase159_inject_foundational_reference_section(\n      presentation,\n      rendered,\n    )\n  )\n'
TEST_CONTENT = 'from low_dimensional_facts import (\n  e_pi_1_1_to_pi_2_2_isomorphism_fact,\n  pi_2_1_zero_fact,\n  pi_3_3_free_cyclic_fact,\n)\nfrom proof import ProofStep\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\nfrom toda_literature_statement_boundary import (\n  TodaLiteratureStatementClassification,\n  classify_toda_literature_statement_step,\n)\n\n\ndef _phase159_r1_6b_pi3_2_presentation():\n  report = build_standard_toda_report(\n    n=2,\n    k=1,\n  )\n  group_result = (\n    report.candidates[\n      0\n    ].source_candidate.group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n\n  return build_toda_group_proof_presentation(\n    replay\n  )\n\n\ndef _phase159_r1_6b_recursive_steps(\n  root_step,\n):\n  steps = []\n  seen_step_ids = set()\n\n  def visit(\n    proof_step,\n  ):\n    step_id = id(\n      proof_step\n    )\n\n    if step_id in seen_step_ids:\n      return\n\n    seen_step_ids.add(\n      step_id\n    )\n    steps.append(\n      proof_step\n    )\n\n    for premise in proof_step.premises:\n      if isinstance(\n        premise,\n        ProofStep,\n      ):\n        visit(\n          premise\n        )\n\n  visit(\n    root_step\n  )\n\n  return tuple(\n    steps\n  )\n\n\ndef test_phase159_r1_6b_pi3_2_low_dimensional_facts_are_toda_51_fixed_statements():\n  presentation = (\n    _phase159_r1_6b_pi3_2_presentation()\n  )\n  steps = (\n    _phase159_r1_6b_recursive_steps(\n      presentation.root_step\n    )\n  )\n\n  expected = {\n    pi_2_1_zero_fact():\n      "circle_higher_homotopy_zero",\n    pi_3_3_free_cyclic_fact():\n      "diagonal_identity_group",\n    e_pi_1_1_to_pi_2_2_isomorphism_fact():\n      "diagonal_suspension_isomorphism",\n  }\n\n  found = {}\n\n  for proof_step in steps:\n    if proof_step.conclusion not in expected:\n      continue\n\n    boundary = (\n      classify_toda_literature_statement_step(\n        proof_step\n      )\n    )\n\n    assert boundary is not None\n    assert (\n      boundary.classification\n      is TodaLiteratureStatementClassification.FIXED_STATEMENT\n    )\n    assert (\n      boundary.reference_locator\n      == "(5.1)"\n    )\n\n    found[\n      proof_step.conclusion\n    ] = boundary.component_key\n\n  assert found == expected\n\n\ndef test_phase159_r1_6b_pi3_2_public_reference_uses_single_toda_51_entry():\n  presentation = (\n    _phase159_r1_6b_pi3_2_presentation()\n  )\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n\n  reference_section = (\n    rendered.split(\n      "## 使用する結果\\n\\n",\n      1,\n    )[1].split(\n      "\\n---\\n",\n      1,\n    )[0]\n  )\n\n  assert (\n    reference_section.count(\n      "**[R1] (5.1).**"\n    )\n    == 1\n  )\n  assert "[F1]" not in reference_section\n  assert "[F2]" not in reference_section\n  assert "[F3]" not in reference_section\n\n  assert (\n    r"$\\pi_{2}^{1} = 0$."\n    in reference_section\n  )\n  assert (\n    r"$\\pi_{3}^{3} = "\n    r"\\mathbb{Z}\\{\\iota_{3}\\}$."\n    in reference_section\n  )\n  assert (\n    r"$E: \\pi_{1}^{1} \\to "\n    r"\\pi_{2}^{2}$ は同型."\n    in reference_section\n  )\n\n  assert (\n    r"\\pi_{3}^{2} = "\n    r"\\mathbb{Z}\\{\\eta_{2}\\}"\n    not in reference_section\n  )\n  assert (\n    "Proposition 5.1"\n    not in reference_section\n  )\n\n\ndef test_phase159_r1_6b_pi3_2_number_tags_include_map_property_statement():\n  presentation = (\n    _phase159_r1_6b_pi3_2_presentation()\n  )\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n\n  assert (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3} "\n    r"\\text{ は単射}. \\tag{1}$"\n    in rendered\n  )\n  assert (\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3} "\n    r"\\text{ は全射}. \\tag{2}$"\n    in rendered\n  )\n\n  assert (\n    r"\\tag{1}$ は単射."\n    not in rendered\n  )\n  assert (\n    r"\\tag{2}$ は全射."\n    not in rendered\n  )\n\n  assert (\n    "(1), (2) より, "\n    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ は同型."\n    in rendered\n  )\n\n\ndef test_phase159_r1_6b_pi3_2_has_no_foundational_reference_labels():\n  presentation = (\n    _phase159_r1_6b_pi3_2_presentation()\n  )\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n\n  assert "[F1]" not in rendered\n  assert "[F2]" not in rendered\n  assert "[F3]" not in rendered\n'


def replace_once(
  source,
  old,
  new,
  label,
):
  count = source.count(
    old
  )

  if count != 1:
    raise RuntimeError(
      label
      + ": expected exactly one match, found "
      + str(
        count
      )
    )

  return source.replace(
    old,
    new,
    1,
  )


def replace_function(
  source,
  function_name,
  replacement,
):
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
    source[:start]
    + replacement.rstrip()
    + "\n\n"
    + source[end:]
  )


def ensure_re_import(
  source,
):
  if (
    source.startswith(
      "import re\n"
    )
    or "\nimport re\n"
    in source
  ):
    return source

  import_anchor = (
    "from dataclasses import"
  )
  anchor_index = source.find(
    import_anchor
  )

  if anchor_index >= 0:
    return (
      "import re\n\n"
      + source
    )

  return (
    "import re\n"
    + source
  )


def replace_phase49_first_three(
  source,
):
  function_start = source.find(
    "def _build_phase49_result():"
  )

  if function_start < 0:
    raise RuntimeError(
      "_build_phase49_result not found"
    )

  premise_start = source.find(
    "  premise_steps = (\n",
    function_start,
  )

  if premise_start < 0:
    raise RuntimeError(
      "phase49 premise_steps not found"
    )

  first_step = source.find(
    "    ProofStep(\n",
    premise_start,
  )

  fourth_step_marker = (
    "    ProofStep(\n"
    "      conclusion=TodaProp42ExactnessStatement("
  )
  fourth_step = source.find(
    fourth_step_marker,
    first_step,
  )

  if (
    first_step < 0
    or fourth_step < 0
  ):
    raise RuntimeError(
      "phase49 first premise block not found"
    )

  return (
    source[:first_step]
    + NEW_FIRST_THREE
    + source[fourth_step:]
  )


def main():
  for path in (
    BOUNDARY,
    BOOTSTRAP,
    RENDERER,
    OLD_R16A_TEST,
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
      "phase159_r1_6b_backup_"
      + stamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )

  for path in (
    BOUNDARY,
    BOOTSTRAP,
    RENDERER,
    OLD_R16A_TEST,
  ):
    shutil.copy2(
      path,
      backup_dir / path.name,
    )

  boundary = BOUNDARY.read_text(
    encoding="utf-8-sig"
  )

  if (
    "_EQUATION_51_COMPONENTS = ("
    not in boundary
  ):
    anchor = (
      "_PROPOSITION_51_COMPONENTS = ("
    )
    index = boundary.find(
      anchor
    )

    if index < 0:
      raise RuntimeError(
        "Proposition 5.1 component anchor not found"
      )

    boundary = (
      boundary[:index]
      + EQUATION51_COMPONENTS
      + boundary[index:]
    )

  if (
    '"(5.1)": _EQUATION_51_COMPONENTS,'
    not in boundary
  ):
    boundary = replace_once(
      boundary,
      '_FIXED_COMPONENTS_BY_REFERENCE = {\n',
      (
        '_FIXED_COMPONENTS_BY_REFERENCE = {\n'
        '  "(5.1)": _EQUATION_51_COMPONENTS,\n'
      ),
      "fixed component dictionary",
    )

  rule_entries = (
    '  "Toda (5.1) circle higher homotopy zero": '
    '"circle_higher_homotopy_zero",\n'
    '  "Toda (5.1) diagonal identity group": '
    '"diagonal_identity_group",\n'
    '  "Toda (5.1) low-dimensional suspension isomorphism": '
    '"diagonal_suspension_isomorphism",\n'
  )

  if (
    '"Toda (5.1) circle higher homotopy zero"'
    not in boundary
  ):
    boundary = replace_once(
      boundary,
      '_FIXED_RULE_COMPONENT_KEYS = {\n',
      (
        '_FIXED_RULE_COMPONENT_KEYS = {\n'
        + rule_entries
      ),
      "fixed rule component dictionary",
    )

  locator_entries = (
    '  "Toda (5.1) circle higher homotopy zero": "(5.1)",\n'
    '  "Toda (5.1) diagonal identity group": "(5.1)",\n'
    '  "Toda (5.1) low-dimensional suspension isomorphism": "(5.1)",\n'
  )

  locator_anchor = (
    "_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME = {\n"
  )

  locator_index = boundary.find(
    locator_anchor
  )

  if locator_index < 0:
    raise RuntimeError(
      "fixed rule locator dictionary not found"
    )

  locator_tail = boundary[
    locator_index:
  ]

  if (
    '"Toda (5.1) circle higher homotopy zero"'
    not in locator_tail
  ):
    boundary = (
      boundary[:locator_index]
      + locator_anchor
      + locator_entries
      + boundary[
        locator_index
        + len(
          locator_anchor
        ):
      ]
    )

  BOUNDARY.write_text(
    boundary,
    encoding="utf-8",
    newline="\n",
  )

  bootstrap = BOOTSTRAP.read_text(
    encoding="utf-8-sig"
  )
  bootstrap = replace_phase49_first_three(
    bootstrap
  )
  BOOTSTRAP.write_text(
    bootstrap,
    encoding="utf-8",
    newline="\n",
  )

  renderer = RENDERER.read_text(
    encoding="utf-8-sig"
  )
  renderer = ensure_re_import(
    renderer
  )

  render_anchor = (
    "def render_toda_group_proof_narrative_markdown("
  )
  render_index = renderer.find(
    render_anchor
  )

  if render_index < 0:
    raise RuntimeError(
      "public render function not found"
    )

  if (
    "def _phase159_number_public_map_property_statement("
    not in renderer
  ):
    renderer = (
      renderer[:render_index]
      + NUMBERING_HELPER.rstrip()
      + "\n\n\n"
      + renderer[render_index:]
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

  OLD_R16A_TEST.write_text(
    (
      "from toda_calculation_facade import (\n"
      "  build_standard_toda_report,\n"
      ")\n"
      "from toda_group_proof_narrative_renderer import (\n"
      "  render_toda_group_proof_narrative_markdown,\n"
      ")\n"
      "from toda_group_proof_presentation import (\n"
      "  build_toda_group_proof_presentation,\n"
      ")\n"
      "from toda_group_result_proof_replay import (\n"
      "  build_toda_group_result_proof_replay,\n"
      ")\n\n\n"
      "def test_phase159_r1_6a_foundational_reference_is_superseded_by_toda_51():\n"
      "  report = build_standard_toda_report(n=2, k=1)\n"
      "  group_result = report.candidates[0].source_candidate.group_result\n"
      "  replay = build_toda_group_result_proof_replay(\n"
      "    group_result,\n"
      "    max_depth=2,\n"
      "  )\n"
      "  presentation = build_toda_group_proof_presentation(replay)\n"
      "  rendered = render_toda_group_proof_narrative_markdown(presentation)\n\n"
      "  assert \"[F1]\" not in rendered\n"
      "  assert \"[F2]\" not in rendered\n"
      "  assert \"[F3]\" not in rendered\n"
      "  assert \"**[R1] (5.1).**\" in rendered\n"
    ),
    encoding="utf-8",
    newline="\n",
  )

  NEW_TEST.write_text(
    TEST_CONTENT,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159-R1-6b applied."
  )
  print(
    "Backup:",
    backup_dir,
  )
  print(
    "Toda (5.1) is now the public literature attribution."
  )
  print(
    "Map-property equation tags now cover the full statement."
  )


if __name__ == "__main__":
  main()
