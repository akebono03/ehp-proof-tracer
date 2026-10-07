from pathlib import Path
import shutil

package_root = Path(__file__).resolve().parent
repo_root = package_root.parent

bootstrap = (
    repo_root
    / "toda_prop515_upper_bootstrap.py"
)

if not bootstrap.exists():
    raise SystemExit(
        "toda_prop515_upper_bootstrap.py was not found"
    )

required = (
    repo_root / "toda_stable_group_transport.py"
)
if not required.exists():
    raise SystemExit(
        "Phase 160-R4 is required before R6"
    )

normalizer_source = (
    package_root
    / "files"
    / "toda_stable_generator_normalization.py"
)
normalizer_target = (
    repo_root
    / "toda_stable_generator_normalization.py"
)
shutil.copy2(
    normalizer_source,
    normalizer_target,
)

text = bootstrap.read_text(
    encoding="utf-8"
)

old_rule_import = """  toda_45_isomorphism_inference_rule,
  toda_45_sigma9_finite_cyclic_transport_inference_rule,
  toda_48_pi16_9_order_and_e4_injective_inference_rule,
"""

new_rule_import = """  toda_45_isomorphism_inference_rule,
  toda_48_pi16_9_order_and_e4_injective_inference_rule,
"""

if old_rule_import not in text:
    raise SystemExit(
        "expected sigma transport import block was not found"
    )

text = text.replace(
    old_rule_import,
    new_rule_import,
    1,
)

anchor = """from toda_prop515_sigma_chain_bootstrap import (
  TodaProp515SigmaChainBootstrapResult,
  build_toda_prop515_sigma_chain_bootstrap,
)
"""

replacement = """from toda_prop515_sigma_chain_bootstrap import (
  TodaProp515SigmaChainBootstrapResult,
  build_toda_prop515_sigma_chain_bootstrap,
)
from toda_stable_generator_normalization import (
  toda_sigma_transport_generator_normalization_inference_rule,
)
from toda_stable_group_transport import (
  toda_45_generic_finite_cyclic_transport_inference_rule,
)
"""

if anchor not in text:
    raise SystemExit(
        "expected Phase 160 import insertion anchor "
        "was not found"
    )

text = text.replace(
    anchor,
    replacement,
    1,
)

old_stable_run = """  stable_result = (
    run_inference_until_stable_with_history(
      (
        toda_45_isomorphism_inference_rule(),
        toda_45_sigma9_finite_cyclic_transport_inference_rule(),
      ),
      (
        pi16_9_step,
        sigma_family_step,
        stable_range_step,
        higher_range_step,
        stable_suspension_map_step,
      ),
    )
  )
"""

new_stable_run = """  stable_result = (
    run_inference_until_stable_with_history(
      (
        toda_45_isomorphism_inference_rule(),
        toda_45_generic_finite_cyclic_transport_inference_rule(),
        toda_sigma_transport_generator_normalization_inference_rule(),
      ),
      (
        pi16_9_step,
        sigma_family_step,
        sigma9_definition_step,
        stable_range_step,
        higher_range_step,
        stable_suspension_map_step,
      ),
    )
  )
"""

if old_stable_run not in text:
    raise SystemExit(
        "expected stable sigma production block "
        "was not found"
    )

text = text.replace(
    old_stable_run,
    new_stable_run,
    1,
)

bootstrap.write_text(
    text,
    encoding="utf-8",
)

test_source = (
    package_root
    / "files"
    / "tests"
    / "test_phase160_k7_generic_transport_connection.py"
)
test_target = (
    repo_root
    / "tests"
    / "test_phase160_k7_generic_transport_connection.py"
)
shutil.copy2(
    test_source,
    test_target,
)

print("Applied Phase 160-R6 files:")
print("  toda_stable_generator_normalization.py")
print("  toda_prop515_upper_bootstrap.py")
print("  tests/test_phase160_k7_generic_transport_connection.py")
