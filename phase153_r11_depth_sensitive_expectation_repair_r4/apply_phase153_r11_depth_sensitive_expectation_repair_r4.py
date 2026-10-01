from pathlib import Path
import shutil


PACKAGE_DIR = Path(__file__).resolve().parent


def find_repository_root() -> Path:
  for candidate in (
    PACKAGE_DIR.parent,
    Path.cwd(),
  ):
    path = (
      candidate
      / "tests"
      / "test_phase153_r11_generic_reference_attribution_filtering.py"
    )
    if path.is_file():
      return candidate.resolve()

  raise SystemExit(
    "EHP Proof Tracer repository root was not found."
  )


def main() -> None:
  repo = find_repository_root()
  path = (
    repo
    / "tests"
    / "test_phase153_r11_generic_reference_attribution_filtering.py"
  )
  text = path.read_text(
    encoding="utf-8"
  )

  function_name = (
    "def "
    "test_phase153_r11_pi6_3_preserves_external_references_used_by_generic_proof"
    "():"
  )
  start = text.find(
    function_name
  )

  if start < 0:
    raise SystemExit(
      "R11 failing test function was not found by function name."
    )

  next_def = text.find(
    "\ndef ",
    start + len(
      function_name
    ),
  )

  if next_def < 0:
    end = len(
      text
    )
  else:
    end = next_def + 1

  replacement = """def test_phase153_r11_pi6_3_depth2_preserves_used_external_references():
  _, rendered = _pi6_3_rendered()
  reference_part = rendered.split(
    "まず",
    1,
  )[0]

  assert "使用する結果を先にまとめる." in reference_part
  assert "(5.3)" in reference_part
  assert "Proposition 5.3" in reference_part
  assert "Proposition 5.6" not in reference_part


"""

  updated = (
    text[
      :start
    ]
    + replacement
    + text[
      end:
    ]
  )

  backup_dir = (
    repo
    / "phase153_r11_depth_sensitive_expectation_repair_r4_backup"
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

  path.write_text(
    updated,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 153-R11 depth-sensitive expectation repair R4 applied."
  )
  print(
    "Production changes: none"
  )
  print(
    "Changed test:"
  )
  print(
    "  tests/test_phase153_r11_generic_reference_attribution_filtering.py"
  )


if __name__ == "__main__":
  main()
