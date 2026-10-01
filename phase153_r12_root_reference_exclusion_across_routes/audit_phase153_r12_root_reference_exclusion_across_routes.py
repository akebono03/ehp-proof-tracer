from pathlib import Path
import re
import sys

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(REPO_ROOT),
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

TARGETS = (
  ("pi6_2", 2, 4, "Proposition 5.8"),
  ("pi6_3", 3, 3, "Proposition 5.6"),
  ("pi11_4", 4, 7, "Proposition 5.15"),
)

def render(
  n,
  k,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  return render_toda_group_proof_narrative_markdown(
    presentation
  )

def main():
  failures = []

  print("=" * 72)
  print(
    "Phase 153-R12 Root Reference exclusion across routes audit"
  )
  print("=" * 72)

  for label, n, k, root_locator in TARGETS:
    rendered = render(
      n,
      k,
    )
    reference_part = (
      rendered.split(
        "## 証明",
        1,
      )[0]
      if "## 証明" in rendered
      else rendered.split(
        "まず",
        1,
      )[0]
    )
    numbers = tuple(
      int(value)
      for value in re.findall(
        r"\*\*\[R([0-9]+)\]",
        reference_part,
      )
    )

    print(
      f"{label}: references={numbers}, root={root_locator}"
    )

    if root_locator in reference_part:
      failures.append(
        (
          label,
          "root Reference remains",
          root_locator,
        )
      )

    if numbers != tuple(
      range(
        1,
        len(numbers) + 1,
      )
    ):
      failures.append(
        (
          label,
          "Reference numbering is not contiguous",
          numbers,
        )
      )

  pi11_4 = render(
    4,
    7,
  )
  pi11_reference_part = pi11_4.split(
    "## 証明",
    1,
  )[0]

  if "**[R1] Proposition 5.8.**" not in pi11_reference_part:
    failures.append(
      (
        "pi11_4",
        "Proposition 5.8 is not R1",
      )
    )

  if "**[R2] Proposition 4.4.**" not in pi11_reference_part:
    failures.append(
      (
        "pi11_4",
        "Proposition 4.4 is not R2",
      )
    )

  print()

  if failures:
    print("FAIL")
    for failure in failures:
      print("  ", failure)
    raise SystemExit(1)

  print("PASS")
  print(
    "Root LiteratureReference entries are excluded at display boundaries "
    "for marker-bearing and generic Narrative routes."
  )

if __name__ == "__main__":
  main()
