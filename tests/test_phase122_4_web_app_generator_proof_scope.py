from web_app import (
  create_app,
)


def _build_test_client():
  app = create_app()

  app.config.update(
    TESTING=True,
  )

  return app.test_client()


def test_phase122_4_get_root_shows_generator_proof_scope_form():
  client = _build_test_client()

  response = client.get(
    "/"
  )

  assert response.status_code == 200
  assert b"Generator proof-scope exploration" in response.data
  assert b'name="proof_scope_generator_input"' in response.data
  assert b'value="generator_proof_scope"' in response.data


def test_phase122_4_post_nu_prime_shows_proof_scope_result():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_proof_scope",
      "proof_scope_generator_input": "nu_prime",
    },
  )

  assert response.status_code == 200
  assert b"Generator proof-scope exploration result" in response.data
  assert b'id="generator-proof-scope-generator"' in response.data
  assert rb"\nu&#39;" in response.data
  assert b"Proof-scope occurrences:" in response.data
  assert b"Toda memberships:" in response.data
  assert b"Map relations:" in response.data


def test_phase122_4_nu_prime_exposes_katex_root_depth_and_match():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_proof_scope",
      "proof_scope_generator_input": "nu_prime",
    },
  )

  assert response.status_code == 200
  assert b'class="generator-proof-scope-math"' in response.data
  assert b'data-latex="' in response.data
  assert b"Root:" in response.data
  assert b"Depth:" in response.data
  assert b"Match:" in response.data


def test_phase122_4_sigma11_web_uses_recursive_proof_scope_specialization():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_proof_scope",
      "proof_scope_generator_input": "sigma_11",
    },
  )

  assert response.status_code == 200
  assert b"Generator proof-scope exploration result" in response.data
  assert rb"\sigma_{11}" in response.data
  assert (
    b"Proof-scope occurrences:\n          0"
    not in response.data
  )


def test_phase122_4_unknown_generator_shows_zero_counts_as_normal_result():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_proof_scope",
      "proof_scope_generator_input": "eta_999",
    },
  )

  assert response.status_code == 200
  assert b"Generator proof-scope exploration result" in response.data
  assert b"Proof-scope occurrences:\n          0" in response.data
  assert b"Toda memberships:\n          0" in response.data
  assert b"Map relations:\n          0" in response.data
  assert b'class="generator-proof-scope-item"' not in response.data


def test_phase122_4_blank_generator_is_safe_error():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_proof_scope",
      "proof_scope_generator_input": "",
    },
  )

  assert response.status_code == 200
  assert b"generator is required" in response.data


def test_phase122_4_existing_web_forms_remain_available():
  client = _build_test_client()

  response = client.get(
    "/"
  )

  assert response.status_code == 200
  assert b"Group query" in response.data
  assert b"Operation query" in response.data
  assert b"Generator proof" in response.data
  assert b"Generator exploration" in response.data
