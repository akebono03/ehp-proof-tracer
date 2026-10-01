from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent


def find_repository_root() -> Path:
  for candidate in (
    PACKAGE_DIR.parent,
    Path.cwd(),
  ):
    if (
      (
        candidate
        / "tests"
        / "test_phase132_7_group_proof_cli_modes.py"
      ).is_file()
      and (
        candidate
        / "main.py"
      ).is_file()
    ):
      return candidate.resolve()

  raise SystemExit(
    "EHP Proof Tracer repository root was not found."
  )


def replace_once(
  text: str,
  old: str,
  new: str,
  label: str,
) -> str:
  count = text.count(
    old
  )

  if count != 1:
    raise SystemExit(
      label
      + ": expected exactly one replacement target, found "
      + str(
        count
      )
      + "."
    )

  return text.replace(
    old,
    new,
    1,
  )


def main() -> None:
  repo = find_repository_root()

  path = (
    repo
    / "tests"
    / "test_phase132_7_group_proof_cli_modes.py"
  )

  backup_dir = (
    repo
    / "phase153_final_regression_stale_phase132_cli_test_repair_r1_backup"
  )
  backup_dir.mkdir(
    exist_ok=True
  )
  backup = (
    backup_dir
    / path.name
  )

  if not backup.exists():
    shutil.copy2(
      path,
      backup,
    )

  text = path.read_text(
    encoding="utf-8"
  )

  old_default = '''def test_phase132_7_group_proof_default_mode_is_narrative(
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
  assert "# Group result" not in captured.out
'''

  new_default = '''def test_phase132_7_group_proof_default_mode_is_narrative(
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
  assert "使用する結果を先にまとめる." in captured.out
  assert (
    r"$\\pi_{16}^{9} = "
    r"\\mathbb{Z}/16\\{\\sigma_{9}\\}$"
    in captured.out
  )
  assert "# Group result" not in captured.out
'''

  old_explicit = '''def test_phase132_7_group_proof_narrative_mode_uses_narrative_renderer(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "# Group proof narrative" in captured.out
  assert "## 使用する結果" in captured.out
  assert "**[R1] Proposition 5.15.**" in captured.out
  assert (
    r"$\\pi_{16}^{9} = "
    r"\\mathbb{Z}/16\\{\\sigma_{9}\\}$"
    in captured.out
  )
  assert "# Group result" not in captured.out
'''

  new_explicit = '''def test_phase132_7_group_proof_narrative_mode_uses_narrative_renderer(
  capsys,
):
  exit_code = cli_main.main(
    [
      "group-proof",
      "9",
      "7",
      "--mode",
      "narrative",
    ]
  )

  captured = capsys.readouterr()

  assert exit_code == 0
  assert captured.err == ""
  assert "使用する結果を先にまとめる." in captured.out
  assert "[R1]" in captured.out
  assert (
    r"$\\pi_{16}^{9} = "
    r"\\mathbb{Z}/16\\{\\sigma_{9}\\}$"
    in captured.out
  )
  assert "# Group result" not in captured.out
'''

  text = replace_once(
    text,
    old_default,
    new_default,
    "Phase 132 CLI default Narrative stale heading expectation",
  )
  text = replace_once(
    text,
    old_explicit,
    new_explicit,
    "Phase 132 CLI explicit Narrative stale Reference expectation",
  )

  path.write_text(
    text,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 153 final regression stale Phase 132 CLI test repair R1 applied."
  )
  print(
    "Production changes: none."
  )
  print(
    "Updated:"
  )
  print(
    "  tests/test_phase132_7_group_proof_cli_modes.py"
  )
  print(
    "Updated test functions:"
  )
  print(
    "  test_phase132_7_group_proof_default_mode_is_narrative"
  )
  print(
    "  test_phase132_7_group_proof_narrative_mode_uses_narrative_renderer"
  )


if __name__ == "__main__":
  main()
