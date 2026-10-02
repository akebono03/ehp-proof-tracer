from web_app import (
  create_app,
)


def _build_test_client():
  app = create_app()

  app.config.update(
    TESTING=True,
  )

  return app.test_client()


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


