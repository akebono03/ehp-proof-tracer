from pathlib import Path
import re


def replace_if_needed(path, old, new, label):
    text = path.read_text(encoding="utf-8")
    if new in text:
        print("already applied:", label)
        return
    if old not in text:
        raise RuntimeError(f"{path}: old/new form not found: {label}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("applied:", label)


def replace_function(path, old_names, new_text):
    text = path.read_text(encoding="utf-8")
    name = next((n for n in old_names if f"def {n}(" in text), None)
    if name is None:
        raise RuntimeError(f"{path}: target test function not found: {old_names}")
    pattern = re.compile(
        rf"^def {re.escape(name)}\([\s\S]*?(?=^def |^@pytest\.mark|\Z)",
        re.MULTILINE,
    )
    match = pattern.search(text)
    if match is None:
        raise RuntimeError(f"{path}: could not isolate {name}")
    replacement = new_text.rstrip() + "\n\n\n"
    path.write_text(
        text[:match.start()] + replacement + text[match.end():],
        encoding="utf-8",
    )
    print("updated:", name)


def main():
    replace_if_needed(
        Path("main.py"),
        '    type=_parse_nonnegative_int,\n    help=(\n      "maximum proof replay depth; "\n      "omit to use the default depth 1"\n    ),\n  )\n\n  parser.add_argument(\n    "--mode",\n    choices=(\n      "trace",\n      "outline",\n      "narrative",\n    ),\n    default="trace",\n    help=(\n      "proof presentation mode; "\n      "default: trace"\n    ),',
        '    type=_parse_nonnegative_int,\n    default=2,\n    help=(\n      "maximum proof replay depth; "\n      "default: 2"\n    ),\n  )\n\n  parser.add_argument(\n    "--mode",\n    choices=(\n      "trace",\n      "outline",\n      "narrative",\n    ),\n    default="narrative",\n    help=(\n      "proof presentation mode; "\n      "default: narrative"\n    ),',
        "CLI parser defaults",
    )
    replace_if_needed(
        Path("main.py"),
        'def _run_group_proof_command(\n  n: int,\n  k: int,\n  max_depth: int | None = None,\n  mode: str = "trace",\n) -> int:',
        'def _run_group_proof_command(\n  n: int,\n  k: int,\n  max_depth: int | None = 2,\n  mode: str = "narrative",\n) -> int:',
        "CLI command defaults",
    )
    replace_if_needed(
        Path("web_app.py"),
        '    group_proof_depth_value = request.form.get(\n      "group_proof_depth",\n      "1",\n    )\n    group_proof_mode_value = request.form.get(\n      "group_proof_mode",\n      "trace",\n    )',
        '    group_proof_depth_value = request.form.get(\n      "group_proof_depth",\n      "2",\n    )\n    group_proof_mode_value = request.form.get(\n      "group_proof_mode",\n      "narrative",\n    )',
        "Web form defaults",
    )
    replace_if_needed(
        Path("web_group_proof.py"),
        'def build_standard_web_group_proof_view(\n  n: int,\n  k: int,\n  max_depth: int = 1,\n  mode: str = "trace",\n) -> WebGroupProofView:',
        'def build_standard_web_group_proof_view(\n  n: int,\n  k: int,\n  max_depth: int = 2,\n  mode: str = "narrative",\n) -> WebGroupProofView:',
        "Web adapter defaults",
    )

    p = Path("tests/test_phase131_4_group_result_proof_replay_cli.py")
    replace_function(
        p,
        ["test_phase131_4_group_proof_sigma9_renders_group_source_and_proof"],
        r'''def test_phase131_4_group_proof_sigma9_renders_group_source_and_proof(
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
  assert "## Source" in captured.out
  assert "## Proof" in captured.out
  assert "Toda Proposition 5.15" in captured.out
  assert "- Phase: 75" in captured.out
  assert "Depth 0" in captured.out
  assert "Depth 1" in captured.out
  assert (
    r"$\pi_{16}^{9} = \mathbb{Z}/16\{\sigma_{9}\}$"
    in captured.out
  )''',
    )
    replace_function(
        p,
        ["test_phase131_4_group_proof_zero_depth_contains_only_root"],
        '''def test_phase131_4_group_proof_zero_depth_contains_only_root(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--depth",
      "0",
      "--mode",
      "trace",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert "Depth 0" in captured.out
  assert "Depth 1" not in captured.out''',
    )
    replace_function(
        p,
        ["test_phase131_4_group_proof_zero_group_does_not_require_generator"],
        r'''def test_phase131_4_group_proof_zero_group_does_not_require_generator(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "2",
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
  assert r"$\pi_{9}^{2} = 0$" in captured.out
  assert "Toda Proposition 5.15" in captured.out
  assert "Depth 0" in captured.out''',
    )
    replace_function(
        p,
        ["test_phase131_4_group_proof_connectivity_zero_is_replayed"],
        r'''def test_phase131_4_group_proof_connectivity_zero_is_replayed(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "11",
      "-1",
      "--depth",
      "1",
      "--mode",
      "trace",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert r"$\pi_{10}^{11} = 0$" in captured.out
  assert "Sphere connectivity" in captured.out
  assert "- Phase: 130" in captured.out
  assert "Depth 0" in captured.out
  assert "Depth 1" not in captured.out''',
    )

    p = Path("tests/test_phase132_7_group_proof_cli_modes.py")
    replace_function(
        p,
        [
            "test_phase132_7_group_proof_default_mode_is_narrative",
            "test_phase132_7_group_proof_default_mode_remains_trace",
        ],
        '''def test_phase132_7_group_proof_default_mode_is_narrative(
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
  assert "# Group result" not in captured.out''',
    )
    replace_function(
        p,
        [
            "test_phase132_7_group_proof_explicit_trace_remains_available",
            "test_phase132_7_group_proof_explicit_trace_matches_default",
        ],
        '''def test_phase132_7_group_proof_explicit_trace_remains_available(
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
  assert "Depth 0" in captured.out
  assert "Depth 1" in captured.out
  assert "# Group proof narrative" not in captured.out''',
    )

    p = Path("tests/test_phase132_9_web_group_proof_modes.py")
    replace_function(
        p,
        [
            "test_phase132_9_narrative_is_default_web_group_proof_mode",
            "test_phase132_9_trace_remains_default_web_group_proof_mode",
        ],
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
  assert view.steps''',
    )

    p = Path("tests/test_phase131_5_web_group_proof.py")
    replace_function(
        p,
        ["test_phase131_5_sigma9_group_proof_view_uses_group_result_replay"],
        r'''def test_phase131_5_sigma9_group_proof_view_uses_group_result_replay():
  view = (
    build_standard_web_group_proof_view(
      9,
      7,
    )
  )

  assert (
    view.conclusion_latex
    == (
      r"\pi_{16}^{9} = "
      r"\mathbb{Z}/16\{\sigma_{9}\}"
    )
  )
  assert view.theorem == "Toda Proposition 5.15"
  assert view.phase == "75"
  assert view.max_depth == 2
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
''',
        encoding="utf-8",
    )

    print("Phase 145 Resume R1 apply: PASS")


if __name__ == "__main__":
    main()
