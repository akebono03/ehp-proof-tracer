from toda_group_proof_aggregate_statement_catalog import (
  is_toda_group_proof_aggregate_statement,
)
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
from toda_group_proof_narrative_step_transitions import (
  extract_toda_group_proof_narrative_step_transitions,
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
from toda_group_proof_narrative_equation_numbering import (
  number_toda_group_proof_narrative_equations,
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
from toda_group_proof_narrative_exactness_exposure import (
  TodaGroupProofNarrativeExactnessExposureClass,
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



def _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  local_body_blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  argument: TodaGroupProofNarrativeArgument,
) -> frozenset[
  int
]:
  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )

  if conclusion_step is None:
    return frozenset()

  direct_premise_steps = list(
    conclusion_step.premises
  )

  if (
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION
  ):
    direct_premise_steps.extend(
      semantic.prerequisite_step
      for semantic in semantic_sidecar.dependency_semantics
      if (
        semantic.dependent_step
        is conclusion_step
      )
    )

  direct_premise_ids = {
    id(
      premise_step
    )
    for premise_step in direct_premise_steps
  }
  transition_step_ids = {
    id(
      step
    )
    for transition in (
      extract_toda_group_proof_narrative_step_transitions(
        presentation,
        blocks,
      )
    )
    for step in (
      transition.source_step,
      transition.target_step,
    )
  }

  protected_step_ids = (
    direct_premise_ids
    | transition_step_ids
    | {
      id(
        conclusion_step
      )
    }
  )

  if (
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION
  ):
    for proof_step in direct_premise_steps:
      protected_step_ids.update(
        id(
          premise_step
        )
        for premise_step in proof_step.premises
      )

  return frozenset(
    id(
      proof_step
    )
    for block in local_body_blocks
    for proof_step in block.steps
    if (
      id(
        proof_step
      ) not in protected_step_ids
      and not is_toda_group_proof_aggregate_statement(
        proof_step.conclusion
      )
      and block.role
      not in (
        TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS,
        TodaGroupProofNarrativeMathematicalBlockRole
        .REFERENCE,
      )
    )
  )

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
  if not arguments:
    return ""

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
  seen_non_exact_step_ids = set()
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
        evidence_block_id = id(evidence_block)
        existing_exposure = exactness_exposure_by_block_id.get(
          evidence_block_id
        )
        if (
          existing_exposure is not None
          and existing_exposure is not exposure_class
        ):
          exactness_exposure_by_block_id[evidence_block_id] = (
            TodaGroupProofNarrativeExactnessExposureClass
            .AMBIGUOUS_RELEVANT
          )
          continue
        exactness_exposure_by_block_id[evidence_block_id] = exposure_class

    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )
    local_body_block_ids = {
      id(
        block
      )
      for block in local_body_blocks
    }
    evidence_block_ids = {
      id(
        block
      )
      for block in evidence
    }
    local_body_blocks = tuple(
      block
      for block in blocks
      if (
        id(
          block
        ) in local_body_block_ids
        or id(
          block
        ) in evidence_block_ids
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
    context_hidden_step_ids = (
      context_hidden_step_ids
      | _toda_group_proof_narrative_argument_frontier_hidden_step_ids(
        presentation,
        blocks,
        local_body_blocks,
        semantic_sidecar,
        argument,
      )
    )
    header = (
      render_toda_group_proof_narrative_argument_header_method_section(
        argument,
        discourse_role,
        primary_component,
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
        conclusion_step=conclusion_step,
        direct_derivation_premises=direct_derivation_premises,
        direct_derivation_support_steps=direct_derivation_support_steps,
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

    seen_non_exact_step_ids.update(
      id(
        support_step
      )
      for support_step in direct_derivation_support_steps
    )

    for block in local_body_blocks:
      if (
        block.role
        is not TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS
      ):
        visible_step_ids = {
          id(
            proof_step
          )
          for proof_step in block.steps
          if id(
            proof_step
          ) not in context_hidden_step_ids
        }
        seen_non_exact_step_ids.update(
          visible_step_ids
        )

        if (
          len(
            visible_step_ids
          )
          == len(
            block.steps
          )
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
          exactness_exposure_by_block_id.get(id(block)),
        )
      )

      for contribution in body_contributions:
        seen_exactness_contribution_keys.add(
          _toda_group_proof_narrative_exactness_contribution_key(
            contribution
          )
        )

  rendered = "\n\n".join(
    rendered_arguments
  )

  return number_toda_group_proof_narrative_equations(
    rendered,
    presentation,
    blocks,
  )


