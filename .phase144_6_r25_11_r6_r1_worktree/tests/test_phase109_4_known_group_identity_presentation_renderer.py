from functools import lru_cache

import pytest

from generator_facts import (
  NU_PRIME_GENERATOR,
)
from repository_generator_known_group_identity_lookup import (
  find_standard_repository_generator_known_group_identity_nodes,
)
from repository_generator_known_group_identity_presentation import (
  RepositoryGeneratorKnownGroupIdentityPresentation,
  build_repository_generator_known_group_identity_presentation,
  build_standard_repository_generator_known_group_identity_presentation_input,
)
from repository_generator_known_group_identity_renderer import (
  render_repository_generator_known_group_identity_markdown,
)


@lru_cache(maxsize=1)
def _phase109_4_data():
  nodes = (
    find_standard_repository_generator_known_group_identity_nodes(
      NU_PRIME_GENERATOR
    )
  )

  presentation = (
    build_repository_generator_known_group_identity_presentation(
      NU_PRIME_GENERATOR,
      nodes,
    )
  )

  return {
    "nodes": nodes,
    "presentation": presentation,
  }


def test_phase109_4_builds_nu_prime_known_group_identity_presentation():
  data = _phase109_4_data()

  presentation = data[
    "presentation"
  ]

  assert isinstance(
    presentation,
    RepositoryGeneratorKnownGroupIdentityPresentation,
  )
  assert (
    presentation.generator
    == NU_PRIME_GENERATOR
  )


def test_phase109_4_presentation_preserves_source_node_and_conclusion_identity():
  data = _phase109_4_data()

  presentation = data[
    "presentation"
  ]
  source_node = data[
    "nodes"
  ][
    0
  ]

  assert (
    presentation.source_node
    is source_node
  )
  assert (
    presentation.conclusion
    is source_node.proof_step.conclusion
  )


def test_phase109_4_standard_input_builder_resolves_nu_prime():
  presentation = (
    build_standard_repository_generator_known_group_identity_presentation_input(
      "nu_prime"
    )
  )

  assert (
    presentation.generator
    == NU_PRIME_GENERATOR
  )
  assert (
    presentation.conclusion
    is presentation.source_node.proof_step.conclusion
  )


def test_phase109_4_renderer_shows_generator_before_known_group():
  presentation = (
    _phase109_4_data()[
      "presentation"
    ]
  )

  markdown = (
    render_repository_generator_known_group_identity_markdown(
      presentation
    )
  )

  assert markdown.startswith(
    "# Generator\n\n$\\nu'$\n"
  )

  generator_position = markdown.index(
    "# Generator"
  )
  known_group_position = markdown.index(
    "# Known group"
  )

  assert (
    generator_position
    < known_group_position
  )


def test_phase109_4_renderer_shows_pi6_3_z4_nu_prime():
  presentation = (
    _phase109_4_data()[
      "presentation"
    ]
  )

  markdown = (
    render_repository_generator_known_group_identity_markdown(
      presentation
    )
  )

  assert (
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$"
    in markdown
  )


def test_phase109_4_renderer_does_not_expose_provenance_metadata():
  presentation = (
    _phase109_4_data()[
      "presentation"
    ]
  )

  markdown = (
    render_repository_generator_known_group_identity_markdown(
      presentation
    )
  )

  assert (
    presentation.source_node.root_entry.key
    not in markdown
  )
  assert "Root:" not in markdown
  assert "Depth:" not in markdown
  assert "Phase:" not in markdown
  assert "Theorem:" not in markdown


def test_phase109_4_builder_rejects_zero_identity_nodes():
  with pytest.raises(
    ValueError,
    match=(
      "nodes must contain exactly one "
      "known-group identity"
    ),
  ):
    build_repository_generator_known_group_identity_presentation(
      NU_PRIME_GENERATOR,
      (),
    )


def test_phase109_4_builder_rejects_multiple_identity_nodes():
  data = _phase109_4_data()

  node = data[
    "nodes"
  ][
    0
  ]

  with pytest.raises(
    ValueError,
    match=(
      "nodes must contain exactly one "
      "known-group identity"
    ),
  ):
    build_repository_generator_known_group_identity_presentation(
      NU_PRIME_GENERATOR,
      (
        node,
        node,
      ),
    )


def test_phase109_4_renderer_rejects_non_presentation():
  with pytest.raises(
    TypeError,
    match=(
      "presentation must be a "
      "RepositoryGeneratorKnownGroupIdentityPresentation"
    ),
  ):
    render_repository_generator_known_group_identity_markdown(
      object()
    )
