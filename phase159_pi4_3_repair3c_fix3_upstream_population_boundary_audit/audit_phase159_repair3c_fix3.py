from collections import Counter, defaultdict, deque
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
  TARGETS,
  _context,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_arguments import (
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_contribution_ordering import (
  _provider_anchor_step_ids,
  _parents_by_premise,
  _reverse_distances,
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaImageUpToSignStatement,
  TodaSuspensionKernelFreeCyclicStatement,
  TodaSuspensionSurjectiveStatement,
)


PI4_REQUIRED_TYPES = (
  TodaDeltaImageUpToSignStatement,
  TodaDeltaImageFreeCyclicStatement,
  TodaSuspensionKernelFreeCyclicStatement,
  TodaSuspensionSurjectiveStatement,
)


def _legacy_downstream_chain_step_ids(
  presentation,
  local_body,
  proof_chain,
  conclusion_step,
):
  local_ids = {
    id(step)
    for block in local_body
    for step in block.steps
  }
  anchors = (
    _provider_anchor_step_ids(
      proof_chain
    )
    & local_ids
  )
  distances = _reverse_distances(
    presentation,
    conclusion_step,
  )
  parents = _parents_by_premise(
    presentation
  )
  chain_ids = {
    id(
      conclusion_step
    )
  }
  queue = deque(
    step
    for block in local_body
    for step in block.steps
    if id(step) in anchors
  )
  visited = set(
    anchors
  )

  while queue:
    step = queue.popleft()
    step_id = id(
      step
    )

    if step_id not in distances:
      continue

    chain_ids.add(
      step_id
    )

    for parent in parents.get(
      step_id,
      (),
    ):
      parent_id = id(
        parent
      )

      if parent_id not in local_ids:
        continue
      if parent_id not in distances:
        continue
      if (
        distances[
          parent_id
        ]
        >= distances[
          step_id
        ]
      ):
        continue

      chain_ids.add(
        parent_id
      )

      if parent_id in visited:
        continue

      visited.add(
        parent_id
      )
      queue.append(
        parent
      )

  return frozenset(
    chain_ids
  )


def main():
  print("=" * 78)
  print("Phase 159 - repair3c fix3 audit")
  print("Upstream contribution population boundary")
  print("=" * 78)
  print("Production code changes: NONE")
  print("Existing test changes: NONE")
  print("Repository-wide pytest: NOT RUN")
  print()

  grand_classification = Counter()
  grand_statement_types = Counter()
  grand_roles = Counter()
  pi4_rows = []

  for n, k in TARGETS:
    (
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
      _aggregate_semantic_sidecar,
      proof_chains,
    ) = _context(
      n,
      k,
    )

    ordered = (
      build_toda_group_proof_narrative_ordered_contributions(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        proof_chains,
      )
    )

    target_classification = Counter()
    target_types = Counter()
    target_roles = Counter()

    for argument_index, rows in enumerate(
      ordered
    ):
      argument = arguments[
        argument_index
      ]
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
      legacy_ids = (
        _legacy_downstream_chain_step_ids(
          presentation,
          local_body,
          proof_chains[
            argument_index
          ],
          conclusion_step,
        )
      )

      for row in rows:
        step = row.proof_step
        step_id = id(
          step
        )
        statement_type = type(
          step.conclusion
        ).__name__

        if step_id in legacy_ids:
          classification = (
            "legacy_downstream"
          )
        else:
          classification = (
            "upstream_only"
          )

        target_classification[
          classification
        ] += 1
        target_types[
          (
            classification,
            statement_type,
          )
        ] += 1
        target_roles[
          (
            classification,
            row.owner_argument_role.value,
            row.placement.value,
            row.provider_anchor,
          )
        ] += 1

        grand_classification[
          classification
        ] += 1
        grand_statement_types[
          (
            classification,
            statement_type,
          )
        ] += 1
        grand_roles[
          (
            classification,
            row.owner_argument_role.value,
            row.placement.value,
            row.provider_anchor,
          )
        ] += 1

        if (
          n,
          k,
        ) == (
          3,
          1,
        ):
          pi4_rows.append(
            (
              classification,
              statement_type,
              row.placement.value,
              row.provider_anchor,
              getattr(
                step.inference_rule,
                "name",
                None,
              ),
            )
          )

    print(
      f"TARGET pi_{n+k}^{n}: "
      f"total={sum(target_classification.values())} "
      f"legacy_downstream={target_classification['legacy_downstream']} "
      f"upstream_only={target_classification['upstream_only']}"
    )

    print(
      "  upstream-only top statement types:"
    )
    upstream_types = [
      (
        count,
        statement_type,
      )
      for (
        classification,
        statement_type,
      ), count in target_types.items()
      if classification == "upstream_only"
    ]

    for count, statement_type in sorted(
      upstream_types,
      reverse=True,
    )[:15]:
      print(
        f"    {count:5d}  {statement_type}"
      )

    print(
      "  upstream-only role/placement/provider-anchor:"
    )
    upstream_roles = [
      (
        count,
        argument_role,
        placement,
        provider_anchor,
      )
      for (
        classification,
        argument_role,
        placement,
        provider_anchor,
      ), count in target_roles.items()
      if classification == "upstream_only"
    ]

    for (
      count,
      argument_role,
      placement,
      provider_anchor,
    ) in sorted(
      upstream_roles,
      reverse=True,
    )[:15]:
      print(
        "    "
        f"{count:5d}  "
        f"argument={argument_role} "
        f"placement={placement} "
        f"provider_anchor={provider_anchor}"
      )

  print()
  print("=" * 78)
  print("GRAND TOTAL")
  print("=" * 78)
  print(
    dict(
      grand_classification
    )
  )

  print()
  print(
    "Top upstream-only statement types:"
  )
  upstream_types = [
    (
      count,
      statement_type,
    )
    for (
      classification,
      statement_type,
    ), count in grand_statement_types.items()
    if classification == "upstream_only"
  ]

  for count, statement_type in sorted(
    upstream_types,
    reverse=True,
  )[:30]:
    print(
      f"{count:6d}  {statement_type}"
    )

  print()
  print(
    "Top upstream-only role/placement/provider-anchor:"
  )
  upstream_roles = [
    (
      count,
      argument_role,
      placement,
      provider_anchor,
    )
    for (
      classification,
      argument_role,
      placement,
      provider_anchor,
    ), count in grand_roles.items()
    if classification == "upstream_only"
  ]

  for (
    count,
    argument_role,
    placement,
    provider_anchor,
  ) in sorted(
    upstream_roles,
    reverse=True,
  )[:30]:
    print(
      f"{count:6d}  "
      f"argument={argument_role} "
      f"placement={placement} "
      f"provider_anchor={provider_anchor}"
    )

  print()
  print("=" * 78)
  print("PI_4^3 DIRECT AUDIT")
  print("=" * 78)

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

  ordered = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
    )
  )

  for argument_index, rows in enumerate(
    ordered
  ):
    argument = arguments[
      argument_index
    ]
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
    legacy_ids = (
      _legacy_downstream_chain_step_ids(
        presentation,
        local_body,
        proof_chains[
          argument_index
        ],
        conclusion_step,
      )
    )

    for row in rows:
      step = row.proof_step

      if not isinstance(
        step.conclusion,
        PI4_REQUIRED_TYPES,
      ):
        continue

      print(
        "argument="
        f"{argument_index} "
        "type="
        f"{type(step.conclusion).__name__} "
        "legacy_downstream="
        f"{id(step) in legacy_ids} "
        "provider_anchor="
        f"{row.provider_anchor} "
        "placement="
        f"{row.placement.value} "
        "provider_keys="
        f"{len(row.provider_keys)}"
      )

  print()
  print("=" * 78)
  print("repair3c fix3 upstream population boundary audit complete")
  print("Production code changes: NONE")
  print("Existing test changes: NONE")
  print("Repository-wide pytest: NOT RUN")
  print("=" * 78)


if __name__ == "__main__":
  main()
