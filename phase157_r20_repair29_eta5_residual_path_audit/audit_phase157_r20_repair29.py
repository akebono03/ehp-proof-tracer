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

import toda_group_proof_narrative_argument_body_renderer as body_renderer
import toda_group_proof_narrative_argument_multi_renderer as multi_renderer
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


TARGET = r"\eta_{5} = \eta_{5}"

original_helper = (
  body_renderer
  ._is_toda_group_proof_narrative_rendered_reflexive_equality_step
)
original_body = (
  body_renderer
  .render_toda_group_proof_narrative_argument_body_markdown
)


def target_paragraphs(
  markdown: str,
):
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


def traced_helper(
  proof_step,
):
  result = original_helper(
    proof_step
  )
  rendered = (
    body_renderer
    ._render_generic_narrative_step(
      proof_step
    )
  )

  if TARGET in rendered:
    print("")
    print("=" * 88)
    print("TARGET HELPER CHECK")
    print("=" * 88)
    print(
      "result:",
      result,
    )
    print(
      "rendered:",
      rendered,
    )
    print(
      "rule:",
      (
        None
        if proof_step.inference_rule is None
        else proof_step.inference_rule.name
      ),
    )

  return result


def traced_body(
  *args,
  **kwargs,
):
  result = original_body(
    *args,
    **kwargs,
  )

  if TARGET in result:
    print("")
    print("=" * 88)
    print("ARGUMENT BODY OUTPUT CONTAINS TARGET")
    print("=" * 88)
    for index, paragraph in target_paragraphs(
      result
    ):
      print(
        f"[{index}]",
        paragraph,
      )

  return result


def wrap_transform(
  name: str,
):
  original = getattr(
    contribution_renderer,
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
      else TARGET in before
    )
    after_has = (
      False
      if after is None
      else TARGET in after
    )

    if before_has or after_has:
      print("")
      print("=" * 88)
      print(name)
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
          after
        ):
          print(
            f"after [{index}]",
            paragraph,
          )

    return result

  setattr(
    contribution_renderer,
    name,
    wrapped,
  )


def main() -> int:
  body_renderer._is_toda_group_proof_narrative_rendered_reflexive_equality_step = (
    traced_helper
  )
  multi_renderer.render_toda_group_proof_narrative_argument_body_markdown = (
    traced_body
  )

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
    "insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges",
    "trim_toda_group_proof_narrative_redundant_left_ehp_terms",
    "normalize_toda_group_proof_narrative_repeated_numeric_equalities",
    "link_toda_group_proof_narrative_unmarked_reference_consumers",
    "suppress_toda_group_proof_narrative_reflexive_equalities",
    "order_toda_group_proof_narrative_surjectivity_support",
  )

  for name in candidates:
    if hasattr(
      contribution_renderer,
      name,
    ):
      wrap_transform(
        name
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
    TARGET in rendered,
  )

  for index, paragraph in target_paragraphs(
    rendered
  ):
    print(
      f"[{index}]",
      paragraph,
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
