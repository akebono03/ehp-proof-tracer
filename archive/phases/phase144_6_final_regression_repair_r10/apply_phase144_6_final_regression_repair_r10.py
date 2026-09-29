from pathlib import Path


ROOT = Path.cwd()
MULTI = ROOT / "toda_group_proof_narrative_argument_multi_renderer.py"

text = MULTI.read_text(encoding="utf-8-sig")

old_import = """from toda_group_proof_narrative_argument_body_renderer import (
  _toda_group_proof_narrative_exactness_contribution_key,
  render_toda_group_proof_narrative_argument_body_markdown,
)
"""
new_import = """from toda_group_proof_aggregate_statement_catalog import (
  is_toda_group_proof_aggregate_statement,
)
from toda_group_proof_narrative_argument_body_renderer import (
  _toda_group_proof_narrative_exactness_contribution_key,
  render_toda_group_proof_narrative_argument_body_markdown,
)
"""
if old_import not in text:
    raise RuntimeError("Expected import anchor was not found.")
text = text.replace(old_import, new_import, 1)

old_frontier = """    if (
      id(
        proof_step
      ) not in protected_step_ids
      and block.role
      not in (
        TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS,
        TodaGroupProofNarrativeMathematicalBlockRole
        .REFERENCE,
      )
    )
"""
new_frontier = """    if (
      id(
        proof_step
      ) not in protected_step_ids
      and not is_toda_group_proof_aggregate_statement(
        proof_step.conclusion
      )
      and block.role
      not in (
        TodaGroupProofNarrativeMathematicalBlockRole
        .EXACTNESS,
        TodaGroupProofNarrativeMathematicalBlockRole
        .REFERENCE,
      )
    )
"""
if old_frontier not in text:
    raise RuntimeError("Expected frontier-filter anchor was not found.")
text = text.replace(old_frontier, new_frontier, 1)

signature_anchor = """) -> str:
  ordered_arguments = (
"""
signature_replacement = """) -> str:
  if not arguments:
    return ""

  ordered_arguments = (
"""
if signature_anchor not in text:
    raise RuntimeError("Expected renderer entry anchor was not found.")
text = text.replace(signature_anchor, signature_replacement, 1)

old_local = """    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )

    context_hidden_step_ids = frozenset(
"""
new_local = """    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )
    local_body_block_ids = {
      id(
        block
      )
      for block in local_body_blocks
    }
    evidence_block_ids = {
      id(
        block
      )
      for block in evidence
    }
    local_body_blocks = tuple(
      block
      for block in blocks
      if (
        id(
          block
        ) in local_body_block_ids
        or id(
          block
        ) in evidence_block_ids
      )
    )

    context_hidden_step_ids = frozenset(
"""
if old_local not in text:
    raise RuntimeError("Expected local-body anchor was not found.")
text = text.replace(old_local, new_local, 1)

MULTI.write_text(text, encoding="utf-8")
print("Updated production renderer:", MULTI)

test17 = ROOT / "tests" / "test_phase143_17_argument_discourse.py"
t17 = test17.read_text(encoding="utf-8-sig")
old17 = """  assert roles == (
    TodaGroupProofNarrativeArgumentDiscourseRole.FIRST,
    TodaGroupProofNarrativeArgumentDiscourseRole.FINAL,
  )
"""
new17 = """  assert roles == (
    TodaGroupProofNarrativeArgumentDiscourseRole.FIRST,
    TodaGroupProofNarrativeArgumentDiscourseRole.MIDDLE,
    TodaGroupProofNarrativeArgumentDiscourseRole.FINAL,
  )
"""
if old17 not in t17:
    raise RuntimeError("Expected Phase 143-17 pi16_9 assertion was not found.")
test17.write_text(t17.replace(old17, new17, 1), encoding="utf-8")
print("Updated stale discourse test:", test17)

for relative in (
    "tests/test_phase143_46_multi_argument_narrative_assembler.py",
    "tests/test_phase143_47_multi_argument_shared_contribution_dedup.py",
):
    path = ROOT / relative
    content = path.read_text(encoding="utf-8-sig")
    old = '"まず、$\\\\sigma_{9}$ を定める."'
    new = '"次に、$\\\\sigma_{9}$ を定める."'
    if old not in content:
        raise RuntimeError(f"Expected sigma_9 discourse assertion was not found: {relative}")
    path.write_text(content.replace(old, new, 1), encoding="utf-8")
    print("Updated stale sigma_9 discourse test:", path)

test53 = ROOT / "tests" / "test_phase143_53a_r_aggregate_derivation.py"
t53 = test53.read_text(encoding="utf-8-sig")
old53 = """  assert len(
    definition_transitions
  ) == 1

  transition = definition_transitions[
    0
  ]

  assert (
    transition.role
    is TodaGroupProofNarrativeTransitionRole
    .SUPPORT
  )
  assert any(
    is_toda_group_proof_aggregate_statement(
      proof_step.conclusion
    )
    for block in transition.source_blocks
    for proof_step in block.steps
  )
"""
new53 = """  assert len(
    definition_transitions
  ) == 2

  assert all(
    transition.role
    is TodaGroupProofNarrativeTransitionRole
    .SUPPORT
    for transition in definition_transitions
  )
  assert any(
    is_toda_group_proof_aggregate_statement(
      proof_step.conclusion
    )
    for transition in definition_transitions
    for block in transition.source_blocks
    for proof_step in block.steps
  )
"""
if old53 not in t53:
    raise RuntimeError("Expected Phase 143-53A definition-transition assertion was not found.")
test53.write_text(t53.replace(old53, new53, 1), encoding="utf-8")
print("Updated stale aggregate-definition test:", test53)
