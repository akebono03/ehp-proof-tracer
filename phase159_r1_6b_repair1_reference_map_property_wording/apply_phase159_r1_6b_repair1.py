from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"

HELPER = 'def _phase159_normalize_public_reference_map_property_wording(\n  rendered: str,\n) -> str:\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  reference_marker = (\n    "## 使用する結果\\n\\n"\n  )\n  proof_boundary = (\n    "\\n---\\n\\n## 証明"\n  )\n  reference_start = rendered.find(\n    reference_marker\n  )\n\n  if reference_start < 0:\n    return rendered\n\n  content_start = (\n    reference_start\n    + len(\n      reference_marker\n    )\n  )\n  boundary_index = rendered.find(\n    proof_boundary,\n    content_start,\n  )\n\n  if boundary_index < 0:\n    return rendered\n\n  reference_body = rendered[\n    content_start:\n    boundary_index\n  ]\n\n  pattern = re.compile(\n    r"^(?P<prefix>\\$.*\\$\\s+は)"\n    r"(?P<property>"\n    r"単射である"\n    r"|全射である"\n    r"|同型写像である"\n    r"|零写像である"\n    r")\\.$"\n  )\n\n  normalized_lines = []\n\n  replacement_by_property = {\n    "単射である": "単射",\n    "全射である": "全射",\n    "同型写像である": "同型",\n    "零写像である": "零写像",\n  }\n\n  for line in reference_body.splitlines():\n    match = pattern.match(\n      line.strip()\n    )\n\n    if match is None:\n      normalized_lines.append(\n        line\n      )\n      continue\n\n    leading = line[\n      :len(\n        line\n      )\n      - len(\n        line.lstrip()\n      )\n    ]\n\n    normalized_lines.append(\n      leading\n      + match.group(\n        "prefix"\n      )\n      + replacement_by_property[\n        match.group(\n          "property"\n        )\n      ]\n      + "."\n    )\n\n  normalized_reference = "\\n".join(\n    normalized_lines\n  )\n\n  return (\n    rendered[\n      :content_start\n    ]\n    + normalized_reference\n    + rendered[\n      boundary_index:\n    ]\n  )\n'
NEW_RENDER = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  rendered = (\n    _phase158_baseline_render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n  rendered = (\n    _phase158_normalize_public_narrative_contract(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_normalize_public_map_property_wording(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_normalize_public_reference_map_property_wording(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_number_public_map_property_statement(\n      rendered\n    )\n  )\n\n  return (\n    _phase159_inject_foundational_reference_section(\n      presentation,\n      rendered,\n    )\n  )\n'

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
  start = source.find(
    marker
  )

  if start < 0:
    raise RuntimeError(
      "function not found: "
      + function_name
    )

  next_function = source.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  end = (
    len(
      source
    )
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
    raise FileNotFoundError(
      RENDERER
    )

  stamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup_dir = (
    ROOT
    / (
      "phase159_r1_6b_repair1_backup_"
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

  anchor = (
    "def _phase159_number_public_map_property_statement("
  )
  anchor_index = source.find(
    anchor
  )

  if anchor_index < 0:
    raise RuntimeError(
      "R1-6b numbering helper not found"
    )

  if (
    "def _phase159_normalize_public_reference_map_property_wording("
    not in source
  ):
    source = (
      source[:anchor_index]
      + HELPER.rstrip()
      + "\n\n\n"
      + source[anchor_index:]
    )

  source = replace_function(
    source,
    "render_toda_group_proof_narrative_markdown",
    NEW_RENDER,
  )

  RENDERER.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase 159-R1-6b repair1 applied."
  )
  print(
    "Backup:",
    backup_dir,
  )
  print(
    "Production change: public Reference map-property wording only."
  )
  print(
    "Test changes: none."
  )

if __name__ == "__main__":
  main()
