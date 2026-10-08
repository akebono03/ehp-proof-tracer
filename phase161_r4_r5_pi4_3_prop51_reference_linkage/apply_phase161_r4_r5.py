from pathlib import Path
import ast
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

TARGET = REPO_ROOT / "toda_prop56_zero_bootstrap.py"
TEST = (
  REPO_ROOT
  / "tests"
  / "test_phase161_r4_r5_pi4_3_prop51_reference_linkage.py"
)

BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"
OUTPUT_DIR = PACKAGE_DIR / "output"

NEW_HELPER = 'def _build_pi4_3_prop51_specialization_link_step(\n  pi4_3_step: ProofStep,\n  prop51_step: ProofStep,\n) -> ProofStep:\n  if not isinstance(\n    pi4_3_step,\n    ProofStep,\n  ):\n    raise TypeError(\n      "pi4_3_step must be a ProofStep"\n    )\n\n  if not isinstance(\n    prop51_step,\n    ProofStep,\n  ):\n    raise TypeError(\n      "prop51_step must be a ProofStep"\n    )\n\n  if not isinstance(\n    pi4_3_step.conclusion,\n    Relation,\n  ):\n    raise TypeError(\n      "pi4_3_step conclusion must be a Relation"\n    )\n\n  if (\n    pi4_3_step.conclusion.lhs\n    != TodaPrimaryGroup(\n      group_dimension=4,\n      sphere_dimension=3,\n    )\n  ):\n    raise ValueError(\n      "pi4_3_step must conclude a relation for pi_4^3"\n    )\n\n  if not isinstance(\n    prop51_step.conclusion,\n    TodaProp51FiniteDimensionalStatement,\n  ):\n    raise TypeError(\n      "prop51_step must conclude a "\n      "TodaProp51FiniteDimensionalStatement"\n    )\n\n  return ProofStep(\n    conclusion=pi4_3_step.conclusion,\n    premises=(\n      pi4_3_step,\n      prop51_step,\n    ),\n    rule=ProofRule.INFERENCE,\n    inference_rule=InferenceRule(\n      name=(\n        "Toda Proposition 5.1 "\n        "pi_4^3 specialization linkage"\n      ),\n      description=(\n        "Link the independently derived concrete "\n        "pi_4^3 group relation to the general "\n        "higher-eta group component of Toda "\n        "Proposition 5.1 without replacing the "\n        "existing pi_4^3 derivation."\n      ),\n    ),\n  )\n'
NEW_BUILD_PI4_2 = 'def _build_pi4_2_step(\n  pi4_3_step: ProofStep,\n  toda52_step: ProofStep,\n  prop51_step: ProofStep | None = None,\n) -> ProofStep:\n  eta_2 = HomotopyElement(\n    name="η₂",\n    dimension=2,\n    source=3,\n    target=2,\n    generator=GeneratorSymbol(\n      family="η",\n      index=2,\n    ),\n  )\n  eta_3 = HomotopyElement(\n    name="η₃",\n    dimension=3,\n    source=4,\n    target=3,\n    generator=GeneratorSymbol(\n      family="η",\n      index=3,\n    ),\n  )\n\n  expected = Relation(\n    lhs=TodaPrimaryGroup(\n      group_dimension=4,\n      sphere_dimension=2,\n    ),\n    rhs=FiniteCyclicGroup(\n      order=2,\n      generator=Composition(\n        left=eta_2,\n        right=eta_3,\n      ),\n    ),\n    relation_type=RelationType.EQUALITY,\n  )\n\n  effective_pi4_3_step = pi4_3_step\n\n  if prop51_step is not None:\n    effective_pi4_3_step = (\n      _build_pi4_3_prop51_specialization_link_step(\n        pi4_3_step,\n        prop51_step,\n      )\n    )\n\n  from toda_rules import (\n    toda_52_pi4_2_finite_cyclic_transport_inference_rule,\n  )\n\n  result = run_inference_until_stable_with_history(\n    toda_52_pi4_2_finite_cyclic_transport_inference_rule(),\n    (\n      effective_pi4_3_step,\n      toda52_step,\n    ),\n  )\n\n  return _find_unique_step(\n    result.steps,\n    lambda step: step.conclusion == expected,\n    "pi_4^2",\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\nfrom toda_prop56_zero_bootstrap import (\n  _build_pi4_3_prop51_specialization_link_step,\n  _build_prop51_step,\n)\nfrom toda_upstream_bootstrap import (\n  _build_phase50_result,\n)\n\n\ndef _phase161_r4_r5_pi4_2_rendered():\n  report = build_standard_toda_report(\n    n=2,\n    k=2,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return (\n    replay,\n    render_toda_group_proof_narrative_markdown(\n      presentation\n    ),\n  )\n\n\ndef test_phase161_r4_r5_pi4_3_prop51_link_is_structural():\n  phase50 = _build_phase50_result()\n  pi4_3_step = phase50[\n    "final_group_step"\n  ]\n  prop51_step = _build_prop51_step()\n\n  linked = (\n    _build_pi4_3_prop51_specialization_link_step(\n      pi4_3_step,\n      prop51_step,\n    )\n  )\n\n  assert linked.conclusion == pi4_3_step.conclusion\n  assert linked.premises == (\n    pi4_3_step,\n    prop51_step,\n  )\n  assert linked.inference_rule is not None\n  assert (\n    linked.inference_rule.name\n    == (\n      "Toda Proposition 5.1 "\n      "pi_4^3 specialization linkage"\n    )\n  )\n  assert (\n    linked.inference_rule.literature_reference\n    is None\n  )\n\n\ndef test_phase161_r4_r5_pi4_2_replay_contains_prop51_ancestry_for_pi4_3():\n  replay, _ = (\n    _phase161_r4_r5_pi4_2_rendered()\n  )\n\n  steps = replay.provenance_steps\n\n  link_step = next(\n    step\n    for step in steps\n    if (\n      step.inference_rule\n      is not None\n      and step.inference_rule.name\n      == (\n        "Toda Proposition 5.1 "\n        "pi_4^3 specialization linkage"\n      )\n    )\n  )\n\n  prop51_step = next(\n    step\n    for step in steps\n    if (\n      step.inference_rule\n      is not None\n      and (\n        step.inference_rule\n        .literature_reference\n        is not None\n      )\n      and (\n        step.inference_rule\n        .literature_reference\n        .locator\n        == "Proposition 5.1"\n      )\n      and step in link_step.premises\n    )\n  )\n\n  assert prop51_step in link_step.premises\n\n\ndef test_phase161_r4_r5_pi4_2_public_reference_links_prop51_to_pi4_3():\n  _, rendered = (\n    _phase161_r4_r5_pi4_2_rendered()\n  )\n  reference, body = rendered.split(\n    "---",\n    1,\n  )\n\n  assert "Proposition 5.1" in reference\n  assert "(5.2)" in reference\n\n  assert (\n    r"\\pi_{n + 1}^{n}"\n    in reference\n    or r"\\pi_{n+1}^{n}"\n    in reference\n  )\n  assert (\n    r"\\mathbb{Z}/2\\{\\eta_{n}\\}"\n    in reference\n  )\n\n  assert (\n    r"\\pi_{4}^{3} = "\n    r"\\mathbb{Z}/2\\{\\eta_{3}\\}"\n    in body\n  )\n\n  prop51_number = next(\n    number\n    for number in range(\n      1,\n      4,\n    )\n    if (\n      f"**[R{number}] Proposition 5.1.**"\n      in reference\n    )\n  )\n\n  pi4_3_paragraph = next(\n    paragraph\n    for paragraph in body.split(\n      "\\n\\n"\n    )\n    if (\n      r"\\pi_{4}^{3} = "\n      r"\\mathbb{Z}/2\\{\\eta_{3}\\}"\n      in paragraph\n    )\n  )\n\n  assert (\n    f"[R{prop51_number}]"\n    in pi4_3_paragraph\n  )\n\n  assert (\n    r"\\pi_{4}^{2} = "\n    r"\\mathbb{Z}/2\\{\\eta_{2}^{2}\\}"\n    in body\n  )\n  assert "□" in body\n'


def _functions(
  source: str,
):
  tree = ast.parse(
    source
  )

  return {
    node.name: node
    for node in tree.body
    if isinstance(
      node,
      ast.FunctionDef,
    )
  }


def _replace_function(
  source: str,
  function_name: str,
  replacement: str,
) -> str:
  functions = _functions(
    source
  )

  if function_name not in functions:
    raise RuntimeError(
      f"Missing function: {function_name}"
    )

  node = functions[
    function_name
  ]
  lines = source.splitlines(
    keepends=True
  )
  replacement_lines = [
    line + "\n"
    for line in replacement.rstrip(
      "\n"
    ).split(
      "\n"
    )
  ]

  return "".join(
    lines[
      :node.lineno - 1
    ]
    + replacement_lines
    + lines[
      node.end_lineno:
    ]
  )


def _insert_before_function(
  source: str,
  function_name: str,
  addition: str,
) -> str:
  functions = _functions(
    source
  )

  if function_name not in functions:
    raise RuntimeError(
      f"Missing insertion anchor: {function_name}"
    )

  node = functions[
    function_name
  ]
  lines = source.splitlines(
    keepends=True
  )
  addition_lines = [
    line + "\n"
    for line in (
      addition.rstrip(
        "\n"
      )
      + "\n\n"
    ).split(
      "\n"
    )[
      :-1
    ]
  ]

  return "".join(
    lines[
      :node.lineno - 1
    ]
    + addition_lines
    + lines[
      node.lineno - 1:
    ]
  )


def _replace_build_zero_block(
  source: str,
) -> str:
  old = """  pi4_2_step = _build_pi4_2_step(
    pi4_3_step,
    core[
      "toda52_step"
    ],
  )

  prop51_step = _build_prop51_step()
"""

  new = """  prop51_step = _build_prop51_step()

  pi4_2_step = _build_pi4_2_step(
    pi4_3_step,
    core[
      "toda52_step"
    ],
    prop51_step=prop51_step,
  )
"""

  if old not in source:
    raise RuntimeError(
      "Expected build_toda_prop56_zero_argument_step "
      "pi4_2/prop51 block not found."
    )

  return source.replace(
    old,
    new,
    1,
  )


def _add_inference_rule_import(
  source: str,
) -> str:
  old = """from proof import (
  ProofRule,
  ProofStep,
"""

  new = """from proof import (
  InferenceRule,
  ProofRule,
  ProofStep,
"""

  if old not in source:
    if "  InferenceRule,\n" in source:
      return source

    raise RuntimeError(
      "Expected proof import block not found."
    )

  return source.replace(
    old,
    new,
    1,
  )


def _extract_function(
  source: str,
  function_name: str,
) -> str:
  functions = _functions(
    source
  )
  node = functions[
    function_name
  ]
  lines = source.splitlines()

  return "\n".join(
    lines[
      node.lineno - 1:
      node.end_lineno
    ]
  ) + "\n"


def _extract_import_block(
  source: str,
  module_name: str,
) -> str:
  tree = ast.parse(
    source
  )
  lines = source.splitlines()

  node = next(
    node
    for node in tree.body
    if (
      isinstance(
        node,
        ast.ImportFrom,
      )
      and node.module == module_name
    )
  )

  return "\n".join(
    lines[
      node.lineno - 1:
      node.end_lineno
    ]
  ) + "\n"


def main():
  source = TARGET.read_text(
    encoding="utf-8"
  )

  functions = _functions(
    source
  )

  for name in (
    "_build_pi4_2_step",
    "_build_prop51_step",
    "build_toda_prop56_zero_argument_step",
  ):
    if name not in functions:
      raise RuntimeError(
        f"Required function missing: {name}"
      )

  updated = _add_inference_rule_import(
    source
  )

  if (
    "_build_pi4_3_prop51_specialization_link_step"
    not in _functions(
      updated
    )
  ):
    updated = _insert_before_function(
      updated,
      "_build_pi4_2_step",
      NEW_HELPER,
    )

  updated = _replace_function(
    updated,
    "_build_pi4_2_step",
    NEW_BUILD_PI4_2,
  )

  updated = _replace_build_zero_block(
    updated
  )

  ast.parse(
    updated
  )

  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    TARGET,
    BACKUP_DIR / TARGET.name,
  )

  TARGET.write_text(
    updated,
    encoding="utf-8",
    newline="\n",
  )
  TEST.write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  (
    OUTPUT_DIR
    / "proof_import_after.py.txt"
  ).write_text(
    _extract_import_block(
      updated,
      "proof",
    ),
    encoding="utf-8",
    newline="\n",
  )

  for function_name in (
    "_build_pi4_3_prop51_specialization_link_step",
    "_build_pi4_2_step",
    "build_toda_prop56_zero_argument_step",
  ):
    (
      OUTPUT_DIR
      / (
        function_name
        + ".py.txt"
      )
    ).write_text(
      _extract_function(
        updated,
        function_name,
      ),
      encoding="utf-8",
      newline="\n",
    )

  (
    OUTPUT_DIR
    / "test_phase161_r4_r5_pi4_3_prop51_reference_linkage.py.txt"
  ).write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Updated:",
    TARGET,
  )
  print(
    "Wrote:",
    TEST,
  )
  print(
    "Full changed/new functions, import block, and test "
    "written to output/."
  )


if __name__ == "__main__":
  main()
