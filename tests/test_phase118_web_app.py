from web_app import (
  create_app,
)


def _build_test_client():
  app = create_app()

  app.config.update(
    TESTING=True,
  )

  return app.test_client()


def test_phase118_2_multiple_facts_are_all_exposed():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "operation",
      "operation_query": (
        "H(nu_prime)"
      ),
    },
  )

  assert response.status_code == 200

  assert (
    response.data.count(
      b'class="operation-result-math"'
    )
    == 2
  )

  assert (
    rb"H\left(\nu&#39;\right) = \eta_{5}"
    in response.data
  )

  assert (
    rb"H\left(\nu&#39;\right) = E^{2}\eta_{3}"
    in response.data
  )


def test_phase118_2_multiple_facts_do_not_select_one_fact():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "operation",
      "operation_query": (
        "Delta(iota_9)"
      ),
    },
  )

  assert response.status_code == 200

  assert (
    response.data.count(
      b'class="operation-result-math"'
    )
    == 2
  )


def test_phase118_3_operation_results_have_explicit_proof_selection():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "operation",
      "operation_query": (
        "H(nu_prime)"
      ),
    },
  )

  assert response.status_code == 200

  assert (
    response.data.count(
      b'value="operation_proof"'
    )
    == 2
  )

  assert (
    b'name="fact_number"'
    in response.data
  )

  assert (
    b'value="1"'
    in response.data
  )

  assert (
    b'value="2"'
    in response.data
  )


