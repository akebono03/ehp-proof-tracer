from web_app import (
  create_app,
)


def _build_test_client():
  app = create_app()

  app.config.update(
    TESTING=True,
  )

  return app.test_client()


def test_phase124_4_get_root_shows_workflow_navigation():
  client = _build_test_client()

  response = client.get(
    "/"
  )

  assert response.status_code == 200
  assert b'id="workflow-navigation-heading"' in response.data
  assert b"Calculation and queries" in response.data
  assert b"Proof and exploration" in response.data
  assert b"Applicability" in response.data


def test_phase124_4_workflow_navigation_links_to_existing_forms():
  client = _build_test_client()

  response = client.get(
    "/"
  )

  assert response.status_code == 200

  expected_links = (
    b'href="#group-query"',
    b'href="#operation-query"',
    b'href="#generator-proof-query"',
    b'href="#generator-exploration-query"',
    b'href="#generator-proof-scope-query"',
    b'href="#generator-applicability-query"',
  )

  for expected_link in expected_links:
    assert expected_link in response.data


def test_phase124_4_existing_forms_have_workflow_targets():
  client = _build_test_client()

  response = client.get(
    "/"
  )

  assert response.status_code == 200

  expected_targets = (
    b'id="group-query"',
    b'id="operation-query"',
    b'id="generator-proof-query"',
    b'id="generator-exploration-query"',
    b'id="generator-proof-scope-query"',
    b'id="generator-applicability-query"',
  )

  for expected_target in expected_targets:
    assert expected_target in response.data


def test_phase124_4_existing_form_actions_remain_available():
  client = _build_test_client()

  response = client.get(
    "/"
  )

  assert response.status_code == 200

  expected_form_kinds = (
    b'value="group"',
    b'value="operation"',
    b'value="generator_proof"',
    b'value="generator_exploration"',
    b'value="generator_proof_scope"',
    b'value="generator_applicability"',
  )

  for expected_form_kind in expected_form_kinds:
    assert expected_form_kind in response.data


def test_phase124_4_existing_workflow_navigation_remains_available_after_execute_extension():
  client = _build_test_client()

  response = client.get(
    "/"
  )

  assert response.status_code == 200
  assert b'id="workflow-navigation-heading"' in response.data
  assert b'href="#generator-applicability-query"' in response.data
