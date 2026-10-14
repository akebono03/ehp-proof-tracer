from dataclasses import dataclass
from toda_conclusion_latex_renderer import render_repository_conclusion_latex
from toda_human_readable_renderer import render_toda_public_group_relation_latex
from toda_proof_narrative_renderer import render_toda_proof_statement_latex

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
class WebGroupProofInlineSegmentView:
  kind: str
  value: str

  def __post_init__(
    self,
  ) -> None:
    if self.kind not in (
      "text",
      "strong",
      "inline_math",
      "display_math",
    ):
      raise ValueError(
        "kind must be text, strong, "
        "inline_math, or display_math"
      )

    if not isinstance(
      self.value,
      str,
    ):
      raise TypeError(
        "value must be a str"
      )

    if not self.value:
      raise ValueError(
        "value must not be empty"
      )

@dataclass(frozen=True)
class WebGroupProofRenderedLineView:
  kind: str
  indent_level: int
  prefix: str
  statement_latex: str | None
  suffix: str
  segments: tuple[
    WebGroupProofInlineSegmentView,
    ...,
  ] = ()

  def __post_init__(
    self,
  ) -> None:
    if self.kind not in (
      "heading",
      "separator",
      "text",
    ):
      raise ValueError(
        "kind must be heading, separator, or text"
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

    if not isinstance(
      self.segments,
      tuple,
    ):
      raise TypeError(
        "segments must be a tuple"
      )

    for segment in self.segments:
      if not isinstance(
        segment,
        WebGroupProofInlineSegmentView,
      ):
        raise TypeError(
          "segments must contain only "
          "WebGroupProofInlineSegmentView values"
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
  partial_result: bool = False

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

    if not isinstance(self.partial_result, bool):
      raise TypeError("partial_result must be a bool")

    if not self.steps and not self.partial_result:
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
  public_group_latex = (
    render_toda_public_group_relation_latex(
      statement
    )
  )

  if public_group_latex is not None:
    return (
      public_group_latex,
      None,
    )

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

def _build_group_proof_inline_segments(
  line: str,
) -> tuple[
  WebGroupProofInlineSegmentView,
  ...,
]:
  if not isinstance(line, str):
    raise TypeError("line must be a str")

  segments = []
  cursor = 0
  while cursor < len(line):
    next_math = line.find("$", cursor)
    next_strong = line.find("**", cursor)
    delimiters = tuple(
      (position, kind)
      for position, kind in (
        (next_math, "inline_math"),
        (next_strong, "strong"),
      )
      if position >= 0
    )
    if not delimiters:
      segments.append(WebGroupProofInlineSegmentView(
        kind="text", value=line[cursor:]
      ))
      break

    position, kind = min(delimiters, key=lambda item: item[0])
    if position > cursor:
      segments.append(WebGroupProofInlineSegmentView(
        kind="text", value=line[cursor:position]
      ))

    if kind == "inline_math":
      closing = line.find("$", position + 1)
      if closing < 0:
        segments.append(WebGroupProofInlineSegmentView(
          kind="text", value=line[position:]
        ))
        break
      math_value = line[position + 1:closing]
      if not math_value:
        segments.append(WebGroupProofInlineSegmentView(
          kind="text", value="$$"
        ))
        cursor = closing + 1
        continue

      is_tagged = r"\tag{" in math_value
      cursor = closing + 1
      if is_tagged:
        # A tagged equation renders as a display block.  A standalone
        # punctuation suffix otherwise becomes an orphaned HTML text span.
        # Keep the punctuation with the equation, before its equation tag.
        suffix = line[cursor:]
        if suffix.strip() in (".", "。", ",", "、"):
          mark = "." if suffix.strip() in (".", "。") else ","
          tag_position = math_value.rfind(r"\tag{")
          math_value = (
            math_value[:tag_position]
            + r"\text{" + mark + "}"
            + math_value[tag_position:]
          )
          cursor = len(line)

      segments.append(WebGroupProofInlineSegmentView(
        kind="display_math" if is_tagged else "inline_math",
        value=math_value,
      ))
      continue

    closing = line.find("**", position + 2)
    if closing < 0:
      segments.append(WebGroupProofInlineSegmentView(
        kind="text", value=line[position:]
      ))
      break
    strong_value = line[position + 2:closing]
    segments.append(WebGroupProofInlineSegmentView(
      kind="strong" if strong_value else "text",
      value=strong_value if strong_value else "****",
    ))
    cursor = closing + 2

  return tuple(segments)

def _build_group_proof_rendered_lines(
  markdown: str,
) -> tuple[
  WebGroupProofRenderedLineView,
  ...,
]:
  if not isinstance(markdown, str):
    raise TypeError("markdown must be a str")

  lines = []
  display_math_lines = None
  display_math_indent_level = 0
  for raw_line in markdown.splitlines():
    stripped = raw_line.lstrip(" ")
    indent_level = (len(raw_line) - len(stripped)) // 2

    if stripped == "---":
      lines.append(WebGroupProofRenderedLineView(
        kind="separator", indent_level=0, prefix="",
        statement_latex=None, suffix="",
      ))
      continue

    if display_math_lines is not None:
      if stripped == r"\]":
        statement_latex = "\n".join(display_math_lines)
        lines.append(WebGroupProofRenderedLineView(
          kind="text", indent_level=display_math_indent_level,
          prefix="", statement_latex=statement_latex, suffix="",
          segments=(WebGroupProofInlineSegmentView(
            kind="display_math", value=statement_latex,
          ),),
        ))
        display_math_lines = None
        display_math_indent_level = 0
        continue
      if stripped:
        display_math_lines.append(stripped)
      continue

    if not raw_line:
      continue
    if raw_line.startswith("# "):
      continue
    if stripped.startswith("### "):
      lines.append(WebGroupProofRenderedLineView(
        kind="heading", indent_level=indent_level,
        prefix=stripped[4:], statement_latex=None, suffix="",
      ))
      continue
    if stripped.startswith("## "):
      lines.append(WebGroupProofRenderedLineView(
        kind="heading", indent_level=0,
        prefix=stripped[3:], statement_latex=None, suffix="",
      ))
      continue
    if stripped == r"\[":
      display_math_lines = []
      display_math_indent_level = indent_level
      continue

    prefix, statement_latex, suffix = _split_group_proof_rendered_line(stripped)
    lines.append(WebGroupProofRenderedLineView(
      kind="text", indent_level=indent_level, prefix=prefix,
      statement_latex=statement_latex, suffix=suffix,
      segments=_build_group_proof_inline_segments(stripped),
    ))

  if display_math_lines is not None:
    raise ValueError("unterminated display-math block in rendered group proof")
  return tuple(lines)
