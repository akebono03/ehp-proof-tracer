from dataclasses import (
  fields,
  is_dataclass,
)
from enum import Enum

from proof import (
  Relation,
)


def toda_group_proof_narrative_statement_semantic_key(
  value,
):
  if isinstance(
    value,
    Relation,
  ):
    return (
      "Relation",
      toda_group_proof_narrative_statement_semantic_key(
        value.lhs
      ),
      toda_group_proof_narrative_statement_semantic_key(
        value.rhs
      ),
      toda_group_proof_narrative_statement_semantic_key(
        value.relation_type
      ),
    )

  if isinstance(
    value,
    Enum,
  ):
    return (
      type(
        value
      ).__module__,
      type(
        value
      ).__qualname__,
      value.value,
    )

  if is_dataclass(
    value
  ):
    return (
      type(
        value
      ).__module__,
      type(
        value
      ).__qualname__,
      tuple(
        (
          field.name,
          toda_group_proof_narrative_statement_semantic_key(
            getattr(
              value,
              field.name
            )
          ),
        )
        for field in fields(
          value
        )
      ),
    )

  if isinstance(
    value,
    tuple,
  ):
    return (
      "tuple",
      tuple(
        toda_group_proof_narrative_statement_semantic_key(
          item
        )
        for item in value
      ),
    )

  if isinstance(
    value,
    list,
  ):
    return (
      "list",
      tuple(
        toda_group_proof_narrative_statement_semantic_key(
          item
        )
        for item in value
      ),
    )

  if isinstance(
    value,
    dict,
  ):
    return (
      "dict",
      tuple(
        sorted(
          (
            toda_group_proof_narrative_statement_semantic_key(
              key
            ),
            toda_group_proof_narrative_statement_semantic_key(
              item
            ),
          )
          for key, item in value.items()
        )
      ),
    )

  if isinstance(
    value,
    (
      str,
      int,
      float,
      bool,
      type(
        None
      ),
    ),
  ):
    return value

  return (
    type(
      value
    ).__module__,
    type(
      value
    ).__qualname__,
    repr(
      value
    ),
  )
