import re

from toda_calculation_facade import (
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

  return (
    build_toda_group_proof_presentation(
      replay
    )
  )


def test_phase157_r5_r6_53_catalog_contains_bracket_definition_component():
  components = (
    get_toda_fixed_statement_components(
      "(5.3)"
    )
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
  assert (
    boundary.reference_locator
    == "(5.3)"
  )
  assert (
    boundary.component_key
    == "nu_prime_bracket_definition"
  )


def test_phase157_r5_r6_53_specialization_remains_proof_internal():
  presentation = (
    _pi6_3_presentation()
  )

  specialization_step = next(
    node.proof_step
    for node in presentation.nodes
    if (
      node.proof_step.inference_rule
      is not None
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
  reference_part = (
    rendered.split(
      "---\n\n## 証明",
      1,
    )[
      0
    ]
  )

  assert (
    re.search(
      r"\*\*\[R\d+\] \(5\.3\)\.\*\*",
      reference_part,
    )
    is not None
  )
  assert (
    r"\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}"
    in reference_part
    or
    r"\nu' \in \{\eta_{3},2\iota_{4},\eta_{4}\}_{1}"
    in reference_part
  )
def test_phase157_r5_r6_pi6_hides_fixed_definition_internal_body():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _pi6_3_presentation()
    )
  )

  assert (
    "Lemma 5.2"
    not in rendered
  )
  assert (
    r"$\nu'$ を定める."
    not in rendered
  )
  assert (
    r"$2\eta_{3} = 0$"
    not in rendered
  )
