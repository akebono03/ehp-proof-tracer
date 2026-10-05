from pathlib import Path
from datetime import datetime
import shutil


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"


def _replace_function(source: str, function_name: str, replacement: str) -> str:
  marker = "def " + function_name + "("
  start = source.find(marker)
  if start < 0:
    raise RuntimeError("function not found: " + function_name)

  next_function = source.find("\ndef ", start + len(marker))
  end = len(source) if next_function < 0 else next_function + 1

  return source[:start] + replacement.rstrip() + "\n\n" + source[end:]


UNIQUE_PREIMAGE_FUNCTION = r'''def _phase159_unique_preimage_definition_line(
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

  map_name = getattr(
    group_map,
    "name",
    None,
  )

  if not isinstance(
    map_name,
    str,
  ):
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
    + r" \in "
    + render_toda_primary_group_latex(
      group_map.source_group
    )
    + "$ が一意に存在する."
  )
'''


CALL_OLD = '''    replacement = _phase159_unique_preimage_definition_line(
      semantic_sidecar,
      proof_step,
    )
'''

CALL_NEW = '''    replacement = _phase159_unique_preimage_definition_line(
      proof_step,
    )
'''


def main() -> None:
  if not RENDERER.exists():
    raise FileNotFoundError(RENDERER)

  stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  backup_dir = ROOT / ("phase159_r1_3_repair2_backup_" + stamp)
  backup_dir.mkdir(parents=True, exist_ok=False)
  shutil.copy2(RENDERER, backup_dir / RENDERER.name)

  source = RENDERER.read_text(encoding="utf-8-sig")

  source = _replace_function(
    source,
    "_phase159_unique_preimage_definition_line",
    UNIQUE_PREIMAGE_FUNCTION,
  )

  call_count = source.count(CALL_OLD)
  if call_count == 1:
    source = source.replace(CALL_OLD, CALL_NEW, 1)
  elif call_count == 0 and CALL_NEW in source:
    pass
  else:
    raise RuntimeError(
      "unexpected unique-preimage call shape: "
      + str(call_count)
    )

  RENDERER.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print("Phase 159-R1-3 repair2 applied.")
  print("Backup:", backup_dir)
  print("Changed only unique-preimage public projection.")


if __name__ == "__main__":
  main()
