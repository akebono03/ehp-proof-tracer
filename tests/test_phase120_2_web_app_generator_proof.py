from web_app import (
  create_app,
)


def _build_test_client():
  app = create_app()

  app.config.update(
    TESTING=True,
  )

  return app.test_client()


def test_phase120_2_get_root_shows_generator_proof_form():
  client = _build_test_client()

  response = client.get(
    "/"
  )

  assert response.status_code == 200

  assert (
    b"Generator proof"
    in response.data
  )

  assert (
    b'name="generator_input"'
    in response.data
  )

  assert (
    b'name="generator_proof_depth"'
    in response.data
  )

  assert (
    b"sigma_11"
    in response.data
  )


def test_phase120_2_post_sigma11_shows_generator_and_conclusion_latex():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_proof",
      "generator_input": "sigma_11",
      "generator_proof_depth": "1",
    },
  )

  assert response.status_code == 200

  assert (
    b"Generator proof result"
    in response.data
  )

  assert (
    b'id="generator-proof-generator"'
    in response.data
  )

  assert (
    b'id="generator-proof-conclusion"'
    in response.data
  )

  assert (
    rb"\sigma_{11}"
    in response.data
  )

  assert (
    rb"\pi_{18}^{11} = "
    rb"\mathbb{Z}/16\{\sigma_{11}\}"
    in response.data
  )


def test_phase120_2_generator_proof_shows_depth_steps():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_proof",
      "generator_input": "sigma_11",
      "generator_proof_depth": "1",
    },
  )

  assert response.status_code == 200

  assert (
    b'class="generator-proof-step"'
    in response.data
  )

  assert (
    b"Depth 0"
    in response.data
  )

  assert (
    b"Depth 1"
    in response.data
  )


def test_phase120_2_generator_proof_forwards_depth_zero():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_proof",
      "generator_input": "sigma_11",
      "generator_proof_depth": "0",
    },
  )

  assert response.status_code == 200

  assert (
    b"Selected depth:\n          0"
    in response.data
  )

  assert (
    response.data.count(
      b'class="generator-proof-step"'
    )
    == 1
  )


def test_phase120_2_blank_generator_is_safe_error():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_proof",
      "generator_input": "",
      "generator_proof_depth": "1",
    },
  )

  assert response.status_code == 200

  assert (
    b"generator is required"
    in response.data
  )


def test_phase120_2_unsupported_generator_proof_depth_is_safe_error():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_proof",
      "generator_input": "sigma_11",
      "generator_proof_depth": "3",
    },
  )

  assert response.status_code == 200

  assert (
    b"generator_proof_depth must be 0, 1, or 2"
    in response.data
  )


def test_phase120_2_existing_group_and_operation_forms_remain_available():
  client = _build_test_client()

  response = client.get(
    "/"
  )

  assert response.status_code == 200

  assert (
    b"Group query"
    in response.data
  )

  assert (
    b"Operation query"
    in response.data
  )
