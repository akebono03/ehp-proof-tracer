from pathlib import Path

from web_app import (
  create_app,
)


def _build_test_client():
  app = create_app()

  app.config.update(
    TESTING=True,
  )

  return app.test_client()


def test_phase137_2_group_query_description_uses_inline_katex():
  client = _build_test_client()

  response = client.get(
    "/"
  )

  assert response.status_code == 200

  assert (
    rb'data-latex="\pi_{n+k}^{n}"'
    in response.data
  )

  assert (
    b'class="group-proof-rendered-inline-math"'
    in response.data
  )

  assert (
    b"pi_(n+k)^n"
    not in response.data
  )


def test_phase137_2_input_syntax_examples_remain_plain_text():
  client = _build_test_client()

  response = client.get(
    "/"
  )

  assert response.status_code == 200

  assert (
    b"H(nu_prime)"
    in response.data
  )

  assert (
    b"E(nu_5)"
    in response.data
  )

  assert (
    b"sigma_11"
    in response.data
  )

  assert (
    rb'data-latex="H(nu_prime)"'
    not in response.data
  )

  assert (
    rb'data-latex="E(nu_5)"'
    not in response.data
  )

  assert (
    rb'data-latex="sigma_11"'
    not in response.data
  )


def test_phase137_2_template_contains_no_mojibake_separator():
  template_text = Path(
    "templates/index.html"
  ).read_text(
    encoding="utf-8",
  )

  assert (
    "窶・"
    not in template_text
  )
