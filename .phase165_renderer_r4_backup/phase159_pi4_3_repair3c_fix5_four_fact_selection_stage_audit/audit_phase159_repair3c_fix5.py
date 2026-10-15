from collections import defaultdict, deque
from pathlib import Path
import sys


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
TESTS_DIR = REPO_ROOT / "tests"

for path in (
  REPO_ROOT,
  TESTS_DIR,
):
  if str(path) not in sys.path:
    sys.path.insert(
      0,
      str(path),
    )


from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
  _context,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_contribution_ordering import (
  _build_visibility_occurrences,
  _effective_hidden_step_ids,
  _group_key,
  _is_rendering_fallback,
  _necessity_for_chain,
  _normalized,
  _owner,
  _provider_keys_by_step_id,
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaImageUpToSignStatement,
  TodaSuspensionKernelFreeCyclicStatement,
  TodaSuspensionSurjectiveStatement,
)


TARGET_TYPES = (
  TodaDeltaImageUpToSignStatement,
  TodaDeltaImageFreeCyclicStatement,
  TodaSuspensionKernelFreeCyclicStatement,
  TodaSuspensionSurjectiveStatement,
)


def _parents_by_premise_id(
  presentation,
):
  result = defaultdict(
    list
  )

  for edge in presentation.edges:
    result[
      id(
        edge.premise_step
      )
    ].append(
      edge.parent_step
    )

  return result


def _reachable_public_descendants(
  step,
  presentation,
  local_ids,
  normalized_markdown,
):
  parents = _parents_by_premise_id(
    presentation
  )
  start_id = id(
    step
  )
  queue = deque(
    (
      parent,
      1,
    )
    for parent in parents.get(
      start_id,
      (),
    )
    if id(parent) in local_ids
  )
  seen = {
    start_id,
  }
  rows = []

  while queue:
    current, distance = queue.popleft()
    current_id = id(
      current
    )

    if current_id in seen:
      continue

    seen.add(
      current_id
    )
    rendered = _render_generic_narrative_step(
      current
    )

    if (
      rendered
      and _normalized(
        rendered
      )
      in normalized_markdown
    ):
      rows.append(
        (
          distance,
          type(
            current.conclusion
          ).__name__,
          rendered,
        )
      )

    for parent in parents.get(
      current_id,
      (),
    ):
      if id(parent) not in local_ids:
        continue

      queue.append(
        (
          parent,
          distance + 1,
        )
      )

  rows.sort(
    key=lambda row: (
      row[0],
      row[1],
      row[2],
    )
  )
  return tuple(
    rows
  )


def main():
  print("=" * 78)
  print("Phase 159 - pi_4^3 repair3c fix5 audit")
  print("Four-fact selection-stage diagnosis")
  print("=" * 78)
  print("Production code changes: NONE")
  print("Existing test changes: NONE")
  print("Repository-wide pytest: NOT RUN")
  print()

  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
    _aggregate_semantic_sidecar,
    proof_chains,
  ) = _context(
    3,
    1,
  )

  markdown = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  normalized_markdown = _normalized(
    markdown
  )

  occurrences = (
    _build_visibility_occurrences(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
    )
  )

  grouped = defaultdict(
    list
  )
  for occurrence in occurrences:
    grouped[
      _group_key(
        occurrence
      )
    ].append(
      occurrence
    )

  owners = {
    (
      row.argument_index,
      id(
        row.proof_step
      ),
    ): row
    for rows in grouped.values()
    for row in (
      _owner(
        rows
      ),
    )
  }

  ordered = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
    )
  )
  selected = {
    (
      row.owner_argument_index,
      id(
        row.proof_step
      ),
    ): row
    for argument_rows in ordered
    for row in argument_rows
  }

  occurrence_keys = {
    (
      row.argument_index,
      id(
        row.proof_step
      ),
    )
    for row in occurrences
  }

  print(
    f"presentation_nodes={len(presentation.nodes)} "
    f"blocks={len(blocks)} "
    f"arguments={len(arguments)} "
    f"occurrences={len(occurrences)} "
    f"selected={sum(len(rows) for rows in ordered)}"
  )
  print()

  for argument_index, argument in enumerate(
    arguments
  ):
    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )

    if conclusion_step is None:
      continue

    local_body = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )
    local_steps = tuple(
      step
      for block in local_body
      for step in block.steps
    )
    local_ids = {
      id(step)
      for step in local_steps
    }
    hidden_ids = (
      _effective_hidden_step_ids(
        presentation,
        blocks,
        local_body,
        semantic_sidecar,
        argument,
      )
    )
    (
      chain_ids,
      anchors,
      distances,
      necessity,
    ) = _necessity_for_chain(
      presentation,
      local_body,
      proof_chains[
        argument_index
      ],
      conclusion_step,
    )
    provider_keys_by_step_id = (
      _provider_keys_by_step_id(
        presentation,
        local_body,
        proof_chains[
          argument_index
        ],
        conclusion_step,
      )
    )

    print("-" * 78)
    print(
      f"ARGUMENT {argument_index} "
      f"role={argument.role.value} "
      f"local_steps={len(local_steps)} "
      f"chain={len(chain_ids)} "
      f"anchors={len(anchors)}"
    )

    for step in local_steps:
      if not isinstance(
        step.conclusion,
        TARGET_TYPES,
      ):
        continue

      step_id = id(
        step
      )
      key = (
        argument_index,
        step_id,
      )
      rendered = (
        _render_generic_narrative_step(
          step
        )
      )
      public_descendants = (
        _reachable_public_descendants(
          step,
          presentation,
          local_ids,
          normalized_markdown,
        )
      )

      print()
      print(
        "TYPE="
        f"{type(step.conclusion).__name__}"
      )
      print(
        "  render="
        f"{rendered}"
      )
      print(
        "  local="
        f"{step_id in local_ids} "
        "hidden="
        f"{step_id in hidden_ids} "
        "chain="
        f"{step_id in chain_ids} "
        "anchor="
        f"{step_id in anchors}"
      )
      print(
        "  necessity_count="
        f"{len(necessity.get(step_id, ()))} "
        "provider_key_count="
        f"{len(provider_keys_by_step_id.get(step_id, ()))} "
        "distance="
        f"{distances.get(step_id)}"
      )
      print(
        "  already_public="
        f"{_normalized(rendered) in normalized_markdown} "
        "fallback="
        f"{_is_rendering_fallback(step, rendered)}"
      )
      print(
        "  occurrence="
        f"{key in occurrence_keys} "
        "owner="
        f"{key in owners} "
        "selected="
        f"{key in selected}"
      )

      if key in owners:
        owner = owners[
          key
        ]
        print(
          "  owner_provider_anchor="
          f"{owner.provider_anchor} "
          "owner_provider_keys="
          f"{len(owner.provider_keys)}"
        )

      if key in selected:
        row = selected[
          key
        ]
        print(
          "  selected_placement="
          f"{row.placement.value} "
          "selected_role="
          f"{row.contribution_role.value}"
        )

      if public_descendants:
        print(
          "  nearest_public_descendants:"
        )
        for (
          distance,
          statement_type,
          descendant_render,
        ) in public_descendants[
          :5
        ]:
          print(
            "    "
            f"distance={distance} "
            f"type={statement_type} "
            f"render={descendant_render}"
          )
      else:
        print(
          "  nearest_public_descendants: NONE"
        )

  print()
  print("=" * 78)
  print("BASE PUBLIC MARKDOWN")
  print("=" * 78)
  print(
    markdown
  )
  print()
  print("=" * 78)
  print("repair3c fix5 audit complete")
  print("Production code changes: NONE")
  print("Existing test changes: NONE")
  print("Repository-wide pytest: NOT RUN")
  print("=" * 78)


if __name__ == "__main__":
  main()
