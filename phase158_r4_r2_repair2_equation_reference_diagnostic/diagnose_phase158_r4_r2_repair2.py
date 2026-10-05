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


TAG_RE = re.compile(
  r"\\tag\{(\d+)\}"
)


def _render(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
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
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def _print_group(
  n: int,
  k: int,
) -> None:
  rendered = _render(
    n,
    k,
  )
  label = (
    f"pi_{n + k}^{n}"
  )

  print()
  print(
    "=" * 78
  )
  print(
    label
  )
  print(
    "=" * 78
  )

  tags = tuple(
    int(
      value
    )
    for value in TAG_RE.findall(
      rendered
    )
  )
  print(
    "visible tags:",
    tags,
  )

  print()
  print(
    "Lines containing tags or numbered connectors"
  )
  print(
    "-" * 78
  )

  for line_number, line in enumerate(
    rendered.splitlines(),
    start=1,
  ):
    stripped = line.strip()

    if (
      r"\tag{" in stripped
      or (
        stripped.startswith(
          "("
        )
        and "より," in stripped
      )
    ):
      print(
        f"{line_number:03d}: {stripped}"
      )

  print()
  print(
    "Paragraphs starting with '(' and containing 'より,'"
  )
  print(
    "-" * 78
  )

  for paragraph_number, paragraph in enumerate(
    rendered.split(
      "\n\n"
    ),
    start=1,
  ):
    stripped = paragraph.strip()

    if (
      stripped.startswith(
        "("
      )
      and "より," in stripped
    ):
      print(
        f"[{paragraph_number}] {repr(stripped)}"
      )


def main() -> int:
  print(
    "=" * 78
  )
  print(
    "Phase 158-R4-R2 repair2 - equation reference diagnostic"
  )
  print(
    "=" * 78
  )
  print(
    "Production code changes: none"
  )
  print(
    "Existing test changes: none"
  )
  print(
    "Full pytest: not run"
  )

  _print_group(
    3,
    3,
  )
  _print_group(
    5,
    3,
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
