from dataclasses import dataclass

from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from repository_operation_query_lookup import (
  RepositoryOperationQueryMatch,
  RepositoryOperationQueryResult,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


@dataclass(frozen=True)
class RepositoryOperationQueryPresentationItem:
  statement: object
  statement_latex: str
  matches: tuple[
    RepositoryOperationQueryMatch,
    ...,
  ]

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

    if not isinstance(
      self.matches,
      tuple,
    ):
      raise TypeError(
        "matches must be a tuple"
      )

    if not self.matches:
      raise ValueError(
        "matches must not be empty"
      )

    for match in self.matches:
      if not isinstance(
        match,
        RepositoryOperationQueryMatch,
      ):
        raise TypeError(
          "matches must contain only "
          "RepositoryOperationQueryMatch values"
        )

      if match.statement != self.statement:
        raise ValueError(
          "all matches must have the same statement"
        )

  @property
  def primary_match(
    self,
  ) -> RepositoryOperationQueryMatch:
    return min(
      self.matches,
      key=lambda match: (
        match.scope_node.shortest_depth,
      ),
    )

  @property
  def provenance_count(
    self,
  ) -> int:
    return len(
      self.matches
    )


@dataclass(frozen=True)
class RepositoryOperationQueryPresentation:
  source_result: RepositoryOperationQueryResult
  items: tuple[
    RepositoryOperationQueryPresentationItem,
    ...,
  ]

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.source_result,
      RepositoryOperationQueryResult,
    ):
      raise TypeError(
        "source_result must be a "
        "RepositoryOperationQueryResult"
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
        RepositoryOperationQueryPresentationItem,
      ):
        raise TypeError(
          "items must contain only "
          "RepositoryOperationQueryPresentationItem values"
        )


def _render_operation_query_statement_latex(
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


def build_repository_operation_query_presentation(
  result: RepositoryOperationQueryResult,
) -> RepositoryOperationQueryPresentation:
  if not isinstance(
    result,
    RepositoryOperationQueryResult,
  ):
    raise TypeError(
      "result must be a "
      "RepositoryOperationQueryResult"
    )

  groups: list[
    tuple[
      object,
      str,
      list[
        RepositoryOperationQueryMatch
      ],
      int,
    ]
  ] = []

  for source_index, match in enumerate(
    result.matches
  ):
    statement_latex = (
      _render_operation_query_statement_latex(
        match.statement
      )
    )

    if statement_latex is None:
      continue

    existing_index = next(
      (
        index
        for index, group in enumerate(
          groups
        )
        if group[
          0
        ] == match.statement
      ),
      None,
    )

    if existing_index is None:
      groups.append(
        (
          match.statement,
          statement_latex,
          [
            match,
          ],
          source_index,
        )
      )
      continue

    groups[
      existing_index
    ][
      2
    ].append(
      match
    )

  ordered_groups = sorted(
    groups,
    key=lambda group: (
      min(
        match.scope_node.shortest_depth
        for match in group[
          2
        ]
      ),
      group[
        3
      ],
    ),
  )

  items = tuple(
    RepositoryOperationQueryPresentationItem(
      statement=statement,
      statement_latex=statement_latex,
      matches=tuple(
        matches
      ),
    )
    for (
      statement,
      statement_latex,
      matches,
      _source_index,
    ) in ordered_groups
  )

  return RepositoryOperationQueryPresentation(
    source_result=result,
    items=items,
  )
