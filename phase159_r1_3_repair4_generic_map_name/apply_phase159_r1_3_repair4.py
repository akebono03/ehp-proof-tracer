from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"

def ensure_import_name(source, module_name, import_name):
    start_marker = f"from {module_name} import (\n"
    block_start = source.find(start_marker)
    if block_start < 0:
        raise RuntimeError(f"import block not found: {module_name}")
    block_end = source.find(")\n", block_start)
    if block_end < 0:
        raise RuntimeError(f"import block end not found: {module_name}")
    block = source[block_start:block_end+2]
    line = f"  {import_name},\n"
    if line in block:
        return source
    updated = block[:-2] + line + ")\n"
    return source[:block_start] + updated + source[block_end+2:]

def replace_function(source, function_name, replacement):
    marker = f"def {function_name}("
    start = source.find(marker)
    if start < 0:
        raise RuntimeError(f"function not found: {function_name}")
    next_function = source.find("\ndef ", start + len(marker))
    end = len(source) if next_function < 0 else next_function + 1
    return source[:start] + replacement.rstrip() + "\n\n" + source[end:]

UNIQUE_PREIMAGE_FUNCTION = '''def _phase159_unique_preimage_definition_line(
  proof_step: ProofStep,
) -> str | None:
  statement = proof_step.conclusion
  group_map = getattr(
    statement,
    "map",
    None,
  )
  element = getattr(
    statement,
    "element",
    None,
  )
  image = getattr(
    statement,
    "image",
    None,
  )

  if (
    group_map is None
    or element is None
    or image is None
  ):
    return None

  isomorphism_premise = next(
    (
      premise_step
      for premise_step in proof_step.premises
      if (
        isinstance(
          premise_step,
          ProofStep,
        )
        and isinstance(
          premise_step.conclusion,
          _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
        )
        and getattr(
          premise_step.conclusion,
          "map",
          None,
        )
        == group_map
      )
    ),
    None,
  )

  if isomorphism_premise is None:
    return None

  map_name = _generic_group_map_name(
    group_map
  )

  if map_name is None:
    return None

  return (
    "この同型写像により, $"
    + map_name
    + "("
    + render_toda_expression_latex(
      element
    )
    + ") = "
    + render_toda_expression_latex(
      image
    )
    + "$ となる $"
    + render_toda_expression_latex(
      element
    )
    + r" \\in "
    + render_toda_primary_group_latex(
      group_map.source_group
    )
    + "$ が一意に存在する."
  )
'''

def main():
    if not RENDERER.exists():
        raise FileNotFoundError(RENDERER)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = ROOT / f"phase159_r1_3_repair4_backup_{stamp}"
    backup_dir.mkdir(parents=True, exist_ok=False)
    shutil.copy2(RENDERER, backup_dir / RENDERER.name)

    source = RENDERER.read_text(encoding="utf-8-sig")
    source = ensure_import_name(
        source,
        "toda_group_proof_generic_narrative_renderer",
        "_generic_group_map_name",
    )
    source = replace_function(
        source,
        "_phase159_unique_preimage_definition_line",
        UNIQUE_PREIMAGE_FUNCTION,
    )
    RENDERER.write_text(source, encoding="utf-8", newline="\n")
    print("Phase 159-R1-3 repair4 applied.")
    print("Backup:", backup_dir)

if __name__ == "__main__":
    main()
