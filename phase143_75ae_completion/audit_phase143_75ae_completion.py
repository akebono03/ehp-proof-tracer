import runpy

import toda_proof_narrative_renderer as narrative
from test_phase73_pi9_3_zero import (
  build_phase73_4_data,
)


TARGET_AUDIT = (
  "phase143_75u/"
  "audit_phase143_75u_remaining_fallbacks.py"
)


def main():
  print("=" * 78)
  print(
    "Phase 143-75AE completion audit"
  )
  print("=" * 78)

  data = build_phase73_4_data()

  pi8_rendered = (
    narrative.render_toda_proof_statement_latex(
      data["pi8_zero_step"].conclusion
    )
  )
  pi7_rendered = (
    narrative.render_toda_proof_statement_latex(
      data["pi7_zero_step"].conclusion
    )
  )

  print("Focused semantic renderings")
  print("-" * 78)
  print("pi8^2 zero suspension:")
  print(pi8_rendered)
  print("pi7^2 zero suspension:")
  print(pi7_rendered)

  print("")
  print(
    "Remaining fallback inventory"
  )
  print("-" * 78)

  runpy.run_path(
    TARGET_AUDIT,
    run_name="__main__",
  )

  print("")
  print("=" * 78)
  print("Expected completion conditions")
  print("=" * 78)
  print(
    "rule-name fallback occurrences: 171"
  )
  print(
    "TodaSuspensionZeroStatement absent "
    "from remaining statement inventory"
  )
  print(
    "Toda Proposition 5.11 E pi_8^2 zero "
    "absent from fallback rule-name inventory"
  )
  print(
    "Toda Proposition 5.11 E pi_7^2 zero "
    "absent from fallback rule-name inventory"
  )
  print("render errors: 0")
  print("")
  print("No source files were changed.")
  print("No pytest was run.")


if __name__ == "__main__":
  main()
