from dataclasses import dataclass

from expression import Expression
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  Relation,
  RelationType,
)
from repository_element_exploration import (
  RepositoryGeneratorExplorationResult,
)
from repository_element_lookup import (
  RepositoryGeneratorOccurrence,
)
from toda_human_readable_renderer import (
  render_toda_expression_latex,
  render_toda_group_structure_latex,
  render_toda_target_latex,
)
from toda_presentation import (
  build_toda_group_structure_presentation,
  build_toda_target_presentation,
)
from toda_rules import (
  TodaBracketMembershipStatement,
  TodaBracketMembershipTheoremStatement,
)


@dataclass(frozen=True)
class RepositoryGeneratorOccurrencePresentation:
  source_occurrence: RepositoryGeneratorOccurrence
  conclusion_latex: str

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_occurrence,
      RepositoryGeneratorOccurrence,
    ):
      raise TypeError(
        "source_occurrence must be a "
        "RepositoryGeneratorOccurrence"
      )

    if not isinstance(
      self.conclusion_latex,
      str,
    ):
      raise TypeError(
        "conclusion_latex must be a str"
      )


@dataclass(frozen=True)
class RepositoryGeneratorExplorationPresentation:
  source_result: RepositoryGeneratorExplorationResult
  occurrences: tuple[
    RepositoryGeneratorOccurrencePresentation,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_result,
      RepositoryGeneratorExplorationResult,
    ):
      raise TypeError(
        "source_result must be a "
        "RepositoryGeneratorExplorationResult"
      )

    if not isinstance(
      self.occurrences,
      tuple,
    ):
      raise TypeError(
        "occurrences must be a tuple"
      )

    if (
      len(
        self.occurrences
      )
      != len(
        self.source_result.occurrences
      )
    ):
      raise ValueError(
        "presentation occurrences must match "
        "source_result occurrences"
      )

    for (
      presentation_occurrence,
      source_occurrence,
    ) in zip(
      self.occurrences,
      self.source_result.occurrences,
    ):
      if not isinstance(
        presentation_occurrence,
        RepositoryGeneratorOccurrencePresentation,
      ):
        raise TypeError(
          "occurrences must contain only "
          "RepositoryGeneratorOccurrencePresentation "
          "objects"
        )

      if (
        presentation_occurrence.source_occurrence
        is not source_occurrence
      ):
        raise ValueError(
          "presentation occurrence source identity "
          "must match source_result occurrences "
          "in order"
        )


def _render_repository_conclusion_value_latex(
  value,
) -> str:
  if isinstance(
    value,
    Expression,
  ):
    return render_toda_expression_latex(
      value
    )

  if isinstance(
    value,
    TodaPrimaryGroup,
  ):
    return render_toda_target_latex(
      build_toda_target_presentation(
        value
      )
    )

  if isinstance(
    value,
    (
      FreeCyclicGroup,
      FiniteCyclicGroup,
      DirectSumGroup,
    ),
  ):
    return render_toda_group_structure_latex(
      build_toda_group_structure_presentation(
        value
      )
    )

  if (
    isinstance(
      value,
      int,
    )
    and not isinstance(
      value,
      bool,
    )
  ):
    return str(
      value
    )

  raise TypeError(
    "unsupported conclusion value for "
    "LaTeX rendering"
  )


def render_repository_conclusion_latex(
  conclusion,
) -> str:
  if isinstance(
    conclusion,
    Relation,
  ):
    if (
      conclusion.relation_type
      is not RelationType.EQUALITY
    ):
      raise ValueError(
        "only equality Relation conclusions "
        "are supported in Phase 99-18"
      )

    return (
      _render_repository_conclusion_value_latex(
        conclusion.lhs
      )
      + " = "
      + _render_repository_conclusion_value_latex(
        conclusion.rhs
      )
    )

  if isinstance(
    conclusion,
    (
      TodaBracketMembershipStatement,
      TodaBracketMembershipTheoremStatement,
    ),
  ):
    return (
      render_toda_expression_latex(
        conclusion.element
      )
      + r" \in "
      + render_toda_expression_latex(
        conclusion.bracket
      )
    )

  if isinstance(
    conclusion,
    Expression,
  ):
    return render_toda_expression_latex(
      conclusion
    )

  raise TypeError(
    "unsupported repository conclusion for "
    "LaTeX rendering"
  )


def build_repository_generator_exploration_presentation(
  result: RepositoryGeneratorExplorationResult,
) -> RepositoryGeneratorExplorationPresentation:
  if not isinstance(
    result,
    RepositoryGeneratorExplorationResult,
  ):
    raise TypeError(
      "result must be a "
      "RepositoryGeneratorExplorationResult"
    )

  occurrences = tuple(
    RepositoryGeneratorOccurrencePresentation(
      source_occurrence=occurrence,
      conclusion_latex=(
        render_repository_conclusion_latex(
          occurrence
          .entry
          .step
          .conclusion
        )
      ),
    )
    for occurrence in result.occurrences
  )

  return RepositoryGeneratorExplorationPresentation(
    source_result=result,
    occurrences=occurrences,
  )
