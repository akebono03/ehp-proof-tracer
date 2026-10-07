from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

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
from toda_group_proof_narrative_argument_body_renderer import (
  render_toda_group_proof_narrative_argument_body_markdown,
)
from toda_group_proof_narrative_argument_direct_premises import (
  extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises,
)
from toda_group_proof_narrative_argument_discourse import (
  classify_toda_group_proof_narrative_argument_discourse_roles,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  _toda_group_proof_narrative_argument_transition_by_conclusion_id,
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_exposure import (
  classify_toda_group_proof_narrative_exactness_component_exposure,
)
from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_argument_primary_exactness_component,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_narrative_transition_renderer import (
  render_toda_group_proof_narrative_transition_connector,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


ROOT_FRAGMENT = (
  r"\pi_{4}^{3} = "
  r"\mathbb{Z}/2\{\eta_{3}\}"
)


def build_data():
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
  raw_presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      raw_presentation
    )
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=semantic_sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=semantic_sidecar,
    )
  )

  return (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
  )


def main() -> int:
  (
    presentation,
    semantic_sidecar,
    blocks,
    arguments,
  ) = build_data()

  ordered_arguments = (
    order_toda_group_proof_narrative_arguments(
      arguments
    )
  )
  discourse_roles = (
    classify_toda_group_proof_narrative_argument_discourse_roles(
      arguments
    )
  )
  source_index_by_identity = {
    id(
      argument
    ): index
    for index, argument in enumerate(
      arguments
    )
  }
  transition_by_conclusion_id = (
    _toda_group_proof_narrative_argument_transition_by_conclusion_id(
      presentation,
      blocks,
      arguments,
    )
  )

  block_index_by_id = {
    id(
      block
    ): index
    for index, block in enumerate(
      blocks
    )
  }

  lines = [
    "# Phase 159 pi4_3 base multi-argument duplication audit",
    "",
    "root_fragment: "
    + ROOT_FRAGMENT,
    "",
    "## Block inventory",
    "",
  ]

  for block_index, block in enumerate(
    blocks
  ):
    root_count = sum(
      ROOT_FRAGMENT
      in str(
        proof_step.conclusion
      )
      for proof_step in block.steps
    )
    contains_root_object = any(
      proof_step is presentation.root_step
      for proof_step in block.steps
    )

    lines.extend(
      (
        "block "
        + str(
          block_index
        )
        + ": role="
        + str(
          getattr(
            block.role,
            "value",
            block.role,
          )
        )
        + ", step_count="
        + str(
          len(
            block.steps
          )
        )
        + ", contains_root_step="
        + str(
          contains_root_object
        ),
      )
    )

  lines.extend(
    (
      "",
      "## Argument detail",
      "",
    )
  )

  seen_non_exact_block_ids = set()
  seen_non_exact_step_ids = set()
  seen_exactness_contribution_keys = set()

  for ordered_position, argument in enumerate(
    ordered_arguments
  ):
    argument_index = source_index_by_identity[
      id(
        argument
      )
    ]
    discourse_role = discourse_roles[
      ordered_position
    ]
    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )
    evidence = (
      extract_toda_group_proof_narrative_argument_method_evidence(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )
    components = (
      build_toda_group_proof_narrative_exactness_method_components(
        evidence
      )
    )
    relevant_groups = (
      extract_toda_group_proof_narrative_argument_relevant_groups(
        presentation,
        blocks,
        argument,
      )
    )
    primary_component = (
      select_toda_group_proof_narrative_argument_primary_exactness_component(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )
    exactness_exposure_by_block_id = {}

    for component in components:
      exposure_class = (
        classify_toda_group_proof_narrative_exactness_component_exposure(
          relevant_groups,
          components,
          component,
        )
      )
      for evidence_block in component.evidence_blocks:
        exactness_exposure_by_block_id[
          id(
            evidence_block
          )
        ] = exposure_class

    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )
    transition = transition_by_conclusion_id.get(
      id(
        argument.conclusion_block
      )
    )
    connector = (
      None
      if transition is None
      else render_toda_group_proof_narrative_transition_connector(
        transition
      )
    )
    connector_conclusion_step = (
      None
      if connector is None
      else conclusion_step
    )
    direct_derivation_premises = (
      ()
      if connector_conclusion_step is None
      else (
        extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
          argument,
          arguments,
        )
      )
    )
    direct_derivation_support_steps = tuple(
      support_step
      for premise_step in direct_derivation_premises
      for support_step in premise_step.premises
      if all(
        support_step is not existing_step
        for existing_step in direct_derivation_premises
      )
    )

    body = (
      render_toda_group_proof_narrative_argument_body_markdown(
        presentation,
        blocks,
        local_body_blocks,
        primary_component,
        exactness_exposure_by_block_id=exactness_exposure_by_block_id,
        excluded_non_exact_block_ids=frozenset(
          seen_non_exact_block_ids
        ),
        excluded_non_exact_step_ids=frozenset(
          seen_non_exact_step_ids
        ),
        excluded_exactness_contribution_keys=frozenset(
          seen_exactness_contribution_keys
        ),
        connector_before_block_id=(
          None
          if connector is None
          else id(
            argument.conclusion_block
          )
        ),
        connector_text=connector,
        conclusion_step=connector_conclusion_step,
        direct_derivation_premises=direct_derivation_premises,
        direct_derivation_support_steps=direct_derivation_support_steps,
        context_hidden_step_ids=frozenset(),
        preserve_provenance_block_ids=frozenset(),
      )
    )

    lines.extend(
      (
        "### ordered argument "
        + str(
          ordered_position
        ),
        "",
        "source_argument_index: "
        + str(
          argument_index
        ),
        "role: "
        + str(
          getattr(
            argument.role,
            "value",
            argument.role,
          )
        ),
        "discourse_role: "
        + str(
          getattr(
            discourse_role,
            "value",
            discourse_role,
          )
        ),
        "conclusion_block_index: "
        + str(
          block_index_by_id[
            id(
              argument.conclusion_block
            )
          ]
        ),
        "conclusion_step_is_root: "
        + str(
          conclusion_step is presentation.root_step
        ),
        "connector: "
        + repr(
          connector
        ),
        "local_body_block_indices: "
        + repr(
          tuple(
            block_index_by_id[
              id(
                block
              )
            ]
            for block in local_body_blocks
          )
        ),
        "local_root_block_occurrences: "
        + str(
          sum(
            any(
              proof_step is presentation.root_step
              for proof_step in block.steps
            )
            for block in local_body_blocks
          )
        ),
        "body_root_count: "
        + str(
          body.count(
            ROOT_FRAGMENT
          )
        ),
        "",
        "BODY:",
        body,
        "",
      )
    )

    for block in local_body_blocks:
      visible_ids = {
        id(
          proof_step
        )
        for proof_step in block.steps
      }
      seen_non_exact_step_ids.update(
        visible_ids
      )
      seen_non_exact_block_ids.add(
        id(
          block
        )
      )

  base = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  lines.extend(
    (
      "## Actual base multi-argument output",
      "",
      "root_count: "
      + str(
        base.count(
          ROOT_FRAGMENT
        )
      ),
      "",
      base,
      "",
    )
  )

  report = "\n".join(
    lines
  )
  output_path = (
    Path(__file__).resolve().parent
    / "phase159_pi4_3_base_multi_argument_duplication_audit.txt"
  )
  output_path.write_text(
    report,
    encoding="utf-8",
  )

  print(
    report
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
