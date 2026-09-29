from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_calculation_facade import (
  build_standard_toda_report,
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
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
)


TARGET_TYPES = (
  ScalarGreaterEqualStatement,
  TodaEtaFamilyDefinitionStatement,
)


def main() -> None:
  found = []

  for k in range(0, 8):
    for n in range(2, 16):
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

      for depth in range(0, 8):
        try:
          replay = (
            build_toda_group_result_proof_replay(
              group_result,
              max_depth=depth,
            )
          )
          presentation = (
            build_toda_group_proof_presentation(
              replay
            )
          )
        except Exception:
          continue

        types = {
          type(
            node.proof_step.conclusion
          )
          for node in presentation.nodes
        }

        present = tuple(
          target.__name__
          for target in TARGET_TYPES
          if target in types
        )

        if not present:
          continue

        rendered = (
          render_toda_group_proof_narrative_markdown(
            presentation
          )
        )

        print("=" * 78)
        print(
          f"pi_{n + k}^{n}, k={k}, depth={depth}"
        )
        print(
          "statement types: "
          + ", ".join(
            present
          )
        )

        for name in (
          "ScalarGreaterEqualStatement",
          "TodaEtaFamilyDefinitionStatement",
        ):
          print(
            f"raw {name}: "
            + (
              "FOUND"
              if name in rendered
              else "not found"
            )
          )

        print(
          r"human-readable \ge: "
          + str(
            r"\ge" in rendered
          )
        )
        print(
          "human-readable eta-family: "
          + str(
            "\u03b7-family \u306e\u5b9a\u7fa9"
            in rendered
          )
        )

        found.append(
          (
            n,
            k,
            depth,
            present,
          )
        )
        break

  print("=" * 78)

  if not found:
    raise SystemExit(
      "NO MATCH: neither target statement type appeared "
      "in the scanned production replay range."
    )

  scalar_found = any(
    "ScalarGreaterEqualStatement"
    in present
    for _, _, _, present in found
  )
  eta_found = any(
    "TodaEtaFamilyDefinitionStatement"
    in present
    for _, _, _, present in found
  )

  print(
    "ScalarGreaterEqualStatement reached: "
    + str(
      scalar_found
    )
  )
  print(
    "TodaEtaFamilyDefinitionStatement reached: "
    + str(
      eta_found
    )
  )

  if not scalar_found or not eta_found:
    raise SystemExit(
      "PARTIAL: scan found only one target statement type."
    )

  print(
    "PASS: production replay cases containing both target "
    "statement types were identified."
  )


if __name__ == "__main__":
  main()
