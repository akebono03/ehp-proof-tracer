from pathlib import Path
import ast
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

BOOTSTRAP = REPO_ROOT / "toda_prop56_zero_bootstrap.py"
BOUNDARY = REPO_ROOT / "toda_literature_statement_boundary.py"
TEST = (
  REPO_ROOT
  / "tests"
  / "test_phase161_r4_r5_pi4_3_prop51_reference_linkage.py"
)

BACKUP_DIR = PACKAGE_DIR / "backup_before_apply"
OUTPUT_DIR = PACKAGE_DIR / "output"


NEW_HELPER = r"""def _build_pi4_3_prop51_specialization_link_step(
  pi4_3_step: ProofStep,
  prop51_step: ProofStep,
) -> ProofStep:
  if not isinstance(
    pi4_3_step,
    ProofStep,
  ):
    raise TypeError(
      "pi4_3_step must be a ProofStep"
    )

  if not isinstance(
    prop51_step,
    ProofStep,
  ):
    raise TypeError(
      "prop51_step must be a ProofStep"
    )

  if not isinstance(
    pi4_3_step.conclusion,
    Relation,
  ):
    raise TypeError(
      "pi4_3_step conclusion must be a Relation"
    )

  if (
    pi4_3_step.conclusion.lhs
    != TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    )
  ):
    raise ValueError(
      "pi4_3_step must conclude a relation for pi_4^3"
    )

  if not isinstance(
    prop51_step.conclusion,
    TodaProp51FiniteDimensionalStatement,
  ):
    raise TypeError(
      "prop51_step must conclude a "
      "TodaProp51FiniteDimensionalStatement"
    )

  general_step = ProofStep(
    conclusion=(
      prop51_step
      .conclusion
      .higher_eta_group_relation
    ),
    premises=(
      prop51_step,
    ),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name=(
        "Toda Proposition 5.1 "
        "higher eta group relation"
      ),
      description=(
        "Expose the higher-eta group component "
        "of Toda Proposition 5.1 as a fixed "
        "general literature statement."
      ),
      literature_reference=LiteratureReference(
        label="Toda Proposition 5.1",
        locator="Proposition 5.1",
      ),
    ),
  )

  return ProofStep(
    conclusion=pi4_3_step.conclusion,
    premises=(
      pi4_3_step,
      general_step,
    ),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name=(
        "pi_4^3 Proposition 5.1 "
        "specialization linkage"
      ),
      description=(
        "Link the independently derived concrete "
        "pi_4^3 group relation to the general "
        "higher-eta group component of Toda "
        "Proposition 5.1 without replacing the "
        "existing pi_4^3 derivation."
      ),
    ),
  )
"""


TEST_SOURCE = r"""from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_prop56_zero_bootstrap import (
  _build_pi4_3_prop51_specialization_link_step,
  _build_prop51_step,
)
from toda_upstream_bootstrap import (
  _build_phase50_result,
)


def _phase161_r4_r5_pi4_2_data():
  report = build_standard_toda_report(
    n=2,
    k=2,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=3,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  return (
    replay,
    rendered,
  )


def test_phase161_r4_r5_pi4_3_prop51_link_is_structural():
  phase50 = _build_phase50_result()
  pi4_3_step = phase50[
    "final_group_step"
  ]
  prop51_step = _build_prop51_step()

  linked = (
    _build_pi4_3_prop51_specialization_link_step(
      pi4_3_step,
      prop51_step,
    )
  )

  assert linked.conclusion == pi4_3_step.conclusion
  assert linked.inference_rule is not None
  assert (
    linked.inference_rule.name
    == (
      "pi_4^3 Proposition 5.1 "
      "specialization linkage"
    )
  )
  assert (
    linked.inference_rule.literature_reference
    is None
  )

  assert len(
    linked.premises
  ) == 2

  general_step = linked.premises[
    1
  ]

  assert (
    general_step.conclusion
    == (
      prop51_step
      .conclusion
      .higher_eta_group_relation
    )
  )
  assert general_step.inference_rule is not None
  assert (
    general_step
    .inference_rule
    .literature_reference
    is not None
  )
  assert (
    general_step
    .inference_rule
    .literature_reference
    .locator
    == "Proposition 5.1"
  )


def test_phase161_r4_r5_pi4_2_replay_contains_general_prop51_component():
  replay, _ = (
    _phase161_r4_r5_pi4_2_data()
  )

  proof_steps = tuple(
    replay_step.proof_step
    for replay_step in replay.steps
  )

  link_step = next(
    step
    for step in proof_steps
    if (
      step.inference_rule
      is not None
      and step.inference_rule.name
      == (
        "pi_4^3 Proposition 5.1 "
        "specialization linkage"
      )
    )
  )

  general_step = next(
    step
    for step in link_step.premises
    if (
      step.inference_rule
      is not None
      and step.inference_rule.name
      == (
        "Toda Proposition 5.1 "
        "higher eta group relation"
      )
    )
  )

  assert (
    general_step
    .inference_rule
    .literature_reference
    .locator
    == "Proposition 5.1"
  )


def test_phase161_r4_r5_pi4_2_public_reference_is_general_prop51():
  _, rendered = (
    _phase161_r4_r5_pi4_2_data()
  )
  reference, body = rendered.split(
    "---",
    1,
  )

  assert "Proposition 5.1" in reference
  assert "(5.2)" in reference

  assert (
    r"\pi_{n + 1}^{n}"
    in reference
    or r"\pi_{n+1}^{n}"
    in reference
  )
  assert (
    r"\mathbb{Z}/2\{\eta_{n}\}"
    in reference
  )

  assert (
    r"\pi_{4}^{3} = "
    r"\mathbb{Z}/2\{\eta_{3}\}"
    not in reference
  )

  assert (
    r"\pi_{4}^{3} = "
    r"\mathbb{Z}/2\{\eta_{3}\}"
    in body
  )

  prop51_number = next(
    number
    for number in range(
      1,
      4,
    )
    if (
      f"**[R{number}] Proposition 5.1.**"
      in reference
    )
  )

  pi4_3_paragraph = next(
    paragraph
    for paragraph in body.split(
      "\n\n"
    )
    if (
      r"\pi_{4}^{3} = "
      r"\mathbb{Z}/2\{\eta_{3}\}"
      in paragraph
    )
  )

  assert (
    f"[R{prop51_number}]"
    in pi4_3_paragraph
  )

  assert (
    r"\pi_{4}^{2} = "
    r"\mathbb{Z}/2\{\eta_{2}^{2}\}"
    in body
  )
  assert "□" in body
"""


def functions(source: str):
    tree = ast.parse(source)
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }


def replace_function(
    source: str,
    function_name: str,
    replacement: str,
) -> str:
    fs = functions(source)
    if function_name not in fs:
        raise RuntimeError(
            f"Missing function: {function_name}"
        )
    node = fs[function_name]
    lines = source.splitlines(keepends=True)
    repl = [
        line + "\n"
        for line in replacement.rstrip("\n").split("\n")
    ]
    return "".join(
        lines[:node.lineno - 1]
        + repl
        + lines[node.end_lineno:]
    )


def add_literature_reference_import(source: str) -> str:
    old = """from proof import (
  InferenceRule,
  ProofRule,
"""
    new = """from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
"""
    if old in source:
        return source.replace(
            old,
            new,
            1,
        )
    if "  LiteratureReference,\n" in source:
        return source
    raise RuntimeError(
        "Expected proof import block not found."
    )


def add_boundary_component_mapping(source: str) -> str:
    anchor = (
        '  "Toda Proposition 5.1 finite-dimensional integration": None,\n'
    )
    addition = (
        '  "Toda Proposition 5.1 higher eta group relation": '
        '"higher_eta_group_relation",\n'
    )

    if addition in source:
        return source

    if anchor not in source:
        raise RuntimeError(
            "Expected Proposition 5.1 boundary anchor not found."
        )

    return source.replace(
        anchor,
        anchor + addition,
        1,
    )


def extract_function(
    source: str,
    function_name: str,
) -> str:
    node = functions(source)[function_name]
    lines = source.splitlines()
    return "\n".join(
        lines[node.lineno - 1:node.end_lineno]
    ) + "\n"


def extract_import_block(
    source: str,
    module_name: str,
) -> str:
    tree = ast.parse(source)
    lines = source.splitlines()
    node = next(
        node
        for node in tree.body
        if (
            isinstance(node, ast.ImportFrom)
            and node.module == module_name
        )
    )
    return "\n".join(
        lines[node.lineno - 1:node.end_lineno]
    ) + "\n"


def main():
    bootstrap_source = BOOTSTRAP.read_text(
        encoding="utf-8"
    )
    boundary_source = BOUNDARY.read_text(
        encoding="utf-8"
    )

    bootstrap_source = add_literature_reference_import(
        bootstrap_source
    )
    bootstrap_source = replace_function(
        bootstrap_source,
        "_build_pi4_3_prop51_specialization_link_step",
        NEW_HELPER,
    )
    boundary_source = add_boundary_component_mapping(
        boundary_source
    )

    ast.parse(bootstrap_source)
    ast.parse(boundary_source)
    ast.parse(TEST_SOURCE)

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )
    shutil.copy2(
        BOOTSTRAP,
        BACKUP_DIR / BOOTSTRAP.name,
    )
    shutil.copy2(
        BOUNDARY,
        BACKUP_DIR / BOUNDARY.name,
    )
    shutil.copy2(
        TEST,
        BACKUP_DIR / TEST.name,
    )

    BOOTSTRAP.write_text(
        bootstrap_source,
        encoding="utf-8",
        newline="\n",
    )
    BOUNDARY.write_text(
        boundary_source,
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
        extract_import_block(
            bootstrap_source,
            "proof",
        ),
        encoding="utf-8",
        newline="\n",
    )
    (
        OUTPUT_DIR
        / "_build_pi4_3_prop51_specialization_link_step.py.txt"
    ).write_text(
        extract_function(
            bootstrap_source,
            "_build_pi4_3_prop51_specialization_link_step",
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
    (
        OUTPUT_DIR
        / "boundary_mapping_addition.txt"
    ).write_text(
        (
            '"Toda Proposition 5.1 higher eta group relation": '
            '"higher_eta_group_relation",\n'
        ),
        encoding="utf-8",
        newline="\n",
    )

    print("Updated:", BOOTSTRAP)
    print("Updated:", BOUNDARY)
    print("Updated:", TEST)
    print("Production change is limited to the general Prop.5.1 component linkage.")


if __name__ == "__main__":
    main()
