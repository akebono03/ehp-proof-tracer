from dataclasses import dataclass

from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from toda_human_readable_renderer import (
  render_toda_expression_latex,
  render_toda_target_latex,
)
from toda_presentation import (
  build_toda_target_presentation,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from toda_rules import (
  Toda53NuPrimeBracketSpecializationStatement,
  TodaDeltaSurjectiveStatement,
  TodaLemma57TwoIota5ImageMembershipStatement,
)


@dataclass(frozen=True)
class RepositoryOperationQueryProofReplayStatementPresentation:
  source_statement: object
  latex: str | None
  fallback_type_name: str | None

  def __post_init__(
    self,
  ) -> None:
    if (
      self.latex is not None
      and not isinstance(
        self.latex,
        str,
      )
    ):
      raise TypeError(
        "latex must be a str or None"
      )

    if (
      self.fallback_type_name is not None
      and not isinstance(
        self.fallback_type_name,
        str,
      )
    ):
      raise TypeError(
        "fallback_type_name must be a str or None"
      )

    if (
      self.latex is None
      and self.fallback_type_name is None
    ):
      raise ValueError(
        "presentation must have latex or fallback_type_name"
      )

    if (
      self.latex is not None
      and self.fallback_type_name is not None
    ):
      raise ValueError(
        "presentation must not have both latex "
        "and fallback_type_name"
      )

    if (
      self.latex is not None
      and not self.latex
    ):
      raise ValueError(
        "latex must not be empty"
      )

    if (
      self.fallback_type_name is not None
      and not self.fallback_type_name
    ):
      raise ValueError(
        "fallback_type_name must not be empty"
      )


def _render_existing_statement_latex(
  statement,
) -> str | None:
  latex = (
    render_toda_proof_statement_latex(
      statement
    )
  )

  if latex is not None:
    return latex

  try:
    return render_repository_conclusion_latex(
      statement
    )
  except (
    TypeError,
    ValueError,
  ):
    return None


def _render_nu_prime_bracket_specialization_latex(
  statement: Toda53NuPrimeBracketSpecializationStatement,
) -> str:
  return render_repository_conclusion_latex(
    statement.bracket_membership
  )


def _render_lemma57_two_iota5_image_membership_latex(
  statement: TodaLemma57TwoIota5ImageMembershipStatement,
) -> str:
  return (
    render_toda_expression_latex(
      statement.element
    )
    + r" \in 2\iota_{5}\circ "
    + render_toda_target_latex(
      build_toda_target_presentation(
        statement.source_group
      )
    )
  )


def _render_delta_surjective_latex(
  statement: TodaDeltaSurjectiveStatement,
) -> str:
  group_map = (
    statement.map
  )

  return (
    r"\Delta: "
    + render_toda_target_latex(
      build_toda_target_presentation(
        group_map.source_group
      )
    )
    + r" \to "
    + render_toda_target_latex(
      build_toda_target_presentation(
        group_map.target_group
      )
    )
    + r" \text{ is surjective}"
  )


def build_repository_operation_query_proof_replay_statement_presentation(
  statement,
) -> RepositoryOperationQueryProofReplayStatementPresentation:
  latex = (
    _render_existing_statement_latex(
      statement
    )
  )

  if latex is None:
    if isinstance(
      statement,
      Toda53NuPrimeBracketSpecializationStatement,
    ):
      latex = (
        _render_nu_prime_bracket_specialization_latex(
          statement
        )
      )
    elif isinstance(
      statement,
      TodaLemma57TwoIota5ImageMembershipStatement,
    ):
      latex = (
        _render_lemma57_two_iota5_image_membership_latex(
          statement
        )
      )
    elif isinstance(
      statement,
      TodaDeltaSurjectiveStatement,
    ):
      latex = (
        _render_delta_surjective_latex(
          statement
        )
      )

  if latex is not None:
    return (
      RepositoryOperationQueryProofReplayStatementPresentation(
        source_statement=statement,
        latex=latex,
        fallback_type_name=None,
      )
    )

  return RepositoryOperationQueryProofReplayStatementPresentation(
    source_statement=statement,
    latex=None,
    fallback_type_name=type(
      statement
    ).__name__,
  )
