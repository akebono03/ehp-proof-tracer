from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(REPO_ROOT),
  )


import toda_group_proof_narrative_contribution_renderer as contribution_renderer
import toda_group_proof_narrative_renderer as narrative_renderer

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _interesting_lines(
  text: str,
) -> tuple[str, ...]:
  return tuple(
    line
    for line in text.splitlines()
    if (
      "[R" in line
      or r"\pi_{n + 1}^{n}" in line
      or r"\pi_{4}^{3}" in line
      or "Proposition 5.1" in line
      or "(5.2)" in line
    )
  )


def _entry_summary(
  entries,
) -> tuple[
  tuple[
    int,
    str,
  ],
  ...,
]:
  return tuple(
    (
      entry.number,
      entry.reference.locator,
    )
    for entry in entries
  )


def _wrap_link(
  label: str,
  original,
):
  call_count = 0

  def wrapped(
    presentation,
    body_markdown,
    reference_entries,
  ):
    nonlocal call_count
    call_count += 1

    print()
    print(
      "=" * 78
    )
    print(
      f"{label} call {call_count} BEFORE"
    )
    print(
      "=" * 78
    )
    print(
      "entries:",
      _entry_summary(
        reference_entries
      ),
    )
    for line in _interesting_lines(
      body_markdown
    ):
      print(
        "  ",
        line,
      )

    result = original(
      presentation,
      body_markdown,
      reference_entries,
    )

    print()
    print(
      f"{label} call {call_count} AFTER"
    )
    print(
      "-" * 78
    )
    for line in _interesting_lines(
      result
    ):
      print(
        "  ",
        line,
      )

    return result

  return wrapped


def _wrap_suppress(
  label: str,
  original,
):
  call_count = 0

  def wrapped(
    body_markdown,
    statement_lines_by_reference_number,
  ):
    nonlocal call_count
    call_count += 1

    print()
    print(
      "=" * 78
    )
    print(
      f"{label} call {call_count} BEFORE"
    )
    print(
      "=" * 78
    )
    print(
      "statement numbers:",
      tuple(
        sorted(
          statement_lines_by_reference_number
        )
      ),
    )
    for line in _interesting_lines(
      body_markdown
    ):
      print(
        "  ",
        line,
      )

    result = original(
      body_markdown,
      statement_lines_by_reference_number,
    )

    print()
    print(
      f"{label} call {call_count} AFTER"
    )
    print(
      "-" * 78
    )
    for line in _interesting_lines(
      result
    ):
      print(
        "  ",
        line,
      )

    return result

  return wrapped


def _wrap_unmarked(
  label: str,
  original,
):
  call_count = 0

  def wrapped(
    presentation,
    body_markdown,
    reference_entries,
  ):
    nonlocal call_count
    call_count += 1

    print()
    print(
      "=" * 78
    )
    print(
      f"{label} call {call_count} BEFORE"
    )
    print(
      "=" * 78
    )
    print(
      "entries:",
      _entry_summary(
        reference_entries
      ),
    )
    for line in _interesting_lines(
      body_markdown
    ):
      print(
        "  ",
        line,
      )

    result = original(
      presentation,
      body_markdown,
      reference_entries,
    )

    print()
    print(
      f"{label} call {call_count} AFTER"
    )
    print(
      "-" * 78
    )
    for line in _interesting_lines(
      result
    ):
      print(
        "  ",
        line,
      )

    return result

  return wrapped


def main():
  original_contribution_link = (
    contribution_renderer
    .link_toda_group_proof_narrative_reference_body_consumers
  )
  original_narrative_link = (
    narrative_renderer
    .link_toda_group_proof_narrative_reference_body_consumers
  )
  original_contribution_suppress = (
    contribution_renderer
    .suppress_toda_group_proof_narrative_reference_body_duplicates
  )
  original_narrative_suppress = (
    narrative_renderer
    .suppress_toda_group_proof_narrative_reference_body_duplicates
  )

  contribution_renderer.link_toda_group_proof_narrative_reference_body_consumers = (
    _wrap_link(
      "CONTRIBUTION reference_body_consumers",
      original_contribution_link,
    )
  )
  narrative_renderer.link_toda_group_proof_narrative_reference_body_consumers = (
    _wrap_link(
      "NARRATIVE reference_body_consumers",
      original_narrative_link,
    )
  )
  contribution_renderer.suppress_toda_group_proof_narrative_reference_body_duplicates = (
    _wrap_suppress(
      "CONTRIBUTION reference_body_duplicates",
      original_contribution_suppress,
    )
  )
  narrative_renderer.suppress_toda_group_proof_narrative_reference_body_duplicates = (
    _wrap_suppress(
      "NARRATIVE reference_body_duplicates",
      original_narrative_suppress,
    )
  )

  if hasattr(
    contribution_renderer,
    "link_toda_group_proof_narrative_unmarked_reference_consumers",
  ):
    original_contribution_unmarked = (
      contribution_renderer
      .link_toda_group_proof_narrative_unmarked_reference_consumers
    )
    contribution_renderer.link_toda_group_proof_narrative_unmarked_reference_consumers = (
      _wrap_unmarked(
        "CONTRIBUTION unmarked_reference_consumers",
        original_contribution_unmarked,
      )
    )

  if hasattr(
    narrative_renderer,
    "link_toda_group_proof_narrative_unmarked_reference_consumers",
  ):
    original_narrative_unmarked = (
      narrative_renderer
      .link_toda_group_proof_narrative_unmarked_reference_consumers
    )
    narrative_renderer.link_toda_group_proof_narrative_unmarked_reference_consumers = (
      _wrap_unmarked(
        "NARRATIVE unmarked_reference_consumers",
        original_narrative_unmarked,
      )
    )

  report = build_standard_toda_report(
    n=2,
    k=2,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=3,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  print()
  print(
    "#" * 78
  )
  print(
    "START FINAL PUBLIC RENDER"
  )
  print(
    "#" * 78
  )

  rendered = (
    narrative_renderer
    .render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  print()
  print(
    "#" * 78
  )
  print(
    "FINAL PUBLIC NARRATIVE"
  )
  print(
    "#" * 78
  )
  print(
    rendered
  )

  reference, body = rendered.split(
    "---",
    1,
  )

  print()
  print(
    "#" * 78
  )
  print(
    "FINAL DIAGNOSTICS"
  )
  print(
    "#" * 78
  )
  print(
    "Proposition 5.1 header:",
    next(
      (
        line
        for line in reference.splitlines()
        if "Proposition 5.1" in line
      ),
      None,
    ),
  )
  print(
    "body marker lines:",
    tuple(
      line
      for line in body.splitlines()
      if "[R" in line
    ),
  )
  print(
    "body general Prop.5.1 count:",
    body.count(
      r"\pi_{n + 1}^{n}"
    ),
  )
  print(
    "body pi_4^3 lines:",
    tuple(
      line
      for line in body.splitlines()
      if r"\pi_{4}^{3}" in line
    ),
  )
  print()
  print(
    "Audit completed. Production changes: NONE"
  )


if __name__ == "__main__":
  main()
