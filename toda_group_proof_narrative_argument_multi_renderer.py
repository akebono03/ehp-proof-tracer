from toda_group_proof_narrative_argument_body_renderer import (
  _toda_group_proof_narrative_exactness_contribution_key,
  render_toda_group_proof_narrative_argument_body_markdown,
)
from toda_group_proof_narrative_argument_direct_premises import (
  extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises,
)
from toda_group_proof_narrative_argument_discourse import (
  TodaGroupProofNarrativeArgumentDiscourseRole,
  classify_toda_group_proof_narrative_argument_discourse_roles,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_argument_renderer import (
  render_toda_group_proof_narrative_argument_header_method_section,
)
from toda_group_proof_narrative_argument_single_renderer import (
  _normalize_toda_group_proof_narrative_argument_header_spacing,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
  TodaGroupProofNarrativeArgumentRole,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_contribution_ownership import (
  filter_toda_group_proof_narrative_exactness_body_contributions,
)
from toda_group_proof_narrative_exactness_display_contributions import (
  extract_toda_group_proof_narrative_exactness_display_contributions,
)
from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_primary_exactness_component,
)
from toda_group_proof_narrative_method_evidence import (
  extract_toda_group_proof_narrative_argument_method_evidence,
)
from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeSemanticSidecar,
)
from toda_group_proof_narrative_transition_renderer import (
  render_toda_group_proof_narrative_transition_connector,
)
from toda_group_proof_narrative_transitions import (
  TodaGroupProofNarrativeTransitionRole,
  extract_toda_group_proof_narrative_transitions,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
)


def _toda_group_proof_narrative_argument_transition_by_conclusion_id(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
) -> dict[
  int,
  object,
]:
  transitions = (
    extract_toda_group_proof_narrative_transitions(
      presentation,
      blocks,
      arguments,
    )
  )

  return {
    id(
      transition.target_block
    ): transition
    for transition in transitions
  }


def render_toda_group_proof_narrative_multi_argument_markdown(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
) -> str:
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
  transition_by_conclusion_id = (
    _toda_group_proof_narrative_argument_transition_by_conclusion_id(
      presentation,
      blocks,
      arguments,
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

  rendered_arguments = []
  seen_non_exact_block_ids = set()
  seen_exactness_contribution_keys = set()

  for ordered_position, argument in enumerate(
    ordered_arguments
  ):
    discourse_role = discourse_roles[
      ordered_position
    ]

    if (
      discourse_role
      is TodaGroupProofNarrativeArgumentDiscourseRole
      .DETACHED
    ):
      continue

    argument_index = source_index_by_identity[
      id(
        argument
      )
    ]

    relevant_groups = (
      extract_toda_group_proof_narrative_argument_relevant_groups(
        presentation,
        blocks,
        argument,
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
    primary_component = (
      select_toda_group_proof_narrative_primary_exactness_component(
        relevant_groups,
        components,
      )
    )
    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )

    context_hidden_step_ids = frozenset(
      id(
        proof_step
      )
      for block in local_body_blocks
      for proof_step in block.steps
      if (
        argument.role
        is not TodaGroupProofNarrativeArgumentRole
        .ESTABLISH_DEFINITION
        and isinstance(
          proof_step.conclusion,
          TodaEtaFamilyDefinitionStatement,
        )
      )
    )
    header = (
      render_toda_group_proof_narrative_argument_header_method_section(
        argument,
        discourse_role,
        primary_component,
      )
    )
    context_hidden_step_ids = frozenset(
      id(
        proof_step
      )
      for block in local_body_blocks
      for proof_step in block.steps
      if (
        argument.role
        is not TodaGroupProofNarrativeArgumentRole
        .ESTABLISH_DEFINITION
        and isinstance(
          proof_step.conclusion,
          TodaEtaFamilyDefinitionStatement,
        )
      )
    )
    header = (
      _normalize_toda_group_proof_narrative_argument_header_spacing(
        header
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
    derivation_source_block_ids = (
      frozenset()
      if (
        transition is None
        or transition.role
        is not TodaGroupProofNarrativeTransitionRole
        .DERIVATION
      )
      else frozenset(
        id(
          source_block
        )
        for source_block in transition.source_blocks
      )
    )
    conclusion_step = (
      None
      if connector is None
      else extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )
    direct_derivation_premises = (
      ()
      if conclusion_step is None
      else (
        extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
          argument,
          arguments,
        )
      )
    )

    body = (
      render_toda_group_proof_narrative_argument_body_markdown(
        presentation,
        blocks,
        local_body_blocks,
        primary_component,
        excluded_non_exact_block_ids=frozenset(
          seen_non_exact_block_ids
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
        conclusion_step=conclusion_step,
        direct_derivation_premises=direct_derivation_premises,
        context_hidden_step_ids=context_hidden_step_ids,
        preserve_provenance_block_ids=(
          derivation_source_block_ids
        ),
      )
    )

    parts = tuple(
      part
      for part in (
        header,
        body,
      )
      if part
    )
    rendered = "\n\n".join(
      parts
    )

    if rendered:
      rendered_arguments.append(
        rendered
      )

    for block in local_body_blocks:
      if (
        block.role
        is not TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS
      ):
        seen_non_exact_block_ids.add(
          id(
            block
          )
        )
        continue

      contributions = (
        extract_toda_group_proof_narrative_exactness_display_contributions(
          presentation,
          block,
        )
      )
      body_contributions = (
        filter_toda_group_proof_narrative_exactness_body_contributions(
          block,
          contributions,
          primary_component,
        )
      )

      for contribution in body_contributions:
        seen_exactness_contribution_keys.add(
          _toda_group_proof_narrative_exactness_contribution_key(
            contribution
          )
        )

  return "\n\n".join(
    rendered_arguments
  )


