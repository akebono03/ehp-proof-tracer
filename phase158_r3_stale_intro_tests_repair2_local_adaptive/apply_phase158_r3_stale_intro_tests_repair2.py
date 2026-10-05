from __future__ import annotations

from pathlib import Path
import re
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_DIR = Path(__file__).resolve().parent
BACKUP_DIR = (
  REPO_ROOT
  / "phase158_r3_stale_intro_tests_repair2_backup"
)

INTRO = "使用する結果を先にまとめる."

TARGET_FILES = (
  "tests/test_phase132_7_group_proof_cli_modes.py",
  "tests/test_phase150_rc4_7a_cross_group_reference_normalization.py",
  "tests/test_phase153_r3_4_reference_statement_rendering_connection.py",
  "tests/test_phase144_6_r3_production_references.py",
  "tests/test_phase156_r5_repair9_test_contract_after_boundary_collapse.py",
  "tests/test_phase153_r11_generic_reference_attribution_filtering.py",
)


def _test_function_name_for_offset(
  source: str,
  offset: int,
) -> str | None:
  prefix = source[
    :offset
  ]
  matches = list(
    re.finditer(
      r"^def (test_[A-Za-z0-9_]+)\(",
      prefix,
      flags=re.MULTILINE,
    )
  )

  if not matches:
    return None

  return matches[
    -1
  ].group(
    1
  )


def _collect_stale_test_nodeids(
  relative_path: str,
  source: str,
) -> set[str]:
  nodeids: set[str] = set()

  for match in re.finditer(
    re.escape(
      INTRO
    ),
    source,
  ):
    function_name = (
      _test_function_name_for_offset(
        source,
        match.start(),
      )
    )

    if function_name is not None:
      nodeids.add(
        relative_path
        + "::"
        + function_name
      )

  return nodeids


def _replace_positive_intro_assertions(
  source: str,
) -> str:
  pattern = re.compile(
    r'(?m)^(\s*)assert "'
    + re.escape(
      INTRO
    )
    + r'" in ([^\n]+)$'
  )

  return pattern.sub(
    lambda match: (
      match.group(
        1
      )
      + 'assert "'
      + INTRO
      + '" not in '
      + match.group(
        2
      )
    ),
    source,
  )


def _remove_intro_from_expected_strings(
  source: str,
) -> str:
  source = source.replace(
    '"使用する結果を先にまとめる.\\n\\n"\n',
    "",
  )
  source = source.replace(
    "'使用する結果を先にまとめる.\\n\\n'\n",
    "",
  )

  return source


def _replace_intro_startswith_contract(
  source: str,
) -> str:
  source = re.sub(
    (
      r'assert ([A-Za-z0-9_\.]+)\.startswith\(\s*'
      r'"'
      + re.escape(
        INTRO
      )
      + r'"\s*\)'
    ),
    (
      r'assert \1.startswith('
      r'"**[R1] "'
      r')'
    ),
    source,
    flags=re.MULTILINE,
  )

  return source


def _patch_source(
  source: str,
) -> str:
  patched = (
    _replace_positive_intro_assertions(
      source
    )
  )
  patched = (
    _remove_intro_from_expected_strings(
      patched
    )
  )
  patched = (
    _replace_intro_startswith_contract(
      patched
    )
  )

  return patched


def main() -> int:
  BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True,
  )

  stale_nodeids: set[
    str
  ] = set()
  changed_files = []

  for relative_path in TARGET_FILES:
    target = (
      REPO_ROOT
      / relative_path
    )

    if not target.exists():
      raise RuntimeError(
        "Missing test file: "
        + str(
          target
        )
      )

    source = target.read_text(
      encoding="utf-8",
    )
    stale_nodeids.update(
      _collect_stale_test_nodeids(
        relative_path,
        source,
      )
    )

    patched = (
      _patch_source(
        source
      )
    )

    compile(
      patched,
      str(
        target
      ),
      "exec",
    )

    if patched != source:
      backup = (
        BACKUP_DIR
        / relative_path
      )
      backup.parent.mkdir(
        parents=True,
        exist_ok=True,
      )

      if not backup.exists():
        shutil.copy2(
          target,
          backup,
        )

      target.write_text(
        patched,
        encoding="utf-8",
      )
      changed_files.append(
        relative_path
      )

  nodeids_path = (
    PACKAGE_DIR
    / "modified_test_nodeids.txt"
  )
  nodeids_path.write_text(
    "\n".join(
      sorted(
        stale_nodeids
      )
    )
    + (
      "\n"
      if stale_nodeids
      else ""
    ),
    encoding="utf-8",
  )

  print(
    "Phase 158-R3 stale intro test repair2 applied."
  )
  print(
    "Production code changes: none"
  )
  print(
    "Changed test files: "
    + str(
      len(
        changed_files
      )
    )
  )

  for path in changed_files:
    print(
      "  "
      + path
    )

  print(
    "Affected test functions detected: "
    + str(
      len(
        stale_nodeids
      )
    )
  )

  for nodeid in sorted(
    stale_nodeids
  ):
    print(
      "  "
      + nodeid
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
