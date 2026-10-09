"""Targeted replacement of the active common-baseline method body prelude."""
from pathlib import Path
import shutil
import sys

root = Path.cwd()
source = Path(__file__).resolve().parent / "files"
renderer = root / "toda_group_proof_narrative_renderer.py"
text = renderer.read_text(encoding="utf-8")
func = "def _phase158_baseline_render_toda_group_proof_narrative_markdown("
start = text.find(func)
if start < 0 or text.find(func, start + 1) >= 0:
    raise RuntimeError("Expected one baseline renderer function")
end = text.find("\ndef ", start + len(func))
if end == -1:
    raise RuntimeError("Could not find function boundary")
body = text[start:end]
anchor = "  presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      presentation\n    )\n  )"
replacement = "  concrete = render_concrete_transport_proof_from_steps(presentation.root_step)\n  if concrete is not None:\n    return concrete\n\n" + anchor
if body.count(anchor) != 1:
    raise RuntimeError("Unexpected baseline renderer prelude; aborting without modifying files")
if "render_concrete_transport_proof_from_steps" in body:
    raise RuntimeError("Renderer already patched")
insert = "from toda_group_proof_narrative_concrete_transport import (\n  render_concrete_transport_proof_from_steps,\n)\n"
if insert not in text:
    text = insert + text
    start = text.find(func)
    end = text.find("\ndef ", start + len(func))
    body = text[start:end]
text = text[:start] + body.replace(anchor, replacement, 1) + text[end:]
backup = renderer.with_suffix(".phase162_r4_b3_pre_fix.bak")
if not backup.exists():
    shutil.copy2(renderer, backup)
for name in ("toda_group_proof_narrative_concrete_transport.py", "tests/test_phase162_r4_b3_common_renderer_fix.py"):
    dst = root / name
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source / name, dst)
renderer.write_text(text, encoding="utf-8")
print("Updated:", renderer.name)
print("Backup:", backup.name)
