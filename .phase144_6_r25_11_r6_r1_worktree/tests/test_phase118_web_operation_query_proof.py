import pytest

from web_operation_query_proof import (
  build_standard_web_operation_query_proof_view,
)


def test_phase118_3_single_fact_replays_with_default_depth_one():
  view = (
    build_standard_web_operation_query_proof_view(
      "E(nu_5)",
      fact_number=1,
    )
  )

  assert (
    view.fact_number
    == 1
  )

  assert (
    view.max_depth
    == 1
  )

  assert all(
    step.depth <= 1
    for step in view.steps
  )


def test_phase118_3_e_nu5_preserves_selected_conclusion_latex():
  view = (
    build_standard_web_operation_query_proof_view(
      "E(nu_5)",
      fact_number=1,
    )
  )

  assert (
    r"\nu_{5}"
    in view.conclusion_latex
  )

  assert (
    r"\nu_{6}"
    in view.conclusion_latex
  )


def test_phase118_3_h_nu_prime_fact_two_is_selected():
  view = (
    build_standard_web_operation_query_proof_view(
      "H(nu_prime)",
      fact_number=2,
    )
  )

  assert (
    view.fact_number
    == 2
  )

  assert (
    view.conclusion_latex
    == r"H\left(\nu'\right) = E^{2}\eta_{3}"
  )


def test_phase118_3_h_nu_prime_fact_one_preserves_provenance():
  view = (
    build_standard_web_operation_query_proof_view(
      "H(nu_prime)",
      fact_number=1,
    )
  )

  assert (
    view.provenance.theorem
    == "Toda Proposition 5.6"
  )

  assert (
    view.provenance.phase
    == "65"
  )

  assert (
    view.provenance.depth
    == 3
  )


def test_phase118_3_replay_steps_use_existing_statement_presentation():
  view = (
    build_standard_web_operation_query_proof_view(
      "H(nu_prime)",
      fact_number=2,
    )
  )

  assert any(
    (
      step.statement_latex
      == (
        r"\nu' \in "
        r"\{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}"
      )
    )
    for step in view.steps
  )


def test_phase118_3_e_sigma11_replays_existing_specialized_root():
  view = (
    build_standard_web_operation_query_proof_view(
      "E(sigma_11)",
      fact_number=1,
    )
  )

  assert (
    r"\sigma_{11}"
    in view.conclusion_latex
  )

  assert (
    r"\sigma_{12}"
    in view.conclusion_latex
  )

  assert (
    view.steps[
      0
    ].depth
    == 0
  )


def test_phase118_3_invalid_fact_number_is_rejected():
  with pytest.raises(
    ValueError,
    match=(
      "fact_number exceeds repository fact count"
    ),
  ):
    build_standard_web_operation_query_proof_view(
      "H(nu_prime)",
      fact_number=3,
    )


def test_phase118_3_nonpositive_fact_number_is_rejected():
  with pytest.raises(
    ValueError,
    match="fact_number must be positive",
  ):
    build_standard_web_operation_query_proof_view(
      "H(nu_prime)",
      fact_number=0,
    )
