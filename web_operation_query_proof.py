from dataclasses import dataclass



@dataclass(frozen=True)
class WebOperationQueryProofProvenanceView:
  theorem: str | None
  phase: str | None
  key: str
  depth: int

  def __post_init__(
    self,
  ) -> None:
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
      isinstance(
        self.depth,
        bool,
      )
      or not isinstance(
        self.depth,
        int,
      )
    ):
      raise TypeError(
        "depth must be an int"
      )

    if self.depth < 0:
      raise ValueError(
        "depth must be nonnegative"
      )


@dataclass(frozen=True)
class WebOperationQueryProofStepView:
  depth: int
  statement_latex: str | None
  fallback_type_name: str | None
  rule_name: str

  def __post_init__(
    self,
  ) -> None:
    if (
      isinstance(
        self.depth,
        bool,
      )
      or not isinstance(
        self.depth,
        int,
      )
    ):
      raise TypeError(
        "depth must be an int"
      )

    if self.depth < 0:
      raise ValueError(
        "depth must be nonnegative"
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
        "proof step must have statement_latex "
        "or fallback_type_name"
      )

    if (
      self.statement_latex is not None
      and self.fallback_type_name is not None
    ):
      raise ValueError(
        "proof step must not have both "
        "statement_latex and fallback_type_name"
      )

    if not isinstance(
      self.rule_name,
      str,
    ):
      raise TypeError(
        "rule_name must be a str"
      )

    if not self.rule_name:
      raise ValueError(
        "rule_name must not be empty"
      )


@dataclass(frozen=True)
class WebOperationQueryProofView:
  query_input: str
  fact_number: int
  conclusion_latex: str
  provenance: WebOperationQueryProofProvenanceView
  steps: tuple[
    WebOperationQueryProofStepView,
    ...,
  ]
  max_depth: int

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.query_input,
      str,
    ):
      raise TypeError(
        "query_input must be a str"
      )

    if not self.query_input.strip():
      raise ValueError(
        "operation query is required"
      )

    if (
      isinstance(
        self.fact_number,
        bool,
      )
      or not isinstance(
        self.fact_number,
        int,
      )
    ):
      raise TypeError(
        "fact_number must be an int"
      )

    if self.fact_number <= 0:
      raise ValueError(
        "fact_number must be positive"
      )

    if not isinstance(
      self.conclusion_latex,
      str,
    ):
      raise TypeError(
        "conclusion_latex must be a str"
      )

    if not self.conclusion_latex:
      raise ValueError(
        "conclusion_latex must not be empty"
      )

    if not isinstance(
      self.provenance,
      WebOperationQueryProofProvenanceView,
    ):
      raise TypeError(
        "provenance must be a "
        "WebOperationQueryProofProvenanceView"
      )

    if not isinstance(
      self.steps,
      tuple,
    ):
      raise TypeError(
        "steps must be a tuple"
      )

    if not self.steps:
      raise ValueError(
        "steps must not be empty"
      )

    for step in self.steps:
      if not isinstance(
        step,
        WebOperationQueryProofStepView,
      ):
        raise TypeError(
          "steps must contain only "
          "WebOperationQueryProofStepView values"
        )

    if (
      isinstance(
        self.max_depth,
        bool,
      )
      or not isinstance(
        self.max_depth,
        int,
      )
    ):
      raise TypeError(
        "max_depth must be an int"
      )

    if self.max_depth < 0:
      raise ValueError(
        "max_depth must be nonnegative"
      )


def _operation_query_proof_rule_name(
  proof_step,
) -> str:
  if proof_step.inference_rule is not None:
    return proof_step.inference_rule.name

  return proof_step.rule.value


def build_standard_web_operation_query_proof_view(
  query_input: str,
  fact_number: int,
  max_depth: int = 1,
) -> WebOperationQueryProofView:
  """Display only steps proved by the canonical typed search, without replay."""
  from phase165_r27_r34_typed_lookup import search_typed_operation_statements
  from toda_proof_narrative_renderer import render_toda_proof_statement_latex
  if not isinstance(query_input, str):
    raise TypeError("query_input must be a str")
  query_input = query_input.strip()
  if not query_input:
    raise ValueError("operation query is required")
  if type(fact_number) is not int:
    raise TypeError("fact_number must be an int")
  if fact_number <= 0:
    raise ValueError("fact_number must be positive")
  if type(max_depth) is not int:
    raise TypeError("max_depth must be an int")
  if max_depth < 0:
    raise ValueError("max_depth must be nonnegative")
  result = search_typed_operation_statements(query_input)
  if fact_number > len(result.proven_steps):
    raise ValueError(
      "requested fact is not proved by typed backward search; "
      f"status={result.status.value}; open_goals={len(result.open_goals)}"
    )
  step = result.proven_steps[fact_number - 1]
  statement_latex = render_toda_proof_statement_latex(step.conclusion)
  if not isinstance(statement_latex, str) or not statement_latex:
    raise ValueError("typed proof conclusion is not renderable")
  rule_name = (
    step.inference_rule.name if step.inference_rule is not None
    else step.rule.value
  )
  return WebOperationQueryProofView(
    query_input=query_input,
    fact_number=fact_number,
    conclusion_latex=statement_latex,
    provenance=WebOperationQueryProofProvenanceView(
      theorem=None,
      phase=None,
      key="typed-backward-search",
      depth=0,
    ),
    steps=(WebOperationQueryProofStepView(
      depth=0,
      statement_latex=statement_latex,
      fallback_type_name=None,
      rule_name=rule_name,
    ),),
    max_depth=max_depth,
  )
