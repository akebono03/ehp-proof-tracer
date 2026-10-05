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
  presentation = build_toda_group_proof_presentation(
    replay
  )
  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def _connector_numbers(
  rendered: str,
) -> set[int]:
  result = set()

  for line in rendered.splitlines():
    stripped = line.strip()

    if (
      not stripped.startswith(
        "("
      )
      or "より," not in stripped
    ):
      continue

    result.update(
      int(
        value
      )
      for value in re.findall(
        r"\((\d+)\)",
        stripped,
      )
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

      lines = rendered.splitlines()

      standalone_period = sum(
        1
        for line in lines
        if line.strip() == "."
      )
      ambiguous = sum(
        1
        for line in lines
        if "この群構造と" in line
      )

      tags = tuple(
        int(
          value
        )
        for value in TAG_RE.findall(
          rendered
        )
      )
      references = (
        _connector_numbers(
          rendered
        )
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

  print(
    "=" * 78
  )
  print(
    "Phase 158-R4-R2 112-group re-audit"
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
      not exceptions
      and not affected
    )
    else 1
  )


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
