from collections import Counter

from toda_group_proof_narrative_renderer import (
  build_toda_group_proof_narrative_presentation,
  render_toda_group_proof_narrative_markdown,
)

fallback_rule_names = Counter()
fallback_statement_types = Counter()
errors = []
group_count = 0
node_count = 0

for n in range(
  2,
  16,
):
  for k in range(
    0,
    8,
  ):
    group_count += 1

    try:
      presentation = (
        build_toda_group_proof_narrative_presentation(
          n,
          k,
        )
      )
      rendered = (
        render_toda_group_proof_narrative_markdown(
          presentation
        )
      )
    except Exception as exc:
      errors.append(
        (
          n,
          k,
          type(
            exc
          ).__name__,
          str(
            exc
          ),
        )
      )
      continue

    # The completion criterion is observable Narrative output:
    # no internal rule-name fallback labels may remain.
    for block in presentation.blocks:
      node_count += len(
        block.steps
      )

      for step in block.steps:
        rule = getattr(
          step,
          "rule",
          None,
        )
        rule_name = getattr(
          rule,
          "name",
          None,
        )

        if (
          isinstance(
            rule_name,
            str,
          )
          and rule_name
          and rule_name in rendered
        ):
          fallback_rule_names[
            rule_name
          ] += 1
          fallback_statement_types[
            type(
              step.conclusion
            ).__name__
          ] += 1

print(
  "=" * 78
)
print(
  "Phase 143-75AP R14 semantic fallback completion audit"
)
print(
  "=" * 78
)
print(
  "scanned groups:",
  group_count,
)
print(
  "scanned presentation nodes:",
  node_count,
)
print(
  "rule-name fallback occurrences:",
  sum(
    fallback_rule_names.values()
  ),
)
print(
  "statement types:",
  len(
    fallback_statement_types
  ),
)
print(
  "distinct fallback rule names:",
  len(
    fallback_rule_names
  ),
)
print(
  "render errors:",
  len(
    errors
  ),
)

if fallback_statement_types:
  print(
    "\nStatement types"
  )
  print(
    "-" * 78
  )
  for name, count in fallback_statement_types.most_common():
    print(
      f"{count:4d} x {name}"
    )

if fallback_rule_names:
  print(
    "\nRule names"
  )
  print(
    "-" * 78
  )
  for name, count in fallback_rule_names.most_common():
    print(
      f"{count:4d} x {name}"
    )

if errors:
  print(
    "\nErrors"
  )
  print(
    "-" * 78
  )
  for item in errors:
    print(
      item
    )

if (
  fallback_rule_names
  or fallback_statement_types
  or errors
):
  raise SystemExit(
    1
  )

print(
  "\nPhase 143 semantic fallback completion audit: PASS"
)
