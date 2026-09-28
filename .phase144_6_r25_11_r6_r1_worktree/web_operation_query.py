from dataclasses import dataclass

from repository_operation_query_facade import (
  query_standard_repository_operation_input,
)
from repository_operation_query_presentation import (
  build_repository_operation_query_presentation,
)


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


def build_standard_web_operation_query_view(
  query_input: str,
) -> WebOperationQueryView:
  if not isinstance(
    query_input,
    str,
  ):
    raise TypeError(
      "query_input must be a str"
    )

  query_input = query_input.strip()

  if not query_input:
    raise ValueError(
      "operation query is required"
    )

  result = (
    query_standard_repository_operation_input(
      query_input
    )
  )

  presentation = (
    build_repository_operation_query_presentation(
      result
    )
  )

  items = tuple(
    WebOperationQueryItemView(
      statement_latex=(
        item.statement_latex
      ),
      provenance_count=(
        item.provenance_count
      ),
    )
    for item in presentation.items
  )

  return WebOperationQueryView(
    query_input=query_input,
    found=result.found,
    items=items,
  )
