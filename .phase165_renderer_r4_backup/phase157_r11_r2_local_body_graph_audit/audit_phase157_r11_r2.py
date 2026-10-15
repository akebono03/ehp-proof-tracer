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
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
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
  presentation = build_toda_group_proof_presentation(
    replay
  )
  return (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )


def _can_reach(
  source_id: int,
  target_id: int,
  parents_by_premise: dict[int, tuple[int, ...]],
  allowed_ids: frozenset[int],
) -> bool:
  if source_id == target_id:
    return True

  stack = list(
    parents_by_premise.get(
      source_id,
      (),
    )
  )
  seen = set()

  while stack:
    current = stack.pop()

    if current == target_id:
      return True

    if (
      current in seen
      or current not in allowed_ids
    ):
      continue

    seen.add(
      current
    )
    stack.extend(
      parents_by_premise.get(
        current,
        (),
      )
    )

  return False


def main() -> None:
  presentation = _presentation()

  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=sidecar,
  )

  target_index = next(
    index
    for index, argument in enumerate(
      arguments
    )
    if argument.role.value == "establish_group_structure"
  )
  argument = arguments[
    target_index
  ]
  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )

  if conclusion_step is None:
    raise RuntimeError(
      "group-structure argument has no conclusion step"
    )

  local_blocks = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      sidecar,
      arguments,
      target_index,
    )
  )

  local_steps = tuple(
    proof_step
    for block in local_blocks
    for proof_step in block.steps
  )
  local_ids = frozenset(
    id(
      proof_step
    )
    for proof_step in local_steps
  )
  allowed_ids = frozenset(
    {
      *local_ids,
      id(
        conclusion_step
      ),
    }
  )

  parents = {}

  for edge in presentation.edges:
    premise_id = id(
      edge.premise_step
    )
    parent_id = id(
      edge.parent_step
    )
    parents.setdefault(
      premise_id,
      [],
    ).append(
      parent_id
    )

  parents = {
    step_id: tuple(
      parent_ids
    )
    for step_id, parent_ids in parents.items()
  }

  step_by_id = {
    id(
      node.proof_step
    ): node.proof_step
    for node in presentation.nodes
  }

  print("=" * 78)
  print("Phase157 R11-R2 — A00 local-body proof-graph audit")
  print("=" * 78)
  print(
    f"argument index: A{target_index:02d}"
  )
  print(
    f"argument role: {argument.role.value}"
  )
  print(
    "conclusion type: "
    + type(
      conclusion_step.conclusion
    ).__name__
  )
  print(
    "conclusion: "
    + (
      _render_generic_narrative_step(
        conclusion_step
      )
      or str(
        conclusion_step.conclusion
      )
    )
  )
  print(
    f"local blocks: {len(local_blocks)}"
  )
  print(
    f"local steps: {len(local_steps)}"
  )

  for block_index, block in enumerate(
    local_blocks
  ):
    print()
    print(
      f"B{block_index:02d}: role={block.role.value}"
    )

    for step_index, proof_step in enumerate(
      block.steps
    ):
      step_id = id(
        proof_step
      )
      rendered = (
        _render_generic_narrative_step(
          proof_step
        )
        or str(
          proof_step.conclusion
        )
      )
      rendered = rendered.replace(
        "\n",
        " ",
      )
      reaches = _can_reach(
        step_id,
        id(
          conclusion_step
        ),
        parents,
        allowed_ids,
      )
      parent_rows = []

      for parent_id in parents.get(
        step_id,
        (),
      ):
        parent_step = step_by_id.get(
          parent_id
        )

        if parent_step is None:
          parent_rows.append(
            f"{parent_id}:<missing>"
          )
          continue

        parent_rendered = (
          _render_generic_narrative_step(
            parent_step
          )
          or str(
            parent_step.conclusion
          )
        ).replace(
          "\n",
          " ",
        )

        if len(
          parent_rendered
        ) > 180:
          parent_rendered = (
            parent_rendered[:177]
            + "..."
          )

        parent_rows.append(
          (
            f"{type(parent_step.conclusion).__name__}: "
            + parent_rendered
          )
        )

      print(
        f"  S{step_index:02d}: "
        f"reaches_conclusion={reaches} "
        f"type={type(proof_step.conclusion).__name__}"
      )
      print(
        f"       value={rendered}"
      )

      if parent_rows:
        for row in parent_rows:
          print(
            f"       consumed_by={row}"
          )
      else:
        print(
          "       consumed_by=(none)"
        )

  output_dir = (
    PACKAGE_DIR
    / "output"
  )
  output_dir.mkdir(
    exist_ok=True
  )

  print()
  print("R11-R2 audit completed.")


if __name__ == "__main__":
  main()
