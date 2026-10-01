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
from toda_group_proof_narrative_references import (
  extract_toda_group_proof_step_literature_reference,
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


EXPECTED_GROUPS = 112
REFERENCE_HEADER_RE = re.compile(
  r"\*\*\[R([0-9]+)\] ([^\n]+?)\.\*\*"
)
REFERENCE_MARKER_RE = re.compile(
  r"\[R([0-9]+)\]"
)


def _build_presentation(
  n: int,
  k: int,
):
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
  return build_toda_group_proof_presentation(
    replay
  )


def _reference_headers(
  rendered: str,
) -> tuple[
  tuple[
    int,
    str,
  ],
  ...,
]:
  return tuple(
    (
      int(
        match.group(
          1
        )
      ),
      match.group(
        2
      ),
    )
    for match in REFERENCE_HEADER_RE.finditer(
      rendered
    )
  )


def _body_markers(
  rendered: str,
  header_numbers: tuple[
    int,
    ...,
  ],
) -> tuple[
  int,
  ...,
]:
  all_numbers = [
    int(
      match.group(
        1
      )
    )
    for match in REFERENCE_MARKER_RE.finditer(
      rendered
    )
  ]

  remaining = list(
    all_numbers
  )

  for header_number in header_numbers:
    try:
      remaining.remove(
        header_number
      )
    except ValueError:
      pass

  return tuple(
    remaining
  )


def _root_locator(
  presentation,
) -> str | None:
  reference = (
    extract_toda_group_proof_step_literature_reference(
      presentation.root_step
    )
  )

  if reference is None:
    return None

  return (
    reference.locator
    or reference.label
  )


def main() -> None:
  errors = []
  violations = []

  scanned_groups = 0
  groups_with_references = 0
  groups_with_body_markers = 0
  groups_without_body_markers = 0
  total_reference_headers = 0
  total_body_markers = 0
  max_reference_count = 0
  max_reference_groups = []

  for k in range(
    8
  ):
    for n in range(
      2,
      16,
    ):
      group_name = (
        f"pi_{n + k}^{n}"
      )

      try:
        presentation = (
          _build_presentation(
            n,
            k,
          )
        )
        rendered = (
          render_toda_group_proof_narrative_markdown(
            presentation
          )
        )
      except Exception as exc:
        errors.append(
          (
            group_name,
            type(
              exc
            ).__name__,
            str(
              exc
            ),
          )
        )
        continue

      scanned_groups += 1

      headers = (
        _reference_headers(
          rendered
        )
      )
      header_numbers = tuple(
        number
        for number, _ in headers
      )
      header_titles = tuple(
        title
        for _, title in headers
      )
      body_markers = (
        _body_markers(
          rendered,
          header_numbers,
        )
      )
      root_locator = (
        _root_locator(
          presentation
        )
      )

      if headers:
        groups_with_references += 1

      if body_markers:
        groups_with_body_markers += 1
      elif headers:
        groups_without_body_markers += 1

      total_reference_headers += len(
        headers
      )
      total_body_markers += len(
        body_markers
      )

      if len(
        headers
      ) > max_reference_count:
        max_reference_count = len(
          headers
        )
        max_reference_groups = [
          group_name
        ]
      elif (
        headers
        and len(
          headers
        ) == max_reference_count
      ):
        max_reference_groups.append(
          group_name
        )

      expected_numbers = tuple(
        range(
          1,
          len(
            headers
          )
          + 1,
        )
      )

      if header_numbers != expected_numbers:
        violations.append(
          (
            group_name,
            "non_contiguous_reference_numbers",
            header_numbers,
          )
        )

      if len(
        set(
          header_numbers
        )
      ) != len(
        header_numbers
      ):
        violations.append(
          (
            group_name,
            "duplicate_reference_numbers",
            header_numbers,
          )
        )

      if len(
        set(
          header_titles
        )
      ) != len(
        header_titles
      ):
        violations.append(
          (
            group_name,
            "duplicate_reference_titles",
            header_titles,
          )
        )

      if (
        root_locator is not None
        and root_locator in header_titles
      ):
        violations.append(
          (
            group_name,
            "root_reference_in_reference_section",
            root_locator,
          )
        )

      header_number_set = set(
        header_numbers
      )
      body_marker_set = set(
        body_markers
      )

      unknown_body_markers = (
        body_marker_set
        - header_number_set
      )

      if unknown_body_markers:
        violations.append(
          (
            group_name,
            "body_marker_without_reference",
            tuple(
              sorted(
                unknown_body_markers
              )
            ),
          )
        )

      if body_markers:
        unused_reference_numbers = (
          header_number_set
          - body_marker_set
        )

        if unused_reference_numbers:
          violations.append(
            (
              group_name,
              "marker_route_unused_reference",
              tuple(
                sorted(
                  unused_reference_numbers
                )
              ),
            )
          )

  print(
    "=" * 78
  )
  print(
    "Phase 153 closure audit"
  )
  print(
    "Reference selection / granularity / reuse / filtering"
  )
  print(
    "range: n=2..15, k=0..7, depth=2"
  )
  print(
    "=" * 78
  )
  print(
    "scanned groups:",
    scanned_groups,
  )
  print(
    "render errors:",
    len(
      errors
    ),
  )
  print(
    "groups with Reference section:",
    groups_with_references,
  )
  print(
    "marker-bearing groups:",
    groups_with_body_markers,
  )
  print(
    "generic/reference-only groups:",
    groups_without_body_markers,
  )
  print(
    "Reference headers:",
    total_reference_headers,
  )
  print(
    "body Reference markers:",
    total_body_markers,
  )
  print(
    "maximum References in one group:",
    max_reference_count,
  )
  print(
    "groups at maximum:",
    ", ".join(
      max_reference_groups
    )
    if max_reference_groups
    else "(none)",
  )
  print(
    "violations:",
    len(
      violations
    ),
  )

  if errors:
    print()
    print(
      "Render errors:"
    )
    for error in errors[
      :30
    ]:
      print(
        "  -",
        error,
      )

  if violations:
    print()
    print(
      "Reference invariant violations:"
    )
    for violation in violations[
      :100
    ]:
      print(
        "  -",
        violation,
      )

  print()
  print(
    "=" * 78
  )

  if (
    scanned_groups
    == EXPECTED_GROUPS
    and not errors
    and not violations
  ):
    print(
      "PASS"
    )
    print(
      "All 112 depth-2 group Narratives satisfy the "
      "Phase 153 Reference invariants."
    )
    print(
      "Next boundary: Phase 153 final full pytest."
    )
    return

  print(
    "FAIL"
  )
  print(
    "Phase 153 is not ready for final full pytest."
  )
  raise SystemExit(
    1
  )


if __name__ == "__main__":
  main()
