from collections import Counter
import importlib.util
from pathlib import Path
import sys

from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_discourse import (
  classify_toda_group_proof_narrative_argument_discourse_roles,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
import toda_group_proof_narrative_contribution_ordering as ordering


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


def load_test_module(filename: str):
  path = Path("tests") / filename
  name = "_r25_11_r3_" + path.stem
  if name in sys.modules:
    return sys.modules[name]
  spec = importlib.util.spec_from_file_location(name, path)
  if spec is None or spec.loader is None:
    raise ImportError(f"cannot load {path}")
  module = importlib.util.module_from_spec(spec)
  sys.modules[name] = module
  spec.loader.exec_module(module)
  return module


foundation = load_test_module(
  "test_phase144_6_r5_18_production_generic_proof_chain_foundation.py"
)


def context(n: int, k: int):
  return foundation._context(n, k)


def selected_rows(n: int, k: int):
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    _aggregate,
    chains,
  ) = context(n, k)
  base = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  )
  ordered = ordering.build_toda_group_proof_narrative_ordered_contributions(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    chains,
    current_markdown=base,
  )
  return (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    chains,
    base,
    ordered,
  )


def describe_selected():
  print("=" * 78)
  print("A. Lightweight selected-contribution inventory")
  print("=" * 78)
  total = 0
  for n, k in TARGETS:
    (
      _presentation,
      _semantic_sidecar,
      _blocks,
      arguments,
      _chains,
      _base,
      ordered,
    ) = selected_rows(n, k)
    count = sum(len(rows) for rows in ordered)
    total += count
    populated = tuple(
      index
      for index, rows in enumerate(ordered)
      if rows
    )
    print(
      f"pi_{n+k}^{n}: selected={count} "
      f"arguments={len(arguments)} populated={populated}"
    )
  print(f"TOTAL_SELECTED={total}")
  print("EXPECTED_PRE_REGRESSION_TOTAL=190")
  print(f"DELTA={total - 190:+d}")


def describe_occurrences():
  print()
  print("=" * 78)
  print("B. Selected owners and raw visibility occurrences")
  print("=" * 78)

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      chains,
      base,
      ordered,
    ) = selected_rows(n, k)

    discourse = classify_toda_group_proof_narrative_argument_discourse_roles(
      arguments
    )
    occurrences = ordering._build_visibility_occurrences(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      chains,
      current_markdown=base,
    )

    print()
    print(f"--- pi_{n+k}^{n} ---")
    print(
      f"raw_occurrences={len(occurrences)} "
      f"selected={sum(len(rows) for rows in ordered)}"
    )

    occurrence_counts = Counter(
      (
        type(row.proof_step.conclusion).__name__,
        row.argument_index,
        row.provider_anchor,
      )
      for row in occurrences
    )
    print("raw occurrence classes:")
    for key, count in sorted(
      occurrence_counts.items(),
      key=lambda item: str(item[0]),
    ):
      print(f"  {key}: {count}")

    for argument_index, rows in enumerate(ordered):
      if not rows:
        continue
      print(
        f"argument[{argument_index}] "
        f"role={arguments[argument_index].role.value} "
        f"discourse={discourse[argument_index].value}"
      )
      for index, row in enumerate(rows):
        step = row.proof_step
        print(f"  selected[{index}]")
        print(
          "    type="
          + type(step.conclusion).__name__
        )
        print(
          "    rule="
          + (
            "<none>"
            if step.inference_rule is None
            else step.inference_rule.name
          )
        )
        print(
          f"    provider_anchor={row.provider_anchor}"
        )
        print(
          f"    placement={row.placement.value}"
        )
        print(
          f"    distance={row.distance_to_conclusion}"
        )
        print(
          f"    provider_key_count={len(row.provider_keys)}"
        )
        print(
          "    rendered="
          + _render_generic_narrative_step(step)
        )


def describe_pi6_order_extra():
  print()
  print("=" * 78)
  print("C. pi_6^3 order-argument ownership trace")
  print("=" * 78)

  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    chains,
    base,
    ordered,
  ) = selected_rows(3, 3)

  occurrences = ordering._build_visibility_occurrences(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    chains,
    current_markdown=base,
  )

  for index, argument in enumerate(arguments):
    print(
      f"argument[{index}] role={argument.role.value}"
    )
    local_body = ordering.extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      index,
    )
    hidden = ordering._effective_hidden_step_ids(
      presentation,
      blocks,
      local_body,
      semantic_sidecar,
      argument,
    )
    conclusion = ordering.extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
    if conclusion is None:
      continue
    chain_ids, anchors, distances, necessity = ordering._necessity_for_chain(
      presentation,
      local_body,
      chains[index],
      conclusion,
    )
    print(
      f"  local_steps={sum(len(block.steps) for block in local_body)} "
      f"hidden={len(hidden)} chain={len(chain_ids)} anchors={len(anchors)}"
    )
    for occurrence in occurrences:
      if occurrence.argument_index != index:
        continue
      step_id = id(occurrence.proof_step)
      print(
        "  occurrence "
        f"type={type(occurrence.proof_step.conclusion).__name__} "
        f"anchor={occurrence.provider_anchor} "
        f"distance={distances.get(step_id)} "
        f"necessity={len(necessity.get(step_id, ()))} "
        f"providers={len(occurrence.provider_keys)}"
      )


def main() -> None:
  describe_selected()
  describe_occurrences()
  describe_pi6_order_extra()
  print()
  print("=" * 78)
  print("R25-11-R3 diagnosis complete.")
  print("No production repair was applied after rollback.")
  print("No full pytest was run.")
  print("=" * 78)


if __name__ == "__main__":
  main()
