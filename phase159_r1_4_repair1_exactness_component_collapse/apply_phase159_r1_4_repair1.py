from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"

HELPERS = 'def _phase159_public_exactness_latex(\n  line: str,\n) -> str | None:\n  stripped = line.strip()\n\n  if (\n    not stripped.startswith("$")\n    or r"\\\\xrightarrow{" not in stripped\n  ):\n    return None\n\n  closing_math = stripped.rfind(\n    "$"\n  )\n\n  if closing_math <= 0:\n    return None\n\n  latex = stripped[\n    1:closing_math\n  ]\n\n  return latex.replace(\n    "Δ",\n    r"\\\\Delta",\n  )\n\n\ndef _phase159_consolidate_public_exactness_lines(\n  lines: list[str],\n) -> list[str]:\n  exactness_by_index = {\n    index: latex\n    for index, line in enumerate(\n      lines\n    )\n    if (\n      latex := _phase159_public_exactness_latex(\n        line\n      )\n    )\n    is not None\n  }\n\n  if not exactness_by_index:\n    return lines\n\n  maximal_indices = []\n\n  for index, latex in exactness_by_index.items():\n    is_strict_subsequence = any(\n      (\n        latex != other_latex\n        and latex in other_latex\n      )\n      for (\n        other_index,\n        other_latex,\n      ) in exactness_by_index.items()\n      if other_index != index\n    )\n\n    if not is_strict_subsequence:\n      maximal_indices.append(\n        index\n      )\n\n  canonical_index_by_latex = {}\n\n  for index in maximal_indices:\n    latex = exactness_by_index[\n      index\n    ]\n    canonical_index_by_latex.setdefault(\n      latex,\n      index,\n    )\n\n  canonical_latex_by_index = {\n    index: latex\n    for (\n      latex,\n      index,\n    ) in canonical_index_by_latex.items()\n  }\n\n  result = []\n\n  for index, line in enumerate(\n    lines\n  ):\n    latex = exactness_by_index.get(\n      index\n    )\n\n    if latex is None:\n      result.append(\n        line\n      )\n      continue\n\n    owner_index = next(\n      (\n        canonical_index\n        for (\n          canonical_index,\n          canonical_latex,\n        ) in canonical_latex_by_index.items()\n        if latex in canonical_latex\n      ),\n      None,\n    )\n\n    if owner_index is None:\n      result.append(\n        line\n      )\n      continue\n\n    if index != owner_index:\n      continue\n\n    result.append(\n      "$"\n      + canonical_latex_by_index[\n        owner_index\n      ]\n      + "$ は完全である."\n    )\n\n  return result\n'
CALL_ANCHOR = '  punctuated_lines = []\n\n  for line in lines:\n'
CALL_REPLACEMENT = '  lines = (\n    _phase159_consolidate_public_exactness_lines(\n      lines\n    )\n  )\n\n  punctuated_lines = []\n\n  for line in lines:\n'

def main() -> None:
  if not RENDERER.exists():
    raise FileNotFoundError(RENDERER)

  stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  backup_dir = ROOT / ("phase159_r1_4_repair1_backup_" + stamp)
  backup_dir.mkdir(parents=True, exist_ok=False)
  shutil.copy2(RENDERER, backup_dir / RENDERER.name)

  source = RENDERER.read_text(encoding="utf-8-sig")

  helper_anchor = "def _phase159_project_generic_semantics_to_public_proof("
  helper_index = source.find(helper_anchor)
  if helper_index < 0:
    raise RuntimeError("Phase 159 projection function not found")

  if "def _phase159_consolidate_public_exactness_lines(" not in source:
    source = (
      source[:helper_index]
      + HELPERS
      + "\n\n"
      + source[helper_index:]
    )

  count = source.count(CALL_ANCHOR)
  if count != 1:
    raise RuntimeError(
      "expected exactly one punctuation anchor, found "
      + str(count)
    )

  source = source.replace(
    CALL_ANCHOR,
    CALL_REPLACEMENT,
    1,
  )

  RENDERER.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print("Phase 159-R1-4 repair1 applied.")
  print("Backup:", backup_dir)
  print("Added generic public exactness-component collapse.")

if __name__ == "__main__":
  main()
