from expression import GeneratorSymbol


_FAMILY_ALIASES = {
  "η": "η",
  "eta": "η",
  "ν": "ν",
  "nu": "ν",
  "σ": "σ",
  "sigma": "σ",
  "ι": "ι",
  "iota": "ι",
}


_DECORATED_GENERATOR_ALIASES = {
  "ν′": GeneratorSymbol(
    family="ν",
    decoration="′",
  ),
  "ν'": GeneratorSymbol(
    family="ν",
    decoration="′",
  ),
  "nu'": GeneratorSymbol(
    family="ν",
    decoration="′",
  ),
  "nu_prime": GeneratorSymbol(
    family="ν",
    decoration="′",
  ),
  "σ'": GeneratorSymbol(
    family="σ",
    decoration="'",
  ),
  "sigma_prime": GeneratorSymbol(
    family="σ",
    decoration="'",
  ),
  "σ''": GeneratorSymbol(
    family="σ",
    decoration="''",
  ),
  "sigma_double_prime": GeneratorSymbol(
    family="σ",
    decoration="''",
  ),
  "σ'''": GeneratorSymbol(
    family="σ",
    decoration="'''",
  ),
  "sigma_triple_prime": GeneratorSymbol(
    family="σ",
    decoration="'''",
  ),
}


def resolve_generator_input(
  value: str,
) -> GeneratorSymbol:
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
      "generator input must not be empty"
    )

  decorated = (
    _DECORATED_GENERATOR_ALIASES.get(
      normalized
    )
  )

  if decorated is not None:
    return decorated

  family = _FAMILY_ALIASES.get(
    normalized
  )

  if family is not None:
    return GeneratorSymbol(
      family=family,
    )

  if "_" not in normalized:
    raise ValueError(
      f"unsupported generator input: {value!r}"
    )

  family_text, index_text = (
    normalized.split(
      "_",
      maxsplit=1,
    )
  )

  family = _FAMILY_ALIASES.get(
    family_text
  )

  if family is None:
    raise ValueError(
      f"unsupported generator family: {family_text!r}"
    )

  if (
    not index_text
    or not index_text.isdecimal()
  ):
    raise ValueError(
      f"invalid generator index: {index_text!r}"
    )

  index = int(
    index_text
  )

  if index <= 0:
    raise ValueError(
      "generator index must be positive"
    )

  return GeneratorSymbol(
    family=family,
    index=index,
  )
