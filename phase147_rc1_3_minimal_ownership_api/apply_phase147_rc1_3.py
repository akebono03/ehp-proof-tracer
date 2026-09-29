from pathlib import Path
import shutil

ROOT = Path.cwd()
BUNDLE = Path(__file__).resolve().parent

selection_target = ROOT / "toda_group_proof_narrative_exactness_selection.py"
multi_target = ROOT / "toda_group_proof_narrative_argument_multi_renderer.py"
test_target = ROOT / "tests" / "test_phase147_rc1_argument_method_ownership.py"

if not selection_target.exists() or not multi_target.exists():
    raise SystemExit(
        "Run this script from the ehp-proof-tracer repository root."
    )

shutil.copy2(
    BUNDLE / "toda_group_proof_narrative_exactness_selection.py",
    selection_target,
)
test_target.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(
    BUNDLE / "tests" / "test_phase147_rc1_argument_method_ownership.py",
    test_target,
)

source = multi_target.read_text(encoding="utf-8")

old_components_import = """from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
"""
if old_components_import not in source:
    raise SystemExit(
        "Expected exactness-components import not found in multi renderer."
    )
source = source.replace(
    old_components_import,
    "",
    1,
)

old_selection_import = """from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_primary_exactness_component,
)
"""
new_selection_import = """from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_argument_primary_exactness_component,
)
"""
if old_selection_import not in source:
    raise SystemExit(
        "Expected exactness-selection import not found in multi renderer."
    )
source = source.replace(
    old_selection_import,
    new_selection_import,
    1,
)

old_relevant_import = """from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
"""
if old_relevant_import not in source:
    raise SystemExit(
        "Expected relevant-groups import not found in multi renderer."
    )
source = source.replace(
    old_relevant_import,
    "",
    1,
)

old_pipeline = """    relevant_groups = (
      extract_toda_group_proof_narrative_argument_relevant_groups(
        presentation,
        blocks,
        argument,
      )
    )
    evidence = (
      extract_toda_group_proof_narrative_argument_method_evidence(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )
    components = (
      build_toda_group_proof_narrative_exactness_method_components(
        evidence
      )
    )
    primary_component = (
      select_toda_group_proof_narrative_primary_exactness_component(
        relevant_groups,
        components,
      )
    )
"""
new_pipeline = """    evidence = (
      extract_toda_group_proof_narrative_argument_method_evidence(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )
    primary_component = (
      select_toda_group_proof_narrative_argument_primary_exactness_component(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )
"""
if old_pipeline not in source:
    raise SystemExit(
        "Expected primary-selection pipeline not found in multi renderer."
    )
source = source.replace(
    old_pipeline,
    new_pipeline,
    1,
)

multi_target.write_text(source, encoding="utf-8")
print("Phase 147 RC1-3 production/test changes applied.")
print("Changed:")
print("  toda_group_proof_narrative_exactness_selection.py")
print("  toda_group_proof_narrative_argument_multi_renderer.py")
print("  tests/test_phase147_rc1_argument_method_ownership.py")
