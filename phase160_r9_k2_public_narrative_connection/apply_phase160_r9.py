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

function_name = (
    "_phase160_r7_render_stable_finite_cyclic_transport_narrative"
)
marker = (
    "def "
    + function_name
    + "("
)

start = text.find(
    marker
)

if start < 0:
    raise SystemExit(
        "Phase 160-R7 stable public Narrative helper "
        "was not found. Apply Phase 160-R7 first."
    )

next_def = text.find(
    "\ndef ",
    start + len(
        marker
    ),
)

if next_def < 0:
    raise SystemExit(
        "could not locate the function boundary after "
        + function_name
    )

new_function = (
    package_root
    / "files"
    / "phase160_r9_stable_public_helper.py"
).read_text(
    encoding="utf-8"
).rstrip()

updated = (
    text[
      :start
    ]
    + new_function
    + "\n\n"
    + text[
      next_def + 1:
    ]
)

renderer.write_text(
    updated,
    encoding="utf-8",
)

test_source = (
    package_root
    / "files"
    / "tests"
    / "test_phase160_k2_public_narrative.py"
)
test_target = (
    repo_root
    / "tests"
    / "test_phase160_k2_public_narrative.py"
)

shutil.copy2(
    test_source,
    test_target,
)

print("Applied Phase 160-R9:")
print("  toda_group_proof_narrative_renderer.py")
print("  tests/test_phase160_k2_public_narrative.py")
