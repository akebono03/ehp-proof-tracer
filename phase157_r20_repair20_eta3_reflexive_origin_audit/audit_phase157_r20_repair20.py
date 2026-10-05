from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

if str(REPOSITORY_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPOSITORY_ROOT
    ),
  )

import toda_group_proof_narrative_contribution_renderer as renderer

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


TARGET = r"\eta_{3}^{3} = \eta_{3}^{3}"


def contains_target(markdown: str) -> bool:
  return TARGET in markdown


def target_paragraphs(markdown: str):
  return tuple(
    (
      index,
      paragraph,
    )
    for index, paragraph in enumerate(
      markdown.split(
        "\n\n"
      )
    )
    if TARGET in paragraph
  )


def wrap_markdown_transform(
  name: str,
):
  original = getattr(
    renderer,
    name,
  )

  def wrapped(*args, **kwargs):
    before = next(
      (
        arg
        for arg in args
        if isinstance(
          arg,
          str,
        )
      ),
      None,
    )

    result = original(
      *args,
      **kwargs,
    )

    after = (
      result
      if isinstance(
        result,
        str,
      )
      else None
    )

    before_has = (
      False
      if before is None
      else contains_target(
        before
      )
    )
    after_has = (
      False
      if after is None
      else contains_target(
        after
      )
    )

    if (
      before_has
      or after_has
    ):
      print("")
      print("=" * 88)
      print(
        name
      )
      print("=" * 88)
      print(
        "before:",
        before_has,
      )
      print(
        "after:",
        after_has,
      )

      if before_has:
        print(
          "before paragraphs:"
        )
        for index, paragraph in target_paragraphs(
          before
        ):
          print(
            f"  [{index}] {paragraph}"
          )

      if after_has:
        print(
          "after paragraphs:"
        )
        for index, paragraph in target_paragraphs(
          after
        ):
          print(
            f"  [{index}] {paragraph}"
          )

    return result

  setattr(
    renderer,
    name,
    wrapped,
  )


def wrap_contribution_insertion():
  name = (
    "_insert_toda_group_proof_narrative_argument_contributions"
  )
  original = getattr(
    renderer,
    name,
  )

  def wrapped(
    presentation,
    markdown,
    blocks,
    arguments,
    ordered_contributions,
  ):
    before_has = contains_target(
      markdown
    )

    result = original(
      presentation,
      markdown,
      blocks,
      arguments,
      ordered_contributions,
    )

    after_has = contains_target(
      result
    )

    print("")
    print("=" * 88)
    print(
      name
    )
    print("=" * 88)
    print(
      "before:",
      before_has,
    )
    print(
      "after:",
      after_has,
    )

    if after_has:
      for index, paragraph in target_paragraphs(
        result
      ):
        print(
          f"  [{index}] {paragraph}"
        )

    return result

  setattr(
    renderer,
    name,
    wrapped,
  )


def main() -> int:
  candidates = (
    "insert_toda_group_proof_narrative_reason_prose",
    "suppress_toda_group_proof_narrative_reference_internal_body",
    "suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry",
    "suppress_toda_group_proof_narrative_reference_body_duplicates",
    "link_toda_group_proof_narrative_reference_body_consumers",
    "normalize_toda_group_proof_narrative_connectors",
    "order_toda_group_proof_narrative_local_equation_derivations",
    "order_toda_group_proof_narrative_order_support",
    "insert_toda_group_proof_narrative_hidden_zero_map_premises",
    "trim_toda_group_proof_narrative_redundant_left_ehp_terms",
    "normalize_toda_group_proof_narrative_repeated_numeric_equalities",
    "link_toda_group_proof_narrative_unmarked_reference_consumers",
    "suppress_toda_group_proof_narrative_reflexive_equalities",
    "order_toda_group_proof_narrative_surjectivity_support",
    "insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges",
  )

  wrapped_names = []

  for name in candidates:
    if not hasattr(
      renderer,
      name,
    ):
      continue

    wrap_markdown_transform(
      name
    )
    wrapped_names.append(
      name
    )

  wrap_contribution_insertion()

  print(
    "Repository root:",
    REPOSITORY_ROOT,
  )
  print(
    "Wrapped transforms:",
    len(
      wrapped_names
    )
    + 1,
  )

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
  presentation = build_toda_group_proof_presentation(
    replay
  )

  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  print("")
  print("=" * 88)
  print("FINAL")
  print("=" * 88)
  print(
    "target present:",
    contains_target(
      rendered
    ),
  )

  for index, paragraph in target_paragraphs(
    rendered
  ):
    print(
      f"[{index}] {paragraph}"
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
