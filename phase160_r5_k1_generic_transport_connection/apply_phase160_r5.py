from pathlib import Path

package_root = Path(__file__).resolve().parent
repo_root = package_root.parent
target = repo_root / "toda_prop56_zero_bootstrap.py"

if not target.exists():
    raise SystemExit(
        "toda_prop56_zero_bootstrap.py was not found"
    )

text = target.read_text(
    encoding="utf-8"
)

old_import = """  toda_36_lemma54_specialization_inference_rule,
  toda_45_pi4_3_finite_cyclic_transport_inference_rule,
  toda_53_eta3_twice_zero_inference_rule,
"""

new_import = """  toda_36_lemma54_specialization_inference_rule,
  toda_53_eta3_twice_zero_inference_rule,
"""

if old_import not in text:
    raise SystemExit(
        "expected toda_rules import block was not found"
    )

text = text.replace(
    old_import,
    new_import,
    1,
)

anchor = """from toda_phase65_bootstrap import (
  build_toda_prop56_bootstrap_step,
)
"""

new_module_import = """from toda_phase65_bootstrap import (
  build_toda_prop56_bootstrap_step,
)
from toda_stable_group_transport import (
  toda_45_generic_finite_cyclic_transport_inference_rule,
)
"""

if anchor not in text:
    raise SystemExit(
        "expected stable transport import insertion anchor "
        "was not found"
    )

text = text.replace(
    anchor,
    new_module_import,
    1,
)

old_call = (
    "toda_45_pi4_3_finite_cyclic_transport_inference_rule()"
)
new_call = (
    "toda_45_generic_finite_cyclic_transport_inference_rule()"
)

count = text.count(
    old_call
)

if count != 1:
    raise SystemExit(
        "expected exactly one pi4_3 transport rule call, "
        f"found {count}"
    )

text = text.replace(
    old_call,
    new_call,
    1,
)

target.write_text(
    text,
    encoding="utf-8",
)

test_source = (
    package_root
    / "files"
    / "tests"
    / "test_phase160_k1_generic_transport_connection.py"
)
test_target = (
    repo_root
    / "tests"
    / "test_phase160_k1_generic_transport_connection.py"
)
test_target.write_text(
    test_source.read_text(
        encoding="utf-8"
    ),
    encoding="utf-8",
)

print("Applied Phase 160-R5 files:")
print("  toda_prop56_zero_bootstrap.py")
print("  tests/test_phase160_k1_generic_transport_connection.py")
