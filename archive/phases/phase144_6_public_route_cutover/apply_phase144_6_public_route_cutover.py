from pathlib import Path

ROOT = Path.cwd()
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"

text = RENDERER.read_text(encoding="utf-8-sig")

old_import = """from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
"""
new_import = """from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
"""

if new_import not in text:
  if old_import not in text:
    raise RuntimeError(
      "current narrative multi-renderer import block not found"
    )
  text = text.replace(
    old_import,
    new_import,
    1,
  )

old_call = """    return (
      render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
      )
    )

  if _is_phase134_9_pi8_5_presentation(
"""
new_call = """    return (
      render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
      )
    )

  if _is_phase134_9_pi8_5_presentation(
"""

if new_call not in text:
  if old_call not in text:
    raise RuntimeError(
      "current pi_6^3 public generic route not found"
    )
  text = text.replace(
    old_call,
    new_call,
    1,
  )

RENDERER.write_text(
  text,
  encoding="utf-8",
)

print("Phase 144-6 Public Route Cutover applied.")
print("Modified: toda_group_proof_narrative_renderer.py")
print(
  "Added: tests/"
  "test_phase144_6_public_route_cutover.py"
)
