from pathlib import Path
import sys


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
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_literature_statement_boundary import (
  classify_toda_literature_statement_step,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)


TARGET_RULES = (
  "Toda Proposition 5.3 n=3 Hopf eta_5 surjectivity",
  "Toda 5.3 nu-prime Lemma 5.2 Hopf specialization",
  "Toda Lemma 5.4 pi_6^5 finite-cyclic specialization",
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


def _walk_recursive(
  root_step,
):
  stack = [
    root_step,
  ]
  visited = set()
  ordered = []

  while stack:
    step = stack.pop()
    step_id = id(
      step
    )

    if step_id in visited:
      continue

    visited.add(
      step_id
    )
    ordered.append(
      step
    )
    stack.extend(
      reversed(
        step.premises
      )
    )

  return tuple(
    ordered
  )


def _rule_name(
  step,
):
  rule = step.inference_rule
  return (
    None
    if rule is None
    else rule.name
  )


def _reference_info(
  step,
):
  boundary = classify_toda_literature_statement_step(
    step
  )

  if boundary is None:
    return (
      None,
      None,
      None,
    )

  return (
    boundary.reference_locator,
    boundary.component_key,
    boundary.classification.value,
  )


def _print_step(
  label,
  step,
  presentation,
  recursive_steps,
):
  presentation_node_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }
  presentation_edge_child_ids = {
    id(
      edge.premise_step
    )
    for edge in presentation.edges
  }
  presentation_edge_parent_ids = {
    id(
      edge.parent_step
    )
    for edge in presentation.edges
  }

  recursive_consumers = tuple(
    candidate
    for candidate in recursive_steps
    if any(
      premise is step
      for premise in candidate.premises
    )
  )

  graph_consumers = tuple(
    edge.parent_step
    for edge in presentation.edges
    if edge.premise_step is step
  )

  print()
  print(label)
  print("-" * len(label))
  print(
    f"id={id(step)}"
  )
  print(
    f"rule={_rule_name(step)!r}"
  )
  print(
    f"rendered={_render_generic_narrative_step(step)!r}"
  )
  locator, component, classification = _reference_info(
    step
  )
  print(
    "boundary="
    f"locator={locator!r} "
    f"component={component!r} "
    f"classification={classification!r}"
  )
  print(
    f"in_presentation_nodes={id(step) in presentation_node_ids}"
  )
  print(
    f"in_presentation_edge_premises={id(step) in presentation_edge_child_ids}"
  )
  print(
    f"in_presentation_edge_parents={id(step) in presentation_edge_parent_ids}"
  )

  print(
    f"direct_premises={len(step.premises)}"
  )
  for index, premise in enumerate(
    step.premises,
    start=1,
  ):
    p_locator, p_component, _ = _reference_info(
      premise
    )
    print(
      f"  premise[{index}]: "
      f"rule={_rule_name(premise)!r} "
      f"locator={p_locator!r} "
      f"component={p_component!r} "
      f"rendered={_render_generic_narrative_step(premise)!r}"
    )

  print(
    f"recursive_direct_consumers={len(recursive_consumers)}"
  )
  for index, consumer in enumerate(
    recursive_consumers,
    start=1,
  ):
    c_locator, c_component, _ = _reference_info(
      consumer
    )
    print(
      f"  recursive_consumer[{index}]: "
      f"rule={_rule_name(consumer)!r} "
      f"locator={c_locator!r} "
      f"component={c_component!r} "
      f"rendered={_render_generic_narrative_step(consumer)!r}"
    )

  print(
    f"presentation_graph_consumers={len(graph_consumers)}"
  )
  for index, consumer in enumerate(
    graph_consumers,
    start=1,
  ):
    c_locator, c_component, _ = _reference_info(
      consumer
    )
    print(
      f"  graph_consumer[{index}]: "
      f"rule={_rule_name(consumer)!r} "
      f"locator={c_locator!r} "
      f"component={c_component!r} "
      f"rendered={_render_generic_narrative_step(consumer)!r}"
    )


def _source_occurrences(
  rule_name,
):
  occurrences = []

  for path in REPO_ROOT.glob(
    "*.py"
  ):
    try:
      text = path.read_text(
        encoding="utf-8"
      )
    except UnicodeDecodeError:
      continue

    if rule_name not in text:
      continue

    for line_number, line in enumerate(
      text.splitlines(),
      start=1,
    ):
      if rule_name in line:
        occurrences.append(
          (
            path.name,
            line_number,
            line.strip(),
          )
        )

  return tuple(
    occurrences
  )


def main():
  presentation = _presentation()
  recursive_steps = _walk_recursive(
    presentation.root_step
  )

  print("=" * 78)
  print("Phase157 R11-R9 - Hopf surjectivity dependency audit")
  print("=" * 78)
  print(
    f"presentation nodes={len(presentation.nodes)} "
    f"edges={len(presentation.edges)} "
    f"recursive steps={len(recursive_steps)}"
  )

  found = {}

  for target_rule in TARGET_RULES:
    matching = tuple(
      step
      for step in recursive_steps
      if _rule_name(
        step
      ) == target_rule
    )

    print()
    print(
      f"TARGET {target_rule!r}: "
      f"matches={len(matching)}"
    )

    for index, step in enumerate(
      matching,
      start=1,
    ):
      found[
        target_rule
      ] = step
      _print_step(
        f"{target_rule} #{index}",
        step,
        presentation,
        recursive_steps,
      )

    print(
      "source occurrences:"
    )
    for (
      filename,
      line_number,
      line,
    ) in _source_occurrences(
      target_rule
    ):
      print(
        f"  {filename}:{line_number}: {line}"
      )

  hopf_value = found.get(
    "Toda 5.3 nu-prime Lemma 5.2 Hopf specialization"
  )
  surjectivity = found.get(
    "Toda Proposition 5.3 n=3 Hopf eta_5 surjectivity"
  )
  target_group = found.get(
    "Toda Lemma 5.4 pi_6^5 finite-cyclic specialization"
  )

  print()
  print("DIRECT IDENTITY CHECKS")
  print("----------------------")

  if (
    hopf_value is not None
    and surjectivity is not None
  ):
    print(
      "hopf_value_is_direct_premise_of_surjectivity="
      + str(
        any(
          premise is hopf_value
          for premise in surjectivity.premises
        )
      )
    )

  if (
    target_group is not None
    and surjectivity is not None
  ):
    print(
      "target_group_is_direct_premise_of_surjectivity="
      + str(
        any(
          premise is target_group
          for premise in surjectivity.premises
        )
      )
    )

  print()
  print("done")


if __name__ == "__main__":
  main()
