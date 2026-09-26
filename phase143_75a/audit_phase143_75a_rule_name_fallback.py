from collections import Counter, defaultdict

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  _group_proof_narrative_statement_label,
  _render_group_proof_narrative_fact,
  _render_group_proof_narrative_latex,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _fallback_kind(
  proof_step,
):
  latex = _render_group_proof_narrative_latex(
    proof_step
  )
  if latex is not None:
    return "semantic_latex"

  label = _group_proof_narrative_statement_label(
    proof_step.conclusion
  )
  if label is not None:
    return "human_label"

  if proof_step.inference_rule is not None:
    return "inference_rule_name"

  return "raw_class_name"


def main():
  scanned_groups = 0
  scanned_nodes = 0
  fallback_rows = []
  render_errors = []

  for k in range(8):
    for n in range(2, 16):
      scanned_groups += 1
      try:
        report = build_standard_toda_report(
          n=n,
          k=k,
        )
        group_result = (
          report.candidates[
            0
          ].source_candidate.group_result
        )
        replay = build_toda_group_result_proof_replay(
          group_result,
          max_depth=7,
        )
        presentation = build_toda_group_proof_presentation(
          replay
        )
      except Exception as exc:
        render_errors.append(
          (
            n,
            k,
            type(exc).__name__,
            str(exc),
          )
        )
        continue

      for node_index, node in enumerate(
        presentation.nodes
      ):
        scanned_nodes += 1
        proof_step = node.proof_step
        kind = _fallback_kind(
          proof_step
        )
        if kind != "inference_rule_name":
          continue

        rule_name = (
          proof_step.inference_rule.name
        )
        statement_type = type(
          proof_step.conclusion
        ).__name__
        rendered = (
          _render_group_proof_narrative_fact(
            proof_step
          )
        )

        fallback_rows.append(
          (
            n,
            k,
            node_index,
            statement_type,
            rule_name,
            rendered,
          )
        )

  by_statement = Counter(
    row[3]
    for row in fallback_rows
  )
  by_rule = Counter(
    row[4]
    for row in fallback_rows
  )
  by_pair = Counter(
    (
      row[3],
      row[4],
    )
    for row in fallback_rows
  )
  groups_by_statement = defaultdict(set)
  for row in fallback_rows:
    groups_by_statement[
      row[3]
    ].add(
      (
        row[0],
        row[1],
      )
    )

  print("=" * 78)
  print(
    "Phase 143-75A inference-rule-name "
    "Narrative fallback audit"
  )
  print(
    "range: n=2..15, k=0..7, depth=7"
  )
  print(
    f"scanned groups: {scanned_groups}"
  )
  print(
    f"scanned presentation nodes: "
    f"{scanned_nodes}"
  )
  print(
    "inference-rule-name fallback "
    f"occurrences: {len(fallback_rows)}"
  )
  print(
    "statement types using fallback: "
    f"{len(by_statement)}"
  )
  print(
    "distinct fallback rule names: "
    f"{len(by_rule)}"
  )
  print("=" * 78)

  print()
  print("BY STATEMENT TYPE")
  for statement_type, count in (
    by_statement.most_common()
  ):
    groups = sorted(
      groups_by_statement[
        statement_type
      ]
    )
    print(
      f"- {statement_type}: "
      f"{count} occurrences, "
      f"{len(groups)} groups"
    )
    print(
      "  groups: "
      + ", ".join(
        f"pi_{n+k}^{n}"
        for n, k in groups[:20]
      )
      + (
        " ..."
        if len(groups) > 20
        else ""
      )
    )

  print()
  print("BY STATEMENT TYPE + RULE NAME")
  for (
    statement_type,
    rule_name,
  ), count in by_pair.most_common():
    print(
      f"- {statement_type}: "
      f"{count} x {rule_name}"
    )

  print()
  print("SAMPLE OCCURRENCES")
  seen = set()
  for row in fallback_rows:
    n, k, node_index, statement_type, (
      rule_name
    ), rendered = row
    key = (
      statement_type,
      rule_name,
    )
    if key in seen:
      continue
    seen.add(key)
    print(
      f"- pi_{n+k}^{n}, "
      f"k={k}, node={node_index}"
    )
    print(
      f"  statement: {statement_type}"
    )
    print(
      f"  rule: {rule_name}"
    )
    print(
      f"  rendered: {rendered}"
    )

  print()
  print(f"render errors: {len(render_errors)}")
  for item in render_errors[:20]:
    print("  -", item)

  print()
  print("=" * 78)
  if not fallback_rows and not render_errors:
    print(
      "PASS: no inference-rule-name "
      "fallback remains."
    )
  else:
    print(
      "AUDIT FINDING: the statement types "
      "above still fall back to "
      "inference_rule.name."
    )
    print(
      "Use this inventory to select the "
      "smallest semantic rendering target "
      "for Phase 143-75B."
    )


if __name__ == "__main__":
  main()
