from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"

TEST = (
  ROOT
  / "tests"
  / "test_phase159_r1_7c_r4_map_property_dearu_public_normalization.py"
)

NEW_FUNCTION = 'def test_phase159_r1_7c_r4_pi11_6_uses_concise_map_property_prose():\n  rendered = _public_narrative(\n    6,\n    5,\n  )\n\n  assert (\n    r"$\\Delta: \\pi_{10}^{9} \\to \\pi_{8}^{4}$ は単射."\n    in rendered\n  )\n  assert (\n    r"$E: \\pi_{9}^{4} \\to \\pi_{10}^{5}$ は全射."\n    in rendered\n  )\n  assert (\n    r"[R1]より, $H: \\pi_{7}^{3} \\to \\pi_{7}^{5}\\tag{1}$ は単射."\n    in rendered\n  )\n  assert (\n    r"$H: \\pi_{7}^{3} \\to \\pi_{7}^{5}\\tag{2}$ は全射."\n    in rendered\n  )\n'


def replace_function(
  source: str,
  function_name: str,
  new_source: str,
) -> str:
  marker = (
    "def "
    + function_name
    + "("
  )
  start = source.find(
    marker
  )

  if start < 0:
    raise SystemExit(
      f"function not found: {function_name}"
    )

  next_start = source.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  if next_start < 0:
    end = len(
      source
    )
  else:
    end = next_start + 1

  return (
    source[:start]
    + new_source.rstrip()
    + "\n\n"
    + source[end:]
  )


def main() -> None:
  BACKUP.mkdir(
    parents=True,
    exist_ok=True,
  )

  shutil.copy2(
    TEST,
    BACKUP / TEST.name,
  )

  source = TEST.read_text(
    encoding="utf-8"
  )

  source = replace_function(
    source,
    "test_phase159_r1_7c_r4_pi11_6_uses_concise_map_property_prose",
    NEW_FUNCTION,
  )

  TEST.write_text(
    source,
    encoding="utf-8",
  )

  print(
    "Phase 159 R1-7c R4 numbered reasoning repair1 fix1 applied."
  )
  print(
    "Production code changes: none"
  )
  print(
    "Updated the earlier prose regression to the current numbered public contract."
  )


if __name__ == "__main__":
  main()
