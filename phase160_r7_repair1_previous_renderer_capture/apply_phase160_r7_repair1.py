from pathlib import Path

package_root = Path(__file__).resolve().parent
repo_root = package_root.parent
target = repo_root / "toda_group_proof_narrative_renderer.py"

if not target.exists():
    raise SystemExit(
        "toda_group_proof_narrative_renderer.py was not found"
    )

text = target.read_text(
    encoding="utf-8"
)

old = """# Phase160-R7 generic stable finite-cyclic public narrative
_phase160_r7_previous_public_narrative_renderer = (
  _phase159_repair3_previous_public_narrative_renderer
)
"""

new = """# Phase160-R7 generic stable finite-cyclic public narrative
_phase160_r7_previous_public_narrative_renderer = (
  render_toda_group_proof_narrative_markdown
)
"""

count = text.count(
    old
)

if count != 1:
    raise SystemExit(
        "expected exactly one Phase 160-R7 previous renderer "
        f"capture block, found {count}"
    )

text = text.replace(
    old,
    new,
    1,
)

target.write_text(
    text,
    encoding="utf-8",
)

print("Applied Phase 160-R7 repair1:")
print("  toda_group_proof_narrative_renderer.py")
print("  previous renderer is captured directly before R7 wrapper")
