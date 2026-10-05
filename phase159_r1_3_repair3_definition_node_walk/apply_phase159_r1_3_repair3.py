from pathlib import Path
from datetime import datetime
import shutil


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"

OLD_BLOCK = '  for dependency in semantic_sidecar.dependency_semantics:\n    if (\n      dependency.role\n      is not TodaGroupProofNarrativeDependencySemanticRole\n      .PRECONDITION_FOR_DEFINITION\n    ):\n      continue\n\n    proof_step = dependency.dependent_step\n    original = _render_generic_narrative_step(proof_step)\n    replacement = _phase159_unique_preimage_definition_line(\n      proof_step,\n    )\n    if replacement is None:\n      continue\n\n    for index, line in enumerate(lines):\n      if original not in line:\n        continue\n\n      prefix = line[:line.find(original)]\n      if prefix in (\n        "これらから, ",\n        "これらより, ",\n        "このことから, ",\n        "したがって, ",\n      ):\n        prefix = ""\n\n      lines[index] = prefix + replacement\n      break\n'
NEW_BLOCK = '  for node in semantic_presentation.nodes:\n    proof_step = node.proof_step\n    original = _render_generic_narrative_step(\n      proof_step\n    )\n    replacement = (\n      _phase159_unique_preimage_definition_line(\n        proof_step,\n      )\n    )\n\n    if replacement is None:\n      continue\n\n    for index, line in enumerate(\n      lines\n    ):\n      if original not in line:\n        continue\n\n      prefix = line[\n        :line.find(\n          original\n        )\n      ]\n\n      if prefix in (\n        "これらから, ",\n        "これらより, ",\n        "このことから, ",\n        "したがって, ",\n      ):\n        prefix = ""\n\n      lines[\n        index\n      ] = (\n        prefix\n        + replacement\n      )\n      break\n'


def main() -> None:
  if not RENDERER.exists():
    raise FileNotFoundError(
      RENDERER
    )

  stamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase159_r1_3_repair3_backup_"
      + stamp
    )
  )
  backup_dir.mkdir(
    parents=True,
    exist_ok=False,
  )
  shutil.copy2(
    RENDERER,
    backup_dir / RENDERER.name,
  )

  source = RENDERER.read_text(
    encoding="utf-8-sig"
  )

  count = source.count(
    OLD_BLOCK
  )

  if count != 1:
    raise RuntimeError(
      "expected exactly one old definition projection loop, found "
      + str(
        count
      )
    )

  source = source.replace(
    OLD_BLOCK,
    NEW_BLOCK,
    1,
  )

  RENDERER.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159-R1-3 repair3 applied."
  )
  print(
    "Backup:",
    backup_dir,
  )
  print(
    "Changed only the generic definition-step traversal."
  )


if __name__ == "__main__":
  main()
