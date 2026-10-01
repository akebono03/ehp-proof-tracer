from pathlib import Path
import shutil
import sys

ROOT = Path.cwd()

BLOCKS = ROOT / "toda_group_proof_narrative_blocks.py"
RENDERER = ROOT / "toda_group_proof_generic_narrative_renderer.py"
SOURCE_TEST = (
  Path(__file__).resolve().parent
  / "payload"
  / "tests"
  / "test_phase153_r2_toda45_map_property_semantic.py"
)
TARGET_TEST = (
  ROOT
  / "tests"
  / "test_phase153_r2_toda45_map_property_semantic.py"
)


def require_file(path: Path) -> None:
  if not path.is_file():
    raise FileNotFoundError(
      f"required file not found: {path}"
    )


def replace_once(
  text: str,
  old: str,
  new: str,
  *,
  label: str,
) -> str:
  count = text.count(old)

  if count == 0:
    if new in text:
      return text
    raise RuntimeError(
      f"{label}: expected source text not found"
    )

  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one source occurrence, found {count}"
    )

  return text.replace(
    old,
    new,
    1,
  )


def patch_blocks(text: str) -> str:
  old_import = """from toda_rules import (
  TodaDeltaImageUpToSignStatement,
  TodaDeltaInjectiveStatement,
  TodaDeltaZeroStatement,
"""
  new_import = """from toda_rules import (
  Toda45IsomorphismStatement,
  TodaDeltaImageUpToSignStatement,
  TodaDeltaInjectiveStatement,
  TodaDeltaZeroStatement,
"""

  text = replace_once(
    text,
    old_import,
    new_import,
    label="blocks import",
  )

  old_tuple = """MAP_PROPERTY_STATEMENT_TYPES = (
  TodaDeltaInjectiveStatement,
"""
  new_tuple = """MAP_PROPERTY_STATEMENT_TYPES = (
  Toda45IsomorphismStatement,
  TodaDeltaInjectiveStatement,
"""

  text = replace_once(
    text,
    old_tuple,
    new_tuple,
    label="MAP_PROPERTY_STATEMENT_TYPES",
  )

  return text


def patch_renderer(text: str) -> str:
  old_import = """from toda_rules import (
  TodaDeltaInjectiveStatement,
  TodaDeltaZeroStatement,
"""
  new_import = """from toda_rules import (
  Toda45IsomorphismStatement,
  TodaDeltaInjectiveStatement,
  TodaDeltaZeroStatement,
"""

  text = replace_once(
    text,
    old_import,
    new_import,
    label="renderer import",
  )

  old_tuple = """_GENERIC_ISOMORPHISM_STATEMENT_TYPES = (
  TodaHopfInvariantIsomorphismStatement,
  TodaSuspensionIsomorphismStatement,
)
"""
  new_tuple = """_GENERIC_ISOMORPHISM_STATEMENT_TYPES = (
  Toda45IsomorphismStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaSuspensionIsomorphismStatement,
)
"""

  text = replace_once(
    text,
    old_tuple,
    new_tuple,
    label="_GENERIC_ISOMORPHISM_STATEMENT_TYPES",
  )

  return text


def main() -> int:
  require_file(BLOCKS)
  require_file(RENDERER)
  require_file(SOURCE_TEST)
  require_file(ROOT / "tests")

  blocks_original = BLOCKS.read_text(
    encoding="utf-8"
  )
  renderer_original = RENDERER.read_text(
    encoding="utf-8"
  )

  blocks_patched = patch_blocks(
    blocks_original
  )
  renderer_patched = patch_renderer(
    renderer_original
  )

  if blocks_patched != blocks_original:
    BLOCKS.write_text(
      blocks_patched,
      encoding="utf-8",
      newline="\n",
    )

  if renderer_patched != renderer_original:
    RENDERER.write_text(
      renderer_patched,
      encoding="utf-8",
      newline="\n",
    )

  shutil.copyfile(
    SOURCE_TEST,
    TARGET_TEST,
  )

  print("Applied Phase153-R2 minimal production change:")
  print(
    "  toda_group_proof_narrative_blocks.py"
    " -> Toda45IsomorphismStatement registered as MAP_PROPERTY"
  )
  print(
    "  toda_group_proof_generic_narrative_renderer.py"
    " -> Toda45IsomorphismStatement registered in generic isomorphism renderer"
  )
  print(
    "  tests/test_phase153_r2_toda45_map_property_semantic.py"
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
