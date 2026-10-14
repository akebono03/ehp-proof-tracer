from dataclasses import dataclass

from toda_conclusion_latex_renderer import render_repository_conclusion_latex
from toda_human_readable_renderer import (
  _render_generator_symbol_latex,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


@dataclass(frozen=True)
class WebGeneratorProofStepView:
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
class WebGeneratorProofView:
  generator_input: str
  generator_latex: str
  conclusion_latex: str
  steps: tuple[
    WebGeneratorProofStepView,
    ...,
  ]
  max_depth: int

  search_status: str = "not_searched"
  diagnostics: tuple[str, ...] = ()
  open_goal_count: int = 0

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

    if not self.generator_input.strip():
      raise ValueError(
        "generator is required"
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
      self.steps,
      tuple,
    ):
      raise TypeError(
        "steps must be a tuple"
      )

    if not self.steps and self.search_status == "complete":
      raise ValueError("complete proof must contain steps")

    for step in self.steps:
      if not isinstance(
        step,
        WebGeneratorProofStepView,
      ):
        raise TypeError(
          "steps must contain only "
          "WebGeneratorProofStepView values"
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


def _generator_proof_rule_name(
  proof_step,
) -> str:
  if proof_step.inference_rule is not None:
    return proof_step.inference_rule.name

  return proof_step.rule.value


def _generator_proof_statement_latex(
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


def build_standard_web_generator_proof_view(generator_input: str, max_depth: int = 1) -> WebGeneratorProofView:
  if not isinstance(generator_input, str):
    raise TypeError("generator_input must be a str")
  generator_input = generator_input.strip()
  if not generator_input:
    raise ValueError("generator is required")
  if isinstance(max_depth, bool) or not isinstance(max_depth, int):
    raise TypeError("max_depth must be an int")
  if max_depth < 0:
    raise ValueError("max_depth must be nonnegative")
  from generator_input import resolve_generator_input
  from phase165_r27_r34_typed_lookup import search_typed_generator_statements
  from toda_proof_narrative_renderer import render_toda_proof_statement_latex
  symbol = resolve_generator_input(generator_input)
  result = search_typed_generator_statements(generator_input)
  steps = tuple(WebGeneratorProofStepView(
    depth=0,
    statement_latex=render_toda_proof_statement_latex(step.conclusion),
    fallback_type_name=None,
    rule_name=_generator_proof_rule_name(step),
  ) for step in result.proven_steps)
  return WebGeneratorProofView(
    generator_input=generator_input,
    generator_latex=_render_generator_symbol_latex(symbol),
    conclusion_latex=(steps[-1].statement_latex if steps else "\\text{未証明}"),
    steps=steps,
    max_depth=max_depth,
    search_status=result.status.value,
    diagnostics=result.diagnostics,
    open_goal_count=len(result.open_goals),
  )
