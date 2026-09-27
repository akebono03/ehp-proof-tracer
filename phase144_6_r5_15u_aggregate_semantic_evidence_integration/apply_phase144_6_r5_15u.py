from pathlib import Path
import ast

ROOT = Path.cwd()
TARGET = ROOT / "toda_group_proof_narrative_evidence_contributions.py"

if not TARGET.exists():
    raise RuntimeError(
        "toda_group_proof_narrative_evidence_contributions.py not found. "
        "Apply Phase 144-6-R5-15M/15P first."
    )

aggregate_target = ROOT / "toda_group_proof_narrative_aggregate_semantics.py"
if not aggregate_target.exists():
    raise RuntimeError(
        "toda_group_proof_narrative_aggregate_semantics.py not found. "
        "Apply Phase 144-6-R5-15T first."
    )

source = TARGET.read_text(encoding="utf-8")
tree = ast.parse(source)

function_node = next(
    (
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name
        == "build_toda_group_proof_narrative_evidence_contribution_sidecar"
    ),
    None,
)
if function_node is None:
    raise RuntimeError(
        "build_toda_group_proof_narrative_evidence_contribution_sidecar "
        "not found."
    )

helper_name = "_aggregate_semantic_contribution_for_edge"
if helper_name in source:
    raise RuntimeError("Phase 144-6-R5-15U appears to be already applied.")

for member in ("ESTABLISH_GROUP", "ESTABLISH_DEFINITION"):
    if member not in source:
        raise RuntimeError(
            f"required EvidenceContribution member missing: {member}"
        )

import_anchor = "from dataclasses import dataclass\n"
if import_anchor not in source:
    raise RuntimeError("dataclasses import anchor not found.")

aggregate_import = '''from toda_group_proof_narrative_aggregate_semantics import (
  TodaGroupProofNarrativeAggregateSemanticSidecar,
)
'''
source = source.replace(
    import_anchor,
    import_anchor + aggregate_import,
    1,
)

helper = '''

def _aggregate_semantic_contribution_for_edge(
  edge: TodaProofEdge,
  block_by_step_id: dict[int, TodaGroupProofNarrativeMathematicalBlock],
  aggregate_semantic_sidecar: (
    TodaGroupProofNarrativeAggregateSemanticSidecar | None
  ),
) -> TodaGroupProofNarrativeEvidenceContribution | None:
  if aggregate_semantic_sidecar is None:
    return None

  aggregate_kind_by_step_id = {
    id(semantic.proof_step): semantic.kind
    for semantic in aggregate_semantic_sidecar.step_semantics
  }
  aggregate_kind = aggregate_kind_by_step_id.get(
    id(edge.premise_step)
  )
  if aggregate_kind is None:
    return None

  consumer_block = block_by_step_id.get(
    id(edge.parent_step)
  )
  if consumer_block is None:
    return None

  if (
    consumer_block.role
    is TodaGroupProofNarrativeMathematicalBlockRole.TARGET
  ):
    return (
      TodaGroupProofNarrativeEvidenceContribution
      .ESTABLISH_GROUP
    )

  if (
    consumer_block.role
    is TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION
  ):
    return (
      TodaGroupProofNarrativeEvidenceContribution
      .ESTABLISH_DEFINITION
    )

  return None
'''

lines = source.splitlines(keepends=True)
insert_at = function_node.lineno - 1
source = "".join(lines[:insert_at]) + helper + "\n" + "".join(lines[insert_at:])

tree = ast.parse(source)
function_node = next(
    node
    for node in tree.body
    if isinstance(node, ast.FunctionDef)
    and node.name
    == "build_toda_group_proof_narrative_evidence_contribution_sidecar"
)

old_function = ast.get_source_segment(source, function_node)
if old_function is None:
    raise RuntimeError("could not read current builder source.")

signature_end = old_function.find("):")
if signature_end < 0:
    raise RuntimeError("builder signature terminator not found.")

signature = old_function[:signature_end + 2]
if "aggregate_semantic_sidecar" in signature:
    raise RuntimeError("builder already has aggregate_semantic_sidecar.")

signature = signature[:-2] + '''  aggregate_semantic_sidecar: (
    TodaGroupProofNarrativeAggregateSemanticSidecar | None
  ) = None,
):'''

body = old_function[signature_end + 2:]

validation_anchor = "\n  block_by_step_id = _block_by_step_id(blocks)"
if validation_anchor not in body:
    raise RuntimeError("block_by_step_id builder anchor not found.")

validation = '''
  if (
    aggregate_semantic_sidecar is not None
    and aggregate_semantic_sidecar.presentation is not presentation
  ):
    raise ValueError(
      "aggregate_semantic_sidecar must belong to presentation"
    )
'''
body = body.replace(
    validation_anchor,
    validation + validation_anchor,
    1,
)

loop_anchor = "    contribution = _contribution_for_premise_block("
if loop_anchor not in body:
    raise RuntimeError("contribution mapper call anchor not found.")

call_start = body.index(loop_anchor)
line_start = body.rfind("\n", 0, call_start) + 1
paren_start = body.index("(", call_start)
depth = 0
call_end = None
for i in range(paren_start, len(body)):
    ch = body[i]
    if ch == "(":
        depth += 1
    elif ch == ")":
        depth -= 1
        if depth == 0:
            call_end = i + 1
            break
if call_end is None:
    raise RuntimeError("could not locate end of contribution mapper call.")

replacement = '''    contribution = _aggregate_semantic_contribution_for_edge(
      edge,
      block_by_step_id,
      aggregate_semantic_sidecar,
    )
    if contribution is None:
      contribution = _contribution_for_premise_block(
        block_by_step_id[id(edge.premise_step)]
      )'''

body = body[:line_start] + replacement + body[call_end:]
new_function = signature + body
source = source.replace(old_function, new_function, 1)

ast.parse(source)
TARGET.write_text(source, encoding="utf-8")
print("Integrated aggregate semantic metadata into EvidenceContribution.")
