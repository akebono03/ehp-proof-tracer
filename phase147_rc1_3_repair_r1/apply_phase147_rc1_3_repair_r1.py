from pathlib import Path

ROOT = Path.cwd()
selection_path = ROOT / "toda_group_proof_narrative_exactness_selection.py"
multi_path = ROOT / "toda_group_proof_narrative_argument_multi_renderer.py"
test_path = ROOT / "tests" / "test_phase147_rc1_argument_method_ownership.py"

for path in (selection_path, multi_path, test_path):
    if not path.exists():
        raise SystemExit(f"Required file not found: {path}")

selection = selection_path.read_text(encoding="utf-8")

old_function = """def select_toda_group_proof_narrative_argument_primary_exactness_component(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  argument_index: int,
) -> (
  TodaGroupProofNarrativeExactnessMethodComponent
  | None
):
  argument = arguments[
    argument_index
  ]

  relevant_groups = (
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

  return (
    select_toda_group_proof_narrative_primary_exactness_component(
      relevant_groups,
      components,
    )
  )
"""

new_function = """def select_toda_group_proof_narrative_argument_primary_exactness_component(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  argument_index: int,
) -> (
  TodaGroupProofNarrativeExactnessMethodComponent
  | None
):
  evidence = (
    extract_toda_group_proof_narrative_argument_method_evidence(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      argument_index,
    )
  )
  argument = arguments[
    argument_index
  ]
  relevant_groups = (
    extract_toda_group_proof_narrative_argument_relevant_groups(
      presentation,
      blocks,
      argument,
    )
  )
  components = (
    build_toda_group_proof_narrative_exactness_method_components(
      evidence
    )
  )

  return (
    select_toda_group_proof_narrative_primary_exactness_component(
      relevant_groups,
      components,
    )
  )
"""

if old_function not in selection:
    if new_function not in selection:
        raise SystemExit("RC1-3 ownership function shape was not recognized.")
else:
    selection = selection.replace(old_function, new_function, 1)

selection_path.write_text(selection, encoding="utf-8")

test_source = test_path.read_text(encoding="utf-8")
old_assert = "    assert actual is expected\n"
new_assert = "    assert actual == expected\n"
if old_assert in test_source:
    test_source = test_source.replace(old_assert, new_assert, 1)
elif new_assert not in test_source:
    raise SystemExit("RC1-3 equivalence assertion was not recognized.")
test_path.write_text(test_source, encoding="utf-8")

multi = multi_path.read_text(encoding="utf-8")

old_selection_import = """from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_primary_exactness_component,
)
"""
new_selection_import = """from toda_group_proof_narrative_exactness_selection import (
  select_toda_group_proof_narrative_argument_primary_exactness_component,
)
"""
if old_selection_import in multi:
    multi = multi.replace(old_selection_import, new_selection_import, 1)
elif new_selection_import not in multi:
    raise SystemExit("Exactness-selection import was not recognized.")

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
if old_pipeline in multi:
    multi = multi.replace(old_pipeline, new_pipeline, 1)
elif new_pipeline not in multi:
    raise SystemExit("Multi-renderer ownership pipeline was not recognized.")

unused_imports = (
"""from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
""",
"""from toda_group_proof_narrative_relevant_groups import (
  extract_toda_group_proof_narrative_argument_relevant_groups,
)
""",
)
for unused_import in unused_imports:
    if unused_import in multi:
        multi = multi.replace(unused_import, "", 1)

multi_path.write_text(multi, encoding="utf-8")

print("Phase 147 RC1-3 Repair R1 applied.")
print("Repaired:")
print("  ownership API validation order")
print("  equivalence test: identity -> value equality")
print("  multi-renderer ownership API integration")
