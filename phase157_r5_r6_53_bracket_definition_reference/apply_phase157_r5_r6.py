
from __future__ import annotations

from pathlib import Path

BOUNDARY = Path("toda_literature_statement_boundary.py")
TEST = Path("tests/test_phase157_r5_r6_53_bracket_definition_reference.py")

OLD_COMPONENT_ANCHOR = '''_EQUATION_53_COMPONENTS = (
  TodaFixedStatementComponent(
    reference_locator="(5.3)",
    component_key="nu_prime_membership",
'''

NEW_COMPONENT_ANCHOR = '''_EQUATION_53_COMPONENTS = (
  TodaFixedStatementComponent(
    reference_locator="(5.3)",
    component_key="nu_prime_bracket_definition",
    statement_role=TodaLiteratureStatementRole.MEMBERSHIP,
    order=None,
    range_text=None,
    range_is_explicit_in_current_aggregate=True,
  ),
  TodaFixedStatementComponent(
    reference_locator="(5.3)",
    component_key="nu_prime_membership",
'''

OLD_RULE_ANCHOR = '''  "Toda 5.3 nu-prime Lemma 5.2 membership specialization": (
    "nu_prime_membership"
  ),
'''

NEW_RULE_ANCHOR = '''  "Toda 5.3 nu-prime Lemma 5.2 bracket specialization": (
    "nu_prime_bracket_definition"
  ),
  "Toda 5.3 nu-prime Lemma 5.2 membership specialization": (
    "nu_prime_membership"
  ),
'''

OLD_LOCATOR_ANCHOR = '''  "Toda 5.3 nu-prime Lemma 5.2 membership specialization": "(5.3)",
'''

NEW_LOCATOR_ANCHOR = '''  "Toda 5.3 nu-prime Lemma 5.2 bracket specialization": "(5.3)",
  "Toda 5.3 nu-prime Lemma 5.2 membership specialization": "(5.3)",
'''

TEST_TEXT = '''from toda_calculation_facade import (
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
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
  get_toda_fixed_statement_components,
)
from toda_rules import (
  Toda53NuPrimeBracketSpecializationStatement,
)


def _pi6_3_presentation():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
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


def test_phase157_r5_r6_53_bracket_specialization_is_fixed_statement():
  presentation = _pi6_3_presentation()

  specialization_step = next(
    node.proof_step
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      Toda53NuPrimeBracketSpecializationStatement,
    )
  )

  boundary = classify_toda_literature_statement_step(
    specialization_step
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


def test_phase157_r5_r6_pi6_reference_53_displays_bracket_definition():
  rendered = render_toda_group_proof_narrative_markdown(
    _pi6_3_presentation()
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
  rendered = render_toda_group_proof_narrative_markdown(
    _pi6_3_presentation()
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
      + ": expected exactly one anchor, found "
      + str(
        count
      )
    )

  return text.replace(
    old,
    new,
    1,
  )


def main() -> None:
  if not BOUNDARY.exists():
    raise SystemExit(
      "target not found: "
      + str(
        BOUNDARY
      )
    )

  text = BOUNDARY.read_text(
    encoding="utf-8"
  )

  if 'component_key="nu_prime_bracket_definition"' not in text:
    text = replace_once(
      text,
      OLD_COMPONENT_ANCHOR,
      NEW_COMPONENT_ANCHOR,
      "(5.3) component catalog",
    )

  rule_name = (
    "Toda 5.3 nu-prime Lemma 5.2 bracket specialization"
  )

  if rule_name not in text:
    text = replace_once(
      text,
      OLD_RULE_ANCHOR,
      NEW_RULE_ANCHOR,
      "fixed rule component mapping",
    )
    text = replace_once(
      text,
      OLD_LOCATOR_ANCHOR,
      NEW_LOCATOR_ANCHOR,
      "fixed rule locator mapping",
    )

  BOUNDARY.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

  TEST.write_text(
    TEST_TEXT,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R5-R6 (5.3) bracket definition Reference patch applied."
  )
  print(
    "updated: "
    + str(
      BOUNDARY.resolve()
    )
  )
  print(
    "added: "
    + str(
      TEST.resolve()
    )
  )
  print(
    "Production renderer changes: none"
  )
  print(
    "Proof data changes: none"
  )


if __name__ == "__main__":
  main()
