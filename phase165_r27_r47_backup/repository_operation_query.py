from dataclasses import dataclass

from expression import GeneratorSymbol
from generator_input import resolve_generator_input


@dataclass(frozen=True)
class RepositoryGeneratorQuery:
  generator: GeneratorSymbol

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.generator,
      GeneratorSymbol,
    ):
      raise TypeError(
        "generator must be a GeneratorSymbol"
      )


@dataclass(frozen=True)
class RepositoryCompositionQuery:
  left: RepositoryGeneratorQuery
  right: RepositoryGeneratorQuery

  def __post_init__(
    self,
  ) -> None:
    if not isinstance(
      self.left,
      RepositoryGeneratorQuery,
    ):
      raise TypeError(
        "left must be a RepositoryGeneratorQuery"
      )

    if not isinstance(
      self.right,
      RepositoryGeneratorQuery,
    ):
      raise TypeError(
        "right must be a RepositoryGeneratorQuery"
      )


@dataclass(frozen=True)
class RepositoryThreeTermCompositionQuery:
  first: RepositoryGeneratorQuery
  second: RepositoryGeneratorQuery
  third: RepositoryGeneratorQuery

  def __post_init__(
    self,
  ) -> None:
    for name, value in (
      (
        "first",
        self.first,
      ),
      (
        "second",
        self.second,
      ),
      (
        "third",
        self.third,
      ),
    ):
      if not isinstance(
        value,
        RepositoryGeneratorQuery,
      ):
        raise TypeError(
          f"{name} must be a RepositoryGeneratorQuery"
        )


RepositoryOperationOperand = (
  RepositoryGeneratorQuery
  | RepositoryCompositionQuery
)


@dataclass(frozen=True)
class RepositoryMapOperationQuery:
  operation: str
  operand: RepositoryOperationOperand

  def __post_init__(
    self,
  ) -> None:
    if self.operation not in (
      "E",
      "H",
      "Delta",
    ):
      raise ValueError(
        "operation must be E, H, or Delta"
      )

    if not isinstance(
      self.operand,
      (
        RepositoryGeneratorQuery,
        RepositoryCompositionQuery,
      ),
    ):
      raise TypeError(
        "operand must be a repository "
        "operation operand"
      )


RepositoryOperationQuery = (
  RepositoryMapOperationQuery
  | RepositoryCompositionQuery
  | RepositoryThreeTermCompositionQuery
)


def _parse_generator_query(
  value: str,
) -> RepositoryGeneratorQuery:
  return RepositoryGeneratorQuery(
    generator=resolve_generator_input(
      value
    )
  )


def _parse_composition_query(
  value: str,
) -> RepositoryCompositionQuery:
  pieces = value.split(
    " o "
  )

  if len(
    pieces
  ) != 2:
    raise ValueError(
      "composition query must contain exactly "
      "one ' o ' operator"
    )

  left_text, right_text = (
    piece.strip()
    for piece in pieces
  )

  if (
    not left_text
    or not right_text
  ):
    raise ValueError(
      "composition operands must not be empty"
    )

  return RepositoryCompositionQuery(
    left=_parse_generator_query(
      left_text
    ),
    right=_parse_generator_query(
      right_text
    ),
  )


def _parse_three_term_composition_query(
  value: str,
) -> RepositoryThreeTermCompositionQuery:
  pieces = tuple(
    piece.strip()
    for piece in value.split(
      " o "
    )
  )

  if len(
    pieces
  ) != 3:
    raise ValueError(
      "three-term composition query must contain "
      "exactly two ' o ' operators"
    )

  if any(
    not piece
    for piece in pieces
  ):
    raise ValueError(
      "composition operands must not be empty"
    )

  return RepositoryThreeTermCompositionQuery(
    first=_parse_generator_query(
      pieces[
        0
      ]
    ),
    second=_parse_generator_query(
      pieces[
        1
      ]
    ),
    third=_parse_generator_query(
      pieces[
        2
      ]
    ),
  )


def _parse_operand(
  value: str,
) -> RepositoryOperationOperand:
  normalized = value.strip()

  if " o " in normalized:
    pieces = normalized.split(
      " o "
    )

    if len(
      pieces
    ) != 2:
      raise ValueError(
        "map-operation composition operands support "
        "exactly two generators"
      )

    return _parse_composition_query(
      normalized
    )

  return _parse_generator_query(
    normalized
  )


def parse_repository_operation_query(
  value: str,
) -> RepositoryOperationQuery:
  if not isinstance(
    value,
    str,
  ):
    raise TypeError(
      "value must be a str"
    )

  normalized = value.strip()

  if not normalized:
    raise ValueError(
      "operation query must not be empty"
    )

  for operation in (
    "Delta",
    "E",
    "H",
  ):
    prefix = operation + "("

    if not normalized.startswith(
      prefix
    ):
      continue

    if not normalized.endswith(
      ")"
    ):
      raise ValueError(
        "map operation query must end with ')'"
      )

    operand_text = normalized[
      len(
        prefix
      ):
      -1
    ]

    if (
      "(" in operand_text
      or ")" in operand_text
    ):
      raise ValueError(
        "nested operation queries are not supported"
      )

    return RepositoryMapOperationQuery(
      operation=operation,
      operand=_parse_operand(
        operand_text
      ),
    )

  if (
    "(" in normalized
    or ")" in normalized
  ):
    raise ValueError(
      "unsupported map operation query"
    )

  if " o " in normalized:
    pieces = normalized.split(
      " o "
    )

    if len(
      pieces
    ) == 2:
      return _parse_composition_query(
        normalized
      )

    if len(
      pieces
    ) == 3:
      return _parse_three_term_composition_query(
        normalized
      )

    raise ValueError(
      "composition query supports exactly two "
      "or three generators"
    )

  raise ValueError(
    "unsupported operation query"
  )
