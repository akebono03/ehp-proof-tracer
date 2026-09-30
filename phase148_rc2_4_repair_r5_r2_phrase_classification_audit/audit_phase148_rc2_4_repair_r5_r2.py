from phase148_rc2_4_repair_r5_two_group_exposure_path_audit.audit_phase148_rc2_4_repair_r5 import (
  CASES,
  _build_case,
  _normalized_exactness_rendering,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
)


def main():
  print("=" * 100)
  print(
    "Phase 148 RC2-4 Repair R5-R2 "
    "exactness phrase classification audit"
  )
  print(
    "Production changes: none"
  )
  print("=" * 100)

  for label, n, k in CASES:
    (
      _presentation,
      closure,
      _sidecar,
      _blocks,
      _arguments,
      rendered,
    ) = _build_case(
      label,
      n,
      k,
    )

    exactness_steps = tuple(
      node.proof_step
      for node in closure.nodes
      if isinstance(
        node.proof_step.conclusion,
        TodaProp42ExactnessStatement,
      )
    )
    normalized_windows = tuple(
      _normalized_exactness_rendering(
        proof_step
      )
      for proof_step in exactness_steps
    )
    phrase_lines = tuple(
      line
      for line in rendered.splitlines()
      if (
        "は完全である" in line
        or r"\text{ is exact}" in line
      )
    )

    print()
    print("-" * 100)
    print(label)
    print("-" * 100)
    print(
      "exactness ProofSteps="
      + str(
        len(
          exactness_steps
        )
      )
    )
    print(
      "phrase lines="
      + str(
        len(
          phrase_lines
        )
      )
    )

    for index, line in enumerate(
      phrase_lines
    ):
      exact_window_matches = tuple(
        normalized
        for normalized in normalized_windows
        if normalized == line
      )
      print(
        "PHRASE["
        + str(
          index
        )
        + "]"
      )
      print(
        "  line="
        + line
      )
      print(
        "  exact-window-match="
        + str(
          bool(
            exact_window_matches
          )
        )
      )
      print(
        "  arrow-count="
        + str(
          line.count(
            r"\xrightarrow"
          )
        )
      )
      print(
        "  long-method-sequence="
        + str(
          (
            line.count(
              r"\xrightarrow"
            )
            >= 3
          )
        )
      )

    print(
      "raw exactness ProofStep visible="
      + str(
        any(
          normalized in rendered
          for normalized in normalized_windows
        )
      )
    )

  print()
  print("=" * 100)
  print(
    "Interpretation rule:"
  )
  print(
    "raw exactness leakage means an actual normalized "
    "TodaProp42ExactnessStatement rendering is visible."
  )
  print(
    "A distinct higher-level method sequence is not classified "
    "as raw exactness merely because it says 'is exact'."
  )
  print("=" * 100)


if __name__ == "__main__":
  main()
