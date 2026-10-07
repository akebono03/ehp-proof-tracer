from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
TEST = ROOT / "tests" / "test_phase159_r1_2_pi3_2_narrative_repair.py"

HELPERS = 'def _phase159_public_formula_map_property_line(\n  proof_step: ProofStep,\n) -> str | None:\n  statement = proof_step.conclusion\n\n  if isinstance(\n    statement,\n    _GENERIC_INJECTIVE_STATEMENT_TYPES,\n  ):\n    property_label = "単射"\n  elif isinstance(\n    statement,\n    _GENERIC_SURJECTIVE_STATEMENT_TYPES,\n  ):\n    property_label = "全射"\n  elif isinstance(\n    statement,\n    _GENERIC_ISOMORPHISM_STATEMENT_TYPES,\n  ):\n    property_label = "同型"\n  elif isinstance(\n    statement,\n    _GENERIC_ZERO_MAP_STATEMENT_TYPES,\n  ):\n    property_label = "零写像"\n  else:\n    return None\n\n  group_map = getattr(\n    statement,\n    "map",\n    None,\n  )\n\n  if group_map is None:\n    return None\n\n  map_latex = (\n    _render_generic_narrative_group_map_latex(\n      group_map\n    )\n  )\n\n  if map_latex is None:\n    return None\n\n  return (\n    "$"\n    + map_latex\n    + "$ は"\n    + property_label\n    + "."\n  )\n\n\ndef _phase159_normalize_public_map_property_wording(\n  presentation: TodaGroupProofPresentation,\n  rendered: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  proof_marker = "## 証明\\n\\n"\n  proof_index = rendered.find(\n    proof_marker\n  )\n\n  if proof_index < 0:\n    return rendered\n\n  body_start = (\n    proof_index\n    + len(\n      proof_marker\n    )\n  )\n  prefix = rendered[\n    :body_start\n  ]\n  proof_body = rendered[\n    body_start:\n  ]\n\n  semantic_presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      presentation\n    )\n  )\n\n  for node in semantic_presentation.nodes:\n    proof_step = node.proof_step\n    original = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n    replacement = (\n      _phase159_public_formula_map_property_line(\n        proof_step\n      )\n    )\n\n    if replacement is None:\n      continue\n\n    proof_body = proof_body.replace(\n      original,\n      replacement,\n    )\n\n  return (\n    prefix\n    + proof_body\n  )\n'
NEW_RENDER = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  rendered = (\n    _phase158_baseline_render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n  rendered = (\n    _phase158_normalize_public_narrative_contract(\n      presentation,\n      rendered,\n    )\n  )\n\n  return (\n    _phase159_normalize_public_map_property_wording(\n      presentation,\n      rendered,\n    )\n  )\n'
TEST_FUNCTION = 'def test_phase159_r1_5_pi3_2_public_map_property_wording_is_terse():\n  presentation = _phase159_r1_2_pi3_2_presentation()\n  rendered = render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n  assert (\n    r"$E: \\pi_{1}^{1} \\to \\pi_{2}^{2}$ は単射."\n    in rendered\n  )\n  assert (\n    r"$\\Delta: \\pi_{3}^{3} \\to \\pi_{1}^{1}$ "\n    "は零写像."\n    in rendered\n  )\n\n  assert "は単射である." not in rendered\n  assert "は全射である." not in rendered\n  assert "は同型写像である." not in rendered\n  assert "は零写像である." not in rendered\n'

def ensure_import_name(source, module_name, import_name):
  start_marker = (
    "from "
    + module_name
    + " import (\n"
  )
  start = source.find(start_marker)
  if start < 0:
    raise RuntimeError(
      "import block not found: "
      + module_name
    )

  end = source.find(
    ")\n",
    start,
  )
  if end < 0:
    raise RuntimeError(
      "import block end not found: "
      + module_name
    )

  block = source[start:end + 2]
  line = (
    "  "
    + import_name
    + ",\n"
  )

  if line in block:
    return source

  updated = (
    block[:-2]
    + line
    + ")\n"
  )

  return (
    source[:start]
    + updated
    + source[end + 2:]
  )

def replace_function(
  source,
  function_name,
  replacement,
):
  marker = (
    "def "
    + function_name
    + "("
  )
  start = source.find(marker)

  if start < 0:
    raise RuntimeError(
      "function not found: "
      + function_name
    )

  next_function = source.find(
    "\ndef ",
    start + len(marker),
  )
  end = (
    len(source)
    if next_function < 0
    else next_function + 1
  )

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n"
    + source[end:]
  )

def main():
  if not RENDERER.exists():
    raise FileNotFoundError(RENDERER)
  if not TEST.exists():
    raise FileNotFoundError(TEST)

  stamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase159_r1_5_backup_"
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
  shutil.copy2(
    TEST,
    backup_dir / TEST.name,
  )

  source = RENDERER.read_text(
    encoding="utf-8-sig"
  )

  source = ensure_import_name(
    source,
    "toda_group_proof_generic_narrative_renderer",
    "_GENERIC_ZERO_MAP_STATEMENT_TYPES",
  )

  helper_anchor = (
    "def render_toda_group_proof_narrative_markdown("
  )
  helper_index = source.find(
    helper_anchor
  )
  if helper_index < 0:
    raise RuntimeError(
      "public render function not found"
    )

  if (
    "def _phase159_normalize_public_map_property_wording("
    not in source
  ):
    source = (
      source[:helper_index]
      + HELPERS.rstrip()
      + "\n\n\n"
      + source[helper_index:]
    )

  source = replace_function(
    source,
    "render_toda_group_proof_narrative_markdown",
    NEW_RENDER,
  )

  tests = TEST.read_text(
    encoding="utf-8-sig"
  )

  if (
    "def test_phase159_r1_5_pi3_2_public_map_property_wording_is_terse("
    not in tests
  ):
    tests = (
      tests.rstrip()
      + "\n\n\n"
      + TEST_FUNCTION.rstrip()
      + "\n"
    )

  RENDERER.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )
  TEST.write_text(
    tests,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159-R1-5 applied."
  )
  print(
    "Backup:",
    backup_dir,
  )
  print(
    "Public map-property wording only."
  )

if __name__ == "__main__":
  main()
