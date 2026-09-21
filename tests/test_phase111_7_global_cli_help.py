import pytest

import main as cli_main


def test_phase111_7_global_help_lists_current_cli_capabilities(
  capsys,
):
  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "--help",
      ]
    )

  captured = capsys.readouterr()

  assert exc_info.value.code == 0
  assert captured.err == ""

  assert "main.py" in captured.out

  commands = (
    "explore",
    "explore-proof",
    "explore-applicable",
    "show-proof",
    "execute",
    "query",
    "query-proof",
  )

  assert all(
    command in captured.out
    for command in commands
  )

  assert (
    "Use 'python main.py <command> --help'"
    in captured.out
  )


def test_phase111_7_global_help_describes_project_group_semantics(
  capsys,
):
  with pytest.raises(
    SystemExit,
  ) as exc_info:
    cli_main.main(
      [
        "--help",
      ]
    )

  captured = capsys.readouterr()

  assert exc_info.value.code == 0
  assert captured.err == ""

  normalized_output = " ".join(
    captured.out.split()
  )

  assert (
    "pi_{n+k}^n"
    in normalized_output
  )

  assert (
    "free part plus 2-primary component"
    in normalized_output
  )

  assert (
    "pi_{n+k}(S^n)"
    not in normalized_output
  )
