from dataclasses import dataclass
from enum import Enum

from expression import (
  HomotopyElement,
)
from proof import (
  ProofStep,
  Relation,
  RelationType,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  TodaGroupResultProofReplayResult,
  TodaGroupResultProofReplayStep,
)
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
)

from toda_proof_dependency import (
  TodaProofDependencyRole,
  TodaProofEdge,
  classify_toda_proof_step_role,
  extract_toda_recursive_proof_provenance,
)
from toda_rules import (
  TodaBracketMembershipStatement,
)


class TodaGroupProofNarrativePremiseSemanticRole(
  Enum
):
  PRECONDITION = "precondition"


class TodaGroupProofNarrativeStepSemanticRole(
  Enum
):
  DEFINITION_INTRODUCTION = (
    "definition_introduction"
  )


class TodaGroupProofNarrativeDependencySemanticRole(
  Enum
):
  PRECONDITION_FOR_DEFINITION = (
    "precondition_for_definition"
  )


@dataclass(frozen=True)
class TodaGroupProofNarrativePremiseSemantic:
  edge: TodaProofEdge
  role: (
    TodaGroupProofNarrativePremiseSemanticRole
  )

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.edge,
      TodaProofEdge,
    ):
      raise TypeError(
        "edge must be a TodaProofEdge"
      )

    if not isinstance(
      self.role,
      TodaGroupProofNarrativePremiseSemanticRole,
    ):
      raise TypeError(
        "role must be a "
        "TodaGroupProofNarrativePremiseSemanticRole"
      )


@dataclass(frozen=True)
class TodaGroupProofNarrativeStepSemantic:
  proof_step: ProofStep
  role: (
    TodaGroupProofNarrativeStepSemanticRole
  )

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.proof_step,
      ProofStep,
    ):
      raise TypeError(
        "proof_step must be a ProofStep"
      )

    if not isinstance(
      self.role,
      TodaGroupProofNarrativeStepSemanticRole,
    ):
      raise TypeError(
        "role must be a "
        "TodaGroupProofNarrativeStepSemanticRole"
      )


@dataclass(frozen=True)
class TodaGroupProofNarrativeDependencySemantic:
  prerequisite_step: ProofStep
  dependent_step: ProofStep
  role: (
    TodaGroupProofNarrativeDependencySemanticRole
  )

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.prerequisite_step,
      ProofStep,
    ):
      raise TypeError(
        "prerequisite_step must be a ProofStep"
      )

    if not isinstance(
      self.dependent_step,
      ProofStep,
    ):
      raise TypeError(
        "dependent_step must be a ProofStep"
      )

    if not isinstance(
      self.role,
      TodaGroupProofNarrativeDependencySemanticRole,
    ):
      raise TypeError(
        "role must be a "
        "TodaGroupProofNarrativeDependencySemanticRole"
      )

    if (
      self.prerequisite_step
      is self.dependent_step
    ):
      raise ValueError(
        "semantic dependency must connect "
        "different proof steps"
      )


@dataclass(frozen=True)
class TodaGroupProofNarrativeReferenceIdentity:
  label: str

  def __post_init__(self) -> None:
    if not isinstance(self.label, str) or not self.label.strip():
      raise TypeError("label must be a non-empty str")


@dataclass(frozen=True)
class TodaGroupProofNarrativeVariableBinding:
  formal_variable: object
  instantiated_expression: object

  def __post_init__(self) -> None:
    if isinstance(self.formal_variable, str):
      raise TypeError(
        "formal_variable must be a mathematical object, not a str"
      )
    if isinstance(self.instantiated_expression, str):
      raise TypeError(
        "instantiated_expression must be a mathematical object, not a str"
      )


@dataclass(frozen=True)
class TodaGroupProofNarrativeReferenceApplicationSemantic:
  dependent_step: ProofStep
  reference: TodaGroupProofNarrativeReferenceIdentity
  bindings: tuple[TodaGroupProofNarrativeVariableBinding, ...]

  def __post_init__(self) -> None:
    if not isinstance(self.dependent_step, ProofStep):
      raise TypeError("dependent_step must be a ProofStep")
    if not isinstance(
      self.reference,
      TodaGroupProofNarrativeReferenceIdentity,
    ):
      raise TypeError(
        "reference must be a TodaGroupProofNarrativeReferenceIdentity"
      )
    if not isinstance(self.bindings, tuple):
      raise TypeError("bindings must be a tuple")
    if not self.bindings:
      raise ValueError("bindings must not be empty")

    seen_formal_variables = set()
    for binding in self.bindings:
      if not isinstance(binding, TodaGroupProofNarrativeVariableBinding):
        raise TypeError(
          "bindings must contain only "
          "TodaGroupProofNarrativeVariableBinding objects"
        )
      key = repr(binding.formal_variable)
      if key in seen_formal_variables:
        raise ValueError(
          "bindings must not contain duplicate formal variables"
        )
      seen_formal_variables.add(key)


@dataclass(frozen=True)
class TodaGroupProofNarrativeSemanticSidecar:
  presentation: TodaGroupProofPresentation
  premise_semantics: tuple[
    TodaGroupProofNarrativePremiseSemantic,
    ...,
  ]
  step_semantics: tuple[
    TodaGroupProofNarrativeStepSemantic,
    ...,
  ]
  dependency_semantics: tuple[
    TodaGroupProofNarrativeDependencySemantic,
    ...,
  ] = ()
  reference_application_semantics: tuple[
    TodaGroupProofNarrativeReferenceApplicationSemantic,
    ...,
  ] = ()

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.presentation,
      TodaGroupProofPresentation,
    ):
      raise TypeError(
        "presentation must be a "
        "TodaGroupProofPresentation"
      )

    if not isinstance(
      self.premise_semantics,
      tuple,
    ):
      raise TypeError(
        "premise_semantics must be a tuple"
      )

    if not isinstance(
      self.step_semantics,
      tuple,
    ):
      raise TypeError(
        "step_semantics must be a tuple"
      )

    if not isinstance(
      self.dependency_semantics,
      tuple,
    ):
      raise TypeError(
        "dependency_semantics must be a tuple"
      )

    if not isinstance(
      self.reference_application_semantics,
      tuple,
    ):
      raise TypeError(
        "reference_application_semantics must be a tuple"
      )

    allowed_step_ids = {
      id(
        node.proof_step
      )
      for node in self.presentation.nodes
    }

    allowed_edge_keys = {
      (
        id(
          edge.parent_step
        ),
        id(
          edge.premise_step
        ),
        edge.premise_index,
      )
      for edge in self.presentation.edges
    }

    seen_premise_keys = set()

    for semantic in self.premise_semantics:
      if not isinstance(
        semantic,
        TodaGroupProofNarrativePremiseSemantic,
      ):
        raise TypeError(
          "premise_semantics must contain only "
          "TodaGroupProofNarrativePremiseSemantic "
          "objects"
        )

      edge_key = (
        id(
          semantic.edge.parent_step
        ),
        id(
          semantic.edge.premise_step
        ),
        semantic.edge.premise_index,
      )

      if edge_key not in allowed_edge_keys:
        raise ValueError(
          "premise semantic edge must appear "
          "in presentation edges"
        )

      if edge_key in seen_premise_keys:
        raise ValueError(
          "premise_semantics must not contain "
          "duplicate edges"
        )

      seen_premise_keys.add(
        edge_key
      )

    seen_step_ids = set()

    for semantic in self.step_semantics:
      if not isinstance(
        semantic,
        TodaGroupProofNarrativeStepSemantic,
      ):
        raise TypeError(
          "step_semantics must contain only "
          "TodaGroupProofNarrativeStepSemantic "
          "objects"
        )

      step_id = id(
        semantic.proof_step
      )

      if step_id not in allowed_step_ids:
        raise ValueError(
          "step semantic proof_step must appear "
          "in presentation nodes"
        )

      if step_id in seen_step_ids:
        raise ValueError(
          "step_semantics must not contain "
          "duplicate proof steps"
        )

      seen_step_ids.add(
        step_id
      )

    seen_dependency_keys = set()

    for semantic in self.dependency_semantics:
      if not isinstance(
        semantic,
        TodaGroupProofNarrativeDependencySemantic,
      ):
        raise TypeError(
          "dependency_semantics must contain only "
          "TodaGroupProofNarrativeDependencySemantic "
          "objects"
        )

      prerequisite_step_id = id(
        semantic.prerequisite_step
      )
      dependent_step_id = id(
        semantic.dependent_step
      )

      if (
        prerequisite_step_id not in allowed_step_ids
        or dependent_step_id not in allowed_step_ids
      ):
        raise ValueError(
          "semantic dependency proof steps must "
          "appear in presentation nodes"
        )

      dependency_key = (
        prerequisite_step_id,
        dependent_step_id,
        semantic.role,
      )

      if dependency_key in seen_dependency_keys:
        raise ValueError(
          "dependency_semantics must not contain "
          "duplicate dependencies"
        )

      seen_dependency_keys.add(
        dependency_key
      )


    seen_reference_application_keys = set()
    for semantic in self.reference_application_semantics:
      if not isinstance(
        semantic,
        TodaGroupProofNarrativeReferenceApplicationSemantic,
      ):
        raise TypeError(
          "reference_application_semantics must contain only "
          "TodaGroupProofNarrativeReferenceApplicationSemantic objects"
        )
      dependent_step_id = id(semantic.dependent_step)
      if dependent_step_id not in allowed_step_ids:
        raise ValueError(
          "reference application dependent_step must appear "
          "in presentation nodes"
        )
      application_key = (
        dependent_step_id,
        semantic.reference,
      )
      if application_key in seen_reference_application_keys:
        raise ValueError(
          "reference_application_semantics must not contain "
          "duplicate applications"
        )
      seen_reference_application_keys.add(application_key)


_PREMISE_ROLE_BY_RULE_NAME_AND_INDEX = {
  (
    (
      "Toda 5.3 nu-prime Lemma 5.2 "
      "Hopf specialization"
    ),
    1,
  ): (
    TodaGroupProofNarrativePremiseSemanticRole
    .PRECONDITION
  ),
  (
    (
      "Toda 5.3 nu-prime Lemma 5.2 "
      "double specialization"
    ),
    1,
  ): (
    TodaGroupProofNarrativePremiseSemanticRole
    .PRECONDITION
  ),
  (
    (
      "Toda 5.3 nu-prime Lemma 5.2 "
      "membership specialization"
    ),
    1,
  ): (
    TodaGroupProofNarrativePremiseSemanticRole
    .PRECONDITION
  ),
}


_STEP_ROLE_BY_CONSUMER_RULE_NAME_AND_INDEX = {
  (
    (
      "Toda 5.3 nu-prime Lemma 5.2 "
      "bracket specialization"
    ),
    0,
  ): (
    TodaGroupProofNarrativeStepSemanticRole
    .DEFINITION_INTRODUCTION
  ),
}


def _inference_rule_name(
  proof_step: ProofStep,
) -> str | None:
  inference_rule = (
    proof_step.inference_rule
  )

  if inference_rule is None:
    return None

  return inference_rule.name


def build_toda_group_proof_narrative_semantic_closure_presentation(
  presentation: TodaGroupProofPresentation,
) -> TodaGroupProofPresentation:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if presentation.max_depth == 0:
    return presentation

  provenance = (
    extract_toda_recursive_proof_provenance(
      presentation.source_replay.group_result
    )
  )
  selected_step_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }
  original_step_ids = frozenset(
    selected_step_ids
  )
  edges_by_parent_step_id = {}

  for edge in provenance.edges:
    edges_by_parent_step_id.setdefault(
      id(
        edge.parent_step
      ),
      [],
    ).append(
      edge
    )

  order_calculation_step_ids = set()

  for node in presentation.nodes:
    order_statement = (
      node.proof_step.conclusion
    )

    if (
      not isinstance(
        order_statement,
        Relation,
      )
      or order_statement.relation_type
      is not RelationType.ORDER
    ):
      continue

    for edge in edges_by_parent_step_id.get(
      id(
        node.proof_step
      ),
      (),
    ):
      premise_statement = (
        edge.premise_step.conclusion
      )

      if (
        isinstance(
          premise_statement,
          Relation,
        )
        and premise_statement.relation_type
        is RelationType.EQUALITY
      ):
        order_calculation_step_ids.add(
          id(
            edge.premise_step
          )
        )

  for calculation_step_id in (
    order_calculation_step_ids
  ):
    for edge in edges_by_parent_step_id.get(
      calculation_step_id,
      (),
    ):
      premise_statement = (
        edge.premise_step.conclusion
      )

      if (
        not isinstance(
          premise_statement,
          Relation,
        )
        or premise_statement.relation_type
        is not RelationType.EQUALITY
      ):
        continue

      selected_step_ids.add(
        id(
          edge.premise_step
        )
      )

  map_property_equality_step_ids = set()

  for node in presentation.nodes:
    if (
      classify_toda_proof_step_role(
        node.proof_step
      )
      is not TodaProofDependencyRole.MAP_PROPERTY
    ):
      continue

    for edge in edges_by_parent_step_id.get(
      id(
        node.proof_step
      ),
      (),
    ):
      premise_statement = (
        edge.premise_step.conclusion
      )

      if (
        isinstance(
          premise_statement,
          Relation,
        )
        and premise_statement.relation_type
        is RelationType.EQUALITY
      ):
        map_property_equality_step_ids.add(
          id(
            edge.premise_step
          )
        )

  for equality_step_id in (
    map_property_equality_step_ids
  ):
    for edge in edges_by_parent_step_id.get(
      equality_step_id,
      (),
    ):
      premise_statement = (
        edge.premise_step.conclusion
      )

      if (
        not isinstance(
          premise_statement,
          Relation,
        )
        or premise_statement.relation_type
        is not RelationType.EQUALITY
      ):
        continue

      selected_step_ids.add(
        id(
          edge.premise_step
        )
      )

  map_property_frontier = [
    node.proof_step
    for node in provenance.nodes
    if (
      id(
        node.proof_step
      )
      in selected_step_ids
      and classify_toda_proof_step_role(
        node.proof_step
      )
      is TodaProofDependencyRole.MAP_PROPERTY
    )
  ]
  expanded_map_dependency_ids = set()

  while map_property_frontier:
    current_step = map_property_frontier.pop()
    current_step_id = id(
      current_step
    )

    if (
      current_step_id
      in expanded_map_dependency_ids
    ):
      continue

    expanded_map_dependency_ids.add(
      current_step_id
    )

    current_boundary = (
      classify_toda_literature_statement_step(
        current_step
      )
    )

    if (
      current_boundary is not None
      and current_boundary.classification
      is TodaLiteratureStatementClassification.FIXED_STATEMENT
    ):
      continue

    for edge in edges_by_parent_step_id.get(
      current_step_id,
      (),
    ):
      premise_step = edge.premise_step
      premise_step_id = id(
        premise_step
      )

      selected_step_ids.add(
        premise_step_id
      )

      premise_boundary = (
        classify_toda_literature_statement_step(
          premise_step
        )
      )

      if (
        premise_boundary is not None
        and premise_boundary.classification
        is TodaLiteratureStatementClassification.FIXED_STATEMENT
      ):
        continue

      premise_role = (
        classify_toda_proof_step_role(
          premise_step
        )
      )

      if premise_role in (
        TodaProofDependencyRole.MAP_PROPERTY,
        TodaProofDependencyRole.RELATION,
        TodaProofDependencyRole.EHP_EXACTNESS,
        TodaProofDependencyRole.EHP_WINDOW,
      ):
        map_property_frontier.append(
          premise_step
        )

  changed = True

  while changed:
    changed = False

    for edge in provenance.edges:
      if (
        id(
          edge.parent_step
        )
        not in selected_step_ids
      ):
        continue

      key = (
        _inference_rule_name(
          edge.parent_step
        ),
        edge.premise_index,
      )

      if (
        key
        not in _STEP_ROLE_BY_CONSUMER_RULE_NAME_AND_INDEX
      ):
        continue

      premise_step_id = id(
        edge.premise_step
      )

      if premise_step_id in selected_step_ids:
        continue

      selected_step_ids.add(
        premise_step_id
      )
      changed = True

  if selected_step_ids == original_step_ids:
    return presentation

  replay_step_by_proof_step_id = {
    id(
      replay_step.proof_step
    ): replay_step
    for replay_step in presentation.source_replay.steps
  }

  for node in provenance.nodes:
    proof_step_id = id(
      node.proof_step
    )

    if (
      proof_step_id not in selected_step_ids
      or proof_step_id
      in replay_step_by_proof_step_id
    ):
      continue

    replay_step_by_proof_step_id[
      proof_step_id
    ] = TodaGroupResultProofReplayStep(
      depth=node.shortest_depth,
      proof_step=node.proof_step,
      role=node.role,
    )

  ordered_steps = tuple(
    replay_step_by_proof_step_id[
      id(
        node.proof_step
      )
    ]
    for node in provenance.nodes
    if (
      id(
        node.proof_step
      )
      in selected_step_ids
    )
  )
  closure_max_depth = max(
    replay_step.depth
    for replay_step in ordered_steps
  )
  source_replay = presentation.source_replay
  closure_replay = (
    TodaGroupResultProofReplayResult(
      group_result=source_replay.group_result,
      source_entry=source_replay.source_entry,
      root_step=source_replay.root_step,
      steps=ordered_steps,
      max_depth=closure_max_depth,
    )
  )

  return build_toda_group_proof_presentation(
    closure_replay
  )

def _semantic_dependency_semantics(
  presentation: TodaGroupProofPresentation,
  premise_semantics: tuple[
    TodaGroupProofNarrativePremiseSemantic,
    ...,
  ],
  step_semantics: tuple[
    TodaGroupProofNarrativeStepSemantic,
    ...,
  ],
) -> tuple[
  TodaGroupProofNarrativeDependencySemantic,
  ...,
]:
  precondition_steps = []
  seen_precondition_step_ids = set()

  for semantic in premise_semantics:
    if (
      semantic.role
      is not TodaGroupProofNarrativePremiseSemanticRole
      .PRECONDITION
    ):
      continue

    proof_step = (
      semantic.edge.premise_step
    )
    proof_step_id = id(
      proof_step
    )

    if proof_step_id in seen_precondition_step_ids:
      continue

    seen_precondition_step_ids.add(
      proof_step_id
    )
    precondition_steps.append(
      proof_step
    )

  definition_steps = tuple(
    semantic.proof_step
    for semantic in step_semantics
    if (
      semantic.role
      is TodaGroupProofNarrativeStepSemanticRole
      .DEFINITION_INTRODUCTION
    )
  )

  if (
    len(
      precondition_steps
    ) != 1
    or len(
      definition_steps
    ) != 1
  ):
    return ()

  return (
    TodaGroupProofNarrativeDependencySemantic(
      prerequisite_step=precondition_steps[
        0
      ],
      dependent_step=definition_steps[
        0
      ],
      role=(
        TodaGroupProofNarrativeDependencySemanticRole
        .PRECONDITION_FOR_DEFINITION
      ),
    ),
  )


def _reference_application_semantics(
  step_semantics: tuple[TodaGroupProofNarrativeStepSemantic, ...],
) -> tuple[TodaGroupProofNarrativeReferenceApplicationSemantic, ...]:
  applications = []

  for semantic in step_semantics:
    if (
      semantic.role
      is not TodaGroupProofNarrativeStepSemanticRole.DEFINITION_INTRODUCTION
    ):
      continue

    conclusion = semantic.proof_step.conclusion
    if not isinstance(conclusion, TodaBracketMembershipStatement):
      continue

    concrete_element = conclusion.element
    if not isinstance(concrete_element, HomotopyElement):
      continue

    formal_beta = HomotopyElement(
      name="β",
      dimension=concrete_element.dimension,
      source=concrete_element.source,
      target=concrete_element.target,
    )

    applications.append(
      TodaGroupProofNarrativeReferenceApplicationSemantic(
        dependent_step=semantic.proof_step,
        reference=TodaGroupProofNarrativeReferenceIdentity(
          label="Lemma 5.2",
        ),
        bindings=(
          TodaGroupProofNarrativeVariableBinding(
            formal_variable=formal_beta,
            instantiated_expression=concrete_element,
          ),
        ),
      )
    )

  return tuple(applications)



def build_toda_group_proof_narrative_semantic_sidecar(
  presentation: TodaGroupProofPresentation,
) -> TodaGroupProofNarrativeSemanticSidecar:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  premise_semantics = []
  step_roles_by_id = {}
  step_by_id = {}

  for edge in presentation.edges:
    rule_name = _inference_rule_name(
      edge.parent_step
    )

    if rule_name is None:
      continue

    key = (
      rule_name,
      edge.premise_index,
    )

    premise_role = (
      _PREMISE_ROLE_BY_RULE_NAME_AND_INDEX
      .get(
        key
      )
    )

    if premise_role is not None:
      premise_semantics.append(
        TodaGroupProofNarrativePremiseSemantic(
          edge=edge,
          role=premise_role,
        )
      )

    step_role = (
      _STEP_ROLE_BY_CONSUMER_RULE_NAME_AND_INDEX
      .get(
        key
      )
    )

    if step_role is None:
      continue

    premise_step_id = id(
      edge.premise_step
    )

    existing_role = (
      step_roles_by_id.get(
        premise_step_id
      )
    )

    if (
      existing_role is not None
      and existing_role is not step_role
    ):
      raise ValueError(
        "conflicting narrative step semantics"
      )

    step_roles_by_id[
      premise_step_id
    ] = step_role
    step_by_id[
      premise_step_id
    ] = edge.premise_step

  ordered_step_semantics = []

  for node in presentation.nodes:
    proof_step_id = id(
      node.proof_step
    )

    step_role = (
      step_roles_by_id.get(
        proof_step_id
      )
    )

    if step_role is None:
      continue

    ordered_step_semantics.append(
      TodaGroupProofNarrativeStepSemantic(
        proof_step=step_by_id[
          proof_step_id
        ],
        role=step_role,
      )
    )

  premise_semantics_tuple = tuple(
    premise_semantics
  )
  step_semantics_tuple = tuple(
    ordered_step_semantics
  )

  return (
    TodaGroupProofNarrativeSemanticSidecar(
      presentation=presentation,
      premise_semantics=premise_semantics_tuple,
      step_semantics=step_semantics_tuple,
      dependency_semantics=(
        _semantic_dependency_semantics(
          presentation,
          premise_semantics_tuple,
          step_semantics_tuple,
        )
      ),
      reference_application_semantics=(
        _reference_application_semantics(
          step_semantics_tuple,
        )
      ),
    )
  )
