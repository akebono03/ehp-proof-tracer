from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
PAYLOAD = Path(__file__).resolve().parent / "payload"

def copy_file(relative_path):
  source = PAYLOAD / relative_path
  destination = ROOT / relative_path
  destination.parent.mkdir(parents=True, exist_ok=True)
  shutil.copyfile(source, destination)
  print("Wrote:", relative_path)

def patch_contribution_renderer():
  path = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
  source = path.read_text(encoding="utf-8")
  anchor = """from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
"""
  replacement = """from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_reason_renderer import (
  insert_toda_group_proof_narrative_reason_prose,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
)
"""
  if anchor not in source:
    raise RuntimeError("Expected import anchor not found.")
  source = source.replace(anchor, replacement, 1)
  old_function = 'def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n  presentation: TodaGroupProofPresentation,\n  blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,\n  arguments: tuple[\n    TodaGroupProofNarrativeArgument,\n    ...,\n  ],\n) -> str:\n  base_markdown = (\n    render_toda_group_proof_narrative_multi_argument_markdown(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n  proof_chains = (\n    build_toda_group_proof_narrative_proof_chains(\n      presentation,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n  ordered_contributions = (\n    build_toda_group_proof_narrative_ordered_contributions(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n      proof_chains,\n      current_markdown=base_markdown,\n    )\n  )\n\n  return _insert_toda_group_proof_narrative_argument_contributions(\n    presentation,\n    base_markdown,\n    blocks,\n    arguments,\n    ordered_contributions,\n  )\n'
  new_function = 'def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n  presentation: TodaGroupProofPresentation,\n  blocks: tuple[\n    TodaGroupProofNarrativeBlock,\n    ...,\n  ],\n  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,\n  arguments: tuple[\n    TodaGroupProofNarrativeArgument,\n    ...,\n  ],\n) -> str:\n  base_markdown = (\n    render_toda_group_proof_narrative_multi_argument_markdown(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n  proof_chains = (\n    build_toda_group_proof_narrative_proof_chains(\n      presentation,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n  ordered_contributions = (\n    build_toda_group_proof_narrative_ordered_contributions(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n      proof_chains,\n      current_markdown=base_markdown,\n    )\n  )\n  contribution_markdown = (\n    _insert_toda_group_proof_narrative_argument_contributions(\n      presentation,\n      base_markdown,\n      blocks,\n      arguments,\n      ordered_contributions,\n    )\n  )\n  reason_sidecar = (\n    build_toda_group_proof_narrative_reason_sidecar(\n      presentation,\n      semantic_sidecar,\n    )\n  )\n\n  return insert_toda_group_proof_narrative_reason_prose(\n    contribution_markdown,\n    reason_sidecar,\n  )\n'
  if old_function not in source:
    raise RuntimeError("Expected render function not found.")
  source = source.replace(old_function, new_function, 1)
  path.write_text(source, encoding="utf-8")
  print("Patched: toda_group_proof_narrative_contribution_renderer.py")

def main():
  copy_file(Path("toda_group_proof_narrative_reason_renderer.py"))
  copy_file(Path("tests") / "test_phase150_rc4_5_visible_reasons.py")
  patch_contribution_renderer()
  print("RC4-5 visible reason integration applied.")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
