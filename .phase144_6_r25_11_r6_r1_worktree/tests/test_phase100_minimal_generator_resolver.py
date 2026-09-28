import pytest

from expression import GeneratorSymbol
from generator_facts import (
  NU_PRIME_GENERATOR,
)
from generator_input import (
  resolve_generator_input,
)
from repository_element_facade import (
  explore_repository_generator,
)
from test_phase99_actual_repository_element_lookup_validation import (
  build_phase99_5_actual_repository,
)


@pytest.mark.parametrize(
  (
    "value",
    "expected",
  ),
  (
    (
      "η",
      GeneratorSymbol(
        family="η",
      ),
    ),
    (
      "eta",
      GeneratorSymbol(
        family="η",
      ),
    ),
    (
      "ν",
      GeneratorSymbol(
        family="ν",
      ),
    ),
    (
      "nu",
      GeneratorSymbol(
        family="ν",
      ),
    ),
    (
      "σ",
      GeneratorSymbol(
        family="σ",
      ),
    ),
    (
      "sigma",
      GeneratorSymbol(
        family="σ",
      ),
    ),
    (
      "ι",
      GeneratorSymbol(
        family="ι",
      ),
    ),
    (
      "iota",
      GeneratorSymbol(
        family="ι",
      ),
    ),
  ),
)
def test_phase100_3_resolves_plain_family_aliases(
  value,
  expected,
):
  assert (
    resolve_generator_input(
      value
    )
    == expected
  )


@pytest.mark.parametrize(
  (
    "value",
    "expected",
  ),
  (
    (
      "η_2",
      GeneratorSymbol(
        family="η",
        index=2,
      ),
    ),
    (
      "eta_2",
      GeneratorSymbol(
        family="η",
        index=2,
      ),
    ),
    (
      "ν_5",
      GeneratorSymbol(
        family="ν",
        index=5,
      ),
    ),
    (
      "nu_5",
      GeneratorSymbol(
        family="ν",
        index=5,
      ),
    ),
    (
      "σ_8",
      GeneratorSymbol(
        family="σ",
        index=8,
      ),
    ),
    (
      "sigma_8",
      GeneratorSymbol(
        family="σ",
        index=8,
      ),
    ),
    (
      "ι_4",
      GeneratorSymbol(
        family="ι",
        index=4,
      ),
    ),
    (
      "iota_4",
      GeneratorSymbol(
        family="ι",
        index=4,
      ),
    ),
  ),
)
def test_phase100_3_resolves_positive_integer_indices(
  value,
  expected,
):
  assert (
    resolve_generator_input(
      value
    )
    == expected
  )


@pytest.mark.parametrize(
  "value",
  (
    "ν′",
    "ν'",
    "nu'",
    "nu_prime",
  ),
)
def test_phase100_3_nu_prime_aliases_preserve_existing_unicode_decoration(
  value,
):
  assert (
    resolve_generator_input(
      value
    )
    == NU_PRIME_GENERATOR
  )

  assert (
    resolve_generator_input(
      value
    )
    == GeneratorSymbol(
      family="ν",
      decoration="′",
    )
  )


@pytest.mark.parametrize(
  (
    "value",
    "expected_decoration",
  ),
  (
    (
      "σ'",
      "'",
    ),
    (
      "sigma_prime",
      "'",
    ),
    (
      "σ''",
      "''",
    ),
    (
      "sigma_double_prime",
      "''",
    ),
    (
      "σ'''",
      "'''",
    ),
    (
      "sigma_triple_prime",
      "'''",
    ),
  ),
)
def test_phase100_3_sigma_prime_aliases_preserve_existing_ascii_decoration(
  value,
  expected_decoration,
):
  assert (
    resolve_generator_input(
      value
    )
    == GeneratorSymbol(
      family="σ",
      decoration=expected_decoration,
    )
  )


def test_phase100_3_strips_only_outer_whitespace():
  assert (
    resolve_generator_input(
      "  nu_prime  "
    )
    == NU_PRIME_GENERATOR
  )

  assert (
    resolve_generator_input(
      "  eta_3  "
    )
    == GeneratorSymbol(
      family="η",
      index=3,
    )
  )


@pytest.mark.parametrize(
  "value",
  (
    "",
    "   ",
  ),
)
def test_phase100_3_rejects_empty_input(
  value,
):
  with pytest.raises(
    ValueError,
    match="generator input must not be empty",
  ):
    resolve_generator_input(
      value
    )


@pytest.mark.parametrize(
  "value",
  (
    None,
    3,
    True,
  ),
)
def test_phase100_3_rejects_non_string_input(
  value,
):
  with pytest.raises(
    TypeError,
    match="value must be a str",
  ):
    resolve_generator_input(
      value
    )


@pytest.mark.parametrize(
  "value",
  (
    "foobar",
    "prime",
    "nu prime",
    "η₂",
    "nu5",
    "{nu,eta,sigma}",
  ),
)
def test_phase100_3_rejects_unsupported_free_form_input(
  value,
):
  with pytest.raises(
    ValueError,
  ):
    resolve_generator_input(
      value
    )


@pytest.mark.parametrize(
  "value",
  (
    "eta_",
    "eta_x",
    "eta_-1",
    "nu__5",
    "eta_2_3",
    "eta_ 2",
  ),
)
def test_phase100_3_rejects_invalid_index_syntax(
  value,
):
  with pytest.raises(
    ValueError,
  ):
    resolve_generator_input(
      value
    )


def test_phase100_3_rejects_zero_index():
  with pytest.raises(
    ValueError,
    match="generator index must be positive",
  ):
    resolve_generator_input(
      "eta_0"
    )


def test_phase100_3_rejects_unknown_indexed_family():
  with pytest.raises(
    ValueError,
    match="unsupported generator family",
  ):
    resolve_generator_input(
      "foobar_3"
    )


def test_phase100_3_unindexed_generator_remains_non_wildcard():
  assert (
    resolve_generator_input(
      "nu"
    )
    != resolve_generator_input(
      "nu_5"
    )
  )

  assert (
    resolve_generator_input(
      "nu"
    )
    != resolve_generator_input(
      "nu_prime"
    )
  )


def test_phase100_3_resolved_nu_prime_connects_to_existing_phase99_exploration():
  data = (
    build_phase99_5_actual_repository()
  )

  report = (
    explore_repository_generator(
      data[
        "repository"
      ],
      resolve_generator_input(
        "nu_prime"
      ),
    )
  )

  assert (
    report.exploration.generator
    == NU_PRIME_GENERATOR
  )

  assert len(
    report.exploration.occurrences
  ) == 4

  assert (
    "Occurrences: 4"
    in report.markdown
  )
