from collections import deque
from dataclasses import (
  fields,
  is_dataclass,
)

from proof import (
  ProofStep,
  Relation,
  RelationType,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_human_readable_renderer import (
  _render_scalar_latex,
)
from toda_group_proof_narrative_argument_discourse import (
  TodaGroupProofNarrativeArgumentDiscourseRole,
  classify_toda_group_proof_narrative_argument_discourse_roles,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_argument_renderer import (
  render_toda_group_proof_narrative_argument_purpose_sentence,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
)
from toda_group_proof_narrative_contribution_ordering import (
  TodaGroupProofNarrativeContributionPlacement,
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_hidden_bridge_semantics import (
  TodaGroupProofNarrativeHiddenBridgeOperationKind,
  TodaGroupProofNarrativeHiddenBridgeSemanticRole,
  build_toda_group_proof_narrative_hidden_bridge_semantics,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_reason_renderer import (
  insert_toda_group_proof_narrative_reason_prose,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  extract_toda_group_proof_step_literature_reference,
  filter_toda_group_proof_narrative_reference_entries_by_body_usage,
  filter_toda_group_proof_narrative_reference_entries_by_step_usage,
  render_toda_group_proof_narrative_reference_entries_markdown,
  select_toda_group_proof_narrative_reference_statement_steps,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeSemanticSidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)


def _provider_anchor_index(
  markdown: str,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  provider_keys: tuple[
    tuple[str, int],
    ...,
  ],
) -> int | None:
  block_by_id = {
    id(block): block
    for block in blocks
  }
  anchor_indices = []

  for provider_kind, provider_id in provider_keys:
    if provider_kind != "block":
      continue

    block = block_by_id.get(
      provider_id
    )
    if block is None:
      continue

    for proof_step in block.steps:
      line = _render_generic_narrative_step(
        proof_step
      )
      if not line:
        continue

      line_index = markdown.find(
        line
      )
      if line_index < 0:
        continue

      anchor_indices.append(
        line_index + len(line)
      )

  if not anchor_indices:
    return None

  return max(
    anchor_indices
  )


def _argument_fallback_anchor_index(
  markdown: str,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  argument: TodaGroupProofNarrativeArgument,
  contributions,
) -> int | None:
  purpose = (
    render_toda_group_proof_narrative_argument_purpose_sentence(
      argument
    )
  )

  if purpose is None:
    return None

  purpose_index = markdown.find(
    purpose
  )

  if purpose_index < 0:
    return None

  provider_anchor_indices = tuple(
    anchor_index
    for contribution in contributions
    for anchor_index in (
      _provider_anchor_index(
        markdown,
        blocks,
        contribution.provider_keys,
      ),
    )
    if anchor_index is not None
  )

  if provider_anchor_indices:
    return max(
      provider_anchor_indices
    )

  return (
    purpose_index
    + len(
      purpose
    )
  )


def _contribution_insertion_indices(
  markdown: str,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  ordered_contributions,
) -> tuple[
  tuple[
    int | None,
    ...,
  ],
  ...,
]:
  result = []

  for argument_index, contributions in enumerate(
    ordered_contributions
  ):
    if not contributions:
      result.append(())
      continue

    argument = arguments[
      argument_index
    ]
    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )
    conclusion_index = None

    if conclusion_step is not None:
      conclusion_line = (
        _render_generic_narrative_step(
          conclusion_step
        )
      )
      candidate_index = markdown.find(
        conclusion_line
      )

      if candidate_index >= 0:
        conclusion_index = candidate_index

    if conclusion_index is None:
      conclusion_index = (
        _argument_fallback_anchor_index(
          markdown,
          blocks,
          argument,
          contributions,
        )
      )

    if conclusion_index is None:
      result.append(
        tuple(
          None
          for _ in contributions
        )
      )
      continue

    indices = [
      None
      for _ in contributions
    ]

    for contribution_index, contribution in enumerate(
      contributions
    ):
      if (
        contribution.placement
        is TodaGroupProofNarrativeContributionPlacement
        .AT_PROVIDER_ANCHOR
      ):
        anchor_index = _provider_anchor_index(
          markdown,
          blocks,
          contribution.provider_keys,
        )
        indices[
          contribution_index
        ] = (
          conclusion_index
          if anchor_index is None
          else anchor_index
        )
        continue

      if (
        contribution.placement
        is TodaGroupProofNarrativeContributionPlacement
        .BEFORE_ARGUMENT_CONCLUSION
      ):
        indices[
          contribution_index
        ] = conclusion_index

    for contribution_index in range(
      len(contributions) - 1,
      -1,
      -1,
    ):
      contribution = contributions[
        contribution_index
      ]
      if (
        contribution.placement
        is not TodaGroupProofNarrativeContributionPlacement
        .BEFORE_DEPENDENT_CONTRIBUTION
      ):
        continue

      dependent_index = next(
        (
          indices[index]
          for index in range(
            contribution_index + 1,
            len(contributions),
          )
          if indices[index] is not None
        ),
        conclusion_index,
      )
      indices[
        contribution_index
      ] = dependent_index

    result.append(
      tuple(
        indices
      )
    )

  return tuple(
    result
  )


def _direct_contribution_dependency_pairs(
  presentation: TodaGroupProofPresentation,
  ordered_contributions,
) -> frozenset[
  tuple[
    int,
    int,
  ]
]:
  contribution_step_ids = {
    id(contribution.proof_step)
    for contributions in ordered_contributions
    for contribution in contributions
  }

  return frozenset(
    (
      id(edge.premise_step),
      id(edge.parent_step),
    )
    for edge in presentation.edges
    if (
      id(edge.premise_step)
      in contribution_step_ids
      and id(edge.parent_step)
      in contribution_step_ids
    )
  )


def _shortest_path_between_steps(
  presentation: TodaGroupProofPresentation,
  source_step,
  target_step,
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

  source_id = id(
    source_step
  )
  target_id = id(
    target_step
  )
  queue = deque(
    [
      source_step,
    ]
  )
  predecessor = {}
  visited = {
    source_id,
  }

  while queue:
    current = queue.popleft()

    if id(
      current
    ) == target_id:
      break

    for child in children.get(
      id(
        current
      ),
      (),
    ):
      child_id = id(
        child
      )

      if child_id in visited:
        continue

      visited.add(
        child_id
      )
      predecessor[
        child_id
      ] = current
      queue.append(
        child
      )

  if target_id not in visited:
    return ()

  reversed_path = [
    target_step,
  ]
  current = target_step

  while id(
    current
  ) != source_id:
    current = predecessor[
      id(
        current
      )
    ]
    reversed_path.append(
      current
    )

  return tuple(
    reversed(
      reversed_path
    )
  )


def _transport_chain_connector(
  presentation: TodaGroupProofPresentation,
  source_step,
  target_step,
) -> str | None:
  path = _shortest_path_between_steps(
    presentation,
    source_step,
    target_step,
  )

  if len(
    path
  ) != 5:
    return None

  hidden_steps = path[
    1:-1
  ]
  semantic_by_step_id = {
    id(
      semantic.proof_step
    ): semantic
    for semantic in (
      build_toda_group_proof_narrative_hidden_bridge_semantics(
        presentation
      )
    )
  }
  hidden_semantics = tuple(
    semantic_by_step_id.get(
      id(
        proof_step
      )
    )
    for proof_step in hidden_steps
  )

  if any(
    semantic is None
    for semantic in hidden_semantics
  ):
    return None

  if not all(
    semantic.role
    is TodaGroupProofNarrativeHiddenBridgeSemanticRole
    .TRANSPORT
    for semantic in hidden_semantics
  ):
    return None

  reference_identities = {
    semantic.reference_identity
    for semantic in hidden_semantics
  }

  if reference_identities != {
    "Proposition 5.3",
  }:
    return None

  operation_kinds = {
    semantic.operation_kind
    for semantic in hidden_semantics
    if semantic.operation_kind is not None
  }

  if operation_kinds != {
    (
      TodaGroupProofNarrativeHiddenBridgeOperationKind
      .SUSPENSION_STABILIZATION
    ),
  }:
    return None

  return (
    "Proposition 5.3 を順次適用し, "
    "suspension による安定化を用いると, "
  )


def _contribution_connector_lines(
  presentation: TodaGroupProofPresentation,
  ordered_contributions,
) -> dict[
  int,
  str,
]:
  direct_pairs = (
    _direct_contribution_dependency_pairs(
      presentation,
      ordered_contributions,
    )
  )
  connector_by_target_step_id = {}

  for contributions in ordered_contributions:
    for contribution_index in range(
      1,
      len(contributions),
    ):
      source = contributions[
        contribution_index - 1
      ]
      target = contributions[
        contribution_index
      ]
      pair = (
        id(source.proof_step),
        id(target.proof_step),
      )

      if pair in direct_pairs:
        connector_by_target_step_id[
          id(target.proof_step)
        ] = "これより, "
        continue

      transport_connector = (
        _transport_chain_connector(
          presentation,
          source.proof_step,
          target.proof_step,
        )
      )

      if transport_connector is None:
        continue

      connector_by_target_step_id[
        id(target.proof_step)
      ] = transport_connector

  return connector_by_target_step_id


def _insert_toda_group_proof_narrative_argument_contributions(
  presentation: TodaGroupProofPresentation,
  markdown: str,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  ordered_contributions,
) -> str:
  insertion_indices = (
    _contribution_insertion_indices(
      markdown,
      blocks,
      arguments,
      ordered_contributions,
    )
  )
  connector_by_target_step_id = (
    _contribution_connector_lines(
      presentation,
      ordered_contributions,
    )
  )
  insertions_by_index = {}

  for argument_index, contributions in enumerate(
    ordered_contributions
  ):
    for contribution_index, contribution in enumerate(
      contributions
    ):
      contribution_line = (
        _render_generic_narrative_step(
          contribution.proof_step
        )
      )
      if not contribution_line:
        continue
      if not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          contribution.proof_step,
          contribution_line,
        )
      ):
        continue
      if contribution_line in markdown:
        continue

      insertion_index = insertion_indices[
        argument_index
      ][
        contribution_index
      ]
      if insertion_index is None:
        continue

      connector = (
        connector_by_target_step_id.get(
          id(
            contribution.proof_step
          )
        )
      )
      lines = []
      if connector is not None:
        lines.append(
          connector
        )
      lines.append(
        contribution_line
      )

      insertions_by_index.setdefault(
        insertion_index,
        [],
      ).append(
        "\n\n".join(
          lines
        )
      )

  rendered = markdown

  for insertion_index in sorted(
    insertions_by_index,
    reverse=True,
  ):
    contribution_fragments = insertions_by_index[
      insertion_index
    ]
    insertion = (
      "\n\n"
      + "\n\n".join(
        contribution_fragments
      )
    )

    if (
      insertion_index < len(markdown)
      and not markdown[
        insertion_index:
      ].startswith(
        "\n\n"
      )
    ):
      insertion += "\n\n"

    rendered = (
      rendered[
        :insertion_index
      ]
      + insertion
      + rendered[
        insertion_index:
      ]
    )

  return rendered

def _is_toda_group_proof_narrative_reference_statement_candidate(
  proof_step,
  rendered_statement: str,
) -> bool:
  if not rendered_statement:
    return False

  inference_rule = proof_step.inference_rule

  if (
    inference_rule is not None
    and rendered_statement == inference_rule.name
  ):
    return False

  if (
    rendered_statement
    == "`"
    + type(
      proof_step.conclusion
    ).__name__
    + "`"
  ):
    return False

  if rendered_statement == repr(
    proof_step.conclusion
  ):
    return False

  if rendered_statement == str(
    proof_step.conclusion
  ):
    return False

  return True


def _phase153_r6_nested_value_contains(
  container,
  needle,
) -> bool:
  if container is needle:
    return True

  if isinstance(
    container,
    (
      str,
      bytes,
      int,
      float,
      bool,
      type(None),
    ),
  ):
    return False

  if isinstance(
    container,
    tuple,
  ):
    return any(
      _phase153_r6_nested_value_contains(
        value,
        needle,
      )
      for value in container
    )

  if isinstance(
    container,
    list,
  ):
    return any(
      _phase153_r6_nested_value_contains(
        value,
        needle,
      )
      for value in container
    )

  if isinstance(
    container,
    dict,
  ):
    return any(
      _phase153_r6_nested_value_contains(
        value,
        needle,
      )
      for value in container.values()
    )

  if not is_dataclass(
    container
  ):
    return False

  return any(
    _phase153_r6_nested_value_contains(
      getattr(
        container,
        field.name,
      ),
      needle,
    )
    for field in fields(
      container
    )
  )


def _phase153_r6_group_relation_generators(
  statement,
) -> tuple:
  if not isinstance(
    statement,
    Relation,
  ):
    return ()

  if (
    statement.relation_type
    is not RelationType.EQUALITY
  ):
    return ()

  rhs = statement.rhs
  generator = getattr(
    rhs,
    "generator",
    None,
  )

  if generator is not None:
    return (
      generator,
    )

  summands = getattr(
    rhs,
    "summands",
    None,
  )

  if not isinstance(
    summands,
    tuple,
  ):
    return ()

  return tuple(
    generator
    for summand in summands
    for generator in (
      getattr(
        summand,
        "generator",
        None,
      ),
    )
    if generator is not None
  )


def _phase153_r6_reference_aggregate_component(
  presentation: TodaGroupProofPresentation,
  entry,
  proof_step: ProofStep,
):
  statement = proof_step.conclusion

  if not is_dataclass(
    statement
  ):
    return None

  relation_components = tuple(
    value
    for field in fields(
      statement
    )
    for value in (
      getattr(
        statement,
        field.name,
      ),
    )
    if (
      isinstance(
        value,
        Relation,
      )
      and _phase153_r6_group_relation_generators(
        value
      )
    )
  )

  if len(
    relation_components
  ) <= 1:
    return None

  external_consumers = tuple(
    edge.parent_step
    for edge in presentation.edges
    if (
      edge.premise_step
      is proof_step
      and extract_toda_group_proof_step_literature_reference(
        edge.parent_step
      )
      != entry.reference
    )
  )

  if not external_consumers:
    return None

  matching_components = []

  for component in relation_components:
    generators = (
      _phase153_r6_group_relation_generators(
        component
      )
    )

    if any(
      _phase153_r6_nested_value_contains(
        consumer.conclusion,
        generator,
      )
      for consumer in external_consumers
      for generator in generators
    ):
      matching_components.append(
        component
      )

  if len(
    matching_components
  ) != 1:
    return None

  return matching_components[
    0
  ]


def _phase153_r6_render_reference_statement(
  presentation: TodaGroupProofPresentation,
  entry,
  proof_step: ProofStep,
  rendered_statement: str,
) -> str:
  component = (
    _phase153_r6_reference_aggregate_component(
      presentation,
      entry,
      proof_step,
    )
  )

  if component is None:
    return rendered_statement

  component_step = ProofStep(
    conclusion=component,
    premises=(),
    rule=proof_step.rule,
    note=proof_step.note,
    inference_rule=proof_step.inference_rule,
  )

  return _render_generic_narrative_step(
    component_step
  )


def build_toda_group_proof_narrative_reference_reuse_marker_by_step_id(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> dict[
  int,
  str,
]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  marker_by_step_id = {}

  for entry in reference_entries:
    candidate_steps = []
    seen_rendered_statements = set()

    for proof_step in entry.proof_steps:
      rendered_statement = (
        _render_generic_narrative_step(
          proof_step
        )
      )

      if not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          proof_step,
          rendered_statement,
        )
      ):
        continue

      if rendered_statement in seen_rendered_statements:
        continue

      seen_rendered_statements.add(
        rendered_statement
      )
      candidate_steps.append(
        proof_step
      )

    selected_steps = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
    )
    marker = (
      "[R"
      + str(
        entry.number
      )
      + "]"
    )

    for proof_step in selected_steps:
      marker_by_step_id[
        id(
          proof_step
        )
      ] = marker

  return marker_by_step_id


def _toda_group_proof_narrative_reference_statement_lines_by_number(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> dict[
  int,
  tuple[
    str,
    ...,
  ],
]:
  statement_lines_by_reference_number = {}

  for entry in reference_entries:
    candidate_steps = []
    rendered_by_step_id = {}
    seen_rendered_statements = set()

    for proof_step in entry.proof_steps:
      rendered_statement = (
        _render_generic_narrative_step(
          proof_step
        )
      )

      if not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          proof_step,
          rendered_statement,
        )
      ):
        continue

      if rendered_statement in seen_rendered_statements:
        continue

      seen_rendered_statements.add(
        rendered_statement
      )
      candidate_steps.append(
        proof_step
      )
      rendered_by_step_id[
        id(
          proof_step
        )
      ] = rendered_statement

    selected_steps = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
    )

    statement_lines = tuple(
      _phase153_r6_render_reference_statement(
        presentation,
        entry,
        proof_step,
        rendered_by_step_id[
          id(
            proof_step
          )
        ],
      )
      for proof_step in selected_steps
    )

    if statement_lines:
      statement_lines_by_reference_number[
        entry.number
      ] = statement_lines

  return statement_lines_by_reference_number


def _phase153_r7_reaches_root_without_steps(
  presentation: TodaGroupProofPresentation,
  source_step: ProofStep,
  excluded_steps: tuple[
    ProofStep,
    ...,
  ],
) -> bool:
  excluded_step_ids = {
    id(
      proof_step
    )
    for proof_step in excluded_steps
  }
  children_by_step_id = {}

  for edge in presentation.edges:
    if (
      id(
        edge.parent_step
      )
      in excluded_step_ids
    ):
      continue

    children_by_step_id.setdefault(
      id(
        edge.premise_step
      ),
      [],
    ).append(
      edge.parent_step
    )

  target_id = id(
    presentation.root_step
  )
  stack = [
    source_step,
  ]
  visited = set()

  while stack:
    current = stack.pop()
    current_id = id(
      current
    )

    if current_id in visited:
      continue

    visited.add(
      current_id
    )

    if current_id == target_id:
      return True

    stack.extend(
      child_step
      for child_step in children_by_step_id.get(
        current_id,
        (),
      )
      if (
        id(
          child_step
        )
        not in excluded_step_ids
      )
    )

  return False


def suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(
  presentation: TodaGroupProofPresentation,
  body_markdown: str,
  reference_entries,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  suppressed_fragments = set()
  aggregate_reference_labels = set()

  for entry in reference_entries:
    for aggregate_step in entry.proof_steps:
      component = (
        _phase153_r6_reference_aggregate_component(
          presentation,
          entry,
          aggregate_step,
        )
      )

      if component is None:
        continue

      retained_premises = tuple(
        premise_step
        for premise_step in aggregate_step.premises
        if premise_step.conclusion == component
      )

      if len(
        retained_premises
      ) != 1:
        continue

      aggregate_reference_labels.add(
        entry.reference.label
      )

      unselected_premises = tuple(
        premise_step
        for premise_step in aggregate_step.premises
        if premise_step is not retained_premises[0]
      )

      for premise_step in unselected_premises:
        blocked_sibling_steps = tuple(
          sibling_step
          for sibling_step in unselected_premises
          if sibling_step is not premise_step
        )

        if (
          _phase153_r7_reaches_root_without_steps(
            presentation,
            premise_step,
            (
              aggregate_step,
              *blocked_sibling_steps,
            ),
          )
        ):
          continue

        if isinstance(
          premise_step.conclusion,
          ScalarGreaterEqualStatement,
        ):
          rendered = (
            "$"
            + _render_scalar_latex(
              premise_step.conclusion.left
            )
            + r" \ge "
            + _render_scalar_latex(
              premise_step.conclusion.right
            )
            + "$"
          )
        else:
          rendered = (
            _render_generic_narrative_step(
              premise_step
            )
          )

        if rendered:
          suppressed_fragments.add(
            rendered
          )

  if not suppressed_fragments and not aggregate_reference_labels:
    return body_markdown

  lines = []

  for line in body_markdown.splitlines():
    if any(
      fragment in line
      for fragment in suppressed_fragments
    ):
      continue

    if (
      any(
        reference_label in line
        for reference_label in aggregate_reference_labels
      )
      and (
        "有限次元結果を得る" in line
        or "有限次元結果を示す" in line
      )
    ):
      continue

    lines.append(
      line
    )

  compacted_lines = []
  previous_blank = False

  for line in lines:
    is_blank = not line.strip()

    if is_blank and previous_blank:
      continue

    compacted_lines.append(
      line
    )
    previous_blank = is_blank

  return "\n".join(
    compacted_lines
  ).strip()


def _phase154_r5_reference_source_steps_by_number(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> dict[
  int,
  tuple[
    ProofStep,
    ...,
  ],
]:
  source_steps_by_number = {}

  for entry in reference_entries:
    candidate_steps = []
    seen_rendered_statements = set()

    for proof_step in entry.proof_steps:
      rendered_statement = (
        _render_generic_narrative_step(
          proof_step
        )
      )

      if not rendered_statement:
        continue

      if rendered_statement in seen_rendered_statements:
        continue

      seen_rendered_statements.add(
        rendered_statement
      )
      candidate_steps.append(
        proof_step
      )

    selected_steps = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
    )

    ordered_source_steps = []
    seen_step_ids = set()

    for proof_step in (
      *selected_steps,
      *entry.proof_steps,
    ):
      proof_step_id = id(
        proof_step
      )

      if proof_step_id in seen_step_ids:
        continue

      seen_step_ids.add(
        proof_step_id
      )
      ordered_source_steps.append(
        proof_step
      )

    if ordered_source_steps:
      source_steps_by_number[
        entry.number
      ] = tuple(
        ordered_source_steps
      )

  return source_steps_by_number


def _phase154_r5_unique_visible_non_root_consumer_line(
  presentation: TodaGroupProofPresentation,
  source_steps: tuple[
    ProofStep,
    ...,
  ],
  body_markdown: str,
) -> str | None:
  if not source_steps:
    return None

  source_step_ids = {
    id(
      source_step
    )
    for source_step in source_steps
  }
  children_by_step_id = {}

  for edge in presentation.edges:
    children_by_step_id.setdefault(
      id(
        edge.premise_step
      ),
      [],
    ).append(
      edge.parent_step
    )

  queue = deque(
    (
      source_step,
      0,
    )
    for source_step in source_steps
  )
  visited_distance_by_step_id = {}
  visible_by_distance = {}

  while queue:
    current_step, distance = queue.popleft()
    current_step_id = id(
      current_step
    )
    known_distance = visited_distance_by_step_id.get(
      current_step_id
    )

    if (
      known_distance is not None
      and known_distance <= distance
    ):
      continue

    visited_distance_by_step_id[
      current_step_id
    ] = distance

    for child_step in children_by_step_id.get(
      current_step_id,
      (),
    ):
      child_step_id = id(
        child_step
      )
      child_distance = distance + 1

      if child_step_id in source_step_ids:
        queue.append(
          (
            child_step,
            child_distance,
          )
        )
        continue

      if child_step is presentation.root_step:
        continue

      rendered_child = (
        _render_generic_narrative_step(
          child_step
        )
      )

      if (
        rendered_child
        and rendered_child in body_markdown
      ):
        visible_by_distance.setdefault(
          child_distance,
          [],
        ).append(
          rendered_child
        )
        continue

      queue.append(
        (
          child_step,
          child_distance,
        )
      )

  if not visible_by_distance:
    return None

  nearest_distance = min(
    visible_by_distance
  )
  nearest_lines = tuple(
    dict.fromkeys(
      visible_by_distance[
        nearest_distance
      ]
    )
  )

  if len(
    nearest_lines
  ) != 1:
    return None

  return nearest_lines[
    0
  ]


def link_toda_group_proof_narrative_reference_body_consumers(
  presentation: TodaGroupProofPresentation,
  body_markdown: str,
  reference_entries,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  source_steps_by_number = (
    _phase154_r5_reference_source_steps_by_number(
      presentation,
      reference_entries,
    )
  )
  lines = body_markdown.splitlines()

  for reference_number, source_steps in (
    source_steps_by_number.items()
  ):
    marker = (
      "[R"
      + str(
        reference_number
      )
      + "]"
    )

    marker_indices = tuple(
      index
      for index, line in enumerate(
        lines
      )
      if (
        marker in line
        and line.rstrip().endswith(
          marker
          + "を用いる."
        )
      )
    )

    if len(
      marker_indices
    ) != 1:
      continue

    current_body = "\n".join(
      lines
    )
    consumer_line = (
      _phase154_r5_unique_visible_non_root_consumer_line(
        presentation,
        source_steps,
        current_body,
      )
    )

    if consumer_line is None:
      continue

    consumer_indices = tuple(
      index
      for index, line in enumerate(
        lines
      )
      if (
        index != marker_indices[0]
        and consumer_line in line
      )
    )

    if len(
      consumer_indices
    ) != 1:
      continue

    marker_index = marker_indices[
      0
    ]
    consumer_index = consumer_indices[
      0
    ]

    if consumer_index <= marker_index:
      continue

    lines[
      marker_index
    ] = (
      marker
      + "より, "
      + consumer_line
    )
    del lines[
      consumer_index
    ]

  compacted_lines = []
  previous_blank = False

  for line in lines:
    is_blank = not line.strip()

    if is_blank and previous_blank:
      continue

    compacted_lines.append(
      line
    )
    previous_blank = is_blank

  return "\n".join(
    compacted_lines
  ).strip()

def suppress_toda_group_proof_narrative_reference_body_restatements(
  body_markdown: str,
  statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
) -> str:
  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  if not isinstance(
    statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be a dict"
    )

  derivation_tokens = (
    "これらから",
    "このことから",
    "したがって",
    "従って",
    "よって",
    "ゆえに",
    "以上より",
    "ここから",
    "計算",
    "導く",
    "導か",
    "得る",
    "従う",
    "分かる",
    "わかる",
    "示す",
    "確認",
  )

  lines = body_markdown.splitlines()

  for reference_number, statement_lines in (
    statement_lines_by_reference_number.items()
  ):
    if (
      isinstance(
        reference_number,
        bool,
      )
      or not isinstance(
        reference_number,
        int,
      )
    ):
      raise TypeError(
        "statement_lines_by_reference_number keys "
        "must be integers"
      )

    if not isinstance(
      statement_lines,
      tuple,
    ):
      raise TypeError(
        "statement_lines_by_reference_number values "
        "must be tuples"
      )

    marker = (
      "[R"
      + str(
        reference_number
      )
      + "]"
    )

    for statement_line in statement_lines:
      if not isinstance(
        statement_line,
        str,
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must contain only strings"
        )

      if not statement_line:
        continue

      updated_lines = []

      for line in lines:
        if statement_line not in line:
          updated_lines.append(
            line
          )
          continue

        stripped = line.strip()

        if stripped == statement_line:
          continue

        if any(
          token in line
          for token in derivation_tokens
        ):
          updated_lines.append(
            line
          )
          continue

        if marker in line:
          updated_lines.append(
            marker
            + "を用いる."
          )
          continue

        replaced_line = line.replace(
          statement_line,
          marker,
        )

        if replaced_line.rstrip().endswith(
          marker
        ):
          replaced_line = (
            replaced_line.rstrip()
            + "を用いる."
          )

        updated_lines.append(
          replaced_line
        )

      lines = updated_lines

  compacted_lines = []
  previous_blank = False

  for line in lines:
    is_blank = not line.strip()

    if is_blank and previous_blank:
      continue

    compacted_lines.append(
      line
    )
    previous_blank = is_blank

  return "\n".join(
    compacted_lines
  ).strip()

def suppress_toda_group_proof_narrative_reference_body_duplicates(
  body_markdown: str,
  statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
) -> str:
  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  if not isinstance(
    statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be a dict"
    )

  lines = body_markdown.splitlines()

  for reference_number, statement_lines in (
    statement_lines_by_reference_number.items()
  ):
    if (
      isinstance(
        reference_number,
        bool,
      )
      or not isinstance(
        reference_number,
        int,
      )
    ):
      raise TypeError(
        "statement_lines_by_reference_number keys "
        "must be integers"
      )

    if not isinstance(
      statement_lines,
      tuple,
    ):
      raise TypeError(
        "statement_lines_by_reference_number values "
        "must be tuples"
      )

    marker = (
      "[R"
      + str(
        reference_number
      )
      + "]"
    )

    for statement_line in statement_lines:
      if not isinstance(
        statement_line,
        str,
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must contain only strings"
        )

      if not statement_line:
        continue

      updated_lines = []

      for line in lines:
        if statement_line not in line:
          updated_lines.append(
            line
          )
          continue

        if line.strip() == statement_line:
          continue

        if marker in line:
          updated_lines.append(
            marker
            + "を用いる."
          )
          continue

        replaced_line = line.replace(
          statement_line,
          marker,
        )

        if (
          marker in replaced_line
          and (
            replaced_line.rstrip().endswith(
              marker
              + "を得る."
            )
            or replaced_line.rstrip().endswith(
              marker
              + "を得る."
            )
          )
        ):
          updated_lines.append(
            marker
            + "を用いる."
          )
          continue

        if replaced_line.rstrip().endswith(
          marker
        ):
          updated_lines.append(
            replaced_line.rstrip()
            + "を用いる."
          )
          continue

        updated_lines.append(
          replaced_line
        )

      lines = updated_lines

  compacted_lines = []
  previous_blank = False

  for line in lines:
    is_blank = not line.strip()

    if is_blank and previous_blank:
      continue

    compacted_lines.append(
      line
    )
    previous_blank = is_blank

  return "\n".join(
    compacted_lines
  ).strip()

def build_toda_group_proof_narrative_generic_used_step_ids(
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
  ordered_contributions,
) -> frozenset[
  int
]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

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
  used_step_ids = set()

  for ordered_position, argument in enumerate(
    ordered_arguments
  ):
    if (
      discourse_roles[
        ordered_position
      ]
      is TodaGroupProofNarrativeArgumentDiscourseRole.DETACHED
    ):
      continue

    argument_index = source_index_by_identity[
      id(
        argument
      )
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

    used_step_ids.update(
      id(
        proof_step
      )
      for block in local_body_blocks
      for proof_step in block.steps
    )

  used_step_ids.update(
    id(
      contribution.proof_step
    )
    for contributions in ordered_contributions
    for contribution in contributions
  )

  return frozenset(
    used_step_ids
  )


def _toda_group_proof_narrative_reference_boundary_step_ids(
  reference_entries,
) -> frozenset[int]:
  return frozenset(
    id(
      proof_step
    )
    for entry in reference_entries
    for proof_step in entry.proof_steps
  )


def _toda_group_proof_narrative_reference_owned_step_ids(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> frozenset[int]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  consumers_by_step_id = {}

  for edge in presentation.edges:
    consumers_by_step_id.setdefault(
      id(
        edge.premise_step
      ),
      [],
    ).append(
      edge.parent_step
    )

  all_owned_step_ids = set()

  for entry in reference_entries:
    entry_step_ids = {
      id(
        proof_step
      )
      for proof_step in entry.proof_steps
    }
    owned_step_ids = set(
      entry_step_ids
    )

    changed = True

    while changed:
      changed = False

      for edge in presentation.edges:
        if (
          id(
            edge.parent_step
          )
          not in owned_step_ids
        ):
          continue

        premise_step = edge.premise_step
        premise_step_id = id(
          premise_step
        )

        if (
          premise_step
          is presentation.root_step
          or premise_step_id
          in owned_step_ids
        ):
          continue

        premise_reference = (
          extract_toda_group_proof_step_literature_reference(
            premise_step
          )
        )

        if premise_reference is not None:
          continue

        consumers = tuple(
          consumers_by_step_id.get(
            premise_step_id,
            (),
          )
        )

        if not consumers:
          continue

        if not all(
          id(
            consumer
          )
          in owned_step_ids
          for consumer in consumers
        ):
          continue

        owned_step_ids.add(
          premise_step_id
        )
        changed = True

    all_owned_step_ids.update(
      owned_step_ids
    )

  return frozenset(
    all_owned_step_ids
  )


def _toda_group_proof_narrative_reference_internal_step_ids(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> frozenset[int]:
  selected_step_ids = set()

  for entry in reference_entries:
    candidate_steps = []
    seen_rendered_statements = set()

    for proof_step in entry.proof_steps:
      rendered_statement = (
        _render_generic_narrative_step(
          proof_step
        )
      )

      if not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          proof_step,
          rendered_statement,
        )
      ):
        continue

      if rendered_statement in seen_rendered_statements:
        continue

      seen_rendered_statements.add(
        rendered_statement
      )
      candidate_steps.append(
        proof_step
      )

    selected_steps = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
    )

    selected_step_ids.update(
      id(
        proof_step
      )
      for proof_step in selected_steps
    )

  owned_step_ids = (
    _toda_group_proof_narrative_reference_owned_step_ids(
      presentation,
      reference_entries,
    )
  )

  return frozenset(
    step_id
    for step_id in owned_step_ids
    if step_id not in selected_step_ids
  )


def suppress_toda_group_proof_narrative_reference_internal_body(
  presentation: TodaGroupProofPresentation,
  body_markdown: str,
  reference_entries,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  internal_step_ids = (
    _toda_group_proof_narrative_reference_internal_step_ids(
      presentation,
      reference_entries,
    )
  )

  if not internal_step_ids:
    return body_markdown

  internal_statement_lines = {
    rendered
    for entry in reference_entries
    for proof_step in entry.proof_steps
    if id(
      proof_step
    )
    in internal_step_ids
    for rendered in (
      _render_generic_narrative_step(
        proof_step
      ),
    )
    if rendered
  }

  internal_purpose_sentences = set()

  for argument in arguments:
    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )

    if (
      conclusion_step is None
      or id(
        conclusion_step
      )
      not in internal_step_ids
    ):
      continue

    purpose = (
      render_toda_group_proof_narrative_argument_purpose_sentence(
        argument
      )
    )

    if purpose is not None:
      internal_purpose_sentences.add(
        purpose
      )

  retained_lines = []

  for line in body_markdown.splitlines():
    stripped = line.strip()

    if stripped in internal_statement_lines:
      continue

    if any(
      stripped.endswith(
        purpose
      )
      for purpose in internal_purpose_sentences
    ):
      continue

    retained_lines.append(
      line
    )

  compacted_lines = []
  previous_blank = False

  for line in retained_lines:
    is_blank = not line.strip()

    if is_blank and previous_blank:
      continue

    compacted_lines.append(
      line
    )
    previous_blank = is_blank

  return "\n".join(
    compacted_lines
  ).strip()


def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
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
  base_markdown = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  proof_chains = (
    build_toda_group_proof_narrative_proof_chains(
      presentation,
      semantic_sidecar,
      arguments,
    )
  )
  ordered_contributions = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
      current_markdown=base_markdown,
    )
  )
  contribution_markdown = (
    _insert_toda_group_proof_narrative_argument_contributions(
      presentation,
      base_markdown,
      blocks,
      arguments,
      ordered_contributions,
    )
  )
  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
  )
  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      reference_entries,
      statement_lines_by_reference_number,
      presentation.root_step,
    )
  )

  reference_owned_step_ids = (
    _toda_group_proof_narrative_reference_owned_step_ids(
      presentation,
      reference_entries,
    )
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )
  boundary_filtered_reason_sidecar = type(
    reason_sidecar
  )(
    presentation=reason_sidecar.presentation,
    reasons=tuple(
      reason
      for reason in reason_sidecar.reasons
      if id(
        reason.conclusion_step
      )
      not in reference_owned_step_ids
    ),
  )

  rendered = (
    insert_toda_group_proof_narrative_reason_prose(
      contribution_markdown,
      boundary_filtered_reason_sidecar,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_reference_internal_body(
      presentation,
      rendered,
      reference_entries,
      arguments,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(
      presentation,
      rendered,
      reference_entries,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      rendered,
      statement_lines_by_reference_number,
    )
  )
  rendered = (
    link_toda_group_proof_narrative_reference_body_consumers(
      presentation,
      rendered,
      reference_entries,
    )
  )

  generic_used_step_ids = (
    build_toda_group_proof_narrative_generic_used_step_ids(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      ordered_contributions,
    )
  )

  if "[R" in rendered:
    (
      reference_entries,
      statement_lines_by_reference_number,
      rendered,
    ) = (
      filter_toda_group_proof_narrative_reference_entries_by_body_usage(
        reference_entries,
        statement_lines_by_reference_number,
        rendered,
      )
    )
  else:
    (
      reference_entries,
      statement_lines_by_reference_number,
    ) = (
      filter_toda_group_proof_narrative_reference_entries_by_step_usage(
        reference_entries,
        statement_lines_by_reference_number,
        generic_used_step_ids,
        presentation.root_step,
      )
    )

  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )

  if not reference_section:
    return rendered

  return (
    reference_section
    + "\n\n"
    + rendered
  )
