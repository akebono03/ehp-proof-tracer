from __future__ import annotations

import toda_group_proof_narrative_contribution_renderer as contribution_module
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


TARGET = (
  r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
)


def _presentation():
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
  return build_toda_group_proof_presentation(
    replay
  )


def _target_paragraphs(
  markdown: str,
):
  return tuple(
    (
      index,
      paragraph.strip(),
    )
    for index, paragraph in enumerate(
      markdown.split(
        "\n\n"
      )
    )
    if TARGET in paragraph
  )


def _print_stage(
  label: str,
  markdown: str,
) -> None:
  matches = _target_paragraphs(
    markdown
  )
  print("")
  print("=" * 78)
  print(label)
  print("=" * 78)
  print(
    "target occurrence count:",
    markdown.count(
      TARGET
    ),
  )
  print(
    "matching paragraph count:",
    len(
      matches
    ),
  )

  for index, paragraph in matches:
    print("")
    print(
      f"[paragraph {index}]"
    )
    print(
      paragraph
    )


def main() -> None:
  presentation = _presentation()
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=semantic_sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=semantic_sidecar,
    )
  )

  final_public = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  _print_stage(
    "FINAL PUBLIC NARRATIVE",
    final_public,
  )

  original_insert = (
    contribution_module
    .insert_toda_group_proof_narrative_map_property_dependencies
  )
  original_dedup = (
    contribution_module
    .suppress_toda_group_proof_narrative_repeated_unique_step_statements
  )
  original_order = (
    contribution_module
    .order_toda_group_proof_narrative_injective_image_order_reason
  )

  counters = {
    "insert": 0,
    "dedup": 0,
    "order": 0,
  }

  def traced_insert(
    presentation,
    markdown,
    reference_entries=(),
  ):
    counters["insert"] += 1
    before = markdown
    after = original_insert(
      presentation,
      markdown,
      reference_entries,
    )
    _print_stage(
      (
        "insert_toda_group_proof_narrative_"
        "map_property_dependencies "
        f"call {counters['insert']} BEFORE"
      ),
      before,
    )
    _print_stage(
      (
        "insert_toda_group_proof_narrative_"
        "map_property_dependencies "
        f"call {counters['insert']} AFTER"
      ),
      after,
    )
    return after

  def traced_dedup(
    presentation,
    markdown,
  ):
    counters["dedup"] += 1
    before = markdown
    after = original_dedup(
      presentation,
      markdown,
    )
    _print_stage(
      (
        "suppress_toda_group_proof_narrative_"
        "repeated_unique_step_statements "
        f"call {counters['dedup']} BEFORE"
      ),
      before,
    )
    _print_stage(
      (
        "suppress_toda_group_proof_narrative_"
        "repeated_unique_step_statements "
        f"call {counters['dedup']} AFTER"
      ),
      after,
    )
    return after

  def traced_order(
    markdown,
    reason_sidecar,
  ):
    counters["order"] += 1
    before = markdown
    after = original_order(
      markdown,
      reason_sidecar,
    )
    _print_stage(
      (
        "order_toda_group_proof_narrative_"
        "injective_image_order_reason "
        f"call {counters['order']} BEFORE"
      ),
      before,
    )
    _print_stage(
      (
        "order_toda_group_proof_narrative_"
        "injective_image_order_reason "
        f"call {counters['order']} AFTER"
      ),
      after,
    )
    return after

  contribution_module.insert_toda_group_proof_narrative_map_property_dependencies = (
    traced_insert
  )
  contribution_module.suppress_toda_group_proof_narrative_repeated_unique_step_statements = (
    traced_dedup
  )
  contribution_module.order_toda_group_proof_narrative_injective_image_order_reason = (
    traced_order
  )

  print("")
  print("=" * 78)
  print("TRACE RUN")
  print("=" * 78)

  traced_rendered = (
    contribution_module
    .render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  _print_stage(
    "TRACE RENDERER FINAL OUTPUT",
    traced_rendered,
  )

  print("")
  print("=" * 78)
  print("CALL COUNTS")
  print("=" * 78)
  for key, value in counters.items():
    print(
      f"{key}: {value}"
    )


if __name__ == "__main__":
  main()
