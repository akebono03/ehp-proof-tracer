from collections import deque
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
from toda_group_proof_narrative_contribution_ordering import (
  _anchored_chain_step_ids,
  _premises_by_parent,
)
from toda_group_proof_narrative_proof_chains import (
  TodaGroupProofNarrativeProofChainProviderKind,
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


INTERESTING_RULE_FRAGMENTS = (
  "pi_4^3 finite cyclic quotient calculation",
  "Proposition 5.1 pi_3^2 group relation",
  "pi_4^3 exactness Delta image equals E kernel",
  "pi_4^3 E-H exactness zero-right suspension surjectivity",
  "free cyclic generator Delta image",
  "Proposition 5.1 Delta iota_5",
  "(5.1) sphere connectivity zero",
)

INTERESTING_TYPES = {
  "Relation",
  "TodaSuspensionKernelFreeCyclicStatement",
  "TodaSuspensionSurjectiveStatement",
  "TodaDeltaImageFreeCyclicStatement",
  "TodaPrimaryGroupZeroStatement",
  "TodaDeltaImageUpToSignStatement",
  "TodaProp42ExactnessStatement",
}


def _presentation():
  report = build_standard_toda_report(
    n=3,
    k=1,
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
  raw = build_toda_group_proof_presentation(
    replay
  )
  return (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw
    )
  )


def _rule_name(step):
  rule = step.inference_rule
  if rule is None:
    return None
  return rule.name


def _render(step):
  try:
    return _render_generic_narrative_step(
      step
    )
  except Exception as exc:
    return (
      "<render-error "
      + type(exc).__name__
      + ": "
      + str(exc)
      + ">"
    )


def _step_label(step):
  return (
    type(
      step.conclusion
    ).__name__
    + " | rule="
    + repr(
      _rule_name(
        step
      )
    )
    + " | "
    + _render(
      step
    )
  )


def _interesting(step):
  type_name = type(
    step.conclusion
  ).__name__

  if type_name in INTERESTING_TYPES:
    return True

  rule_name = (
    _rule_name(
      step
    )
    or ""
  )

  return any(
    fragment in rule_name
    for fragment in INTERESTING_RULE_FRAGMENTS
  )


def _block_index_by_step_id(
  blocks,
):
  return {
    id(step): block_index
    for block_index, block in enumerate(
      blocks
    )
    for step in block.steps
  }


def _upstream_ancestry(
  presentation,
  start_steps,
  allowed_step_ids=None,
):
  premises = _premises_by_parent(
    presentation
  )

  distance = {}
  predecessor = {}
  queue = deque()

  for start_step in start_steps:
    start_id = id(
      start_step
    )
    distance[start_id] = 0
    predecessor[start_id] = None
    queue.append(
      start_step
    )

  while queue:
    current = queue.popleft()
    current_id = id(
      current
    )
    next_distance = (
      distance[
        current_id
      ]
      + 1
    )

    for premise in premises.get(
      current_id,
      (),
    ):
      premise_id = id(
        premise
      )

      if (
        allowed_step_ids is not None
        and premise_id not in allowed_step_ids
      ):
        continue

      if premise_id in distance:
        continue

      distance[
        premise_id
      ] = next_distance
      predecessor[
        premise_id
      ] = current_id
      queue.append(
        premise
      )

  return (
    distance,
    predecessor,
  )


def _step_by_id(
  local_body,
):
  return {
    id(step): step
    for block in local_body
    for step in block.steps
  }


def _path_to_anchor(
  step_id,
  predecessor,
  step_lookup,
):
  ids = []
  current = step_id

  while current is not None:
    ids.append(
      current
    )
    current = predecessor.get(
      current
    )

  return tuple(
    step_lookup[
      candidate_id
    ]
    for candidate_id in ids
    if candidate_id in step_lookup
  )


def _print_path(
  label,
  path,
):
  print(
    label
  )

  if not path:
    print(
      "  NOT FOUND"
    )
    return

  for index, step in enumerate(
    path
  ):
    arrow = (
      "  start"
      if index == 0
      else "    ->"
    )
    print(
      arrow,
      _step_label(
        step
      ),
    )


def main():
  print("=" * 78)
  print("Phase 159 - pi_4^3 repair3b audit")
  print("Provider-anchor ancestry only")
  print("=" * 78)
  print("Production code changes: NONE")
  print("Existing test changes: NONE")
  print("Repository-wide pytest: NOT RUN")
  print()

  presentation = _presentation()
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
  proof_chains = (
    build_toda_group_proof_narrative_proof_chains(
      presentation,
      semantic_sidecar,
      arguments,
    )
  )

  if not arguments:
    raise RuntimeError(
      "pi_4^3 produced no narrative arguments"
    )

  argument_index = 0
  argument = arguments[
    argument_index
  ]
  proof_chain = proof_chains[
    argument_index
  ]
  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )

  if conclusion_step is None:
    raise RuntimeError(
      "argument 0 has no conclusion step"
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
  local_step_ids = frozenset(
    id(step)
    for block in local_body
    for step in block.steps
  )
  step_lookup = _step_by_id(
    local_body
  )
  block_index_by_step = _block_index_by_step_id(
    blocks
  )

  print("=== ARGUMENT 0 ===")
  print(
    "conclusion:",
    _step_label(
      conclusion_step
    ),
  )
  print(
    "local_block_count=",
    len(
      local_body
    ),
  )
  print(
    "local_step_count=",
    len(
      local_step_ids
    ),
  )
  print()

  supporting_block_providers = tuple(
    provider
    for provider in proof_chain.providers
    if (
      provider.kind
      is TodaGroupProofNarrativeProofChainProviderKind
      .SUPPORTING_BLOCK
    )
  )

  print("=== SUPPORTING-BLOCK PROVIDERS ===")
  print(
    "provider_count=",
    len(
      supporting_block_providers
    ),
  )

  anchor_steps = []

  for provider_index, provider in enumerate(
    supporting_block_providers
  ):
    block = provider.supporting_block
    print(
      f"provider {provider_index}: "
      f"role={block.role} "
      f"block_index={blocks.index(block)}"
    )

    for step_index, step in enumerate(
      block.steps
    ):
      anchor_steps.append(
        step
      )
      print(
        f"  anchor {step_index}: "
        + _step_label(
          step
        )
      )

  print()

  (
    current_chain_ids,
    current_anchor_ids,
    current_distances,
  ) = _anchored_chain_step_ids(
    presentation,
    local_body,
    proof_chain,
    conclusion_step,
  )

  print("=== CURRENT DOWNSTREAM-ORIENTED CHAIN ===")
  print(
    "chain_ids=",
    len(
      current_chain_ids
    ),
  )
  print(
    "anchor_ids=",
    len(
      current_anchor_ids
    ),
  )

  for step_id in sorted(
    current_chain_ids,
    key=lambda candidate_id: (
      current_distances.get(
        candidate_id,
        10**9,
      ),
      block_index_by_step.get(
        candidate_id,
        10**9,
      ),
    ),
  ):
    step = step_lookup.get(
      step_id
    )
    if step is None:
      continue
    print(
      f"distance_to_conclusion={current_distances.get(step_id)} "
      f"anchor={step_id in current_anchor_ids} | "
      + _step_label(
        step
      )
    )

  print()

  upstream_distance, upstream_predecessor = _upstream_ancestry(
    presentation,
    anchor_steps,
    allowed_step_ids=local_step_ids,
  )

  print("=== UPSTREAM ANCESTRY OF ALL PROVIDER ANCHORS ===")
  print(
    "upstream_step_count=",
    len(
      upstream_distance
    ),
  )

  upstream_rows = []

  for step_id, distance in upstream_distance.items():
    step = step_lookup.get(
      step_id
    )
    if step is None:
      continue

    upstream_rows.append(
      (
        distance,
        block_index_by_step.get(
          step_id,
          10**9,
        ),
        step,
      )
    )

  for distance, block_index, step in sorted(
    upstream_rows,
    key=lambda row: (
      row[0],
      row[1],
    ),
  ):
    if not _interesting(
      step
    ):
      continue
    print(
      f"upstream_distance={distance} "
      f"block={block_index} | "
      + _step_label(
        step
      )
    )

  print()

  target_specs = (
    (
      "direct_delta",
      lambda step: (
        type(
          step.conclusion
        ).__name__
        == "TodaDeltaImageUpToSignStatement"
      ),
    ),
    (
      "image_delta",
      lambda step: (
        type(
          step.conclusion
        ).__name__
        == "TodaDeltaImageFreeCyclicStatement"
      ),
    ),
    (
      "kernel_E",
      lambda step: (
        type(
          step.conclusion
        ).__name__
        == "TodaSuspensionKernelFreeCyclicStatement"
      ),
    ),
    (
      "pi4_5_zero",
      lambda step: (
        type(
          step.conclusion
        ).__name__
        == "TodaPrimaryGroupZeroStatement"
        and "pi_{4}^{5}" in _render(
          step
        )
      ),
    ),
    (
      "E_surjective",
      lambda step: (
        type(
          step.conclusion
        ).__name__
        == "TodaSuspensionSurjectiveStatement"
      ),
    ),
  )

  target_steps = {}

  for label, predicate in target_specs:
    matches = tuple(
      step
      for step in step_lookup.values()
      if predicate(
        step
      )
    )

    target_steps[
      label
    ] = matches[
      0
    ] if matches else None

  print("=== TARGET ANCESTRY MEMBERSHIP ===")

  for label, step in target_steps.items():
    if step is None:
      print(
        f"{label}: local_body=False upstream=False"
      )
      continue

    step_id = id(
      step
    )
    print(
      f"{label}: "
      f"local_body=True "
      f"current_chain={step_id in current_chain_ids} "
      f"upstream={step_id in upstream_distance} "
      f"upstream_distance={upstream_distance.get(step_id)}"
    )
    print(
      "  "
      + _step_label(
        step
      )
    )

  print()

  print("=== SHORTEST UPSTREAM PATHS TO PROVIDER ANCHORS ===")

  for label in (
    "direct_delta",
    "image_delta",
    "kernel_E",
    "pi4_5_zero",
    "E_surjective",
  ):
    step = target_steps[
      label
    ]

    if (
      step is None
      or id(
        step
      )
      not in upstream_distance
    ):
      _print_path(
        label + ":",
        (),
      )
      continue

    path = _path_to_anchor(
      id(
        step
      ),
      upstream_predecessor,
      step_lookup,
    )

    _print_path(
      label + ":",
      path,
    )

  print()

  premises = _premises_by_parent(
    presentation
  )

  print("=== LOCAL PRESENTATION EDGES AROUND TARGETS ===")

  interesting_ids = {
    id(
      step
    )
    for step in target_steps.values()
    if step is not None
  }

  interesting_ids.update(
    id(
      step
    )
    for step in anchor_steps
  )

  for parent_id, parent_step in step_lookup.items():
    child_steps = tuple(
      premise
      for premise in premises.get(
        parent_id,
        (),
      )
      if id(
        premise
      )
      in local_step_ids
    )

    if not child_steps:
      continue

    if (
      parent_id not in interesting_ids
      and not any(
        id(
          premise
        )
        in interesting_ids
        for premise in child_steps
      )
    ):
      continue

    print(
      "PARENT:",
      _step_label(
        parent_step
      ),
    )

    for premise in child_steps:
      print(
        "  PREMISE:",
        _step_label(
          premise
        ),
      )

  print()

  direct_delta = target_steps[
    "direct_delta"
  ]
  image_delta = target_steps[
    "image_delta"
  ]
  kernel_e = target_steps[
    "kernel_E"
  ]
  pi4_5_zero = target_steps[
    "pi4_5_zero"
  ]
  e_surjective = target_steps[
    "E_surjective"
  ]

  required = (
    direct_delta,
    image_delta,
    kernel_e,
  )

  quotient_side_upstream = (
    all(
      step is not None
      and id(
        step
      )
      in upstream_distance
      for step in required
    )
  )

  surjectivity_side_upstream = (
    e_surjective is not None
    and id(
      e_surjective
    )
    in upstream_distance
  )

  zero_support_upstream = (
    pi4_5_zero is not None
    and id(
      pi4_5_zero
    )
    in upstream_distance
  )

  print("=== DIAGNOSIS ===")

  if (
    quotient_side_upstream
    and surjectivity_side_upstream
    and zero_support_upstream
  ):
    print(
      "PROVIDER_ANCESTRY_CONTAINS_REQUIRED_BODY: "
      "the missing pi_4^3 body facts are upstream prerequisites of "
      "current provider anchors, but current anchored-chain construction "
      "only keeps the downstream route from anchors to conclusion."
    )
  elif quotient_side_upstream:
    print(
      "QUOTIENT_ANCESTRY_CONFIRMED_ONLY: "
      "Delta/image/kernel are upstream of provider anchors, but "
      "surjectivity support is not fully inside the same provider ancestry."
    )
  else:
    print(
      "PROVIDER_ANCESTRY_INCOMPLETE: "
      "the required Delta/image/kernel chain is not fully reachable "
      "upstream from current provider anchors; do not change chain "
      "construction before auditing argument/provider ownership."
    )

  print()
  print("=" * 78)
  print("repair3b provider-anchor ancestry audit complete")
  print("Production code changes: NONE")
  print("Existing test changes: NONE")
  print("Repository-wide pytest: NOT RUN")
  print("=" * 78)


if __name__ == "__main__":
  main()
