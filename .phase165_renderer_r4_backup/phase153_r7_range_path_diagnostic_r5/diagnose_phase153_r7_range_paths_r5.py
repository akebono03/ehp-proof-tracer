from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
  sys.path.insert(
    0,
    str(REPO_ROOT),
  )


from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_contribution_renderer import (
  _phase153_r6_reference_aggregate_component,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
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


def build_pi6_2_presentation():
  report = build_standard_toda_report(
    n=2,
    k=4,
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

  return build_toda_group_proof_narrative_semantic_closure_presentation(
    presentation
  )


def unique_steps(
  presentation,
):
  steps = []
  seen = set()

  for step in (
    presentation.root_step,
    *(
      edge.parent_step
      for edge in presentation.edges
    ),
    *(
      edge.premise_step
      for edge in presentation.edges
    ),
  ):
    step_id = id(
      step
    )

    if step_id in seen:
      continue

    seen.add(
      step_id
    )
    steps.append(
      step
    )

  return tuple(
    steps
  )


def step_label(
  step,
):
  rendered = _render_generic_narrative_step(
    step
  )

  return (
    type(
      step.conclusion
    ).__name__
    + " :: "
    + rendered
  )


def build_children(
  presentation,
):
  children = {}

  for edge in presentation.edges:
    children.setdefault(
      id(
        edge.premise_step
      ),
      [],
    ).append(
      edge.parent_step
    )

  return {
    step_id: tuple(
      child_steps
    )
    for step_id, child_steps in children.items()
  }


def find_paths_to_root(
  presentation,
  source_step,
  excluded_step_ids=frozenset(),
  max_paths=30,
):
  children = build_children(
    presentation
  )
  root_id = id(
    presentation.root_step
  )
  results = []
  stack = [
    (
      source_step,
      (
        source_step,
      ),
    ),
  ]

  while stack and len(
    results
  ) < max_paths:
    current, path = stack.pop()
    current_id = id(
      current
    )

    if current_id == root_id:
      results.append(
        path
      )
      continue

    for child in children.get(
      current_id,
      (),
    ):
      child_id = id(
        child
      )

      if child_id in excluded_step_ids:
        continue

      if any(
        child is existing
        for existing in path
      ):
        continue

      stack.append(
        (
          child,
          (
            *path,
            child,
          ),
        )
      )

  return tuple(
    results
  )


def main():
  presentation = build_pi6_2_presentation()
  entries = build_toda_group_proof_narrative_reference_entries(
    presentation
  )
  steps = unique_steps(
    presentation
  )

  prop56_entry = next(
    entry
    for entry in entries
    if entry.reference.locator == "Proposition 5.6"
  )

  aggregate_steps = tuple(
    step
    for step in prop56_entry.proof_steps
    if (
      _phase153_r6_reference_aggregate_component(
        presentation,
        prop56_entry,
        step,
      )
      is not None
    )
  )

  if len(
    aggregate_steps
  ) != 1:
    raise SystemExit(
      "Expected exactly one Proposition 5.6 aggregate step, "
      f"found {len(aggregate_steps)}."
    )

  aggregate_step = aggregate_steps[
    0
  ]
  component = (
    _phase153_r6_reference_aggregate_component(
      presentation,
      prop56_entry,
      aggregate_step,
    )
  )
  retained_premises = tuple(
    premise
    for premise in aggregate_step.premises
    if premise.conclusion == component
  )

  if len(
    retained_premises
  ) != 1:
    raise SystemExit(
      "Expected exactly one retained aggregate premise."
    )

  retained_premise = retained_premises[
    0
  ]
  unselected_premises = tuple(
    premise
    for premise in aggregate_step.premises
    if premise is not retained_premise
  )

  range_steps = tuple(
    step
    for step in steps
    if isinstance(
      step.conclusion,
      ScalarGreaterEqualStatement,
    )
    and step.conclusion.right == 6
  )

  print(
    "=" * 78
  )
  print(
    "Phase 153-R7 R5 diagnostic — n >= 6 root paths"
  )
  print(
    "=" * 78
  )
  print()
  print(
    "root:"
  )
  print(
    "  "
    + step_label(
      presentation.root_step
    )
  )
  print()
  print(
    "selected Proposition 5.6 component:"
  )
  print(
    "  "
    + repr(
      component
    )
  )
  print()
  print(
    "retained direct premise:"
  )
  print(
    "  "
    + step_label(
      retained_premise
    )
  )
  print()
  print(
    "unselected direct premises:"
  )

  for index, premise in enumerate(
    unselected_premises,
    start=1,
  ):
    print(
      f"  U{index}: "
      + step_label(
        premise
      )
    )

  print()
  print(
    f"n>=6 steps found: {len(range_steps)}"
  )

  for range_index, range_step in enumerate(
    range_steps,
    start=1,
  ):
    print()
    print(
      "-" * 78
    )
    print(
      f"RANGE {range_index}"
    )
    print(
      "  "
      + step_label(
        range_step
      )
    )

    exclusion_sets = (
      (
        "no exclusions",
        frozenset(),
      ),
      (
        "exclude aggregate only",
        frozenset(
          (
            id(
              aggregate_step
            ),
          )
        ),
      ),
      (
        "exclude aggregate + all unselected direct siblings",
        frozenset(
          (
            id(
              aggregate_step
            ),
            *(
              id(
                premise
              )
              for premise in unselected_premises
            ),
          )
        ),
      ),
    )

    for title, excluded_ids in exclusion_sets:
      paths = find_paths_to_root(
        presentation,
        range_step,
        excluded_step_ids=excluded_ids,
        max_paths=20,
      )

      print()
      print(
        f"[{title}] paths={len(paths)}"
      )

      for path_index, path in enumerate(
        paths,
        start=1,
      ):
        print(
          f"  PATH {path_index}"
        )

        for depth, step in enumerate(
          path
        ):
          print(
            "    "
            + "  " * depth
            + "-> "
            + step_label(
              step
            )
          )

  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )
  marker = "## 証明\n\n"

  print()
  print(
    "=" * 78
  )
  print(
    "CURRENT PI6_2 PROOF BODY"
  )
  print(
    "=" * 78
  )

  if marker in rendered:
    print(
      rendered.split(
        marker,
        1,
      )[1]
    )
  else:
    print(
      rendered
    )

  print()
  print(
    "DIAGNOSTIC_COMPLETE"
  )


if __name__ == "__main__":
  main()
