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


from proof import Relation
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
  _anchored_chain_step_ids,
  _provider_anchor_step_ids,
)
from toda_proof_dependency import (
  classify_toda_proof_step_role,
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


def _block_by_step_id(
  local_body,
):
  return {
    id(step): block
    for block in local_body
    for step in block.steps
  }


def _local_step_by_id(
  local_body,
):
  return {
    id(step): step
    for block in local_body
    for step in block.steps
  }


def _distance_to_nearest_anchor(
  start_id,
  anchors,
  parents,
  local_ids,
):
  if start_id in anchors:
    return 0

  queue = deque(
    [
      (
        start_id,
        0,
      ),
    ]
  )
  seen = {
    start_id,
  }

  while queue:
    current_id, distance = queue.popleft()

    for parent in parents.get(
      current_id,
      (),
    ):
      parent_id = id(
        parent
      )
      if parent_id not in local_ids:
        continue
      if parent_id in anchors:
        return distance + 1
      if parent_id in seen:
        continue
      seen.add(
        parent_id
      )
      queue.append(
        (
          parent_id,
          distance + 1,
        )
      )

  return None


def _corridor_metadata(
  presentation,
  local_body,
  proof_chain,
  conclusion_step,
):
  local_steps = _local_step_by_id(
    local_body
  )
  local_ids = set(
    local_steps
  )
  block_by_id = _block_by_step_id(
    local_body
  )
  parents = _parents_by_premise_id(
    presentation
  )
  premises = _premises_by_parent_id(
    presentation
  )
  anchors = (
    _provider_anchor_step_ids(
      proof_chain
    )
    & local_ids
  )
  current_chain, _, _ = (
    _anchored_chain_step_ids(
      presentation,
      local_body,
      proof_chain,
      conclusion_step,
    )
  )

  rows = {}

  for step_id, step in local_steps.items():
    block = block_by_id[
      step_id
    ]
    dependency_role = (
      classify_toda_proof_step_role(
        step
      )
    )
    local_consumers = tuple(
      parent
      for parent in parents.get(
        step_id,
        (),
      )
      if id(parent) in local_ids
    )
    local_premises = tuple(
      premise
      for premise in premises.get(
        step_id,
        (),
      )
      if id(premise) in local_ids
    )

    rows[
      step_id
    ] = {
      "step": step,
      "statement_type": type(
        step.conclusion
      ).__name__,
      "is_relation": isinstance(
        step.conclusion,
        Relation,
      ),
      "block_role": block.role.value,
      "dependency_role": dependency_role.value,
      "consumer_count": len(
        local_consumers
      ),
      "premise_count": len(
        local_premises
      ),
      "anchor_distance": (
        _distance_to_nearest_anchor(
          step_id,
          anchors,
          parents,
          local_ids,
        )
      ),
      "in_current_chain": (
        step_id in current_chain
      ),
      "anchor": (
        step_id in anchors
      ),
      "rule_name": (
        step.inference_rule.name
        if step.inference_rule is not None
        else None
      ),
    }

  return rows


def _candidate_flags(
  row,
):
  semantic_block = (
    row[
      "block_role"
    ]
    in {
      "calculation",
      "group_structure",
      "map_property",
    }
  )
  bounded_consumer = (
    row[
      "consumer_count"
    ]
    == 1
  )
  short_anchor = (
    row[
      "anchor_distance"
    ]
    is not None
    and row[
      "anchor_distance"
    ]
    <= 3
  )
  non_relation = not row[
    "is_relation"
  ]

  return {
    "semantic_block": semantic_block,
    "semantic_block_single_consumer": (
      semantic_block
      and bounded_consumer
    ),
    "semantic_block_short_anchor": (
      semantic_block
      and short_anchor
    ),
    "semantic_block_single_consumer_short_anchor": (
      semantic_block
      and bounded_consumer
      and short_anchor
    ),
    "semantic_block_single_consumer_short_anchor_non_relation": (
      semantic_block
      and bounded_consumer
      and short_anchor
      and non_relation
    ),
  }


def _print_pi4_metadata():
  print("=" * 78)
  print("PI_4^3 REQUIRED-FACT METADATA")
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
  metadata = _corridor_metadata(
    presentation,
    local_body,
    proof_chains[
      argument_index
    ],
    conclusion_step,
  )

  for row in metadata.values():
    if not isinstance(
      row[
        "step"
      ].conclusion,
      PI4_REQUIRED_TYPES,
    ):
      continue

    flags = _candidate_flags(
      row
    )

    print(
      f"type={row['statement_type']}"
    )
    print(
      "  "
      f"block_role={row['block_role']} "
      f"dependency_role={row['dependency_role']} "
      f"consumers={row['consumer_count']} "
      f"premises={row['premise_count']} "
      f"anchor_distance={row['anchor_distance']} "
      f"anchor={row['anchor']} "
      f"in_current_chain={row['in_current_chain']}"
    )
    print(
      "  "
      f"rule={row['rule_name']}"
    )
    print(
      "  candidate_flags="
      + repr(
        flags
      )
    )


def _print_six_group_filter_impact():
  print()
  print("=" * 78)
  print("SIX-GROUP UPSTREAM-ONLY SEMANTIC FILTER IMPACT")
  print("=" * 78)

  filter_totals = Counter()
  filter_types = defaultdict(
    Counter
  )
  filter_roles = defaultdict(
    Counter
  )

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

    target_counts = Counter()

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
      metadata = _corridor_metadata(
        presentation,
        local_body,
        proof_chains[
          argument_index
        ],
        conclusion_step,
      )

      for row in metadata.values():
        if not row[
          "in_current_chain"
        ]:
          continue
        if row[
          "anchor"
        ]:
          continue

        flags = _candidate_flags(
          row
        )

        for name, selected in flags.items():
          if not selected:
            continue

          target_counts[
            name
          ] += 1
          filter_totals[
            name
          ] += 1
          filter_types[
            name
          ][
            row[
              "statement_type"
            ]
          ] += 1
          filter_roles[
            name
          ][
            (
              row[
                "block_role"
              ],
              row[
                "dependency_role"
              ],
            )
          ] += 1

    print(
      f"TARGET pi_{n+k}^{n}"
    )
    for name in (
      "semantic_block",
      "semantic_block_single_consumer",
      "semantic_block_short_anchor",
      "semantic_block_single_consumer_short_anchor",
      "semantic_block_single_consumer_short_anchor_non_relation",
    ):
      print(
        f"  {name}={target_counts[name]}"
      )

  print()
  print("GRAND TOTAL")

  for name in (
    "semantic_block",
    "semantic_block_single_consumer",
    "semantic_block_short_anchor",
    "semantic_block_single_consumer_short_anchor",
    "semantic_block_single_consumer_short_anchor_non_relation",
  ):
    print(
      f"{name}={filter_totals[name]}"
    )
    print(
      "  top_types="
      + ", ".join(
        f"{statement_type}:{count}"
        for statement_type, count
        in filter_types[
          name
        ].most_common(
          12
        )
      )
    )
    print(
      "  top_roles="
      + ", ".join(
        f"{block_role}/{dependency_role}:{count}"
        for (
          block_role,
          dependency_role,
        ), count
        in filter_roles[
          name
        ].most_common(
          12
        )
      )
    )


def main():
  print("=" * 78)
  print("Phase 159 - pi_4^3 repair3c fix8 audit")
  print("Semantic corridor boundary audit")
  print("=" * 78)
  print("Production code changes: NONE")
  print("Existing test changes: NONE")
  print("Repository-wide pytest: NOT RUN")
  print()

  _print_pi4_metadata()
  _print_six_group_filter_impact()

  print()
  print("=" * 78)
  print("repair3c fix8 semantic corridor boundary audit complete")
  print("Production code changes: NONE")
  print("Existing test changes: NONE")
  print("Repository-wide pytest: NOT RUN")
  print("=" * 78)


if __name__ == "__main__":
  main()
