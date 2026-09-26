from collections import defaultdict

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  _render_group_proof_narrative_fact,
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


MAX_DEPTH = 7
N_MIN = 2
N_MAX = 15
K_MIN = 0
K_MAX = 7


def main() -> None:
  exposed = defaultdict(
    list
  )
  scanned_groups = 0
  scanned_nodes = 0

  for k in range(
    K_MIN,
    K_MAX + 1,
  ):
    for n in range(
      N_MIN,
      N_MAX + 1,
    ):
      try:
        report = build_standard_toda_report(
          n=n,
          k=k,
        )
      except Exception:
        continue

      if not report.candidates:
        continue

      group_result = (
        report.candidates[
          0
        ].source_candidate.group_result
      )

      try:
        replay = (
          build_toda_group_result_proof_replay(
            group_result,
            max_depth=MAX_DEPTH,
          )
        )
        presentation = (
          build_toda_group_proof_presentation(
            replay
          )
        )
        narrative = (
          render_toda_group_proof_narrative_markdown(
            presentation
          )
        )
      except Exception as exc:
        print(
          "SKIP "
          f"pi_{n + k}^{n}: "
          f"{type(exc).__name__}: {exc}"
        )
        continue

      scanned_groups += 1

      for node in presentation.nodes:
        step = node.proof_step
        scanned_nodes += 1

        class_name = type(
          step.conclusion
        ).__name__

        rendered_fact = (
          _render_group_proof_narrative_fact(
            step
          )
        )

        raw_fallback = (
          "`"
          + class_name
          + "`"
        )

        if rendered_fact != raw_fallback:
          continue

        if raw_fallback not in narrative:
          continue

        exposed[
          class_name
        ].append(
          (
            n,
            k,
            node.depth,
            step.inference_rule.name
            if step.inference_rule is not None
            else None,
          )
        )

  print("=" * 78)
  print("Phase 143-74 internal statement-name Narrative exposure audit")
  print(
    f"range: n={N_MIN}..{N_MAX}, "
    f"k={K_MIN}..{K_MAX}, "
    f"depth={MAX_DEPTH}"
  )
  print(
    f"scanned groups: {scanned_groups}"
  )
  print(
    f"scanned presentation nodes: {scanned_nodes}"
  )
  print(
    "raw exposed statement classes: "
    + str(
      len(
        exposed
      )
    )
  )
  print("=" * 78)

  if not exposed:
    print(
      "PASS: no raw internal statement class name "
      "was exposed in the audited 0-7 stem Narrative range."
    )
    return

  for class_name in sorted(
    exposed
  ):
    occurrences = exposed[
      class_name
    ]

    print(class_name)
    print(
      "  occurrences: "
      + str(
        len(
          occurrences
        )
      )
    )

    for (
      n,
      k,
      depth,
      inference_rule_name,
    ) in occurrences[:12]:
      suffix = ""
      if inference_rule_name is not None:
        suffix = (
          ", inference_rule="
          + inference_rule_name
        )

      print(
        "  - "
        f"pi_{n + k}^{n}, "
        f"k={k}, "
        f"depth={depth}"
        + suffix
      )

    if len(
      occurrences
    ) > 12:
      print(
        "  - ... "
        + str(
          len(
            occurrences
          )
          - 12
        )
        + " more"
      )

    print()

  print(
    "AUDIT FINDING: raw internal statement names remain. "
    "Use this inventory to choose the minimal generic "
    "rendering work for the next subphase."
  )


if __name__ == "__main__":
  main()
