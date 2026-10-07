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


stable_group_transport = (
  repo_root
  / "toda_stable_group_transport.py"
)
stable_group_text = (
  stable_group_transport.read_text(
    encoding="utf-8",
  )
)

if (
  "TodaPrimaryGroupZeroStatement,"
  not in stable_group_text
):
  replace_once(
    stable_group_transport,
    """from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
""",
    """from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
""",
    "stable group transport import",
  )

stable_group_text = (
  stable_group_transport.read_text(
    encoding="utf-8",
  )
)

if (
  "def toda_45_generic_zero_group_transport_inference_rule("
  not in stable_group_text
):
  stable_group_transport.write_text(
    stable_group_text.rstrip()
    + "\n\n\n"
    + (
      package_root
      / "files"
      / "generic_zero_transport.py"
    ).read_text(
      encoding="utf-8",
    ).rstrip()
    + "\n",
    encoding="utf-8",
  )


normalization = (
  repo_root
  / "toda_stable_generator_normalization.py"
)

replace_once(
  normalization,
  """from expression import (
  IteratedSuspension,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
""",
  """from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
""",
  "generator normalization expression import",
)

normalization_text = (
  normalization.read_text(
    encoding="utf-8",
  )
)

if (
  "ScalarGreaterEqualStatement,"
  not in normalization_text
):
  insert_before = (
    "from toda_rules import (\n"
  )
  if insert_before not in normalization_text:
    raise SystemExit(
      "normalization scalar import anchor not found"
    )

  normalization_text = (
    normalization_text.replace(
      insert_before,
      """from scalar_rules import (
  ScalarGreaterEqualStatement,
)
"""
      + insert_before,
      1,
    )
  )
  normalization.write_text(
    normalization_text,
    encoding="utf-8",
  )

normalization_text = (
  normalization.read_text(
    encoding="utf-8",
  )
)

if (
  "def toda_nu_squared_transport_generator_normalization_inference_rule("
  not in normalization_text
):
  normalization.write_text(
    normalization_text.rstrip()
    + "\n\n\n"
    + (
      package_root
      / "files"
      / "nu_squared_normalization.py"
    ).read_text(
      encoding="utf-8",
    ).rstrip()
    + "\n",
    encoding="utf-8",
  )


phase65 = (
  repo_root
  / "toda_phase65_bootstrap.py"
)

phase65_text = phase65.read_text(
  encoding="utf-8",
)

if (
  "from toda_stable_group_transport import ("
  not in phase65_text
):
  replace_once(
    phase65,
    """from toda_rules import (
""",
    """from toda_stable_group_transport import (
  toda_45_generic_finite_cyclic_transport_inference_rule,
)
from toda_rules import (
""",
    "phase65 generic transport import",
  )

phase65_text = phase65.read_text(
  encoding="utf-8",
)

phase65_text = phase65_text.replace(
  "  toda_prop56_nu5_stable_transport_inference_rule,\n",
  "",
  1,
)

old_phase65_call = (
  "        toda_prop56_nu5_stable_transport_inference_rule(),\n"
)
if old_phase65_call not in phase65_text:
  raise SystemExit(
    "phase65 specialized transport call not found"
  )

phase65_text = phase65_text.replace(
  old_phase65_call,
  (
    "        "
    "toda_45_generic_finite_cyclic_transport_inference_rule(),\n"
  ),
  1,
)

phase65.write_text(
  phase65_text,
  encoding="utf-8",
)


prop58 = (
  repo_root
  / "toda_prop58_zero_bootstrap.py"
)
prop58_text = prop58.read_text(
  encoding="utf-8",
)

if (
  "from toda_stable_group_transport import ("
  not in prop58_text
):
  replace_once(
    prop58,
    """from toda_rules import (
""",
    """from toda_stable_group_transport import (
  toda_45_generic_zero_group_transport_inference_rule,
)
from toda_rules import (
""",
    "prop58 generic zero import",
  )

prop58_text = prop58.read_text(
  encoding="utf-8",
)
prop58_text = prop58_text.replace(
  "  toda_prop58_higher_four_stem_zero_transport_inference_rule,\n",
  "",
  1,
)
prop58_text = prop58_text.replace(
  "      toda_prop58_higher_four_stem_zero_transport_inference_rule(),\n",
  "      toda_45_generic_zero_group_transport_inference_rule(),\n",
  1,
)
prop58.write_text(
  prop58_text,
  encoding="utf-8",
)


prop511 = (
  repo_root
  / "toda_prop511_zero_bootstrap.py"
)
prop511_text = prop511.read_text(
  encoding="utf-8",
)

if (
  "  run_inference_until_stable_with_history,\n"
  not in prop511_text
):
  proof_import_old = """from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
"""
  proof_import_new = """from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
  run_inference_until_stable_with_history,
)
"""
  if proof_import_old not in prop511_text:
    raise SystemExit(
      "prop511 proof import block not found"
    )
  prop511_text = prop511_text.replace(
    proof_import_old,
    proof_import_new,
    1,
  )
  prop511.write_text(
    prop511_text,
    encoding="utf-8",
  )
  prop511_text = prop511.read_text(
    encoding="utf-8",
  )

if (
  "from toda_stable_group_transport import ("
  not in prop511_text
):
  replace_once(
    prop511,
    """from toda_rules import (
""",
    """from toda_stable_generator_normalization import (
  toda_nu_squared_transport_generator_normalization_inference_rule,
)
from toda_stable_group_transport import (
  toda_45_generic_finite_cyclic_transport_inference_rule,
  toda_45_generic_zero_group_transport_inference_rule,
)
from toda_rules import (
""",
    "prop511 stable generic imports",
  )

prop511_text = prop511.read_text(
  encoding="utf-8",
)
prop511_text = prop511_text.replace(
  "  toda_prop59_higher_five_stem_zero_transport_inference_rule,\n",
  "",
  1,
)
prop511_text = prop511_text.replace(
  "  toda_prop511_higher_six_stem_nu_squared_transport_inference_rule,\n",
  "",
  1,
)
prop511_text = prop511_text.replace(
  "    toda_prop59_higher_five_stem_zero_transport_inference_rule(),\n",
  "    toda_45_generic_zero_group_transport_inference_rule(),\n",
  1,
)
prop511.write_text(
  prop511_text,
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


renderer_path = (
  repo_root
  / "toda_group_proof_narrative_renderer.py"
)

replace_function(
  renderer_path,
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


print("Applied Phase 160-R10:")
print("  toda_stable_group_transport.py")
print("  toda_stable_generator_normalization.py")
print("  toda_phase65_bootstrap.py")
print("  toda_prop58_zero_bootstrap.py")
print("  toda_prop511_zero_bootstrap.py")
print("  toda_group_proof_narrative_renderer.py")
print("  tests/test_phase160_remaining_stable_production.py")
print("  tests/test_phase160_remaining_stable_public_narrative.py")
