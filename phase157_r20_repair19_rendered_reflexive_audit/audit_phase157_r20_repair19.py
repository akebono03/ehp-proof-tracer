from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(0, str(REPOSITORY_ROOT))

from proof import (
  Relation,
  RelationType,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_expression_latex,
  _render_generic_narrative_step,
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


def main() -> int:
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
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )

  print(
    "Repository root:",
    REPOSITORY_ROOT,
  )
  print(
    "nodes:",
    len(
      presentation.nodes
    ),
  )

  rendered_reflexive = []

  for index, node in enumerate(
    presentation.nodes
  ):
    step = node.proof_step
    statement = step.conclusion

    if (
      not isinstance(
        statement,
        Relation,
      )
      or statement.relation_type
      is not RelationType.EQUALITY
    ):
      continue

    lhs_latex = (
      _render_generic_narrative_expression_latex(
        statement.lhs
      )
    )
    rhs_latex = (
      _render_generic_narrative_expression_latex(
        statement.rhs
      )
    )
    rendered_step = (
      _render_generic_narrative_step(
        step
      )
    )

    if lhs_latex != rhs_latex:
      continue

    rendered_reflexive.append(
      step
    )

    print("")
    print("=" * 88)
    print(
      "RENDERED-REFLEXIVE NODE",
      index,
    )
    print("=" * 88)
    print(
      "original_lhs_equals_rhs:",
      statement.lhs == statement.rhs,
    )
    print(
      "lhs type:",
      type(
        statement.lhs
      ).__name__,
    )
    print(
      "rhs type:",
      type(
        statement.rhs
      ).__name__,
    )
    print(
      "lhs repr:",
      repr(
        statement.lhs
      ),
    )
    print(
      "rhs repr:",
      repr(
        statement.rhs
      ),
    )
    print(
      "normalized lhs:",
      lhs_latex,
    )
    print(
      "normalized rhs:",
      rhs_latex,
    )
    print(
      "rendered step:",
      rendered_step,
    )
    print(
      "rule:",
      (
        None
        if step.inference_rule is None
        else step.inference_rule.name
      ),
    )
    print(
      "premises:",
      len(
        step.premises
      ),
    )

    for premise_index, premise in enumerate(
      step.premises
    ):
      print(
        "  premise",
        premise_index,
        "type=",
        type(
          premise.conclusion
        ).__name__,
        "rule=",
        (
          None
          if premise.inference_rule is None
          else premise.inference_rule.name
        ),
      )

  print("")
  print("=" * 88)
  print("SUMMARY")
  print("=" * 88)
  print(
    "rendered-reflexive equality steps:",
    len(
      rendered_reflexive
    ),
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
