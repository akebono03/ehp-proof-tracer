from web_app import (
  create_app,
)


def _build_test_client():
  app = create_app()

  app.config.update(
    TESTING=True,
  )

  return app.test_client()


def test_phase123_4_get_root_shows_generator_applicability_form():
  client = _build_test_client()

  response = client.get(
    "/"
  )

  assert response.status_code == 200
  assert b"Applicable theorem / lemma candidates" in response.data
  assert b'name="applicability_generator_input"' in response.data
  assert b'value="generator_applicability"' in response.data


def test_phase123_4_post_nu_prime_shows_compact_applicability_result():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_applicability",
      "applicability_generator_input": "nu_prime",
    },
  )

  assert response.status_code == 200
  assert b"Applicable theorem / lemma candidates result" in response.data
  assert b'id="generator-applicability-generator"' in response.data
  assert rb"\nu&#39;" in response.data
  assert b"Proof-scope occurrences:" in response.data
  assert b"Applicability candidates:" in response.data
  assert b"Source statements with candidates:" in response.data
  assert b"Rule groups:" in response.data
  assert b"Rule families:" in response.data


def test_phase123_4_nu_prime_exposes_katex_source_and_compact_rule_family_fields():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_applicability",
      "applicability_generator_input": "nu_prime",
    },
  )

  assert response.status_code == 200
  assert b'class="generator-applicability-math"' in response.data
  assert b'data-latex="' in response.data
  assert b"Root:" in response.data
  assert b"Depth:" in response.data
  assert b"Source statement type:" in response.data
  assert b"Raw candidates:" in response.data
  assert b"Catalog entries:" in response.data

  assert b"Fixed-point safe:" not in response.data
  assert b"Premise index:" not in response.data
  assert b"Bindings:" not in response.data


def test_phase123_4_unknown_generator_shows_zero_counts_as_normal_result():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_applicability",
      "applicability_generator_input": "eta_999",
    },
  )

  assert response.status_code == 200
  assert b"Applicable theorem / lemma candidates result" in response.data
  assert b"Proof-scope occurrences:\n          0" in response.data
  assert b"Applicability candidates:\n          0" in response.data
  assert b"Source statements with candidates:\n          0" in response.data
  assert b"Rule groups:\n          0" in response.data
  assert b"Rule families:\n          0" in response.data
  assert b'class="generator-applicability-source"' not in response.data


def test_phase123_4_blank_generator_is_safe_error():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_applicability",
      "applicability_generator_input": "",
    },
  )

  assert response.status_code == 200
  assert b"generator is required" in response.data


def test_phase123_4_existing_web_forms_remain_available():
  client = _build_test_client()

  response = client.get(
    "/"
  )

  assert response.status_code == 200
  assert b"Group query" in response.data
  assert b"Operation query" in response.data
  assert b"Generator proof" in response.data
  assert b"Generator exploration" in response.data
  assert b"Generator proof-scope exploration" in response.data
