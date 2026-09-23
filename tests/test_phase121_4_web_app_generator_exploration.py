from web_app import (
  create_app,
)


def _build_test_client():
  app = create_app()

  app.config.update(
    TESTING=True,
  )

  return app.test_client()


def test_phase121_4_get_root_shows_generator_exploration_form():
  client = _build_test_client()

  response = client.get(
    "/"
  )

  assert response.status_code == 200

  assert (
    b"Generator exploration"
    in response.data
  )

  assert (
    b'name="exploration_generator_input"'
    in response.data
  )

  assert (
    b'value="generator_exploration"'
    in response.data
  )

  assert (
    b"nu_prime"
    in response.data
  )


def test_phase121_4_post_nu_prime_shows_generator_and_occurrences():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_exploration",
      "exploration_generator_input": "nu_prime",
    },
  )

  assert response.status_code == 200

  assert (
    b"Generator exploration result"
    in response.data
  )

  assert (
    b'id="generator-exploration-generator"'
    in response.data
  )

  assert (
    rb"\nu&#39;"
    in response.data
  )

  assert (
    b"Occurrences:"
    in response.data
  )

  assert (
    b'class="generator-exploration-occurrence"'
    in response.data
  )


def test_phase121_4_exploration_exposes_katex_latex_and_metadata():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_exploration",
      "exploration_generator_input": "nu_prime",
    },
  )

  assert response.status_code == 200

  assert (
    b'class="generator-exploration-math"'
    in response.data
  )

  assert (
    b'data-latex="'
    in response.data
  )

  assert (
    b"Roles:"
    in response.data
  )

  assert (
    b"Phase:"
    in response.data
  )

  assert (
    b"Theorem:"
    in response.data
  )


def test_phase121_4_unknown_generator_shows_zero_occurrences_as_normal_result():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_exploration",
      "exploration_generator_input": "eta_999",
    },
  )

  assert response.status_code == 200

  assert (
    b"Generator exploration result"
    in response.data
  )

  assert (
    b"Occurrences:\n          0"
    in response.data
  )

  assert (
    b'class="generator-exploration-occurrence"'
    not in response.data
  )


def test_phase121_4_blank_generator_is_safe_error():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "generator_exploration",
      "exploration_generator_input": "",
    },
  )

  assert response.status_code == 200

  assert (
    b"generator is required"
    in response.data
  )


def test_phase121_4_existing_web_forms_remain_available():
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

  assert (
    b"Generator proof"
    in response.data
  )
