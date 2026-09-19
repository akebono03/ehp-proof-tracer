from dataclasses import (
  fields,
  is_dataclass,
)

from expression import GeneratorSymbol


def _find_generator_occurrence_paths(
  value,
  generator: GeneratorSymbol,
  path: tuple[str, ...],
  ancestor_ids: frozenset[int],
) -> tuple[
  tuple[str, ...],
  ...,
]:
  if isinstance(
    value,
    GeneratorSymbol,
  ):
    if value == generator:
      return (
        path,
      )

    return ()

  if isinstance(
    value,
    tuple,
  ):
    value_id = id(
      value
    )

    if value_id in ancestor_ids:
      return ()

    next_ancestor_ids = (
      ancestor_ids
      | frozenset(
        (
          value_id,
        )
      )
    )

    paths = []

    for index, item in enumerate(
      value
    ):
      paths.extend(
        _find_generator_occurrence_paths(
          item,
          generator,
          path
          + (
            str(
              index
            ),
          ),
          next_ancestor_ids,
        )
      )

    return tuple(
      paths
    )

  if (
    is_dataclass(
      value
    )
    and not isinstance(
      value,
      type,
    )
  ):
    value_id = id(
      value
    )

    if value_id in ancestor_ids:
      return ()

    next_ancestor_ids = (
      ancestor_ids
      | frozenset(
        (
          value_id,
        )
      )
    )

    paths = []

    for field in fields(
      value
    ):
      paths.extend(
        _find_generator_occurrence_paths(
          getattr(
            value,
            field.name,
          ),
          generator,
          path
          + (
            field.name,
          ),
          next_ancestor_ids,
        )
      )

    return tuple(
      paths
    )

  return ()


def find_generator_occurrence_paths(
  value,
  generator: GeneratorSymbol,
) -> tuple[
  tuple[str, ...],
  ...,
]:
  if not isinstance(
    generator,
    GeneratorSymbol,
  ):
    raise TypeError(
      "generator must be a GeneratorSymbol"
    )

  return _find_generator_occurrence_paths(
    value,
    generator,
    (),
    frozenset(),
  )


def contains_generator_symbol(
  value,
  generator: GeneratorSymbol,
) -> bool:
  return bool(
    find_generator_occurrence_paths(
      value,
      generator,
    )
  )
