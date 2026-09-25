from pathlib import Path

path = Path("tests/test_phase143_10_fix1_compatibility.py")
text = path.read_text(encoding="utf-8")

text = text.replace(
"""from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
""",
"""from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
""",
1,
)

old = """def test_phase143_10_fix1_child_argument_indices_default_empty():
  block = TodaGroupProofNarrativeBlock(
    role=(
      TodaGroupProofNarrativeMathematicalBlockRole.TARGET
    ),
    steps=(),
  )

  argument = TodaGroupProofNarrativeArgument(
    role=(
      TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_GROUP_STRUCTURE
    ),
    supporting_blocks=(),
    conclusion_block=block,
  )

  assert argument.child_argument_indices == ()
"""

new = """def test_phase143_10_fix1_child_argument_indices_default_empty():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=3,
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    )
  )
  block = blocks[
    0
  ]

  argument = TodaGroupProofNarrativeArgument(
    role=(
      TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_GROUP_STRUCTURE
    ),
    supporting_blocks=(),
    conclusion_block=block,
  )

  assert argument.child_argument_indices == ()
"""

if old not in text:
    raise RuntimeError("Phase143-10 fix1 compatibility test not found.")

path.write_text(text.replace(old,new,1),encoding="utf-8")
print("Updated:", path)
