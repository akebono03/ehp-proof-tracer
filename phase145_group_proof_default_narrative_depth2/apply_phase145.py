from pathlib import Path


def replace_once(path, old, new):
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"{path}: expected exactly one replacement target, found {count}"
        )
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def main():
    replace_once(
        Path("main.py"),
        '''  parser.add_argument(
    "--depth",
    type=_parse_nonnegative_int,
    help=(
      "maximum proof replay depth; "
      "omit to use the default depth 1"
    ),
  )

  parser.add_argument(
    "--mode",
    choices=(
      "trace",
      "outline",
      "narrative",
    ),
    default="trace",
    help=(
      "proof presentation mode; "
      "default: trace"
    ),
  )''',
        '''  parser.add_argument(
    "--depth",
    type=_parse_nonnegative_int,
    default=2,
    help=(
      "maximum proof replay depth; "
      "default: 2"
    ),
  )

  parser.add_argument(
    "--mode",
    choices=(
      "trace",
      "outline",
      "narrative",
    ),
    default="narrative",
    help=(
      "proof presentation mode; "
      "default: narrative"
    ),
  )''',
    )

    replace_once(
        Path("main.py"),
        '''def _run_group_proof_command(
  n: int,
  k: int,
  max_depth: int | None = None,
  mode: str = "trace",
) -> int:''',
        '''def _run_group_proof_command(
  n: int,
  k: int,
  max_depth: int | None = 2,
  mode: str = "narrative",
) -> int:''',
    )

    replace_once(
        Path("web_app.py"),
        '''    group_proof_depth_value = request.form.get(
      "group_proof_depth",
      "1",
    )
    group_proof_mode_value = request.form.get(
      "group_proof_mode",
      "trace",
    )''',
        '''    group_proof_depth_value = request.form.get(
      "group_proof_depth",
      "2",
    )
    group_proof_mode_value = request.form.get(
      "group_proof_mode",
      "narrative",
    )''',
    )

    replace_once(
        Path("web_group_proof.py"),
        '''def build_standard_web_group_proof_view(
  n: int,
  k: int,
  max_depth: int = 1,
  mode: str = "trace",
) -> WebGroupProofView:''',
        '''def build_standard_web_group_proof_view(
  n: int,
  k: int,
  max_depth: int = 2,
  mode: str = "narrative",
) -> WebGroupProofView:''',
    )

    replace_once(
        Path("tests/test_phase132_7_group_proof_cli_modes.py"),
        '''def test_phase132_7_group_proof_default_mode_remains_trace(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "# Group result" in captured.out
  assert "## Proof" in captured.out
  assert "Depth 0" in captured.out
  assert "Depth 1" in captured.out
  assert "# Group proof outline" not in captured.out
  assert "# Group proof narrative" not in captured.out


def test_phase132_7_group_proof_explicit_trace_matches_default(
  capsys,
):
  default_exit = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
    ]
  )
  default_output = (
    capsys.readouterr()
  )

  explicit_exit = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--mode",
      "trace",
    ]
  )
  explicit_output = (
    capsys.readouterr()
  )

  assert default_exit == 0
  assert explicit_exit == 0
  assert (
    explicit_output.out
    == default_output.out
  )
''',
        '''def test_phase132_7_group_proof_default_mode_is_narrative(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "# Group proof narrative" in captured.out
  assert "# Group result" not in captured.out
  assert "# Group proof outline" not in captured.out


def test_phase132_7_group_proof_explicit_trace_remains_available(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--depth",
      "1",
      "--mode",
      "trace",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "# Group result" in captured.out
  assert "## Proof" in captured.out
  assert "Depth 0" in captured.out
  assert "Depth 1" in captured.out
  assert "# Group proof narrative" not in captured.out
''',
    )

    p = Path("tests/test_phase131_4_group_result_proof_replay_cli.py")
    text = p.read_text(encoding="utf-8")
    replacements = (
        (
            '''      "9",
      "7",
    ]''',
            '''      "9",
      "7",
      "--depth",
      "1",
      "--mode",
      "trace",
    ]''',
        ),
        (
            '''      "--depth",
      "0",
    ]''',
            '''      "--depth",
      "0",
      "--mode",
      "trace",
    ]''',
        ),
        (
            '''      "2",
      "7",
    ]''',
            '''      "2",
      "7",
      "--depth",
      "1",
      "--mode",
      "trace",
    ]''',
        ),
        (
            '''      "11",
      "-1",
    ]''',
            '''      "11",
      "-1",
      "--depth",
      "1",
      "--mode",
      "trace",
    ]''',
        ),
    )
    for old, new in replacements:
        if text.count(old) != 1:
            raise RuntimeError(f"{p}: expected one legacy CLI block")
        text = text.replace(old, new, 1)
    p.write_text(text, encoding="utf-8")

    replace_once(
        Path("tests/test_phase132_9_web_group_proof_modes.py"),
        '''def test_phase132_9_trace_remains_default_web_group_proof_mode():
  view = (
    build_standard_web_group_proof_view(
      9,
      7,
    )
  )

  assert view.mode == "trace"
  assert view.rendered_lines == ()
  assert view.steps
''',
        '''def test_phase132_9_narrative_is_default_web_group_proof_mode():
  view = (
    build_standard_web_group_proof_view(
      9,
      7,
    )
  )

  assert view.mode == "narrative"
  assert view.max_depth == 2
  assert view.rendered_lines
  assert view.steps
''',
    )

    replace_once(
        Path("tests/test_phase131_5_web_group_proof.py"),
        '''  assert view.max_depth == 1
  assert (
    view.steps[
      0
    ].depth
    == 0
  )''',
        '''  assert view.max_depth == 2
  assert view.mode == "narrative"
  assert (
    view.steps[
      0
    ].depth
    == 0
  )''',
    )

    Path("tests/test_phase145_group_proof_defaults.py").write_text(
        '''import main as cli_main

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


def test_phase145_cli_group_proof_defaults_to_narrative_depth2(
  capsys,
):
  parser = cli_main.build_group_proof_argument_parser()
  args = parser.parse_args(
    [
      "9",
      "7",
    ]
  )

  assert args.mode == "narrative"
  assert args.depth == 2

  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
    ]
  )
  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "# Group proof narrative" in captured.out


def test_phase145_cli_explicit_trace_depth1_is_preserved(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--depth",
      "1",
      "--mode",
      "trace",
    ]
  )
  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "# Group result" in captured.out
  assert "Depth 1" in captured.out
  assert "Depth 2" not in captured.out


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
  assert b"Selected depth:" in response.data
  assert b">2<" in response.data


def test_phase145_web_explicit_trace_depth1_is_preserved():
  client = _build_test_client()

  response = client.post(
    "/",
    data={
      "form_kind": "group_proof",
      "n": "9",
      "k": "7",
      "group_proof_depth": "1",
      "group_proof_mode": "trace",
    },
  )

  assert response.status_code == 200
  assert b"Selected view:" in response.data
  assert b"trace" in response.data
  assert b"Depth 1" in response.data
  assert b"Depth 2" not in response.data
''',
        encoding="utf-8",
    )

    print("Phase 145 group-proof defaults applied.")
    print("default mode: narrative")
    print("default depth: 2")
    print("explicit mode/depth behavior preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
