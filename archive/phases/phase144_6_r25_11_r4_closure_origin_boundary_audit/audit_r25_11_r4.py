from collections import Counter
import importlib.util
from pathlib import Path
import sys

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_aggregate_semantics import (
  build_toda_group_proof_narrative_aggregate_semantic_sidecar,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_proof_dependency import (
  extract_toda_recursive_proof_provenance,
)

import toda_group_proof_narrative_contribution_ordering as ordering
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)


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
  name = "_r25_11_r4_" + path.stem
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


def step_signature(step):
  return (
    type(step.conclusion).__name__,
    (
      "<none>"
      if step.inference_rule is None
      else step.inference_rule.name
    ),
    _render_generic_narrative_step(step),
  )


def presentation_step_ids(presentation):
  return frozenset(
    id(node.proof_step)
    for node in presentation.nodes
  )


def build_depth2_pi6():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report.candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  original = build_toda_group_proof_presentation(
    replay
  )
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      original
    )
  )
  return group_result, original, closure


def build_context(presentation):
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=semantic_sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=semantic_sidecar,
  )
  aggregate = (
    build_toda_group_proof_narrative_aggregate_semantic_sidecar(
      presentation
    )
  )
  chains = build_toda_group_proof_narrative_proof_chains(
    presentation,
    semantic_sidecar,
    arguments,
    aggregate_semantic_sidecar=aggregate,
  )
  base = render_toda_group_proof_narrative_multi_argument_markdown(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  )
  occurrences = ordering._build_visibility_occurrences(
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    chains,
    current_markdown=base,
  )
  ordered = (
    ordering.build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      chains,
      current_markdown=base,
    )
  )
  return (
    semantic_sidecar,
    blocks,
    arguments,
    chains,
    base,
    occurrences,
    ordered,
  )


def print_step(label, step, original_ids):
  print(label)
  print(
    "  origin="
    + (
      "original"
      if id(step) in original_ids
      else "closure_added"
    )
  )
  print(
    "  type="
    + type(step.conclusion).__name__
  )
  print(
    "  rule="
    + (
      "<none>"
      if step.inference_rule is None
      else step.inference_rule.name
    )
  )
  print(
    "  rendered="
    + _render_generic_narrative_step(step)
  )
  print(
    "  premise_count="
    + str(len(step.premises))
  )


def audit_depth2_closure():
  print("=" * 78)
  print("A. depth=2 pi_6^3 semantic-closure origin boundary")
  print("=" * 78)

  group_result, original, closure = build_depth2_pi6()
  original_ids = presentation_step_ids(
    original
  )
  closure_ids = presentation_step_ids(
    closure
  )
  added_ids = closure_ids - original_ids

  print(
    f"original_nodes={len(original.nodes)} "
    f"closure_nodes={len(closure.nodes)} "
    f"closure_added={len(added_ids)}"
  )
  print(
    "identity_preserved_for_original="
    + str(
      original_ids.issubset(
        closure_ids
      )
    )
  )

  added_steps = tuple(
    node.proof_step
    for node in closure.nodes
    if id(node.proof_step) in added_ids
  )
  for index, step in enumerate(
    added_steps
  ):
    print_step(
      f"closure_added[{index}]",
      step,
      original_ids,
    )

  provenance = (
    extract_toda_recursive_proof_provenance(
      group_result
    )
  )
  print()
  print("Consumers of closure-added steps:")
  for step in added_steps:
    consumers = tuple(
      edge
      for edge in provenance.edges
      if edge.premise_step is step
    )
    print(
      f"  {step_signature(step)} "
      f"consumer_count={len(consumers)}"
    )
    for edge in consumers:
      print(
        "    consumer_rule="
        + (
          "<none>"
          if edge.parent_step.inference_rule is None
          else edge.parent_step.inference_rule.name
        )
        + f" premise_index={edge.premise_index}"
      )

  return original, closure, original_ids


def audit_depth2_ownership(
  original,
  closure,
  original_ids,
):
  print()
  print("=" * 78)
  print("B. depth=2 ownership before/after closure")
  print("=" * 78)

  for label, presentation in (
    ("original", original),
    ("closure", closure),
  ):
    (
      _sidecar,
      _blocks,
      arguments,
      _chains,
      _base,
      occurrences,
      ordered,
    ) = build_context(
      presentation
    )

    selected = tuple(
      contribution
      for rows in ordered
      for contribution in rows
    )

    print()
    print(
      f"{label}: arguments={len(arguments)} "
      f"occurrences={len(occurrences)} "
      f"selected={len(selected)}"
    )

    origins = Counter(
      (
        "original"
        if id(row.proof_step) in original_ids
        else "closure_added"
      )
      for row in occurrences
    )
    print(
      "  occurrence_origins="
      + repr(dict(origins))
    )

    selected_origins = Counter(
      (
        "original"
        if id(row.proof_step) in original_ids
        else "closure_added"
      )
      for row in selected
    )
    print(
      "  selected_origins="
      + repr(dict(selected_origins))
    )

    for argument_index, rows in enumerate(
      ordered
    ):
      if not rows:
        continue
      print(
        f"  argument[{argument_index}] "
        f"role={arguments[argument_index].role.value}"
      )
      for row in rows:
        origin = (
          "original"
          if id(row.proof_step) in original_ids
          else "closure_added"
        )
        print(
          "    "
          f"origin={origin} "
          f"type={type(row.proof_step.conclusion).__name__} "
          f"anchor={row.provider_anchor} "
          f"placement={row.placement.value} "
          f"providers={len(row.provider_keys)} "
          f"distance={row.distance_to_conclusion}"
        )
        print(
          "      "
          + _render_generic_narrative_step(
            row.proof_step
          )
        )


def audit_full_depth_boundary():
  print()
  print("=" * 78)
  print("C. full-depth six-group boundary")
  print("=" * 78)
  print(
    "This section does not apply semantic closure. "
    "It verifies whether the 192-vs-190 issue is a "
    "separate full-depth ownership regression."
  )

  total = 0
  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      _aggregate,
      chains,
    ) = foundation._context(
      n,
      k,
    )
    base = render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
    ordered = (
      ordering.build_toda_group_proof_narrative_ordered_contributions(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        chains,
        current_markdown=base,
      )
    )
    selected = sum(
      len(rows)
      for rows in ordered
    )
    total += selected
    print(
      f"pi_{n+k}^{n}: selected={selected}"
    )

  print(
    f"FULL_DEPTH_TOTAL={total}"
  )
  print(
    "EXPECTED_PRE_REGRESSION_TOTAL=190"
  )
  print(
    f"FULL_DEPTH_DELTA={total - 190:+d}"
  )


def main():
  original, closure, original_ids = (
    audit_depth2_closure()
  )
  audit_depth2_ownership(
    original,
    closure,
    original_ids,
  )
  audit_full_depth_boundary()

  print()
  print("=" * 78)
  print("R25-11-R4 closure-origin boundary audit complete.")
  print("Production changes: none.")
  print("Existing test changes: none.")
  print("Full pytest: not run.")
  print("=" * 78)


if __name__ == "__main__":
  main()
