from __future__ import annotations

import re
import sys
from collections import Counter
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


def _canonical_equation_references(
  rendered: str,
) -> set[int]:
  result = set()

  for line in rendered.splitlines():
    stripped = line.strip()
    suffix = "より,"

    if not stripped.endswith(
      suffix
    ):
      continue

    reference_text = stripped[
      :-len(
        suffix
      )
    ].strip()

    if " と " in reference_text:
      left, right = reference_text.rsplit(
        " と ",
        1,
      )
      pieces = tuple(
        (
          *(
            piece.strip()
            for piece in left.split(
              ","
            )
            if piece.strip()
          ),
          right.strip(),
        )
      )
    else:
      pieces = (
        reference_text,
      )

    numbers = []

    for piece in pieces:
      if (
        not piece.startswith(
          "("
        )
        or not piece.endswith(
          ")"
        )
      ):
        numbers = []
        break

      number_text = piece[
        1:-1
      ]

      if not number_text.isdigit():
        numbers = []
        break

      numbers.append(
        int(
          number_text
        )
      )

    result.update(
      numbers
    )

  return result


def main() -> int:
  counts = Counter()
  affected = set()
  exceptions = []

  for n in range(
    2,
    16,
  ):
    for k in range(
      0,
      8,
    ):
      label = (
        f"pi_{n + k}^{n}"
      )

      try:
        rendered = _render(
          n,
          k,
        )
      except Exception as exc:
        exceptions.append(
          (
            label,
            type(
              exc
            ).__name__,
            str(
              exc
            ),
          )
        )
        continue

      tags = tuple(
        int(
          value
        )
        for value in TAG_RE.findall(
          rendered
        )
      )
      references = (
        _canonical_equation_references(
          rendered
        )
      )

      standalone_period = sum(
        1
        for line in rendered.splitlines()
        if line.strip() == "."
      )
      ambiguous = rendered.count(
        "この群構造と"
      )
      unused = tuple(
        number
        for number in tags
        if number not in references
      )
      missing = tuple(
        number
        for number in references
        if number not in tags
      )
      duplicate = (
        len(
          tags
        )
        - len(
          set(
            tags
          )
        )
      )
      noncompact = (
        1
        if (
          tags
          and tags
          != tuple(
            range(
              1,
              len(
                tags
              )
              + 1,
            )
          )
        )
        else 0
      )

      local = (
        standalone_period
        + ambiguous
        + len(
          unused
        )
        + len(
          missing
        )
        + duplicate
        + noncompact
      )

      if local:
        affected.add(
          label
        )

      counts[
        "standalone_period"
      ] += standalone_period
      counts[
        "ambiguous_anaphora"
      ] += ambiguous
      counts[
        "unused_equation_tag"
      ] += len(
        unused
      )
      counts[
        "missing_equation_tag"
      ] += len(
        missing
      )
      counts[
        "duplicate_equation_tag"
      ] += duplicate
      counts[
        "noncompact_equation_tags"
      ] += noncompact

  print(
    "=" * 78
  )
  print(
    "Phase 158-R4-R2 repair3 - 112-group public re-audit"
  )
  print(
    "=" * 78
  )
  print(
    "Full pytest: not run"
  )
  print()
  print(
    "rendered groups:",
    112 - len(
      exceptions
    ),
  )
  print(
    "exceptions:",
    len(
      exceptions
    ),
  )
  print(
    "affected groups:",
    len(
      affected
    ),
  )

  for key in (
    "standalone_period",
    "ambiguous_anaphora",
    "unused_equation_tag",
    "missing_equation_tag",
    "duplicate_equation_tag",
    "noncompact_equation_tags",
  ):
    print(
      f"{key}: {counts[key]}"
    )

  if affected:
    print(
      "affected:",
      ", ".join(
        sorted(
          affected
        )
      ),
    )

  if exceptions:
    print(
      "exceptions:",
      repr(
        exceptions
      ),
    )

  return (
    0
    if (
      not affected
      and not exceptions
    )
    else 1
  )


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
