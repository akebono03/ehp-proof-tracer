from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]

DEPENDENCY_PATH = ROOT / "toda_proof_dependency.py"
BOUNDARY_PATH = ROOT / "toda_literature_statement_boundary.py"
BOOTSTRAP_PATH = ROOT / "toda_upstream_bootstrap.py"
CONTRIBUTION_PATH = (
  ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
REFERENCES_PATH = (
  ROOT
  / "toda_group_proof_narrative_references.py"
)
TEST_PATH = (
  ROOT
  / "tests"
  / "test_phase159_pi4_3_repair2g_reference_policy.py"
)


TEST_TEXT = 'from homotopy_groups import (\n  TodaPrimaryGroup,\n)\nfrom low_dimensional_facts import (\n  pi_4_5_zero_fact,\n  pi_5_5_free_cyclic_fact,\n)\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_narrative_references import (\n  extract_toda_group_proof_step_literature_reference,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\nfrom toda_literature_statement_boundary import (\n  TodaLiteratureStatementClassification,\n  classify_toda_literature_statement_step,\n)\nfrom toda_proof_dependency import (\n  TodaProofDependencyRole,\n  classify_toda_proof_step_role,\n)\nfrom toda_rules import (\n  TodaDeltaImageFreeCyclicStatement,\n  TodaDeltaImageUpToSignStatement,\n  TodaSuspensionKernelFreeCyclicStatement,\n)\nfrom toda_upstream_bootstrap import (\n  _build_phase49_result,\n  _build_phase50_result,\n)\n\n\ndef _group_data(\n  n: int,\n  k: int,\n  depth: int = 2,\n):\n  report = build_standard_toda_report(\n    n=n,\n    k=k,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=depth,\n  )\n  raw = build_toda_group_proof_presentation(\n    replay\n  )\n  closure = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      raw\n    )\n  )\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      raw\n    )\n  )\n\n  return (\n    raw,\n    closure,\n    rendered,\n  )\n\n\ndef _reference_section(\n  rendered: str,\n) -> str:\n  marker = "## 使用する結果"\n  assert marker in rendered\n  start = rendered.index(\n    marker\n  )\n  end = rendered.index(\n    "---",\n    start,\n  )\n  return rendered[\n    start:end\n  ]\n\n\ndef test_phase159_repair2g_pi4_map_image_and_kernel_are_map_properties():\n  phase50 = _build_phase50_result()\n\n  image_step = next(\n    step\n    for step in phase50[\n      "result"\n    ].steps\n    if isinstance(\n      step.conclusion,\n      (\n        TodaDeltaImageFreeCyclicStatement,\n        TodaDeltaImageUpToSignStatement,\n      ),\n    )\n  )\n  kernel_step = next(\n    step\n    for step in phase50[\n      "result"\n    ].steps\n    if isinstance(\n      step.conclusion,\n      TodaSuspensionKernelFreeCyclicStatement,\n    )\n  )\n\n  assert (\n    classify_toda_proof_step_role(\n      image_step\n    )\n    is TodaProofDependencyRole.MAP_PROPERTY\n  )\n  assert (\n    classify_toda_proof_step_role(\n      kernel_step\n    )\n    is TodaProofDependencyRole.MAP_PROPERTY\n  )\n\n\ndef test_phase159_repair2g_phase50_fixed_sources_have_expected_boundaries():\n  phase50 = _build_phase50_result()\n\n  pi5_step = next(\n    step\n    for step in phase50[\n      "result"\n    ].steps\n    if step.conclusion\n    == pi_5_5_free_cyclic_fact()\n  )\n  pi4_zero_step = next(\n    step\n    for step in phase50[\n      "result"\n    ].steps\n    if step.conclusion\n    == pi_4_5_zero_fact()\n  )\n  delta_step = next(\n    step\n    for step in phase50[\n      "result"\n    ].steps\n    if isinstance(\n      step.conclusion,\n      TodaDeltaImageUpToSignStatement,\n    )\n  )\n\n  for step in (\n    pi5_step,\n    pi4_zero_step,\n  ):\n    boundary = (\n      classify_toda_literature_statement_step(\n        step\n      )\n    )\n    reference = (\n      extract_toda_group_proof_step_literature_reference(\n        step\n      )\n    )\n\n    assert boundary is not None\n    assert (\n      boundary.classification\n      is TodaLiteratureStatementClassification.FIXED_STATEMENT\n    )\n    assert boundary.reference_locator == "(5.1)"\n    assert (\n      boundary.component_key\n      == "basic_sphere_group_relations"\n    )\n    assert reference is not None\n    assert reference.locator == "(5.1)"\n\n  delta_boundary = (\n    classify_toda_literature_statement_step(\n      delta_step\n    )\n  )\n\n  assert delta_boundary is not None\n  assert (\n    delta_boundary.classification\n    is TodaLiteratureStatementClassification.FIXED_STATEMENT\n  )\n  assert (\n    delta_boundary.reference_locator\n    == "Proposition 5.1"\n  )\n  assert (\n    delta_boundary.component_key\n    == "delta_iota5_relation"\n  )\n\n\ndef test_phase159_repair2g_phase49_keeps_given_contract_with_51_metadata():\n  phase49 = _build_phase49_result()\n\n  assert all(\n    step.rule.value == "given"\n    for step in phase49[\n      "premise_steps"\n    ]\n  )\n\n  fixed_51_steps = tuple(\n    step\n    for step in phase49[\n      "premise_steps"\n    ]\n    if (\n      extract_toda_group_proof_step_literature_reference(\n        step\n      )\n      is not None\n      and (\n        extract_toda_group_proof_step_literature_reference(\n          step\n        ).locator\n        == "(5.1)"\n      )\n    )\n  )\n\n  assert len(\n    fixed_51_steps\n  ) == 2\n\n\ndef test_phase159_repair2g_pi4_depth2_closure_reaches_delta_reference_sources():\n  _, closure, _ = _group_data(\n    3,\n    1,\n  )\n\n  conclusions = tuple(\n    node.proof_step.conclusion\n    for node in closure.nodes\n  )\n\n  assert any(\n    isinstance(\n      conclusion,\n      (\n        TodaDeltaImageFreeCyclicStatement,\n        TodaDeltaImageUpToSignStatement,\n      ),\n    )\n    for conclusion in conclusions\n  )\n  assert any(\n    isinstance(\n      conclusion,\n      TodaSuspensionKernelFreeCyclicStatement,\n    )\n    for conclusion in conclusions\n  )\n  assert any(\n    isinstance(\n      conclusion,\n      TodaDeltaImageUpToSignStatement,\n    )\n    for conclusion in conclusions\n  )\n  assert (\n    pi_5_5_free_cyclic_fact()\n    in conclusions\n  )\n  assert (\n    pi_4_5_zero_fact()\n    in conclusions\n  )\n\n\ndef test_phase159_repair2g_pi4_public_reference_policy_is_51_then_prop51():\n  _, _, rendered = _group_data(\n    3,\n    1,\n  )\n  reference = _reference_section(\n    rendered\n  )\n\n  assert "**[R1] (5.1).**" in reference\n  assert (\n    "**[R2] Proposition 5.1.**"\n    in reference\n  )\n\n  assert (\n    r"\\pi_i^1=0"\n    in reference\n  )\n  assert (\n    r"\\pi_i^n=0"\n    in reference\n  )\n  assert (\n    r"\\pi_n^n="\n    in reference\n  )\n  assert (\n    r"\\mathbb{Z}\\{\\iota_n\\}"\n    in reference\n  )\n\n  assert (\n    r"\\pi_{3}^{2}"\n    in reference\n  )\n  assert (\n    r"\\mathbb{Z}\\{\\eta_{2}\\}"\n    in reference\n  )\n  assert (\n    r"\\Delta"\n    in reference\n  )\n  assert (\n    r"\\iota_{5}"\n    in reference\n  )\n  assert (\n    r"2\\eta_{2}"\n    in reference\n  )\n\n  assert "Proposition 4.2" not in reference\n  assert r"\\xrightarrow" not in reference\n\n\ndef test_phase159_repair2g_pi3_keeps_single_51_reference_policy():\n  _, _, rendered = _group_data(\n    2,\n    1,\n  )\n  reference = _reference_section(\n    rendered\n  )\n\n  assert "**[R1] (5.1).**" in reference\n  assert "Proposition 5.1" not in reference\n  assert (\n    reference.count(\n      "**[R"\n    )\n    == 1\n  )\n\n\ndef test_phase159_repair2g_ehp_exactness_is_not_a_reference():\n  _, _, rendered = _group_data(\n    3,\n    1,\n  )\n  reference = _reference_section(\n    rendered\n  )\n\n  assert "Proposition 4.2" not in reference\n  assert "EHP" not in reference\n  assert "完全" not in reference\n'


def replace_once(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = text.count(
    old
  )

  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one match, "
      f"found {count}"
    )

  return text.replace(
    old,
    new,
    1,
  )


def function_span(
  source: str,
  function_name: str,
) -> tuple[int, int]:
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
      f"{function_name}: function not found"
    )

  match = re.search(
    r"\n(?=def [A-Za-z0-9_]+\()",
    source[
      start + 1:
    ],
  )

  if match is None:
    return (
      start,
      len(
        source
      ),
    )

  end = (
    start
    + 1
    + match.start()
    + 1
  )

  return (
    start,
    end,
  )


def replace_in_function(
  source: str,
  function_name: str,
  old: str,
  new: str,
  label: str,
) -> str:
  start, end = function_span(
    source,
    function_name,
  )
  body = source[
    start:end
  ]

  body = replace_once(
    body,
    old,
    new,
    label,
  )

  return (
    source[
      :start
    ]
    + body
    + source[
      end:
    ]
  )


def patch_dependency() -> None:
  source = DEPENDENCY_PATH.read_text(
    encoding="utf-8"
  )

  if (
    "  TodaDeltaImageFreeCyclicStatement,\n"
    not in source
  ):
    source = replace_once(
      source,
      (
        "from toda_rules import (\n"
        "  TodaSuspensionInjectiveStatement,\n"
      ),
      (
        "from toda_rules import (\n"
        "  TodaDeltaImageFreeCyclicStatement,\n"
        "  TodaSuspensionInjectiveStatement,\n"
        "  TodaSuspensionKernelFreeCyclicStatement,\n"
      ),
      "dependency toda_rules import",
    )

  classify_start, classify_end = function_span(
    source,
    "classify_toda_proof_step_role",
  )
  classify_source = source[
    classify_start:classify_end
  ]

  if (
    "      TodaDeltaImageFreeCyclicStatement,\n"
    not in classify_source
  ):
    source = replace_in_function(
      source,
      "classify_toda_proof_step_role",
      '''    (
      TodaDeltaImageUpToSignStatement,
      TodaDeltaInjectiveStatement,
''',
      '''    (
      TodaDeltaImageFreeCyclicStatement,
      TodaDeltaImageUpToSignStatement,
      TodaDeltaInjectiveStatement,
''',
      "Delta image MAP_PROPERTY classification",
    )

  classify_start, classify_end = function_span(
    source,
    "classify_toda_proof_step_role",
  )
  classify_source = source[
    classify_start:classify_end
  ]

  if (
    "      TodaSuspensionKernelFreeCyclicStatement,\n"
    not in classify_source
  ):
    source = replace_in_function(
      source,
      "classify_toda_proof_step_role",
      '''      TodaSuspensionInjectiveStatement,
      TodaSuspensionSurjectiveStatement,
''',
      '''      TodaSuspensionInjectiveStatement,
      TodaSuspensionKernelFreeCyclicStatement,
      TodaSuspensionSurjectiveStatement,
''',
      "suspension kernel MAP_PROPERTY classification",
    )

  DEPENDENCY_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )


def patch_boundary() -> None:
  source = BOUNDARY_PATH.read_text(
    encoding="utf-8"
  )

  if "_EQUATION_51_COMPONENTS" not in source:
    anchor = (
      "\n\n_PROPOSITION_22_COMPONENTS = (\n"
    )
    addition = r'''

_EQUATION_51_COMPONENTS = (
  TodaFixedStatementComponent(
    reference_locator="(5.1)",
    component_key="basic_sphere_group_relations",
    statement_role=TodaLiteratureStatementRole.GROUP_STRUCTURE,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
)
'''
    source = replace_once(
      source,
      anchor,
      addition
      + anchor,
      "(5.1) fixed component",
    )

  if (
    '  "(5.1)": _EQUATION_51_COMPONENTS,\n'
    not in source
  ):
    source = replace_once(
      source,
      (
        '_FIXED_COMPONENTS_BY_REFERENCE = {\n'
        '  "Proposition 2.2": '
        '_PROPOSITION_22_COMPONENTS,\n'
      ),
      (
        '_FIXED_COMPONENTS_BY_REFERENCE = {\n'
        '  "(5.1)": _EQUATION_51_COMPONENTS,\n'
        '  "Proposition 2.2": '
        '_PROPOSITION_22_COMPONENTS,\n'
      ),
      "(5.1) fixed reference catalog",
    )

  fixed_mapping_anchor = (
    '  "Toda Prop.2.2 right formula": '
    '"hopf_right_composition_formula",\n'
  )
  fixed_mapping_addition = (
    '  "Toda (5.1) below-diagonal zero": '
    '"basic_sphere_group_relations",\n'
    '  "Toda (5.1) diagonal free cyclic": '
    '"basic_sphere_group_relations",\n'
    '  "Toda Proposition 5.1 pi_3^2 group relation": '
    '"pi3_2_group_relation",\n'
    '  "Toda Proposition 5.1 Delta iota_5": '
    '"delta_iota5_relation",\n'
  )

  fixed_section_start = source.find(
    "_FIXED_RULE_COMPONENT_KEYS"
  )
  fixed_section_end = source.find(
    "_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME",
    fixed_section_start,
  )

  if (
    '"Toda (5.1) below-diagonal zero"'
    not in source[
      fixed_section_start:fixed_section_end
    ]
  ):
    source = replace_once(
      source,
      fixed_mapping_anchor,
      fixed_mapping_addition
      + fixed_mapping_anchor,
      "fixed rule component mappings",
    )

  locator_anchor = (
    '  "Toda Prop.2.2 right formula": '
    '"Proposition 2.2",\n'
  )
  locator_addition = (
    '  "Toda (5.1) below-diagonal zero": "(5.1)",\n'
    '  "Toda (5.1) diagonal free cyclic": "(5.1)",\n'
    '  "Toda Proposition 5.1 pi_3^2 group relation": '
    '"Proposition 5.1",\n'
    '  "Toda Proposition 5.1 Delta iota_5": '
    '"Proposition 5.1",\n'
  )

  locator_section_start = source.find(
    "_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME"
  )

  if (
    source.find(
      '"Toda (5.1) below-diagonal zero"',
      locator_section_start,
    )
    < 0
  ):
    source = replace_once(
      source,
      locator_anchor,
      locator_addition
      + locator_anchor,
      "fixed rule locator mappings",
    )

  BOUNDARY_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )


def _patch_given_fact_metadata_in_function(
  source: str,
  function_name: str,
  conclusion_marker: str,
  rule_name: str,
  locator: str,
  label: str,
) -> str:
  start, end = function_span(
    source,
    function_name,
  )
  body = source[
    start:end
  ]

  marker_index = body.find(
    conclusion_marker
  )
  if marker_index < 0:
    raise RuntimeError(
      f"{label}: conclusion marker not found: "
      f"{conclusion_marker!r}"
    )
  if body.find(
    conclusion_marker,
    marker_index + 1,
  ) >= 0:
    raise RuntimeError(
      f"{label}: conclusion marker is not unique"
    )

  proof_step_start = body.rfind(
    "    ProofStep(",
    0,
    marker_index,
  )
  if proof_step_start < 0:
    raise RuntimeError(
      f"{label}: enclosing ProofStep start not found"
    )

  next_proof_step = body.find(
    "    ProofStep(",
    marker_index + len(
      conclusion_marker
    ),
  )
  search_end = (
    len(body)
    if next_proof_step < 0
    else next_proof_step
  )
  proof_step_end = body.rfind(
    "    ),",
    proof_step_start,
    search_end,
  )
  if proof_step_end < 0:
    raise RuntimeError(
      f"{label}: enclosing ProofStep end not found"
    )
  proof_step_end += len(
    "    ),"
  )

  block = body[
    proof_step_start:proof_step_end
  ]

  if "inference_rule=" in block:
    return source

  given_line = "      rule=ProofRule.GIVEN,\n"
  if block.count(
    given_line
  ) != 1:
    raise RuntimeError(
      f"{label}: expected one GIVEN rule in enclosing "
      f"ProofStep, found {block.count(given_line)}\n"
      + block
    )

  metadata = (
    given_line
    + "      inference_rule=(\n"
    + "        _toda_fixed_reference_metadata_rule(\n"
    + "          " + repr(rule_name) + ",\n"
    + "          " + repr(locator) + ",\n"
    + "        )\n"
    + "      ),\n"
  )
  block = block.replace(
    given_line,
    metadata,
    1,
  )
  body = (
    body[:proof_step_start]
    + block
    + body[proof_step_end:]
  )
  return (
    source[:start]
    + body
    + source[end:]
  )


def patch_bootstrap() -> None:
  source = BOOTSTRAP_PATH.read_text(
    encoding="utf-8"
  )

  if (
    "def _toda_fixed_reference_metadata_rule("
    not in source
  ):
    helper = """


def _toda_fixed_reference_metadata_rule(
  name: str,
  locator: str,
) -> InferenceRule:
  return InferenceRule(
    name=name,
    description=(
      "Attach fixed Toda literature provenance "
      "to an existing GIVEN fact."
    ),
    literature_reference=LiteratureReference(
      label="Toda " + locator,
      author="H. Toda",
      title=(
        "Composition Methods in "
        "Homotopy Groups of Spheres"
      ),
      year=1962,
      locator=locator,
    ),
  )


"""
    source = replace_once(
      source,
      "\ndef _build_phase49_result():\n",
      helper
      + "def _build_phase49_result():\n",
      "fixed reference metadata helper",
    )

  source = _patch_given_fact_metadata_in_function(
    source,
    "_build_phase49_result",
    "conclusion=pi_2_1_zero_fact()",
    "Toda (5.1) below-diagonal zero",
    "(5.1)",
    "phase49 pi_2^1 (5.1) metadata",
  )
  source = _patch_given_fact_metadata_in_function(
    source,
    "_build_phase49_result",
    "conclusion=pi_3_3_free_cyclic_fact()",
    "Toda (5.1) diagonal free cyclic",
    "(5.1)",
    "phase49 pi_3^3 (5.1) metadata",
  )
  source = _patch_given_fact_metadata_in_function(
    source,
    "_build_phase50_result",
    "conclusion=pi_5_5_free_cyclic_fact()",
    "Toda (5.1) diagonal free cyclic",
    "(5.1)",
    "phase50 pi_5^5 (5.1) metadata",
  )
  source = _patch_given_fact_metadata_in_function(
    source,
    "_build_phase50_result",
    "conclusion=pi_4_5_zero_fact()",
    "Toda (5.1) below-diagonal zero",
    "(5.1)",
    "phase50 pi_4^5 (5.1) metadata",
  )
  source = _patch_given_fact_metadata_in_function(
    source,
    "_build_phase50_result",
    "lhs=pi_3_2,\n        rhs=FreeCyclicGroup(",
    "Toda Proposition 5.1 pi_3^2 group relation",
    "Proposition 5.1",
    "phase50 pi_3^2 Proposition 5.1 metadata",
  )

  required_direct_delta = (
    '"Toda Proposition 5.1 "\n'
    '        "Delta iota_5"'
  )

  if required_direct_delta not in source:
    raise RuntimeError(
      "Phase159 repair1 direct Proposition 5.1 "
      "Delta route is not present. "
      "Apply repair1/1a/1b first."
    )

  BOOTSTRAP_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

def patch_contribution_renderer() -> None:
  source = CONTRIBUTION_PATH.read_text(
    encoding="utf-8"
  )

  old = r'''def _phase157_r20_canonical_fixed_reference_line(
  proof_step: ProofStep,
  rendered_statement: str,
) -> str:
  boundary = (
    classify_toda_literature_statement_step(
      proof_step
    )
  )

  if (
    boundary is not None
    and boundary.component_key
    == "hopf_right_composition_formula"
  ):
    return (
      r"$H(\alpha\circ E\beta)"
      r" = H(\alpha)\circ E\beta$."
    )

  return rendered_statement
'''

  new = r'''def _phase157_r20_canonical_fixed_reference_line(
  proof_step: ProofStep,
  rendered_statement: str,
) -> str:
  boundary = (
    classify_toda_literature_statement_step(
      proof_step
    )
  )

  if (
    boundary is not None
    and boundary.reference_locator
    == "(5.1)"
    and boundary.component_key
    == "basic_sphere_group_relations"
  ):
    return (
      r"$\pi_i^1=0\ (i>1),\ "
      r"\pi_i^n=0\ (i<n),\ "
      r"\pi_n^n=\mathbb{Z}\{\iota_n\}$."
    )

  if (
    boundary is not None
    and boundary.component_key
    == "hopf_right_composition_formula"
  ):
    return (
      r"$H(\alpha\circ E\beta)"
      r" = H(\alpha)\circ E\beta$."
    )

  return rendered_statement
'''

  if new not in source:
    source = replace_once(
      source,
      old,
      new,
      "(5.1) canonical fixed reference line",
    )

  CONTRIBUTION_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )


def patch_references() -> None:
  source = REFERENCES_PATH.read_text(
    encoding="utf-8"
  )

  start, end = function_span(
    source,
    "filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary",
  )
  body = source[
    start:end
  ]

  old = '''  return tuple(
    retained_entries
  )
'''
  new = '''  retained_entries = sorted(
    retained_entries,
    key=lambda entry: (
      0
      if entry.reference.locator
      == "(5.1)"
      else 1
    ),
  )

  return tuple(
    replace(
      entry,
      number=number,
    )
    for number, entry in enumerate(
      retained_entries,
      start=1,
    )
  )
'''

  if new not in body:
    body = replace_once(
      body,
      old,
      new,
      "(5.1) foundational Reference ordering",
    )
    source = (
      source[
        :start
      ]
      + body
      + source[
        end:
      ]
    )

  REFERENCES_PATH.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )


def write_test() -> None:
  TEST_PATH.write_text(
    TEST_TEXT,
    encoding="utf-8",
    newline="\n",
  )


def main() -> int:
  patch_dependency()
  patch_boundary()
  patch_bootstrap()
  patch_contribution_renderer()
  patch_references()
  write_test()

  print(
    "Phase 159 pi_4^3 repair2g applied."
  )
  print(
    "Changed: toda_proof_dependency.py"
  )
  print(
    "Changed: toda_literature_statement_boundary.py"
  )
  print(
    "Changed: toda_upstream_bootstrap.py"
  )
  print(
    "Changed: "
    "toda_group_proof_narrative_contribution_renderer.py"
  )
  print(
    "Changed: "
    "toda_group_proof_narrative_references.py"
  )
  print(
    "Added: tests/"
    "test_phase159_pi4_3_repair2g_reference_policy.py"
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
