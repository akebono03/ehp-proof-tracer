from collections import Counter, defaultdict

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_renderer import (
  _render_group_proof_narrative_fact,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


EXPECTED_GROUPS = 112
EXPECTED_PRESENTATION_NODES = 11033
EXPECTED_FALLBACK_OCCURRENCES = 410
EXPECTED_STATEMENT_TYPES = 32


def main():
  scanned_groups = 0
  presentation_nodes = 0
  fallback_by_type = Counter()
  fallback_rule_names = Counter()
  groups_by_type = defaultdict(set)
  errors = []

  for n in range(2, 16):
    for k in range(0, 8):
      group_label = (
        "pi_"
        + str(n + k)
        + "^"
        + str(n)
      )

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
        replay = (
          build_toda_group_result_proof_replay(
            group_result,
            max_depth=7,
          )
        )
        presentation = (
          build_toda_group_proof_presentation(
            replay
          )
        )
      except Exception as exc:
        errors.append(
          (
            group_label,
            type(exc).__name__,
            str(exc),
          )
        )
        continue

      scanned_groups += 1
      presentation_nodes += len(
        presentation.nodes
      )

      for node in presentation.nodes:
        proof_step = node.proof_step
        rule = proof_step.inference_rule

        if rule is None:
          continue

        try:
          rendered = (
            _render_group_proof_narrative_fact(
              proof_step
            )
          )
        except Exception as exc:
          errors.append(
            (
              group_label,
              type(exc).__name__,
              str(exc),
            )
          )
          continue

        if rendered != rule.name:
          continue

        statement_type = type(
          proof_step.conclusion
        ).__name__

        fallback_by_type[
          statement_type
        ] += 1
        fallback_rule_names[
          rule.name
        ] += 1
        groups_by_type[
          statement_type
        ].add(
          group_label
        )

  total_fallback = sum(
    fallback_by_type.values()
  )

  print("=" * 78)
  print(
    "Phase 143-75Q full rule-name fallback audit"
  )
  print(
    "range: n=2..15, k=0..7, depth=7"
  )
  print(
    "scanned groups:",
    scanned_groups,
  )
  print(
    "scanned presentation nodes:",
    presentation_nodes,
  )
  print(
    "rule-name fallback occurrences:",
    total_fallback,
  )
  print(
    "statement types:",
    len(fallback_by_type),
  )
  print(
    "distinct fallback rule names:",
    len(fallback_rule_names),
  )
  print(
    "render errors:",
    len(errors),
  )
  print("=" * 78)

  print()
  print("Remaining fallback inventory")
  print("-" * 78)

  for index, (
    statement_type,
    count,
  ) in enumerate(
    fallback_by_type.most_common(),
    start=1,
  ):
    print(
      str(index)
      + ". "
      + statement_type
      + ": "
      + str(count)
    )
    print(
      "   groups: "
      + str(
        len(
          groups_by_type[
            statement_type
          ]
        )
      )
    )

  print()
  print("Fallback rule-name inventory")
  print("-" * 78)

  for rule_name, count in (
    fallback_rule_names.most_common()
  ):
    print(
      str(count)
      + " x "
      + rule_name
    )

  if errors:
    print()
    print("Errors")
    print("-" * 78)
    for error in errors[:50]:
      print(
        " - "
        + repr(error)
      )

  print()
  print("=" * 78)

  if (
    scanned_groups == EXPECTED_GROUPS
    and presentation_nodes
    == EXPECTED_PRESENTATION_NODES
    and total_fallback
    == EXPECTED_FALLBACK_OCCURRENCES
    and len(fallback_by_type)
    == EXPECTED_STATEMENT_TYPES
    and not errors
  ):
    print(
      "PASS: Phase 143-75P removed exactly "
      "55 fallback occurrences; "
      "410 remain across 32 statement types."
    )
  else:
    print(
      "MEASURED RESULT: expected fallback=410 "
      "and statement types=32 are checkpoints only; "
      "use the inventory above as the actual state."
    )


if __name__ == "__main__":
  main()
