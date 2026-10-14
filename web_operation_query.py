from dataclasses import dataclass



@dataclass(frozen=True)
class WebOperationQueryItemView:
  statement_latex: str
  provenance_count: int

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.statement_latex,
      str,
    ):
      raise TypeError(
        "statement_latex must be a str"
      )

    if not self.statement_latex:
      raise ValueError(
        "statement_latex must not be empty"
      )

    if (
      isinstance(
        self.provenance_count,
        bool,
      )
      or not isinstance(
        self.provenance_count,
        int,
      )
    ):
      raise TypeError(
        "provenance_count must be an int"
      )

    if self.provenance_count <= 0:
      raise ValueError(
        "provenance_count must be positive"
      )


@dataclass(frozen=True)
class WebOperationQueryView:
  query_input: str
  found: bool
  items: tuple[
    WebOperationQueryItemView,
    ...,
  ]

  search_status: str = "not_searched"
  diagnostics: tuple[str, ...] = ()
  open_goal_count: int = 0

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

    if not isinstance(
      self.found,
      bool,
    ):
      raise TypeError(
        "found must be a bool"
      )

    if not isinstance(
      self.items,
      tuple,
    ):
      raise TypeError(
        "items must be a tuple"
      )

    for item in self.items:
      if not isinstance(
        item,
        WebOperationQueryItemView,
      ):
        raise TypeError(
          "items must contain only "
          "WebOperationQueryItemView values"
        )

    if (
      not self.found
      and self.items
    ):
      raise ValueError(
        "not-found view must not contain items"
      )


def build_standard_web_operation_query_view(query_input: str) -> WebOperationQueryView:
  if not isinstance(query_input, str):
    raise TypeError("query_input must be a str")
  query_input = query_input.strip()
  if not query_input:
    raise ValueError("operation query is required")
  from phase165_r27_r34_typed_lookup import search_typed_operation_statements
  from toda_proof_narrative_renderer import render_toda_proof_statement_latex
  result = search_typed_operation_statements(query_input)
  items = []
  for step in result.proven_steps:
    statement_latex = render_toda_proof_statement_latex(step.conclusion)
    if not isinstance(statement_latex, str) or not statement_latex:
      continue
    items.append(WebOperationQueryItemView(statement_latex=statement_latex, provenance_count=1))
  return WebOperationQueryView(
    query_input=query_input, found=bool(items), items=tuple(items),
    search_status=result.status.value, diagnostics=result.diagnostics,
    open_goal_count=len(result.open_goals),
  )
