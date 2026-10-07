from collections import Counter, defaultdict
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
  queue = [
    step
    for block in local_body
    for step in block.steps
    if id(step) in anchors
  ]
  visited = set(
    anchors
  )

  while queue:
    step = queue.pop(
      0
    )
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


def _premises_by_parent_id(
  presentation,
):
  result = defaultdict(
    list
  )

  for edge in presentation.edges:
    result[
      id(
        edge.parent_step
      )
    ].append(
      edge.premise_step
    )

  return result


def _bounded_upstream_ids(
  presentation,
  local_body,
  base_chain_ids,
  max_hops,
):
  local_step_by_id = {
    id(step): step
    for block in local_body
    for step in block.steps
  }
  local_ids = set(
    local_step_by_id
  )
  premises = _premises_by_parent_id(
    presentation
  )

  selected = set(
    base_chain_ids
  )
  frontier = set(
    base_chain_ids
  )
  added_by_hop = []

  for _hop in range(
    1,
    max_hops + 1,
  ):
    added = set()

    for parent_id in frontier:
      for premise in premises.get(
        parent_id,
        (),
      ):
        premise_id = id(
          premise
        )

        if premise_id not in local_ids:
          continue
        if premise_id in selected:
          continue

        added.add(
          premise_id
        )

    added_by_hop.append(
      frozenset(
        added
      )
    )
    selected.update(
      added
    )
    frontier = added

    if not frontier:
      break

  return (
    frozenset(
      selected
    ),
    tuple(
      added_by_hop
    ),
  )


def _block_role_by_step_id(
  local_body,
):
  return {
    id(step): block.role.value
    for block in local_body
    for step in block.steps
  }


def _statement_type_by_step_id(
  local_body,
):
  return {
    id(step): type(
      step.conclusion
    ).__name__
    for block in local_body
    for step in block.steps
  }


def _six_group_audit():
  print("=" * 78)
  print("SIX-GROUP BOUNDED UPSTREAM IMPACT")
  print("=" * 78)

  grand = {
    1: Counter(),
    2: Counter(),
    3: Counter(),
  }

  for n, k in TARGETS:
    target = {
      1: Counter(),
      2: Counter(),
      3: Counter(),
    }

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
      base_chain_ids = (
        _legacy_downstream_chain_step_ids(
          presentation,
          local_body,
          proof_chains[
            argument_index
          ],
          conclusion_step,
        )
      )
      role_by_id = (
        _block_role_by_step_id(
          local_body
        )
      )
      type_by_id = (
        _statement_type_by_step_id(
          local_body
        )
      )

      for max_hops in (
        1,
        2,
        3,
      ):
        selected, added_by_hop = (
          _bounded_upstream_ids(
            presentation,
            local_body,
            base_chain_ids,
            max_hops,
          )
        )
        added_ids = (
          selected
          - base_chain_ids
        )

        target[
          max_hops
        ][
          "added_steps"
        ] += len(
          added_ids
        )
        target[
          max_hops
        ][
          "arguments_with_added"
        ] += int(
          bool(
            added_ids
          )
        )

        grand[
          max_hops
        ][
          "added_steps"
        ] += len(
          added_ids
        )
        grand[
          max_hops
        ][
          "arguments_with_added"
        ] += int(
          bool(
            added_ids
          )
        )

        for step_id in added_ids:
          role = role_by_id.get(
            step_id,
            "UNKNOWN",
          )
          statement_type = (
            type_by_id.get(
              step_id,
              "UNKNOWN",
            )
          )
          target[
            max_hops
          ][
            "role:"
            + role
          ] += 1
          target[
            max_hops
          ][
            "type:"
            + statement_type
          ] += 1
          grand[
            max_hops
          ][
            "role:"
            + role
          ] += 1
          grand[
            max_hops
          ][
            "type:"
            + statement_type
          ] += 1

    print(
      f"TARGET pi_{n+k}^{n}"
    )

    for max_hops in (
      1,
      2,
      3,
    ):
      rows = target[
        max_hops
      ]
      print(
        f"  hops={max_hops}: "
        f"added_steps={rows['added_steps']} "
        f"arguments_with_added={rows['arguments_with_added']}"
      )

      top_roles = sorted(
        (
          (
            count,
            key[
              len(
                "role:"
              ):
            ],
          )
          for key, count in rows.items()
          if key.startswith(
            "role:"
          )
        ),
        reverse=True,
      )[
        :6
      ]

      if top_roles:
        print(
          "    roles="
          + ", ".join(
            f"{role}:{count}"
            for count, role
            in top_roles
          )
        )

      top_types = sorted(
        (
          (
            count,
            key[
              len(
                "type:"
              ):
            ],
          )
          for key, count in rows.items()
          if key.startswith(
            "type:"
          )
        ),
        reverse=True,
      )[
        :8
      ]

      if top_types:
        print(
          "    types="
          + ", ".join(
            f"{statement_type}:{count}"
            for count, statement_type
            in top_types
          )
        )

  print()
  print("=" * 78)
  print("GRAND TOTAL")
  print("=" * 78)

  for max_hops in (
    1,
    2,
    3,
  ):
    rows = grand[
      max_hops
    ]
    print(
      f"hops={max_hops}: "
      f"added_steps={rows['added_steps']} "
      f"arguments_with_added={rows['arguments_with_added']}"
    )

    top_roles = sorted(
      (
        (
          count,
          key[
            len(
              "role:"
            ):
          ],
        )
        for key, count in rows.items()
        if key.startswith(
          "role:"
        )
      ),
      reverse=True,
    )[
      :10
    ]

    print(
      "  roles="
      + ", ".join(
        f"{role}:{count}"
        for count, role
        in top_roles
      )
    )


def _pi4_coverage():
  print()
  print("=" * 78)
  print("PI_4^3 FOUR-FACT COVERAGE")
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

  argument_index = 0
  argument = arguments[
    argument_index
  ]
  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )
  local_body = (
    extract_toda_group_proof_narrative_argument_local_body_blocks(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      argument_index,
    )
  )
  base_chain_ids = (
    _legacy_downstream_chain_step_ids(
      presentation,
      local_body,
      proof_chains[
        argument_index
      ],
      conclusion_step,
    )
  )

  target_steps = tuple(
    step
    for block in local_body
    for step in block.steps
    if isinstance(
      step.conclusion,
      PI4_REQUIRED_TYPES,
    )
  )

  print(
    f"base_chain_steps={len(base_chain_ids)}"
  )

  for max_hops in (
    0,
    1,
    2,
    3,
  ):
    if max_hops == 0:
      selected = base_chain_ids
      added_by_hop = ()
    else:
      selected, added_by_hop = (
        _bounded_upstream_ids(
          presentation,
          local_body,
          base_chain_ids,
          max_hops,
        )
      )

    print(
      f"hops={max_hops}: "
      f"selected_steps={len(selected)} "
      f"added={len(selected - base_chain_ids)}"
    )

    for step in target_steps:
      print(
        "  "
        f"{type(step.conclusion).__name__}: "
        f"{id(step) in selected}"
      )

  print()
  print("Exact first hop for each required fact:")

  selected3, added_by_hop = (
    _bounded_upstream_ids(
      presentation,
      local_body,
      base_chain_ids,
      3,
    )
  )

  for step in target_steps:
    step_id = id(
      step
    )
    first_hop = None

    if step_id in base_chain_ids:
      first_hop = 0
    else:
      for index, hop_ids in enumerate(
        added_by_hop,
        start=1,
      ):
        if step_id in hop_ids:
          first_hop = index
          break

    print(
      "  "
      f"{type(step.conclusion).__name__}: "
      f"first_hop={first_hop}"
    )


def main():
  print("=" * 78)
  print("Phase 159 - pi_4^3 repair3c fix7 audit")
  print("Bounded upstream hop audit")
  print("=" * 78)
  print("Production code changes: NONE")
  print("Existing test changes: NONE")
  print("Repository-wide pytest: NOT RUN")
  print()
  print(
    "Historical boundary being tested: "
    "Phase 144 R5-30 preferred non-recursive single-hop upstream attachment "
    "and explicitly rejected unbounded recursive widening."
  )
  print()

  _six_group_audit()
  _pi4_coverage()

  print()
  print("=" * 78)
  print("repair3c fix7 bounded upstream hop audit complete")
  print("Production code changes: NONE")
  print("Existing test changes: NONE")
  print("Repository-wide pytest: NOT RUN")
  print("=" * 78)


if __name__ == "__main__":
  main()
