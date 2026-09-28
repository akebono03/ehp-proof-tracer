from dataclasses import dataclass
from enum import Enum

from proof import (
  ProofStep,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_proof_dependency import (
  TodaProofEdge,
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
    )
  )
