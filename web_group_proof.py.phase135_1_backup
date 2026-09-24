from dataclasses import dataclass

from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)
from toda_group_query import TodaGroupQuery
from toda_group_query_semantics import (
  TodaGroupQueryDomainKind,
  classify_toda_group_query_domain,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_outline_renderer import (
  render_toda_group_proof_outline_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


@dataclass(frozen=True)
class WebGroupProofStepView:
  depth: int
  statement_latex: str | None
  fallback_type_name: str | None
  rule_name: str
  role_name: str

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

    if not isinstance(
      self.role_name,
      str,
    ):
      raise TypeError(
        "role_name must be a str"
      )

    if not self.role_name:
      raise ValueError(
        "role_name must not be empty"
      )


@dataclass(frozen=True)
class WebGroupProofRenderedLineView:
  kind: str
  indent_level: int
  prefix: str
  statement_latex: str | None
  suffix: str

  def __post_init__(
    self,
  ) -> None:
    if self.kind not in (
      "heading",
      "text",
    ):
      raise ValueError(
        "kind must be heading or text"
      )

    if (
      isinstance(
        self.indent_level,
        bool,
      )
      or not isinstance(
        self.indent_level,
        int,
      )
    ):
      raise TypeError(
        "indent_level must be an int"
      )

    if self.indent_level < 0:
      raise ValueError(
        "indent_level must be nonnegative"
      )

    if not isinstance(
      self.prefix,
      str,
    ):
      raise TypeError(
        "prefix must be a str"
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

    if not isinstance(
      self.suffix,
      str,
    ):
      raise TypeError(
        "suffix must be a str"
      )


@dataclass(frozen=True)
class WebGroupProofView:
  n: int
  k: int
  conclusion_latex: str
  theorem: str | None
  phase: str | None
  key: str
  steps: tuple[
    WebGroupProofStepView,
    ...,
  ]
  max_depth: int
  mode: str = "trace"
  rendered_lines: tuple[
    WebGroupProofRenderedLineView,
    ...,
  ] = ()

  def __post_init__(
    self,
  ) -> None:
    for name, value in (
      ("n", self.n),
      ("k", self.k),
    ):
      if (
        isinstance(
          value,
          bool,
        )
        or not isinstance(
          value,
          int,
        )
      ):
        raise TypeError(
          f"{name} must be an int"
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
        WebGroupProofStepView,
      ):
        raise TypeError(
          "steps must contain only "
          "WebGroupProofStepView values"
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

    if self.mode not in (
      "trace",
      "outline",
      "narrative",
    ):
      raise ValueError(
        "mode must be trace, outline, or narrative"
      )

    if not isinstance(
      self.rendered_lines,
      tuple,
    ):
      raise TypeError(
        "rendered_lines must be a tuple"
      )

    for line in self.rendered_lines:
      if not isinstance(
        line,
        WebGroupProofRenderedLineView,
      ):
        raise TypeError(
          "rendered_lines must contain only "
          "WebGroupProofRenderedLineView values"
        )

    if (
      self.mode == "trace"
      and self.rendered_lines
    ):
      raise ValueError(
        "trace mode must not have rendered_lines"
      )

    if (
      self.mode != "trace"
      and not self.rendered_lines
    ):
      raise ValueError(
        "outline and narrative modes require "
        "rendered_lines"
      )


def _group_proof_rule_name(
  proof_step,
) -> str:
  if proof_step.inference_rule is not None:
    return proof_step.inference_rule.name

  return proof_step.rule.value


def _group_proof_statement_latex(
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


def _split_group_proof_rendered_line(
  line: str,
) -> tuple[
  str,
  str | None,
  str,
]:
  first_math = line.find(
    "$"
  )

  if first_math < 0:
    return (
      line,
      None,
      "",
    )

  second_math = line.find(
    "$",
    first_math + 1,
  )

  if second_math < 0:
    return (
      line,
      None,
      "",
    )

  return (
    line[
      :first_math
    ],
    line[
      first_math + 1:
      second_math
    ],
    line[
      second_math + 1:
    ],
  )


def _build_group_proof_rendered_lines(
  markdown: str,
) -> tuple[
  WebGroupProofRenderedLineView,
  ...,
]:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  lines = []

  for raw_line in markdown.splitlines():
    if not raw_line:
      continue

    if raw_line.startswith(
      "# "
    ):
      continue

    stripped = raw_line.lstrip(
      " "
    )
    leading_spaces = (
      len(
        raw_line
      )
      - len(
        stripped
      )
    )
    indent_level = (
      leading_spaces // 2
    )

    if stripped.startswith(
      "## "
    ):
      lines.append(
        WebGroupProofRenderedLineView(
          kind="heading",
          indent_level=0,
          prefix=stripped[
            3:
          ],
          statement_latex=None,
          suffix="",
        )
      )
      continue

    (
      prefix,
      statement_latex,
      suffix,
    ) = _split_group_proof_rendered_line(
      stripped
    )

    lines.append(
      WebGroupProofRenderedLineView(
        kind="text",
        indent_level=indent_level,
        prefix=prefix,
        statement_latex=statement_latex,
        suffix=suffix,
      )
    )

  return tuple(
    lines
  )


def build_standard_web_group_proof_view(
  n: int,
  k: int,
  max_depth: int = 1,
  mode: str = "trace",
) -> WebGroupProofView:
  query = TodaGroupQuery(
    n=n,
    k=k,
  )

  domain = (
    classify_toda_group_query_domain(
      query
    )
  )

  if (
    domain.kind
    is not (
      TodaGroupQueryDomainKind
      .POSITIVE_DIMENSION
    )
  ):
    raise ValueError(
      "group proof is available only for "
      "repository-backed group results"
    )

  if (
    isinstance(
      max_depth,
      bool,
    )
    or not isinstance(
      max_depth,
      int,
    )
  ):
    raise TypeError(
      "max_depth must be an int"
    )

  if max_depth < 0:
    raise ValueError(
      "max_depth must be nonnegative"
    )

  if mode not in (
    "trace",
    "outline",
    "narrative",
  ):
    raise ValueError(
      "mode must be trace, outline, or narrative"
    )

  report = (
    build_standard_toda_report(
      n=n,
      k=k,
    )
  )

  if (
    report.status
    is TodaCalculationStatus.NOT_FOUND
  ):
    raise ValueError(
      "no proof-backed group result found"
    )

  if (
    report.status
    is TodaCalculationStatus.MULTIPLE_RESULTS
  ):
    raise ValueError(
      "group proof requires exactly one result"
    )

  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )

  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=max_depth,
    )
  )

  (
    conclusion_latex,
    conclusion_fallback,
  ) = _group_proof_statement_latex(
    replay.root_step.conclusion
  )

  if conclusion_latex is None:
    raise ValueError(
      "group conclusion is not renderable as LaTeX: "
      f"{conclusion_fallback}"
    )

  steps = []

  for replay_step in replay.steps:
    (
      statement_latex,
      fallback_type_name,
    ) = _group_proof_statement_latex(
      replay_step.proof_step.conclusion
    )

    steps.append(
      WebGroupProofStepView(
        depth=replay_step.depth,
        statement_latex=statement_latex,
        fallback_type_name=fallback_type_name,
        rule_name=(
          _group_proof_rule_name(
            replay_step.proof_step
          )
        ),
        role_name=replay_step.role.value,
      )
    )

  rendered_lines = ()

  if mode != "trace":
    presentation = (
      build_toda_group_proof_presentation(
        replay
      )
    )

    if mode == "outline":
      markdown = (
        render_toda_group_proof_outline_markdown(
          presentation
        )
      )
    else:
      markdown = (
        render_toda_group_proof_narrative_markdown(
          presentation
        )
      )

    rendered_lines = (
      _build_group_proof_rendered_lines(
        markdown
      )
    )

  return WebGroupProofView(
    n=n,
    k=k,
    conclusion_latex=conclusion_latex,
    theorem=replay.source_entry.theorem,
    phase=replay.source_entry.phase,
    key=replay.source_entry.key,
    steps=tuple(
      steps
    ),
    max_depth=replay.max_depth,
    mode=mode,
    rendered_lines=rendered_lines,
  )
