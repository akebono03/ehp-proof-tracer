from __future__ import annotations

import csv
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(0, str(REPOSITORY_ROOT))

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
)
from homotopy_groups import (
  TodaDeltaMap,
  TodaPrimaryGroup,
)
from low_dimensional_facts import (
  pi_4_5_zero_fact,
)
from proof import (
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
)
from toda_proof_dependency import (
  extract_toda_recursive_proof_provenance,
)
from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaImageUpToSignStatement,
  TodaPrimaryGroupZeroStatement,
  TodaSuspensionSurjectiveStatement,
  toda_delta_iota5_two_eta2_up_to_sign_inference_rule,
  toda_pi4_3_delta_image_free_cyclic_inference_rule,
)


N = 3
K = 1

OUTPUT_DIR = (
  Path(__file__).resolve().parent
  / "audit_output"
)


def safe_render(
  step: ProofStep,
) -> str:
  try:
    rendered = (
      _render_generic_narrative_step(
        step
      )
    )
  except Exception as exc:
    return (
      "<RENDER_ERROR "
      + type(exc).__name__
      + ": "
      + str(exc)
      + ">"
    )

  return "" if rendered is None else rendered


def rule_name(
  step: ProofStep,
) -> str:
  if step.inference_rule is None:
    return ""

  return step.inference_rule.name


def is_eta2(
  expression,
) -> bool:
  return (
    isinstance(
      expression,
      HomotopyElement,
    )
    and expression.generator
    == GeneratorSymbol(
      family="η",
      index=2,
    )
  )


def is_two_eta2(
  expression,
) -> bool:
  return (
    isinstance(
      expression,
      Multiple,
    )
    and expression.coefficient == 2
    and is_eta2(
      expression.expression
    )
  )


def is_pi4_5_zero_step(
  step: ProofStep,
) -> bool:
  statement = step.conclusion

  return (
    isinstance(
      statement,
      TodaPrimaryGroupZeroStatement,
    )
    and statement.group
    == TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=5,
    )
  )


def is_direct_delta_iota5_two_eta2_step(
  step: ProofStep,
) -> bool:
  statement = step.conclusion

  if not isinstance(
    statement,
    TodaDeltaImageUpToSignStatement,
  ):
    return False

  expected_map = TodaDeltaMap(
    source_group=TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=5,
    ),
    target_group=TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    ),
  )

  return (
    statement.map == expected_map
    and getattr(
      statement.element,
      "generator",
      None,
    )
    == GeneratorSymbol(
      family="ι",
      index=5,
    )
    and is_two_eta2(
      statement.positive_value
    )
  )


def is_delta_image_step(
  step: ProofStep,
) -> bool:
  return isinstance(
    step.conclusion,
    TodaDeltaImageFreeCyclicStatement,
  )


def is_E_surjective_step(
  step: ProofStep,
) -> bool:
  return isinstance(
    step.conclusion,
    TodaSuspensionSurjectiveStatement,
  )


def describe_step(
  step: ProofStep,
  depth_by_id,
) -> dict:
  return {
    "depth": depth_by_id.get(
      id(step),
      "",
    ),
    "statement_type": type(
      step.conclusion
    ).__name__,
    "rule": rule_name(step),
    "premise_count": len(
      step.premises
    ),
    "is_pi4_5_zero": (
      is_pi4_5_zero_step(
        step
      )
    ),
    "is_direct_delta": (
      is_direct_delta_iota5_two_eta2_step(
        step
      )
    ),
    "is_delta_image": (
      is_delta_image_step(
        step
      )
    ),
    "is_E_surjective": (
      is_E_surjective_step(
        step
      )
    ),
    "rendered": safe_render(
      step
    ),
  }


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  report = build_standard_toda_report(
    n=N,
    k=K,
  )

  if len(
    report.candidates
  ) != 1:
    raise AssertionError(
      "pi_4^3 must have exactly one candidate"
    )

  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )

  provenance = (
    extract_toda_recursive_proof_provenance(
      group_result
    )
  )

  complete = (
    build_complete_toda_group_result_proof_replay(
      group_result
    )
  )

  depth_by_id = {
    id(
      node.proof_step
    ): node.shortest_depth
    for node in provenance.nodes
  }

  steps = tuple(
    node.proof_step
    for node in provenance.nodes
  )

  zero_steps = tuple(
    step
    for step in steps
    if is_pi4_5_zero_step(
      step
    )
  )

  direct_delta_steps = tuple(
    step
    for step in steps
    if is_direct_delta_iota5_two_eta2_step(
      step
    )
  )

  delta_image_steps = tuple(
    step
    for step in steps
    if is_delta_image_step(
      step
    )
  )

  E_surjective_steps = tuple(
    step
    for step in steps
    if is_E_surjective_step(
      step
    )
  )

  if len(
    delta_image_steps
  ) != 1:
    raise AssertionError(
      "expected exactly one Delta-image step"
    )

  if len(
    E_surjective_steps
  ) != 1:
    raise AssertionError(
      "expected exactly one E-surjective step"
    )

  delta_image_step = (
    delta_image_steps[0]
  )
  E_surjective_step = (
    E_surjective_steps[0]
  )

  delta_premise_rows = tuple(
    describe_step(
      premise,
      depth_by_id,
    )
    for premise in (
      delta_image_step.premises
    )
  )

  surjective_premise_rows = tuple(
    describe_step(
      premise,
      depth_by_id,
    )
    for premise in (
      E_surjective_step.premises
    )
  )

  zero_is_direct_premise = any(
    is_pi4_5_zero_step(
      premise
    )
    for premise in (
      E_surjective_step.premises
    )
  )

  direct_delta_is_image_premise = any(
    is_direct_delta_iota5_two_eta2_step(
      premise
    )
    for premise in (
      delta_image_step.premises
    )
  )

  # Build the direct Delta bridge from the actual indirect prerequisites,
  # when they are both present in the current ancestry.
  delta_up_to_sign_candidates = tuple(
    step
    for step in steps
    if (
      isinstance(
        step.conclusion,
        TodaDeltaImageUpToSignStatement,
      )
      and not (
        is_direct_delta_iota5_two_eta2_step(
          step
        )
      )
    )
  )

  direct_bridge_result = None
  direct_bridge_step = None

  bridge_rule = (
    toda_delta_iota5_two_eta2_up_to_sign_inference_rule()
  )

  bridge_match = find_inference_match(
    bridge_rule,
    steps,
  )

  if bridge_match is not None:
    direct_bridge_result = (
      run_inference_until_stable_with_history(
        bridge_rule,
        steps,
      )
    )

    direct_bridge_matches = tuple(
      step
      for step in (
        direct_bridge_result.steps
      )
      if is_direct_delta_iota5_two_eta2_step(
        step
      )
    )

    if direct_bridge_matches:
      direct_bridge_step = (
        direct_bridge_matches[0]
      )

  current_image_rule = (
    toda_pi4_3_delta_image_free_cyclic_inference_rule()
  )

  image_match_with_direct_only = None

  if direct_bridge_step is not None:
    candidate_steps = tuple(
      step
      for step in steps
      if (
        type(
          step.conclusion
        ).__name__
        == "Relation"
      )
    ) + (
      direct_bridge_step,
    )

    image_match_with_direct_only = (
      find_inference_match(
        current_image_rule,
        candidate_steps,
      )
    )

  all_rows = tuple(
    describe_step(
      step,
      depth_by_id,
    )
    for step in steps
  )

  with (
    OUTPUT_DIR
    / "all_provenance_nodes.csv"
  ).open(
    "w",
    encoding="utf-8",
    newline="",
  ) as handle:
    fieldnames = (
      "depth",
      "statement_type",
      "rule",
      "premise_count",
      "is_pi4_5_zero",
      "is_direct_delta",
      "is_delta_image",
      "is_E_surjective",
      "rendered",
    )
    writer = csv.DictWriter(
      handle,
      fieldnames=fieldnames,
    )
    writer.writeheader()
    writer.writerows(
      all_rows
    )

  def write_rows(
    filename,
    rows,
  ):
    with (
      OUTPUT_DIR
      / filename
    ).open(
      "w",
      encoding="utf-8",
      newline="",
    ) as handle:
      fieldnames = (
        "depth",
        "statement_type",
        "rule",
        "premise_count",
        "is_pi4_5_zero",
        "is_direct_delta",
        "is_delta_image",
        "is_E_surjective",
        "rendered",
      )
      writer = csv.DictWriter(
        handle,
        fieldnames=fieldnames,
      )
      writer.writeheader()
      writer.writerows(
        rows
      )

  write_rows(
    "delta_image_premises.csv",
    delta_premise_rows,
  )

  write_rows(
    "E_surjective_premises.csv",
    surjective_premise_rows,
  )

  summary = [
    "=" * 80,
    "Phase 159 - pi_4^3 corrected provenance route audit",
    "=" * 80,
    "Production code changes: none",
    "Existing test changes: none",
    f"complete max depth: {complete.max_depth}",
    f"complete provenance nodes: {len(steps)}",
    "",
    "Corrected structural checks:",
    (
      "  pi_4^5 zero nodes in provenance: "
      + str(
        len(
          zero_steps
        )
      )
    ),
    (
      "  direct Delta(iota_5)=+/-2eta_2 "
      "nodes in provenance: "
      + str(
        len(
          direct_delta_steps
        )
      )
    ),
    (
      "  pi_4^5 zero is direct premise "
      "of E-surjective step: "
      + str(
        zero_is_direct_premise
      )
    ),
    (
      "  direct Delta statement is direct "
      "premise of Im Delta step: "
      + str(
        direct_delta_is_image_premise
      )
    ),
    "",
    "Current Im Delta premises:",
  ]

  for index, row in enumerate(
    delta_premise_rows
  ):
    summary.extend(
      (
        (
          "  premise["
          + str(index)
          + "] depth="
          + str(row["depth"])
          + " type="
          + row["statement_type"]
        ),
        (
          "    rule="
          + row["rule"]
        ),
        (
          "    rendered="
          + row["rendered"]
        ),
      )
    )

  summary.extend(
    (
      "",
      "Current E-surjective premises:",
    )
  )

  for index, row in enumerate(
    surjective_premise_rows
  ):
    summary.extend(
      (
        (
          "  premise["
          + str(index)
          + "] depth="
          + str(row["depth"])
          + " type="
          + row["statement_type"]
        ),
        (
          "    rule="
          + row["rule"]
        ),
        (
          "    rendered="
          + row["rendered"]
        ),
      )
    )

  summary.extend(
    (
      "",
      "Direct-bridge feasibility:",
      (
        "  current ancestry can derive "
        "Delta(iota_5)=+/-2eta_2 with existing bridge rule: "
        + str(
          direct_bridge_step
          is not None
        )
      ),
      (
        "  current Im Delta rule matches a reduced "
        "candidate set containing the direct Delta step: "
        + str(
          image_match_with_direct_only
          is not None
        )
      ),
      "",
      "Interpretation:",
      (
        "  If pi_4^5 zero is a direct E-surjective premise, "
        "the previous NOT_IN_PROVENANCE result was an audit false negative."
      ),
      (
        "  If the direct Delta statement is absent from provenance "
        "but derivable with the existing bridge rule, the production "
        "pi_4^3 ancestry is still using the older indirect route."
      ),
      (
        "  The next repair should be chosen only after this distinction "
        "is confirmed."
      ),
      "",
      "Output:",
      "  audit_output/summary.txt",
      "  audit_output/all_provenance_nodes.csv",
      "  audit_output/delta_image_premises.csv",
      "  audit_output/E_surjective_premises.csv",
      "",
      "Boundary:",
      "  Audit only. No production repair is performed.",
      "  Repository-wide pytest is not run.",
      "=" * 80,
    )
  )

  summary_text = (
    "\n".join(
      summary
    )
    + "\n"
  )

  (
    OUTPUT_DIR
    / "summary.txt"
  ).write_text(
    summary_text,
    encoding="utf-8",
    newline="\n",
  )

  print(
    summary_text
  )
  print(
    "AUDIT_RESULT=PASS"
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
