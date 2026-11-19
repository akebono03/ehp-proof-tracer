from dataclasses import (
  fields,
  is_dataclass,
)

from expression import GeneratorSymbol


def _contains_generator_symbol(
  value,
  generator: GeneratorSymbol,
  visited_ids: set[int],
) -> bool:
  if isinstance(
    value,
    GeneratorSymbol,
  ):
    return value == generator

  if isinstance(
    value,
    tuple,
  ):
    value_id = id(
      value
    )

    if value_id in visited_ids:
      return False

    visited_ids.add(
      value_id
    )

    return any(
      _contains_generator_symbol(
        item,
        generator,
        visited_ids,
      )
      for item in value
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

    if value_id in visited_ids:
      return False

    visited_ids.add(
      value_id
    )

    return any(
      _contains_generator_symbol(
        getattr(
          value,
          field.name,
        ),
        generator,
        visited_ids,
      )
      for field in fields(
        value
      )
    )

  return False


def contains_generator_symbol(
  value,
  generator: GeneratorSymbol,
) -> bool:
  if not isinstance(
    generator,
    GeneratorSymbol,
  ):
    raise TypeError(
      "generator must be a GeneratorSymbol"
    )

  return _contains_generator_symbol(
    value,
    generator,
    set(),
  )
