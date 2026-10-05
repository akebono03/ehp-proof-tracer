from __future__ import annotations

import re
import sys
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
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


def main() -> int:
  report = build_standard_toda_report(
    n=8,
    k=7,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  reference_marker = "\n## 使用する結果\n"
  proof_marker = "\n## 証明\n"

  if (
    reference_marker not in rendered
    or proof_marker not in rendered
  ):
    raise RuntimeError(
      "public Reference / proof sections are missing"
    )

  reference_tail = rendered.split(
    reference_marker,
    1,
  )[1]
  reference_section, body = reference_tail.split(
    proof_marker,
    1,
  )

  headers = re.findall(
    r"\*\*\[R([0-9]+)\] ([^\n]+?)\.\*\*",
    reference_section,
  )
  body_markers = tuple(
    int(
      match.group(
        1
      )
    )
    for match in re.finditer(
      r"\[R([0-9]+)\]",
      body,
    )
  )

  print(
    "=" * 96
  )
  print(
    "Phase157-R20 repair53-r5 pi15^8 public Reference check"
  )
  print(
    "=" * 96
  )
  print(
    "headers:",
    headers,
  )
  print(
    "body markers:",
    body_markers,
  )
  print()
  print(
    "REFERENCE SECTION"
  )
  print(
    "-" * 96
  )
  print(
    reference_section.strip()
  )
  print()
  print(
    "PROOF BODY"
  )
  print(
    "-" * 96
  )
  print(
    body.strip()
  )

  expected_headers = [
    (
      "1",
      "Proposition 5.15",
    ),
    (
      "2",
      "Proposition 4.4",
    ),
  ]

  if headers != expected_headers:
    raise RuntimeError(
      "unexpected public Reference headers: "
      + repr(
        headers
      )
    )

  if body_markers != (
    1,
    2,
  ):
    raise RuntimeError(
      "unexpected proof-body Reference markers: "
      + repr(
        body_markers
      )
    )

  if (
    r"$\pi_{14}^{7} = \mathbb{Z}/8\{\sigma'\}$"
    not in reference_section
  ):
    raise RuntimeError(
      "Proposition 5.15 pi14_7 fixed component "
      "is missing from Reference"
    )

  if (
    r"\pi_{15}^{8} \cong"
    in reference_section
  ):
    raise RuntimeError(
      "Proposition 5.15 root component leaked into Reference"
    )

  print()
  print(
    "AUDIT PASS"
  )
  print(
    "Proposition 5.15 pi14_7 component and Proposition 4.4 "
    "are both linked to the proof body."
  )
  print(
    "Production changes are limited to the pi15^8 dedicated "
    "Reference connection path."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
