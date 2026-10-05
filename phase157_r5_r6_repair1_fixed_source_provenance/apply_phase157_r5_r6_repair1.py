
from __future__ import annotations

from pathlib import Path


BOUNDARY = Path("toda_literature_statement_boundary.py")
UPSTREAM = Path("toda_upstream_bootstrap.py")
R2_TEST = Path("tests/test_phase157_r2_literature_statement_boundary.py")
R56_TEST = Path("tests/test_phase157_r5_r6_53_bracket_definition_reference.py")
OUTPUT_DIR = Path("phase157_r5_r6_repair1_output")

SPECIALIZATION_RULE = (
  "Toda 5.3 nu-prime Lemma 5.2 bracket specialization"
)
DEFINITION_RULE = (
  "Toda (5.3) nu-prime bracket definition"
)

OLD_PROOF_IMPORT = '''from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
  run_inference_until_stable_with_history,
)
'''

NEW_PROOF_IMPORT = '''from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
  run_inference_until_stable_with_history,
)
'''

OLD_BRACKET_STEP = '''  bracket_membership_step = ProofStep(
    conclusion=TodaBracketMembershipStatement(
      element=nu_prime,
      bracket=TodaBracket(
        first=eta_3,
        second=Multiple(
          coefficient=2,
          expression=iota_4,
        ),
        third=eta_4,
        index=1,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )
'''

NEW_BRACKET_STEP = '''  bracket_membership_step = ProofStep(
    conclusion=TodaBracketMembershipStatement(
      element=nu_prime,
      bracket=TodaBracket(
        first=eta_3,
        second=Multiple(
          coefficient=2,
          expression=iota_4,
        ),
        third=eta_4,
        index=1,
      ),
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name=(
        "Toda (5.3) nu-prime bracket definition"
      ),
      description=(
        "Record the fixed Toda (5.3) definition "
        "nu-prime in "
        "{eta_3, 2 iota_4, eta_4}_1."
      ),
      literature_reference=LiteratureReference(
        label="Toda (5.3)",
        author="H. Toda",
        title=(
          "Composition Methods in "
          "Homotopy Groups of Spheres"
        ),
        year=1962,
        locator="(5.3)",
      ),
    ),
  )
'''

FIXED_SPECIALIZATION_MAPPING = '''  "Toda 5.3 nu-prime Lemma 5.2 bracket specialization": (
    "nu_prime_bracket_definition"
  ),
'''

FIXED_SPECIALIZATION_LOCATOR = '''  "Toda 5.3 nu-prime Lemma 5.2 bracket specialization": "(5.3)",
'''

MEMBERSHIP_MAPPING_ANCHOR = '''  "Toda 5.3 nu-prime Lemma 5.2 membership specialization": (
    "nu_prime_membership"
  ),
'''

DEFINITION_MAPPING = '''  "Toda (5.3) nu-prime bracket definition": (
    "nu_prime_bracket_definition"
  ),
'''

MEMBERSHIP_LOCATOR_ANCHOR = '''  "Toda 5.3 nu-prime Lemma 5.2 membership specialization": "(5.3)",
'''

DEFINITION_LOCATOR = '''  "Toda (5.3) nu-prime bracket definition": "(5.3)",
'''

OLD_R2_EXPECTED = '''  assert tuple(
    component.component_key
    for component in components
  ) == (
    "nu_prime_membership",
    "nu_prime_hopf_relation",
    "nu_prime_double_relation",
  )
'''

NEW_R2_EXPECTED = '''  assert tuple(
    component.component_key
    for component in components
  ) == (
    "nu_prime_bracket_definition",
    "nu_prime_membership",
    "nu_prime_hopf_relation",
    "nu_prime_double_relation",
  )
'''

R56_TEST_TEXT = '''from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
  get_toda_fixed_statement_components,
)
from toda_rules import (
  TodaBracketMembershipStatement,
)


def _pi6_3_presentation():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[
      0
    ]
    .source_candidate
    .group_result
  )
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )
  return build_toda_group_proof_presentation(
    replay
  )


def test_phase157_r5_r6_53_catalog_contains_bracket_definition_component():
  components = get_toda_fixed_statement_components(
    "(5.3)"
  )

  assert tuple(
    component.component_key
    for component in components
  ) == (
    "nu_prime_bracket_definition",
    "nu_prime_membership",
    "nu_prime_hopf_relation",
    "nu_prime_double_relation",
  )


def test_phase157_r5_r6_53_bracket_definition_source_is_fixed_statement():
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      _pi6_3_presentation()
    )
  )

  bracket_step = next(
    node.proof_step
    for node in closure.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaBracketMembershipStatement,
    )
  )

  boundary = (
    classify_toda_literature_statement_step(
      bracket_step
    )
  )

  assert boundary is not None
  assert (
    boundary.classification
    == TodaLiteratureStatementClassification.FIXED_STATEMENT
  )
  assert boundary.reference_locator == "(5.3)"
  assert (
    boundary.component_key
    == "nu_prime_bracket_definition"
  )


def test_phase157_r5_r6_53_specialization_remains_proof_internal():
  presentation = _pi6_3_presentation()

  specialization_step = next(
    node.proof_step
    for node in presentation.nodes
    if (
      node.proof_step.inference_rule is not None
      and node.proof_step.inference_rule.name
      == (
        "Toda 5.3 nu-prime Lemma 5.2 "
        "bracket specialization"
      )
    )
  )

  boundary = (
    classify_toda_literature_statement_step(
      specialization_step
    )
  )

  assert boundary is not None
  assert (
    boundary.classification
    == TodaLiteratureStatementClassification.PROOF_INTERNAL
  )


def test_phase157_r5_r6_pi6_reference_53_displays_bracket_definition():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _pi6_3_presentation()
    )
  )
  reference_part = rendered.split(
    "まず",
    1,
  )[0]

  assert "**[R1] (5.3).**" in reference_part
  assert (
    r"\\nu' \\in \\{\\eta_{3},2\\iota_{4},\\eta_{4}\\}_{1}"
    in reference_part
  )


def test_phase157_r5_r6_pi6_lemma52_application_remains_in_proof_body():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _pi6_3_presentation()
    )
  )

  assert "Lemma 5.2 を適用" in rendered
'''


def replace_once(
  text: str,
  old: str,
  new: str,
  description: str,
) -> str:
  count = text.count(
    old
  )
  if count != 1:
    raise SystemExit(
      description
      + ": expected exactly one match, found "
      + str(
        count
      )
    )
  return text.replace(
    old,
    new,
    1,
  )


def extract_function(
  text: str,
  function_name: str,
) -> str:
  marker = "def " + function_name + "("
  start = text.find(
    marker
  )
  if start < 0:
    raise SystemExit(
      "function not found: "
      + function_name
    )

  next_function = text.find(
    "\ndef ",
    start + len(
      marker
    ),
  )
  if next_function < 0:
    return text[
      start:
    ]

  return text[
    start:
    next_function + 1
  ]


def extract_import_block(
  text: str,
  module_name: str,
) -> str:
  marker = (
    "from "
    + module_name
    + " import (\n"
  )
  start = text.find(
    marker
  )
  if start < 0:
    raise SystemExit(
      "import block not found: "
      + module_name
    )
  end = text.find(
    ")\n",
    start,
  )
  if end < 0:
    raise SystemExit(
      "import block end not found: "
      + module_name
    )
  return text[
    start:
    end + 2
  ]


def main() -> None:
  for path in (
    BOUNDARY,
    UPSTREAM,
    R2_TEST,
  ):
    if not path.exists():
      raise SystemExit(
        "target not found: "
        + str(
          path
        )
      )

  boundary_text = BOUNDARY.read_text(
    encoding="utf-8"
  )

  if FIXED_SPECIALIZATION_MAPPING in boundary_text:
    boundary_text = boundary_text.replace(
      FIXED_SPECIALIZATION_MAPPING,
      "",
      1,
    )

  if FIXED_SPECIALIZATION_LOCATOR in boundary_text:
    boundary_text = boundary_text.replace(
      FIXED_SPECIALIZATION_LOCATOR,
      "",
      1,
    )

  if DEFINITION_MAPPING not in boundary_text:
    boundary_text = replace_once(
      boundary_text,
      MEMBERSHIP_MAPPING_ANCHOR,
      (
        DEFINITION_MAPPING
        + MEMBERSHIP_MAPPING_ANCHOR
      ),
      "definition fixed mapping",
    )

  if DEFINITION_LOCATOR not in boundary_text:
    boundary_text = replace_once(
      boundary_text,
      MEMBERSHIP_LOCATOR_ANCHOR,
      (
        DEFINITION_LOCATOR
        + MEMBERSHIP_LOCATOR_ANCHOR
      ),
      "definition locator mapping",
    )

  BOUNDARY.write_text(
    boundary_text,
    encoding="utf-8",
    newline="\n",
  )

  upstream_text = UPSTREAM.read_text(
    encoding="utf-8"
  )

  if (
    "  InferenceRule,\n"
    not in upstream_text
    or "  LiteratureReference,\n"
    not in upstream_text
  ):
    upstream_text = replace_once(
      upstream_text,
      OLD_PROOF_IMPORT,
      NEW_PROOF_IMPORT,
      "proof import block",
    )

  if DEFINITION_RULE not in upstream_text:
    upstream_text = replace_once(
      upstream_text,
      OLD_BRACKET_STEP,
      NEW_BRACKET_STEP,
      "bracket membership source step",
    )

  UPSTREAM.write_text(
    upstream_text,
    encoding="utf-8",
    newline="\n",
  )

  r2_text = R2_TEST.read_text(
    encoding="utf-8"
  )

  if (
    '"nu_prime_bracket_definition",'
    not in r2_text[
      r2_text.find(
        "def test_phase157_r2_equation53_inventory_has_no_group_order_policy"
      ):
      r2_text.find(
        "\ndef ",
        r2_text.find(
          "def test_phase157_r2_equation53_inventory_has_no_group_order_policy"
        ) + 1,
      )
    ]
  ):
    r2_text = replace_once(
      r2_text,
      OLD_R2_EXPECTED,
      NEW_R2_EXPECTED,
      "R2 (5.3) inventory test",
    )

  R2_TEST.write_text(
    r2_text,
    encoding="utf-8",
    newline="\n",
  )

  R56_TEST.write_text(
    R56_TEST_TEXT,
    encoding="utf-8",
    newline="\n",
  )

  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  (
    OUTPUT_DIR
    / "toda_upstream_bootstrap_import_after.txt"
  ).write_text(
    extract_import_block(
      upstream_text,
      "proof",
    ),
    encoding="utf-8",
    newline="\n",
  )

  (
    OUTPUT_DIR
    / "build_toda_53_nu_prime_steps_after.txt"
  ).write_text(
    extract_function(
      upstream_text,
      "build_toda_53_nu_prime_steps",
    ),
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R5-R6 repair1 applied."
  )
  print(
    "Bracket definition source now carries Toda (5.3) provenance."
  )
  print(
    "Bracket specialization restored to PROOF_INTERNAL."
  )
  print(
    "Updated R2 inventory contract to four (5.3) fixed components."
  )
  print(
    "Production renderer changes: none"
  )


if __name__ == "__main__":
  main()
