from dataclasses import dataclass

from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from repository_generator_user_execution_candidate_presentation import (
  build_repository_generator_user_execution_candidate_list_presentation,
)
from repository_generator_user_execution_facade import (
  RepositoryGeneratorUserExecutionWorkflowStatus,
  run_standard_repository_generator_user_execution_workflow,
)
from toda_human_readable_renderer import (
  _render_generator_symbol_latex,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


@dataclass(frozen=True)
class WebGeneratorExecutionCandidateView:
  candidate_number: int
  statement_latex: str | None
  fallback_type_name: str | None

  def __post_init__(
    self,
  ) -> None:
    if (
      isinstance(
        self.candidate_number,
        bool,
      )
      or not isinstance(
        self.candidate_number,
        int,
      )
    ):
      raise TypeError(
        "candidate_number must be an int"
      )

    if self.candidate_number < 1:
      raise ValueError(
        "candidate_number must be positive"
      )

    if (
      self.statement_latex is not None
      and not isinstance(
        self.statement_latex,
        str,
      )
    ):
      raise TypeError(
        "statement_latex must be a str or None"
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
      self.statement_latex is None
      and self.fallback_type_name is None
    ):
      raise ValueError(
        "candidate must have statement_latex or fallback_type_name"
      )

    if (
      self.statement_latex is not None
      and self.fallback_type_name is not None
    ):
      raise ValueError(
        "candidate must not have both statement_latex and fallback_type_name"
      )


@dataclass(frozen=True)
class WebGeneratorExecutionPremiseView:
  premise_number: int
  statement_latex: str | None
  fallback_type_name: str | None

  def __post_init__(
    self,
  ) -> None:
    if (
      isinstance(
        self.premise_number,
        bool,
      )
      or not isinstance(
        self.premise_number,
        int,
      )
    ):
      raise TypeError(
        "premise_number must be an int"
      )

    if self.premise_number < 1:
      raise ValueError(
        "premise_number must be positive"
      )

    if (
      self.statement_latex is not None
      and not isinstance(
        self.statement_latex,
        str,
      )
    ):
      raise TypeError(
        "statement_latex must be a str or None"
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
      self.statement_latex is None
      and self.fallback_type_name is None
    ):
      raise ValueError(
        "premise must have statement_latex or fallback_type_name"
      )

    if (
      self.statement_latex is not None
      and self.fallback_type_name is not None
    ):
      raise ValueError(
        "premise must not have both statement_latex and fallback_type_name"
      )


@dataclass(frozen=True)
class WebGeneratorExecutionProvenanceView:
  key: str
  theorem: str | None
  phase: str | None

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.key,
      str,
    ):
      raise TypeError(
        "key must be a str"
      )

    if not self.key:
      raise ValueError(
        "key must not be empty"
      )

    if (
      self.theorem is not None
      and not isinstance(
        self.theorem,
        str,
      )
    ):
      raise TypeError(
        "theorem must be a str or None"
      )

    if (
      self.phase is not None
      and not isinstance(
        self.phase,
        str,
      )
    ):
      raise TypeError(
        "phase must be a str or None"
      )


@dataclass(frozen=True)
class WebGeneratorExecutionView:
  generator_input: str
  generator_latex: str
  status: RepositoryGeneratorUserExecutionWorkflowStatus
  candidates: tuple[
    WebGeneratorExecutionCandidateView,
    ...,
  ]
  selected_candidate_number: int | None
  conclusion_latex: str | None
  premises: tuple[
    WebGeneratorExecutionPremiseView,
    ...,
  ]
  rule_name: str | None
  provenance: WebGeneratorExecutionProvenanceView | None

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.generator_input,
      str,
    ):
      raise TypeError(
        "generator_input must be a str"
      )

    if not self.generator_input:
      raise ValueError(
        "generator_input must not be empty"
      )

    if not isinstance(
      self.generator_latex,
      str,
    ):
      raise TypeError(
        "generator_latex must be a str"
      )

    if not self.generator_latex:
      raise ValueError(
        "generator_latex must not be empty"
      )

    if not isinstance(
      self.status,
      RepositoryGeneratorUserExecutionWorkflowStatus,
    ):
      raise TypeError(
        "status must be a RepositoryGeneratorUserExecutionWorkflowStatus"
      )

    if not isinstance(
      self.candidates,
      tuple,
    ):
      raise TypeError(
        "candidates must be a tuple"
      )

    for candidate in self.candidates:
      if not isinstance(
        candidate,
        WebGeneratorExecutionCandidateView,
      ):
        raise TypeError(
          "candidates must contain only WebGeneratorExecutionCandidateView values"
        )

    if self.selected_candidate_number is not None:
      if (
        isinstance(
          self.selected_candidate_number,
          bool,
        )
        or not isinstance(
          self.selected_candidate_number,
          int,
        )
      ):
        raise TypeError(
          "selected_candidate_number must be an int or None"
        )

      if self.selected_candidate_number < 1:
        raise ValueError(
          "selected_candidate_number must be positive"
        )

    if not isinstance(
      self.premises,
      tuple,
    ):
      raise TypeError(
        "premises must be a tuple"
      )

    for premise in self.premises:
      if not isinstance(
        premise,
        WebGeneratorExecutionPremiseView,
      ):
        raise TypeError(
          "premises must contain only WebGeneratorExecutionPremiseView values"
        )

    if (
      self.status
      is RepositoryGeneratorUserExecutionWorkflowStatus.NONE
    ):
      if (
        self.candidates
        or self.selected_candidate_number is not None
        or self.conclusion_latex is not None
        or self.premises
        or self.rule_name is not None
        or self.provenance is not None
      ):
        raise ValueError(
          "NONE status must not contain execution output"
        )
      return

    if (
      self.status
      is RepositoryGeneratorUserExecutionWorkflowStatus.AMBIGUOUS
    ):
      if len(
        self.candidates
      ) <= 1:
        raise ValueError(
          "AMBIGUOUS status requires multiple candidates"
        )

      if (
        self.selected_candidate_number is not None
        or self.conclusion_latex is not None
        or self.premises
        or self.rule_name is not None
        or self.provenance is not None
      ):
        raise ValueError(
          "AMBIGUOUS status must not contain execution output"
        )
      return

    if self.candidates:
      raise ValueError(
        "EXECUTED status must not contain candidate list"
      )

    if self.selected_candidate_number is None:
      raise ValueError(
        "EXECUTED status requires selected_candidate_number"
      )

    if not isinstance(
      self.conclusion_latex,
      str,
    ) or not self.conclusion_latex:
      raise ValueError(
        "EXECUTED status requires conclusion_latex"
      )

    if not isinstance(
      self.rule_name,
      str,
    ) or not self.rule_name:
      raise ValueError(
        "EXECUTED status requires rule_name"
      )

    if not isinstance(
      self.provenance,
      WebGeneratorExecutionProvenanceView,
    ):
      raise TypeError(
        "EXECUTED status requires provenance"
      )


def _render_execution_statement(
  statement,
) -> tuple[
  str | None,
  str | None,
]:
  try:
    latex = (
      render_repository_conclusion_latex(
        statement
      )
    )
  except (
    TypeError,
    ValueError,
  ):
    latex = (
      render_toda_proof_statement_latex(
        statement
      )
    )

  if latex is None:
    return (
      None,
      type(
        statement
      ).__name__,
    )

  return (
    latex,
    None,
  )


def build_standard_web_generator_execution_view(
  generator_input: str,
  candidate_number: int | None = None,
) -> WebGeneratorExecutionView:
  if not isinstance(
    generator_input,
    str,
  ):
    raise TypeError(
      "generator_input must be a str"
    )

  generator_input = (
    generator_input.strip()
  )

  if not generator_input:
    raise ValueError(
      "generator is required"
    )

  result = (
    run_standard_repository_generator_user_execution_workflow(
      generator_input,
      candidate_number=candidate_number,
    )
  )

  generator_latex = (
    _render_generator_symbol_latex(
      result.resolution.applicability_result.generator
    )
  )

  if (
    result.status
    is RepositoryGeneratorUserExecutionWorkflowStatus.NONE
  ):
    return WebGeneratorExecutionView(
      generator_input=generator_input,
      generator_latex=generator_latex,
      status=result.status,
      candidates=(),
      selected_candidate_number=None,
      conclusion_latex=None,
      premises=(),
      rule_name=None,
      provenance=None,
    )

  if (
    result.status
    is RepositoryGeneratorUserExecutionWorkflowStatus.AMBIGUOUS
  ):
    presentation = (
      build_repository_generator_user_execution_candidate_list_presentation(
        result
      )
    )

    candidates = []

    for candidate in presentation.candidates:
      statement_latex, fallback_type_name = (
        _render_execution_statement(
          candidate.conclusion
        )
      )

      candidates.append(
        WebGeneratorExecutionCandidateView(
          candidate_number=(
            candidate.candidate_number
          ),
          statement_latex=statement_latex,
          fallback_type_name=(
            fallback_type_name
          ),
        )
      )

    return WebGeneratorExecutionView(
      generator_input=generator_input,
      generator_latex=generator_latex,
      status=result.status,
      candidates=tuple(
        candidates
      ),
      selected_candidate_number=None,
      conclusion_latex=None,
      premises=(),
      rule_name=None,
      provenance=None,
    )

  if (
    result.status
    is not RepositoryGeneratorUserExecutionWorkflowStatus.EXECUTED
  ):
    raise RuntimeError(
      "unsupported user execution workflow status"
    )

  if result.presentation is None:
    raise RuntimeError(
      "executed workflow result must contain presentation"
    )

  if result.selected_target is None:
    raise RuntimeError(
      "executed workflow result must contain selected_target"
    )

  conclusion_latex, conclusion_fallback = (
    _render_execution_statement(
      result.presentation.conclusion
    )
  )

  if conclusion_latex is None:
    raise ValueError(
      "executed conclusion is not renderable as LaTeX: "
      f"{conclusion_fallback}"
    )

  premises = []

  for index, premise in enumerate(
    result.presentation.premises,
    start=1,
  ):
    statement_latex, fallback_type_name = (
      _render_execution_statement(
        premise.conclusion
      )
    )

    premises.append(
      WebGeneratorExecutionPremiseView(
        premise_number=index,
        statement_latex=statement_latex,
        fallback_type_name=(
          fallback_type_name
        ),
      )
    )

  root_entry = (
    result.selected_target.root_entry
  )

  return WebGeneratorExecutionView(
    generator_input=generator_input,
    generator_latex=generator_latex,
    status=result.status,
    candidates=(),
    selected_candidate_number=(
      candidate_number
      if candidate_number is not None
      else 1
    ),
    conclusion_latex=conclusion_latex,
    premises=tuple(
      premises
    ),
    rule_name=(
      result.presentation.rule_name
    ),
    provenance=(
      WebGeneratorExecutionProvenanceView(
        key=root_entry.key,
        theorem=root_entry.theorem,
        phase=root_entry.phase,
      )
    ),
  )
