from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(
  REPO_ROOT
) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
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


def main():
  report = build_standard_toda_report(
    n=2,
    k=2,
  )
  result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    result,
    max_depth=3,
  )
  raw = build_toda_group_proof_presentation(
    replay
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )
  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )

  print(
    "Reference entries before public filtering:"
  )

  for entry in entries:
    print(
      f"R{entry.number}: "
      f"{entry.reference.locator} "
      f"steps={len(entry.proof_steps)}"
    )

  prop51_entries = tuple(
    entry
    for entry in entries
    if entry.reference.locator
    == "Proposition 5.1"
  )

  print(
    "Proposition 5.1 entry count:",
    len(
      prop51_entries
    ),
  )

  if prop51_entries:
    print(
      "Proposition 5.1 rules:"
    )
    for step in prop51_entries[
      0
    ].proof_steps:
      if step.inference_rule is not None:
        print(
          "  ",
          step.inference_rule.name,
        )

  rendered = render_toda_group_proof_narrative_markdown(
    raw
  )

  print()
  print(
    rendered
  )

  reference, body = rendered.split(
    "---",
    1,
  )

  diagnostics = {
    "single initial Proposition 5.1 entry": (
      len(
        prop51_entries
      )
      == 1
    ),
    "R1 is (5.2)": (
      "**[R1] (5.2).**"
      in reference
    ),
    "R2 is Proposition 5.1": (
      "**[R2] Proposition 5.1.**"
      in reference
    ),
    "general Prop.5.1 absent from body": (
      (
        r"\pi_{n + 1}^{n} = "
        r"\mathbb{Z}/2\{\eta_{n}\}"
      )
      not in body
    ),
    "R2 marker on pi_4^3": (
      any(
        (
          "[R2]"
          in paragraph
          and r"\pi_{4}^{3}"
          in paragraph
        )
        for paragraph in body.split(
          "\n\n"
        )
      )
    ),
    "QED": (
      "□"
      in body
    ),
  }

  print()
  print(
    "=" * 78
  )
  print(
    "Phase 161-R4-R5 repair14 diagnostics"
  )
  print(
    "=" * 78
  )

  for label, result in diagnostics.items():
    print(
      f"{label}: {result}"
    )

  failed = tuple(
    label
    for label, result in diagnostics.items()
    if not result
  )

  if failed:
    raise SystemExit(
      "Repair14 verification failed: "
      + ", ".join(
        failed
      )
    )


if __name__ == "__main__":
  main()
