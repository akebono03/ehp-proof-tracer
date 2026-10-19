import main as cli_main

from web_app import create_app
from web_group_proof import (
  build_standard_web_group_proof_view,
)


def _build_test_client():
  app = create_app()
  app.config.update(
    TESTING=True,
  )
  return app.test_client()


def test_phase145_cli_parser_defaults_to_narrative_depth2():
  parser = cli_main.build_group_proof_argument_parser()
  args = parser.parse_args(
    [
      "9",
      "7",
    ]
  )

  assert args.mode == "narrative"
  assert args.depth == 2




def test_phase145_web_adapter_defaults_to_narrative_depth2():
  view = build_standard_web_group_proof_view(
    9,
    7,
  )

  assert view.mode == "narrative"
  assert view.max_depth == 2
  assert view.rendered_lines


def test_phase145_web_form_defaults_to_narrative_depth2():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "group_proof",
      "n": "9",
      "k": "7",
    },
  )

  assert response.status_code == 200
  assert b'data-proof-mode="narrative"' in response.data


