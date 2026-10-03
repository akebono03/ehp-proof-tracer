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


from proof import (
  Relation,
  RelationType,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
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


SURJECTIVITY_RULE = (
  "Toda Proposition 5.3 n=3 Hopf eta_5 surjectivity"
)


def _raw_presentation():
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


def _boundary(
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


def _describe(
  prefix,
  step,
  raw_ids,
  closure_ids,
):
  locator, component, classification = _boundary(
    step
  )

  print(
    f"{prefix}: "
    f"id={id(step)} "
    f"raw={id(step) in raw_ids} "
    f"closure={id(step) in closure_ids}"
  )
  print(
    f"  rule={_rule_name(step)!r}"
  )
  print(
    f"  rendered={_render_generic_narrative_step(step)!r}"
  )
  print(
    "  boundary="
    f"locator={locator!r} "
    f"component={component!r} "
    f"classification={classification!r}"
  )


def main():
  raw = _raw_presentation()
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )

  recursive_steps = _walk_recursive(
    raw.root_step
  )

  raw_ids = {
    id(
      node.proof_step
    )
    for node in raw.nodes
  }
  closure_ids = {
    id(
      node.proof_step
    )
    for node in closure.nodes
  }

  print("=" * 78)
  print("Phase157 R11-R10 - Hopf chain semantic-closure audit")
  print("=" * 78)
  print(
    f"raw nodes={len(raw.nodes)} edges={len(raw.edges)}"
  )
  print(
    f"closure nodes={len(closure.nodes)} edges={len(closure.edges)}"
  )
  print(
    f"added nodes={len(closure_ids - raw_ids)}"
  )
  print()

  surjectivity_steps = tuple(
    step
    for step in recursive_steps
    if _rule_name(
      step
    ) == SURJECTIVITY_RULE
  )

  print(
    f"surjectivity matches={len(surjectivity_steps)}"
  )

  for s_index, surjectivity in enumerate(
    surjectivity_steps,
    start=1,
  ):
    print()
    print(
      f"SURJECTIVITY #{s_index}"
    )
    print(
      "-" * 40
    )
    _describe(
      "surjectivity",
      surjectivity,
      raw_ids,
      closure_ids,
    )

    for p_index, premise in enumerate(
      surjectivity.premises,
      start=1,
    ):
      _describe(
        f"premise[{p_index}]",
        premise,
        raw_ids,
        closure_ids,
      )

      if (
        isinstance(
          premise.conclusion,
          Relation,
        )
        and premise.conclusion.relation_type
        is RelationType.EQUALITY
      ):
        for q_index, subpremise in enumerate(
          premise.premises,
          start=1,
        ):
          _describe(
            f"  equality-premise[{q_index}]",
            subpremise,
            raw_ids,
            closure_ids,
          )

  print()
  print("ADDED CLOSURE NODES")
  print("-------------------")

  for node in closure.nodes:
    step = node.proof_step

    if id(
      step
    ) in raw_ids:
      continue

    _describe(
      "added",
      step,
      raw_ids,
      closure_ids,
    )

  print()
  print("done")


if __name__ == "__main__":
  main()
