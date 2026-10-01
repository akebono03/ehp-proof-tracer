from pathlib import Path
import shutil

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


def require_directory(path: Path) -> None:
  if not path.is_dir():
    raise FileNotFoundError(
      f"required directory not found: {path}"
    )


def replace_once(
  text: str,
  old: str,
  new: str,
  *,
  label: str,
) -> str:
  if new in text:
    return text

  count = text.count(old)

  if count != 1:
    raise RuntimeError(
      f"{label}: expected exactly one source occurrence, found {count}"
    )

  return text.replace(
    old,
    new,
    1,
  )


def ensure_blocks_registration(text: str) -> str:
  old_import = '''from toda_rules import (
  TodaDeltaImageUpToSignStatement,
'''
  new_import = '''from toda_rules import (
  Toda45IsomorphismStatement,
  TodaDeltaImageUpToSignStatement,
'''

  text = replace_once(
    text,
    old_import,
    new_import,
    label="blocks import",
  )

  old_tuple = '''MAP_PROPERTY_STATEMENT_TYPES = (
  TodaDeltaInjectiveStatement,
'''
  new_tuple = '''MAP_PROPERTY_STATEMENT_TYPES = (
  Toda45IsomorphismStatement,
  TodaDeltaInjectiveStatement,
'''

  text = replace_once(
    text,
    old_tuple,
    new_tuple,
    label="MAP_PROPERTY_STATEMENT_TYPES",
  )

  return text


def patch_renderer(text: str) -> str:
  old_human_import = '''from toda_human_readable_renderer import (
  render_toda_expression_latex,
)
'''
  new_human_import = '''from toda_human_readable_renderer import (
  _render_scalar_latex,
  render_toda_expression_latex,
)
'''

  text = replace_once(
    text,
    old_human_import,
    new_human_import,
    label="scalar renderer import",
  )

  old_rules_import = '''from toda_rules import (
  TodaDeltaInjectiveStatement,
'''
  new_rules_import = '''from toda_rules import (
  Toda45IsomorphismStatement,
  TodaDeltaInjectiveStatement,
'''

  text = replace_once(
    text,
    old_rules_import,
    new_rules_import,
    label="Toda45 renderer import",
  )

  old_tuple = '''_GENERIC_ISOMORPHISM_STATEMENT_TYPES = (
  TodaHopfInvariantIsomorphismStatement,
  TodaSuspensionIsomorphismStatement,
)
'''
  new_tuple = '''_GENERIC_ISOMORPHISM_STATEMENT_TYPES = (
  Toda45IsomorphismStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaSuspensionIsomorphismStatement,
)
'''

  text = replace_once(
    text,
    old_tuple,
    new_tuple,
    label="_GENERIC_ISOMORPHISM_STATEMENT_TYPES",
  )

  old_function = '''def _generic_group_map_name(
  group_map,
) -> str | None:
  if isinstance(
    group_map,
    TodaSuspensionMap,
  ):
    return "E"

  if isinstance(
    group_map,
    TodaIteratedSuspensionMap,
  ):
    exponent = group_map.exponent

    if (
      not isinstance(
        exponent,
        int,
      )
      or isinstance(
        exponent,
        bool,
      )
      or exponent < 1
    ):
      return None

    if exponent == 1:
      return "E"

    return (
      r"E^{"
      + str(
        exponent
      )
      + "}"
    )

  if isinstance(
    group_map,
    TodaHopfInvariantMap,
  ):
    return "H"

  if isinstance(
    group_map,
    TodaDeltaMap,
  ):
    return r"\\Delta"

  return None
'''

  new_function = '''def _generic_group_map_name(
  group_map,
) -> str | None:
  if isinstance(
    group_map,
    TodaSuspensionMap,
  ):
    return "E"

  if isinstance(
    group_map,
    TodaIteratedSuspensionMap,
  ):
    exponent = group_map.exponent

    if isinstance(
      exponent,
      bool,
    ):
      return None

    if isinstance(
      exponent,
      int,
    ):
      if exponent < 1:
        return None

      if exponent == 1:
        return "E"

      exponent_latex = str(
        exponent
      )
    else:
      try:
        exponent_latex = (
          _render_scalar_latex(
            exponent
          )
        )
      except TypeError:
        return None

    return (
      r"E^{"
      + exponent_latex
      + "}"
    )

  if isinstance(
    group_map,
    TodaHopfInvariantMap,
  ):
    return "H"

  if isinstance(
    group_map,
    TodaDeltaMap,
  ):
    return r"\\Delta"

  return None
'''

  text = replace_once(
    text,
    old_function,
    new_function,
    label="_generic_group_map_name",
  )

  return text


def main() -> int:
  require_file(BLOCKS)
  require_file(RENDERER)
  require_file(SOURCE_TEST)
  require_directory(ROOT / "tests")

  blocks_original = BLOCKS.read_text(
    encoding="utf-8"
  )
  renderer_original = RENDERER.read_text(
    encoding="utf-8"
  )

  blocks_patched = ensure_blocks_registration(
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

  print("Applied Phase153-R2 Fixed2:")
  print(
    "  Toda45IsomorphismStatement -> MAP_PROPERTY"
  )
  print(
    "  Toda45IsomorphismStatement -> generic isomorphism rendering"
  )
  print(
    "  symbolic TodaIteratedSuspensionMap exponent"
    " -> existing _render_scalar_latex"
  )
  print(
    "  tests/test_phase153_r2_toda45_map_property_semantic.py"
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
