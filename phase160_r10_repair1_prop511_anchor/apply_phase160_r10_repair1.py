from pathlib import Path
import shutil


package_root = Path(__file__).resolve().parent
repo_root = package_root.parent


def replace_once(
  path: Path,
  old: str,
  new: str,
  description: str,
) -> None:
  text = path.read_text(
    encoding="utf-8",
  )

  count = text.count(
    old
  )

  if count != 1:
    raise SystemExit(
      description
      + ": expected exactly one match in "
      + str(
        path
      )
      + ", found "
      + str(
        count
      )
    )

  path.write_text(
    text.replace(
      old,
      new,
      1,
    ),
    encoding="utf-8",
  )


def replace_function(
  path: Path,
  function_name: str,
  replacement_path: Path,
) -> None:
  text = path.read_text(
    encoding="utf-8",
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
      "function not found: "
      + function_name
      + " in "
      + str(
        path
      )
    )

  next_def = text.find(
    "\ndef ",
    start + len(
      marker
    ),
  )

  if next_def < 0:
    end = len(
      text
    )
  else:
    end = (
      next_def
      + 1
    )

  replacement = (
    replacement_path.read_text(
      encoding="utf-8",
    ).rstrip()
    + "\n\n"
  )

  path.write_text(
    (
      text[
        :start
      ]
      + replacement
      + text[
        end:
      ]
    ),
    encoding="utf-8",
  )


def require_marker(
  path: Path,
  marker: str,
  description: str,
) -> None:
  text = path.read_text(
    encoding="utf-8",
  )

  if marker not in text:
    raise SystemExit(
      "Phase 160-R10 prerequisite missing: "
      + description
      + " in "
      + str(
        path
      )
    )


# The first R10 apply stopped only after these four changes.
# Verify them instead of applying them again.
require_marker(
  repo_root / "toda_stable_group_transport.py",
  "def toda_45_generic_zero_group_transport_inference_rule(",
  "generic zero-group transport",
)
require_marker(
  repo_root / "toda_stable_generator_normalization.py",
  "def toda_nu_squared_transport_generator_normalization_inference_rule(",
  "nu-squared normalization",
)
require_marker(
  repo_root / "toda_phase65_bootstrap.py",
  "toda_45_generic_finite_cyclic_transport_inference_rule(),",
  "3-stem generic finite-cyclic production connection",
)
require_marker(
  repo_root / "toda_prop58_zero_bootstrap.py",
  "toda_45_generic_zero_group_transport_inference_rule(),",
  "4-stem generic zero-group production connection",
)


prop511 = (
  repo_root
  / "toda_prop511_zero_bootstrap.py"
)

text = prop511.read_text(
  encoding="utf-8",
)

# Add run_inference_until_stable_with_history to the complete top-level proof import.
old_proof_import = """from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
"""
new_proof_import = """from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
  run_inference_until_stable_with_history,
)
"""

if old_proof_import in text:
  text = text.replace(
    old_proof_import,
    new_proof_import,
    1,
  )
elif new_proof_import not in text:
  raise SystemExit(
    "prop511 proof import does not match the expected current form"
  )

# Insert stable imports using a unique top-level anchor.
stable_import = """from toda_stable_generator_normalization import (
  toda_nu_squared_transport_generator_normalization_inference_rule,
)
from toda_stable_group_transport import (
  toda_45_generic_finite_cyclic_transport_inference_rule,
  toda_45_generic_zero_group_transport_inference_rule,
)
"""

if stable_import not in text:
  anchor = """from toda_prop58_zero_bootstrap import (
  _build_delta_eta9_step,
  _build_equation57_steps,
  _build_eta2_nu_prime_zero_step,
  _build_higher_eta_nu_zero_step,
  _build_nu6_eta9_zero_step,
  _build_phase66_step,
  _build_pi6_2_step,
  _build_pi7_3_steps,
  _build_pi8_4_step,
  _build_pi9_5_step,
  _build_support,
  _build_toda59_step,
  build_toda_prop58_zero_argument_step,
)
from toda_rules import (
"""

  replacement = """from toda_prop58_zero_bootstrap import (
  _build_delta_eta9_step,
  _build_equation57_steps,
  _build_eta2_nu_prime_zero_step,
  _build_higher_eta_nu_zero_step,
  _build_nu6_eta9_zero_step,
  _build_phase66_step,
  _build_pi6_2_step,
  _build_pi7_3_steps,
  _build_pi8_4_step,
  _build_pi9_5_step,
  _build_support,
  _build_toda59_step,
  build_toda_prop58_zero_argument_step,
)
from toda_stable_generator_normalization import (
  toda_nu_squared_transport_generator_normalization_inference_rule,
)
from toda_stable_group_transport import (
  toda_45_generic_finite_cyclic_transport_inference_rule,
  toda_45_generic_zero_group_transport_inference_rule,
)
from toda_rules import (
"""

  if text.count(
    anchor
  ) != 1:
    raise SystemExit(
      "prop511 unique top-level stable import anchor "
      "was not found exactly once"
    )

  text = text.replace(
    anchor,
    replacement,
    1,
  )

# Remove only the two top-level specialized imports.
text = text.replace(
  "  toda_prop59_higher_five_stem_zero_transport_inference_rule,\n",
  "",
  1,
)
text = text.replace(
  "  toda_prop511_higher_six_stem_nu_squared_transport_inference_rule,\n",
  "",
  1,
)

# Replace only the 5-stem production call.
old_five_call = (
  "    toda_prop59_higher_five_stem_zero_transport_inference_rule(),\n"
)
new_five_call = (
  "    toda_45_generic_zero_group_transport_inference_rule(),\n"
)

if old_five_call in text:
  text = text.replace(
    old_five_call,
    new_five_call,
    1,
  )
elif new_five_call not in text:
  raise SystemExit(
    "prop511 five-stem production call was not found"
  )

prop511.write_text(
  text,
  encoding="utf-8",
)

replace_function(
  prop511,
  "_build_nu_squared_aggregate_step",
  (
    package_root
    / "files"
    / "nu_squared_aggregate_function.py"
  ),
)


renderer = (
  repo_root
  / "toda_group_proof_narrative_renderer.py"
)

replace_function(
  renderer,
  "_phase160_r7_render_stable_finite_cyclic_transport_narrative",
  (
    package_root
    / "files"
    / "phase160_r10_public_helper.py"
  ),
)


for test_name in (
  "test_phase160_remaining_stable_production.py",
  "test_phase160_remaining_stable_public_narrative.py",
):
  shutil.copy2(
    package_root
    / "files"
    / "tests"
    / test_name,
    repo_root
    / "tests"
    / test_name,
  )


print("Applied Phase 160-R10 repair1:")
print("  verified already-applied R10 prefix")
print("  toda_prop511_zero_bootstrap.py")
print("  toda_group_proof_narrative_renderer.py")
print("  tests/test_phase160_remaining_stable_production.py")
print("  tests/test_phase160_remaining_stable_public_narrative.py")
