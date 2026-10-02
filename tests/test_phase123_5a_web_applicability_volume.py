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


