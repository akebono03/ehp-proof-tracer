from pathlib import Path

path = Path.cwd() / "toda_group_proof_narrative_renderer.py"
text = path.read_text(encoding="utf-8-sig")

anchor = """from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
"""
imports = """from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
"""

if imports not in text:
  if anchor not in text:
    raise RuntimeError("presentation import anchor not found")
  text = text.replace(anchor, imports, 1)

old = """  if (
    _is_phase134_3_pi6_3_presentation(
      presentation
    )
  ):
    return (
      _render_phase134_3_pi6_3_narrative_markdown(
        presentation
      )
    )
"""
new = """  if (
    _is_phase134_3_pi6_3_presentation(
      presentation
    )
  ):
    semantic_sidecar = (
      build_toda_group_proof_narrative_semantic_sidecar(
        presentation
      )
    )
    blocks = (
      build_toda_group_proof_narrative_blocks(
        presentation,
        semantic_sidecar=semantic_sidecar,
      )
    )
    arguments = (
      build_toda_group_proof_narrative_arguments(
        presentation,
        blocks,
        semantic_sidecar=semantic_sidecar,
      )
    )

    return (
      render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
      )
    )
"""

if new not in text:
  if old not in text:
    raise RuntimeError("pi6 legacy production branch not found")
  text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("Phase 144-6 applied.")
print("Modified: toda_group_proof_narrative_renderer.py")
print("Added: tests/test_phase144_6_pi6_generic_production_route.py")
