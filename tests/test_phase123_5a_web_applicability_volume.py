from web_app import (
  create_app,
)


def _build_test_client():
  app = create_app()

  app.config.update(
    TESTING=True,
  )

  return app.test_client()


def test_phase123_5a_nu_prime_limits_rendered_sources_and_rule_families():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_applicability",
      "applicability_generator_input": "nu_prime",
    },
  )

  assert response.status_code == 200

  assert (
    response.data.count(
      b'class="generator-applicability-source"'
    )
    <= 15
  )

  assert (
    response.data.count(
      b'class="generator-applicability-rule-family"'
    )
    <= 150
  )

  assert (
    b"showing first 5"
    in response.data
  )

  assert (
    b"additional source statements are omitted "
    b"from this compact Web view."
    in response.data
  )

  assert (
    b"additional rule families are omitted "
    b"from this compact Web view."
    in response.data
  )


def test_phase123_5a_rule_families_are_collapsed_by_default():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_applicability",
      "applicability_generator_input": "sigma_11",
    },
  )

  assert response.status_code == 200

  assert (
    b'<details class="generator-applicability-rule-families">'
    in response.data
  )

  assert (
    b"Show rule families"
    in response.data
  )

  assert (
    b"<details "
    in response.data
  )

  assert (
    b"<details open"
    not in response.data
  )


def test_phase123_5a_summary_counts_remain_full_result_counts():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_applicability",
      "applicability_generator_input": "nu_prime",
    },
  )

  assert response.status_code == 200

  assert (
    b"Proof-scope occurrences:\n          626"
    in response.data
  )

  assert (
    b"Applicability candidates:\n          176616"
    in response.data
  )

  assert (
    b"Source statements with candidates:\n          542"
    in response.data
  )

  assert (
    b"Rule groups:\n          123300"
    in response.data
  )

  assert (
    b"Rule families:\n          29308"
    in response.data
  )


def test_phase123_5a_unknown_generator_remains_zero_result_without_truncation_notice():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_applicability",
      "applicability_generator_input": "eta_999",
    },
  )

  assert response.status_code == 200

  assert (
    b"Applicability candidates:\n          0"
    in response.data
  )

  assert (
    b'class="generator-applicability-source"'
    not in response.data
  )

  assert (
    b"additional source statements are omitted "
    b"from this compact Web view."
    not in response.data
  )
