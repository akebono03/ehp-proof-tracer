import pytest

from repository_generator_user_execution_facade import (
  RepositoryGeneratorUserExecutionWorkflowStatus,
)
from web_app import (
  create_app,
)
from web_generator_execution import (
  build_standard_web_generator_execution_view,
)


def _build_test_client():
  app = create_app()

  app.config.update(
    TESTING=True,
  )

  return app.test_client()


def test_phase125_4_nu_prime_without_candidate_is_ambiguous():
  view = (
    build_standard_web_generator_execution_view(
      "nu_prime"
    )
  )

  assert (
    view.status
    is RepositoryGeneratorUserExecutionWorkflowStatus.AMBIGUOUS
  )
  assert len(
    view.candidates
  ) >= 2
  assert [
    candidate.candidate_number
    for candidate in view.candidates
  ] == list(
    range(
      1,
      len(
        view.candidates
      ) + 1,
    )
  )
  assert view.conclusion_latex is None
  assert view.provenance is None


def test_phase125_4_nu_prime_candidate_1_executes_structured_result():
  view = (
    build_standard_web_generator_execution_view(
      "nu_prime",
      candidate_number=1,
    )
  )

  assert (
    view.status
    is RepositoryGeneratorUserExecutionWorkflowStatus.EXECUTED
  )
  assert view.selected_candidate_number == 1
  assert view.conclusion_latex
  assert view.rule_name
  assert view.provenance is not None
  assert view.provenance.key


def test_phase125_4_nu_prime_candidate_2_executes_with_premises():
  view = (
    build_standard_web_generator_execution_view(
      "nu_prime",
      candidate_number=2,
    )
  )

  assert (
    view.status
    is RepositoryGeneratorUserExecutionWorkflowStatus.EXECUTED
  )
  assert view.selected_candidate_number == 2
  assert view.conclusion_latex
  assert view.premises
  assert view.rule_name


def test_phase125_4_eta_999_has_no_executable_target():
  view = (
    build_standard_web_generator_execution_view(
      "eta_999"
    )
  )

  assert (
    view.status
    is RepositoryGeneratorUserExecutionWorkflowStatus.NONE
  )
  assert view.candidates == ()
  assert view.conclusion_latex is None
  assert view.premises == ()
  assert view.rule_name is None
  assert view.provenance is None


def test_phase125_4_rejects_empty_generator():
  with pytest.raises(
    ValueError,
    match="generator is required",
  ):
    build_standard_web_generator_execution_view(
      "   "
    )


def test_phase125_4_get_root_shows_execute_form_and_navigation():
  client = _build_test_client()

  response = client.get(
    "/"
  )

  assert response.status_code == 200
  assert b'href="#generator-execution-query"' in response.data
  assert b'id="generator-execution-query"' in response.data
  assert b'value="generator_execution"' in response.data
  assert b'name="execution_generator_input"' in response.data


def test_phase125_4_web_nu_prime_lists_executable_candidates():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_execution",
      "execution_generator_input": "nu_prime",
    },
  )

  assert response.status_code == 200
  assert b"Executable candidates" in response.data
  assert b'name="execution_candidate"' in response.data
  assert b'value="1"' in response.data
  assert b"Execute candidate" in response.data
  assert b'data-latex=' in response.data


def test_phase125_4_web_candidate_selection_returns_result_and_proof():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_execution",
      "execution_generator_input": "nu_prime",
      "execution_candidate": "2",
    },
  )

  assert response.status_code == 200
  assert b"Execution result" in response.data
  assert b"Premises" in response.data
  assert b"Rule" in response.data
  assert b"Conclusion" in response.data
  assert b"Provenance" in response.data
  assert b'id="generator-execution-conclusion"' in response.data
  assert b'data-latex=' in response.data


def test_phase125_4_web_none_is_normal_result():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_execution",
      "execution_generator_input": "eta_999",
    },
  )

  assert response.status_code == 200
  assert b"No executable target found for this generator." in response.data
