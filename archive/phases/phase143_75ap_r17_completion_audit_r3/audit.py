from collections import Counter

from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _internal_rule_names(presentation):
  names = set()

  for node in presentation.nodes:
    proof_step = getattr(node, "proof_step", None)

    if proof_step is None:
      continue

    rule = getattr(proof_step, "rule", None)
    name = getattr(rule, "name", None)

    if isinstance(name, str) and name:
      names.add(name)

  return names


scanned_groups = 0
scanned_presentation_nodes = 0
fallback_occurrences = 0
fallback_rule_names = Counter()
render_errors = []

for n in range(2, 18):
  for k in range(0, 8):
    try:
      (
        presentation,
        blocks,
        sidecar,
        arguments,
      ) = _method_evidence_data(
        n,
        k,
      )
    except Exception:
      continue

    scanned_groups += 1
    scanned_presentation_nodes += len(
      presentation.nodes
    )

    try:
      rendered = (
        render_toda_group_proof_narrative_multi_argument_markdown(
          presentation,
          blocks,
          sidecar,
          arguments,
        )
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

    for rule_name in _internal_rule_names(
      presentation
    ):
      count = rendered.count(
        rule_name
      )

      if count:
        fallback_occurrences += count
        fallback_rule_names[
          rule_name
        ] += count


print("=" * 78)
print("Phase 143-75AP R17 current-entrypoint completion audit")
print("=" * 78)
print(f"scanned groups: {scanned_groups}")
print(
  "scanned presentation nodes: "
  f"{scanned_presentation_nodes}"
)
print(
  "rule-name fallback occurrences: "
  f"{fallback_occurrences}"
)
print(
  "distinct fallback rule names: "
  f"{len(fallback_rule_names)}"
)
print(
  "render errors: "
  f"{len(render_errors)}"
)

if fallback_rule_names:
  print()
  print("Fallback rule names")
  print("-" * 78)

  for name, count in (
    fallback_rule_names.most_common()
  ):
    print(
      f"{count:4d} x {name}"
    )

if render_errors:
  print()
  print("Render errors")
  print("-" * 78)

  for (
    n,
    k,
    error_type,
    message,
  ) in render_errors:
    print(
      f"n={n}, k={k}: "
      f"{error_type}: {message}"
    )

if fallback_occurrences != 0:
  raise SystemExit(
    "FAIL: rule-name fallback remains."
  )

if render_errors:
  raise SystemExit(
    "FAIL: render errors remain."
  )

print()
print("PASS: fallback=0 and render errors=0.")
