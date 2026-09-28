from repository_generator_known_group_proof_replay import (
  build_standard_repository_generator_known_group_proof_replay_input,
)
from repository_generator_known_group_proof_replay_presentation import (
  build_repository_generator_known_group_proof_replay_presentation,
)
from repository_generator_known_group_proof_replay_renderer import (
  render_repository_generator_known_group_proof_replay_markdown,
)


def test_phase111_12_depth_two_show_proof_uses_safe_type_name_fallback():
  result = (
    build_standard_repository_generator_known_group_proof_replay_input(
      "sigma_11",
      max_depth=2,
    )
  )

  presentation = (
    build_repository_generator_known_group_proof_replay_presentation(
      result
    )
  )

  markdown = (
    render_repository_generator_known_group_proof_replay_markdown(
      presentation
    )
  )

  assert (
    "`Toda45IsomorphismStatement`"
    in markdown
  )

  assert (
    "`TodaSigmaFamilyDefinitionStatement`"
    in markdown
  )

  assert (
    "Toda45IsomorphismStatement("
    not in markdown
  )

  assert (
    "TodaSigmaFamilyDefinitionStatement("
    not in markdown
  )


def test_phase111_12_depth_two_show_proof_keeps_renderable_statements():
  result = (
    build_standard_repository_generator_known_group_proof_replay_input(
      "sigma_11",
      max_depth=2,
    )
  )

  presentation = (
    build_repository_generator_known_group_proof_replay_presentation(
      result
    )
  )

  markdown = (
    render_repository_generator_known_group_proof_replay_markdown(
      presentation
    )
  )

  assert (
    r"$\pi_{18}^{11} = \mathbb{Z}/16\{\sigma_{11}\}$"
    in markdown
  )

  assert (
    r"$\pi_{n + 7}^{n} = \mathbb{Z}/16\{\sigma_{n}\}$"
    in markdown
  )

  assert (
    r"$\pi_{16}^{9} = \mathbb{Z}/16\{\sigma_{9}\}$"
    in markdown
  )
