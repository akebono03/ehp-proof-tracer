from functools import lru_cache

import pytest

from proof import (
  ProofStep,
)
from repository_generator_user_execution_handoff import (
  execute_repository_generator_executable_target,
)
from repository_generator_user_execution_presentation import (
  RepositoryGeneratorUserExecutionPresentation,
  build_repository_generator_user_execution_presentation,
)
from repository_generator_user_execution_proof_step import (
  extract_repository_generator_executed_target_proof_step,
)
from repository_generator_user_execution_renderer import (
  render_repository_generator_user_execution_markdown,
)
from repository_generator_user_execution_resolver import (
  resolve_standard_repository_generator_executable_targets_input,
)


_FIRST_FAMILY = (
  "toda_58_delta_iota9_nu4_nu_prime_inference_rule"
)

_SECOND_FAMILY = (
  "toda_lemma57_pi6_2_eta2_nu_prime_inference_rule"
)


@lru_cache(maxsize=1)
def _phase108_8_resolution():
  return (
    resolve_standard_repository_generator_executable_targets_input(
      "nu_prime"
    )
  )


def _first_target_for_family(
  family_name,
):
  resolution = (
    _phase108_8_resolution()
  )

  for target in resolution.targets:
    if target.family_name == family_name:
      return (
        resolution,
        target,
      )

  raise AssertionError(
    f"no executable target found for family: {family_name}"
  )


@lru_cache(maxsize=2)
def _phase108_8_proof_result(
  family_name,
):
  resolution, target = (
    _first_target_for_family(
      family_name
    )
  )

  execution_result = (
    execute_repository_generator_executable_target(
      resolution,
      target,
    )
  )

  proof_result = (
    extract_repository_generator_executed_target_proof_step(
      execution_result
    )
  )

  return (
    target,
    proof_result,
  )


def test_phase108_8_builds_first_family_user_execution_presentation():
  target, proof_result = (
    _phase108_8_proof_result(
      _FIRST_FAMILY
    )
  )

  presentation = (
    build_repository_generator_user_execution_presentation(
      proof_result
    )
  )

  assert isinstance(
    presentation,
    RepositoryGeneratorUserExecutionPresentation,
  )

  assert (
    presentation.source_result
    is proof_result
  )

  assert (
    presentation.proof_step
    is proof_result.proof_step
  )

  assert (
    presentation.conclusion
    is proof_result.proof_step.conclusion
  )

  assert (
    presentation.conclusion
    == target.goal
  )


def test_phase108_8_builds_second_family_user_execution_presentation():
  _target, proof_result = (
    _phase108_8_proof_result(
      _SECOND_FAMILY
    )
  )

  presentation = (
    build_repository_generator_user_execution_presentation(
      proof_result
    )
  )

  assert isinstance(
    presentation,
    RepositoryGeneratorUserExecutionPresentation,
  )

  assert (
    presentation.premises
    == proof_result.proof_step.premises
  )

  assert all(
    isinstance(
      premise,
      ProofStep,
    )
    for premise in presentation.premises
  )


def test_phase108_8_presentation_preserves_direct_premise_identity():
  for family_name in (
    _FIRST_FAMILY,
    _SECOND_FAMILY,
  ):
    _target, proof_result = (
      _phase108_8_proof_result(
        family_name
      )
    )

    presentation = (
      build_repository_generator_user_execution_presentation(
        proof_result
      )
    )

    assert len(
      presentation.premises
    ) == len(
      proof_result.proof_step.premises
    )

    assert all(
      presented is source
      for presented, source in zip(
        presentation.premises,
        proof_result.proof_step.premises,
      )
    )


def test_phase108_8_rule_name_comes_from_final_inference_rule():
  for family_name in (
    _FIRST_FAMILY,
    _SECOND_FAMILY,
  ):
    _target, proof_result = (
      _phase108_8_proof_result(
        family_name
      )
    )

    presentation = (
      build_repository_generator_user_execution_presentation(
        proof_result
      )
    )

    inference_rule = (
      proof_result
      .proof_step
      .inference_rule
    )

    assert inference_rule is not None

    assert (
      presentation.rule_name
      == inference_rule.name
    )


def test_phase108_8_renders_minimal_result_and_proof_sections():
  _target, proof_result = (
    _phase108_8_proof_result(
      _SECOND_FAMILY
    )
  )

  presentation = (
    build_repository_generator_user_execution_presentation(
      proof_result
    )
  )

  markdown = (
    render_repository_generator_user_execution_markdown(
      presentation
    )
  )

  assert markdown.startswith(
    "# Result\n"
  )

  assert "\n## Proof\n" in markdown
  assert "\nPremises:\n" in markdown
  assert "\nRule: " in markdown
  assert "\nConclusion:\n" in markdown


def test_phase108_8_renderer_does_not_expose_internal_addressing():
  target, proof_result = (
    _phase108_8_proof_result(
      _SECOND_FAMILY
    )
  )

  presentation = (
    build_repository_generator_user_execution_presentation(
      proof_result
    )
  )

  markdown = (
    render_repository_generator_user_execution_markdown(
      presentation
    )
  )

  assert target.family_name not in markdown
  assert target.root_entry.key not in markdown

  assert "catalog" not in markdown.lower()
  assert "binding" not in markdown.lower()


def test_phase108_8_renderer_uses_direct_premises_only():
  _target, proof_result = (
    _phase108_8_proof_result(
      _SECOND_FAMILY
    )
  )

  presentation = (
    build_repository_generator_user_execution_presentation(
      proof_result
    )
  )

  markdown = (
    render_repository_generator_user_execution_markdown(
      presentation
    )
  )

  numbered_premise_lines = tuple(
    line
    for line in markdown.splitlines()
    if (
      len(
        line
      ) >= 3
      and line[
        0
      ].isdigit()
      and line[
        1:
        3
      ] == ". "
    )
  )

  assert len(
    numbered_premise_lines
  ) == len(
    presentation.premises
  )


def test_phase108_8_rejects_non_proof_result():
  with pytest.raises(
    TypeError,
    match=(
      "result must be a "
      "RepositoryGeneratorExecutedProofStepResult"
    ),
  ):
    build_repository_generator_user_execution_presentation(
      object()
    )


def test_phase108_8_renderer_rejects_non_presentation():
  with pytest.raises(
    TypeError,
    match=(
      "presentation must be a "
      "RepositoryGeneratorUserExecutionPresentation"
    ),
  ):
    render_repository_generator_user_execution_markdown(
      object()
    )
