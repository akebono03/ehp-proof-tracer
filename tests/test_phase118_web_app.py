from web_app import (
  create_app,
)


def _build_test_client():
  app = create_app()

  app.config.update(
    TESTING=True,
  )

  return app.test_client()


def test_phase118_2_get_root_shows_operation_query_form():
  client = _build_test_client()

  response = client.get(
    "/"
  )

  assert response.status_code == 200

  assert (
    b'Operation query'
    in response.data
  )

  assert (
    b'name="operation_query"'
    in response.data
  )

  assert (
    b'H(nu_prime)'
    in response.data
  )

  assert (
    b'Delta(iota_9)'
    in response.data
  )

  assert (
    b'E(nu_5)'
    in response.data
  )

  assert (
    b'E(sigma_11)'
    in response.data
  )


def test_phase118_2_post_e_sigma11_exposes_existing_latex():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "operation",
      "operation_query": (
        "E(sigma_11)"
      ),
    },
  )

  assert response.status_code == 200

  assert (
    b'Operation query result'
    in response.data
  )

  assert (
    b'class="operation-result-math"'
    in response.data
  )

  assert (
    rb"\sigma_{11}"
    in response.data
  )

  assert (
    rb"\sigma_{12}"
    in response.data
  )


def test_phase118_2_post_e_nu5_exposes_existing_latex():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "operation",
      "operation_query": (
        "E(nu_5)"
      ),
    },
  )

  assert response.status_code == 200

  assert (
    rb"\nu_{5}"
    in response.data
  )

  assert (
    rb"\nu_{6}"
    in response.data
  )


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


def test_phase118_2_not_found_operation_query_is_explicit():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "operation",
      "operation_query": (
        "H(sigma_11)"
      ),
    },
  )

  assert response.status_code == 200

  assert (
    b"No proof-backed operation fact found for this query."
    in response.data
  )

  assert (
    b'class="operation-result-math"'
    not in response.data
  )


def test_phase118_2_blank_operation_query_shows_validation_message():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "operation",
      "operation_query": "",
    },
  )

  assert response.status_code == 200

  assert (
    b"operation query is required"
    in response.data
  )


def test_phase118_2_existing_group_query_remains_available():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "n": "11",
      "k": "7",
    },
  )

  assert response.status_code == 200

  assert (
    b'id="result-math"'
    in response.data
  )

  assert (
    rb"\pi_{18}^{11} \cong "
    rb"\mathbb{Z}/16\{\sigma_{11}\}"
    in response.data
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


def test_phase118_3_selected_h_nu_prime_fact_two_shows_proof():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "operation_proof",
      "operation_query": (
        "H(nu_prime)"
      ),
      "fact_number": "2",
    },
  )

  assert response.status_code == 200

  assert (
    b"Query proof"
    in response.data
  )

  assert (
    b'id="operation-proof-conclusion"'
    in response.data
  )

  assert (
    rb"H\left(\nu&#39;\right) = E^{2}\eta_{3}"
    in response.data
  )


def test_phase118_3_selected_fact_displays_provenance():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "operation_proof",
      "operation_query": (
        "H(nu_prime)"
      ),
      "fact_number": "1",
    },
  )

  assert response.status_code == 200

  assert (
    b"Toda Proposition 5.6"
    in response.data
  )

  assert (
    b"Phase"
    in response.data
  )

  assert (
    b"65"
    in response.data
  )

  assert (
    b"repository depth"
    in response.data
  )


def test_phase118_3_selected_fact_displays_default_depth_proof_steps():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "operation_proof",
      "operation_query": (
        "E(nu_5)"
      ),
      "fact_number": "1",
    },
  )

  assert response.status_code == 200

  assert (
    b'class="operation-proof-step"'
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


def test_phase118_3_e_sigma11_proof_uses_existing_latex():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "operation_proof",
      "operation_query": (
        "E(sigma_11)"
      ),
      "fact_number": "1",
    },
  )

  assert response.status_code == 200

  assert (
    rb"\sigma_{11}"
    in response.data
  )

  assert (
    rb"\sigma_{12}"
    in response.data
  )


def test_phase118_3_invalid_fact_number_is_safe_error():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "operation_proof",
      "operation_query": (
        "H(nu_prime)"
      ),
      "fact_number": "3",
    },
  )

  assert response.status_code == 200

  assert (
    b"fact_number exceeds repository fact count"
    in response.data
  )


def test_phase118_3_missing_fact_number_is_safe_error():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "operation_proof",
      "operation_query": (
        "H(nu_prime)"
      ),
    },
  )

  assert response.status_code == 200

  assert (
    b"fact_number is required"
    in response.data
  )
