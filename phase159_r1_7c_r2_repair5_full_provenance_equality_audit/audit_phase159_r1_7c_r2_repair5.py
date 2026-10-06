from __future__ import annotations

from pathlib import Path

from proof import (
  Relation,
  RelationType,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_human_readable_renderer import (
  render_toda_expression_latex,
)
from toda_proof_dependency import (
  extract_toda_recursive_proof_provenance,
)


ROOT = Path.cwd()
OUTPUT_DIR = (
  ROOT
  / "phase159_r1_7c_r2_repair5_full_provenance_equality_audit"
  / "audit_output"
)


def _group_result(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  return (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )


def _relation_latex(
  relation: Relation,
) -> str:
  return (
    render_toda_expression_latex(
      relation.lhs
    )
    + " = "
    + render_toda_expression_latex(
      relation.rhs
    )
  )


def _interesting(
  relation: Relation,
) -> bool:
  try:
    latex = _relation_latex(
      relation
    )
  except Exception:
    return False

  needles = (
    r"2\nu'",
    r"\eta_{3}\eta_{4}\eta_{5}",
    r"\eta_{3}^{3}",
    r"\eta_{3}E\eta_{3}\eta_{5}",
  )

  return any(
    needle in latex
    for needle in needles
  )


def main() -> int:
  OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  group_result = _group_result(
    3,
    3,
  )
  provenance = (
    extract_toda_recursive_proof_provenance(
      group_result
    )
  )

  report = [
    "# Phase 159-R1-7c R2 repair5 full provenance equality audit",
    "",
    "Production code changes: none",
    "Test changes: none",
    "pytest: not run",
    "",
    f"nodes={len(provenance.nodes)}",
    f"edges={len(provenance.edges)}",
    "",
    "## Interesting equality nodes",
    "",
  ]

  interesting_ids = set()

  for node in provenance.nodes:
    step = node.proof_step
    conclusion = step.conclusion

    if (
      not isinstance(
        conclusion,
        Relation,
      )
      or conclusion.relation_type
      is not RelationType.EQUALITY
      or not _interesting(
        conclusion
      )
    ):
      continue

    interesting_ids.add(
      id(
        step
      )
    )

    rule = (
      step.inference_rule.name
      if step.inference_rule is not None
      else None
    )
    rendered = (
      _render_generic_narrative_step(
        step
      )
    )

    report.extend(
      (
        (
          f"### id={id(step)} "
          f"depth={node.shortest_depth}"
        ),
        f"- rule={rule!r}",
        f"- rendered={rendered!r}",
        f"- latex={_relation_latex(conclusion)!r}",
        f"- premises={len(step.premises)}",
      )
    )

    for index, premise in enumerate(
      step.premises,
      start=1,
    ):
      premise_conclusion = (
        premise.conclusion
      )
      premise_rule = (
        premise.inference_rule.name
        if premise.inference_rule is not None
        else None
      )

      if (
        isinstance(
          premise_conclusion,
          Relation,
        )
        and premise_conclusion.relation_type
        is RelationType.EQUALITY
      ):
        try:
          premise_latex = (
            _relation_latex(
              premise_conclusion
            )
          )
        except Exception:
          premise_latex = repr(
            premise_conclusion
          )
      else:
        premise_latex = repr(
          premise_conclusion
        )

      report.append(
        (
          f"- premise {index}: "
          f"id={id(premise)} "
          f"rule={premise_rule!r} "
          f"latex={premise_latex!r}"
        )
      )

    report.append("")

  report.extend(
    (
      "## Edges touching interesting equality nodes",
      "",
    )
  )

  for edge in provenance.edges:
    parent_id = id(
      edge.parent_step
    )
    premise_id = id(
      edge.premise_step
    )

    if (
      parent_id not in interesting_ids
      and premise_id not in interesting_ids
    ):
      continue

    parent_rule = (
      edge.parent_step.inference_rule.name
      if edge.parent_step.inference_rule is not None
      else None
    )
    premise_rule = (
      edge.premise_step.inference_rule.name
      if edge.premise_step.inference_rule is not None
      else None
    )

    report.append(
      (
        f"- parent={parent_id} "
        f"parent_rule={parent_rule!r} "
        f"premise_index={edge.premise_index} "
        f"premise={premise_id} "
        f"premise_rule={premise_rule!r}"
      )
    )

  report.extend(
    (
      "",
      "## Full-depth replay occurrences",
      "",
    )
  )

  full_depth = max(
    node.shortest_depth
    for node in provenance.nodes
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=full_depth,
  )

  for replay_step in replay.steps:
    step = replay_step.proof_step
    conclusion = step.conclusion

    if (
      isinstance(
        conclusion,
        Relation,
      )
      and conclusion.relation_type
      is RelationType.EQUALITY
      and _interesting(
        conclusion
      )
    ):
      report.append(
        (
          f"- replay_depth={replay_step.depth} "
          f"id={id(step)} "
          f"rule={step.inference_rule.name if step.inference_rule else None!r} "
          f"latex={_relation_latex(conclusion)!r}"
        )
      )

  report.append("")

  text = "\n".join(
    report
  )

  (
    OUTPUT_DIR
    / "full_provenance_equality_audit.md"
  ).write_text(
    text,
    encoding="utf-8",
  )

  print(
    text
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
