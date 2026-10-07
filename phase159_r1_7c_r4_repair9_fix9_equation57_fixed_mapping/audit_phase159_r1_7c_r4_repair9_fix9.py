from __future__ import annotations

from proof import (
  InferenceRule,
  ProofRule,
  ProofStep,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_references import (
  _infer_toda_group_proof_literature_reference_from_rule_name,
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
  classify_toda_literature_statement_step,
)


RULE_NAME = (
  "Toda Equation 5.7 nu-prime eta_6 Hopf value"
)


def main() -> int:
  step = ProofStep(
    conclusion="audit",
    premises=(),
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name=RULE_NAME,
    ),
  )

  boundary = classify_toda_literature_statement_step(
    step
  )

  inferred = (
    _infer_toda_group_proof_literature_reference_from_rule_name(
      RULE_NAME
    )
  )

  print(
    "=== Equation 5.7 boundary ==="
  )
  print(
    "classification=",
    None
    if boundary is None
    else boundary.classification.value,
    sep="",
  )
  print(
    "boundary_locator=",
    None
    if boundary is None
    else boundary.reference_locator,
    sep="",
  )
  print(
    "component_key=",
    None
    if boundary is None
    else boundary.component_key,
    sep="",
  )
  print(
    "inferred_locator=",
    None
    if inferred is None
    else inferred.locator,
    sep="",
  )

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
  presentation = build_toda_group_proof_presentation(
    replay
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  reference_section = rendered.split(
    "---",
    1,
  )[0]

  print(
    "=== pi_6^3 Reference headers ==="
  )
  for line in reference_section.splitlines():
    if line.startswith(
      "**[R"
    ):
      print(
        line
      )

  print(
    "has_parenthesized_57=",
    int(
      "**[R5] (5.7).**"
      in reference_section
    ),
    sep="",
  )
  print(
    "has_equation_word_57=",
    int(
      "Equation 5.7"
      in reference_section
    ),
    sep="",
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
