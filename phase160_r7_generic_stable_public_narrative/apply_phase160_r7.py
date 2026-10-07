from pathlib import Path
import shutil

package_root = Path(__file__).resolve().parent
repo_root = package_root.parent

renderer = (
    repo_root
    / "toda_group_proof_narrative_renderer.py"
)

if not renderer.exists():
    raise SystemExit(
        "toda_group_proof_narrative_renderer.py was not found"
    )

text = renderer.read_text(
    encoding="utf-8"
)

marker = (
    "# Phase159 pi_(n+1)^n "
    "stable transport repair3 public wrapper"
)

start = text.find(
    marker
)

if start < 0:
    raise SystemExit(
        "Phase 159 stable transport wrapper marker "
        "was not found"
    )

new_tail = (
    package_root
    / "files"
    / "phase160_r7_renderer_tail.py"
).read_text(
    encoding="utf-8"
)

renderer.write_text(
    text[:start]
    + new_tail
    + "\n",
    encoding="utf-8",
)

test_source = (
    package_root
    / "files"
    / "tests"
    / "test_phase160_generic_stable_public_narrative.py"
)
test_target = (
    repo_root
    / "tests"
    / "test_phase160_generic_stable_public_narrative.py"
)

shutil.copy2(
    test_source,
    test_target,
)

print("Applied Phase 160-R7 files:")
print("  toda_group_proof_narrative_renderer.py")
print("  tests/test_phase160_generic_stable_public_narrative.py")
