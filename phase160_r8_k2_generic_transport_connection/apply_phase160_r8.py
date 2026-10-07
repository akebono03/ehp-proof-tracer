from pathlib import Path
import shutil

package_root = Path(__file__).resolve().parent
repo_root = package_root.parent

target = (
    repo_root
    / "toda_prop56_zero_bootstrap.py"
)

if not target.exists():
    raise SystemExit(
        "toda_prop56_zero_bootstrap.py was not found"
    )

text = target.read_text(
    encoding="utf-8"
)

specialized_import = (
    "  toda_prop53_eta4_squared_stable_transport_inference_rule,\n"
)

count = text.count(
    specialized_import
)

if count != 1:
    raise SystemExit(
        "expected exactly one specialized k=2 transport import, "
        f"found {count}"
    )

text = text.replace(
    specialized_import,
    "",
    1,
)

old_call = """  result = run_inference_until_stable_with_history(
    toda_prop53_eta4_squared_stable_transport_inference_rule(),
    (
      pi6_4_step,
      stable_step,
      higher_range_step,
    ),
  )
"""

new_call = """  result = run_inference_until_stable_with_history(
    toda_45_generic_finite_cyclic_transport_inference_rule(),
    (
      pi6_4_step,
      stable_step,
    ),
  )
"""

count = text.count(
    old_call
)

if count != 1:
    raise SystemExit(
        "expected exactly one specialized k=2 transport call, "
        f"found {count}"
    )

text = text.replace(
    old_call,
    new_call,
    1,
)

generic_import = """from toda_stable_group_transport import (
  toda_45_generic_finite_cyclic_transport_inference_rule,
)
"""

if generic_import not in text:
    anchor = """from toda_upstream_bootstrap import (
"""
    if anchor not in text:
        raise SystemExit(
            "could not locate import insertion anchor"
        )
    text = text.replace(
        anchor,
        generic_import
        + anchor,
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
    / "test_phase160_k2_generic_transport_connection.py"
)
test_target = (
    repo_root
    / "tests"
    / "test_phase160_k2_generic_transport_connection.py"
)

shutil.copy2(
    test_source,
    test_target,
)

print("Applied Phase 160-R8:")
print("  toda_prop56_zero_bootstrap.py")
print("  tests/test_phase160_k2_generic_transport_connection.py")
