from __future__ import annotations

import functools
import inspect
import re

import toda_group_proof_narrative_contribution_renderer as contribution_renderer
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


TARGET_PATTERNS = (
  r"2\nu' = \eta_{3}^{3}",
  r"2\nu' = \eta_{3}^{3}\tag{",
)

CANDIDATE_FUNCTIONS = (
  "normalize_toda_group_proof_narrative_connectors",
  "normalize_toda_group_proof_narrative_repeated_numeric_equalities",
  "link_toda_group_proof_narrative_unmarked_reference_consumers",
  "suppress_toda_group_proof_narrative_reflexive_equalities",
  "order_toda_group_proof_narrative_surjectivity_support",
  "order_toda_group_proof_narrative_short_exact_support",
  "suppress_toda_group_proof_narrative_repeated_reference_restatements",
  "suppress_toda_group_proof_narrative_dangling_connectors",
  "order_toda_group_proof_narrative_visible_relation_dependencies",
  "suppress_toda_group_proof_narrative_repeated_unique_step_statements",
  "insert_toda_group_proof_narrative_map_property_dependencies",
  "order_toda_group_proof_narrative_injective_image_order_reason",
  "suppress_toda_group_proof_narrative_literal_reflexive_equalities",
  "filter_toda_group_proof_narrative_reference_entries_by_body_usage",
  "restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage",
)


def _contains_target(
  text: str,
) -> bool:
  return any(
    pattern in text
    for pattern in TARGET_PATTERNS
  )


def _strings_from_value(
  value,
):
  if isinstance(
    value,
    str,
  ):
    yield value
    return

  if isinstance(
    value,
    tuple,
  ):
    for item in value:
      yield from _strings_from_value(
        item
      )


def _first_markdown_string(
  args,
  kwargs,
) -> str | None:
  candidates = []

  for value in args:
    candidates.extend(
      _strings_from_value(
        value
      )
    )

  for value in kwargs.values():
    candidates.extend(
      _strings_from_value(
        value
      )
    )

  markdown_candidates = tuple(
    text
    for text in candidates
    if (
      "\n" in text
      or "$" in text
    )
  )

  if not markdown_candidates:
    return None

  return max(
    markdown_candidates,
    key=len,
  )


def _output_markdown_string(
  result,
) -> str | None:
  strings = tuple(
    _strings_from_value(
      result
    )
  )

  markdown_candidates = tuple(
    text
    for text in strings
    if (
      "\n" in text
      or "$" in text
    )
  )

  if not markdown_candidates:
    return None

  return max(
    markdown_candidates,
    key=len,
  )


def _wrap_stage(
  name: str,
) -> None:
  original = getattr(
    contribution_renderer,
    name,
    None,
  )

  if original is None:
    print(
      f"SKIP {name}: not present"
    )
    return

  if not callable(
    original
  ):
    print(
      f"SKIP {name}: not callable"
    )
    return

  @functools.wraps(
    original
  )
  def wrapper(
    *args,
    **kwargs,
  ):
    before_text = (
      _first_markdown_string(
        args,
        kwargs,
      )
    )
    before = (
      _contains_target(
        before_text
      )
      if before_text is not None
      else None
    )

    result = original(
      *args,
      **kwargs,
    )

    after_text = (
      _output_markdown_string(
        result
      )
    )
    after = (
      _contains_target(
        after_text
      )
      if after_text is not None
      else None
    )

    if (
      before is not None
      or after is not None
    ):
      print(
        "STAGE "
        + name
        + ": before="
        + str(
          before
        )
        + " after="
        + str(
          after
        )
      )

    if (
      before is True
      and after is False
    ):
      print(
        ">>> FIRST OBSERVED DROP CANDIDATE: "
        + name
      )

    return result

  setattr(
    contribution_renderer,
    name,
    wrapper,
  )


def _render_pi6_3() -> str:
  report = build_standard_toda_report(
    n=3,
    k=3,
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


def main() -> int:
  print(
    "Phase 159 R1-7c R4 repair9 "
    "R9-A stage audit"
  )
  print(
    "Production changes: none"
  )
  print()

  for name in CANDIDATE_FUNCTIONS:
    _wrap_stage(
      name
    )

  print()
  print(
    "=== render pi_6^3 ==="
  )
  rendered = _render_pi6_3()

  print()
  print(
    "=== final ==="
  )
  print(
    "double_nu_prime=",
    int(
      _contains_target(
        rendered
      )
    ),
    sep="",
  )

  compact = re.sub(
    r"\s+",
    "",
    rendered,
  )
  print(
    "eta5_reflexive=",
    int(
      r"$\eta_{5}=\eta_{5}$"
      in compact
    ),
    sep="",
  )

  print()
  print(
    "Relevant final lines:"
  )
  for line in rendered.splitlines():
    if (
      r"\nu'" in line
      or r"\eta_{3}^{3}" in line
      or r"\eta_{5}" in line
    ):
      print(
        line
      )

  return 0


if __name__ == "__main__":
    raise SystemExit(
      main()
    )
