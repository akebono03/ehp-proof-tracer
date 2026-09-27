from pathlib import Path
import ast

path = Path("toda_group_proof_narrative_evidence_contributions.py")

if not path.exists():
  raise RuntimeError("EvidenceContribution file is missing.")

text = path.read_text(encoding="utf-8")
ast.parse(text)

if "def _aggregate_semantic_contribution_for_edge(" in text:
  raise RuntimeError(
    "15U helper already exists. "
    "Do not apply R1 over a completed 15U integration."
  )

required_fragments = (
  'ESTABLISH_GROUP = "establish_group"',
  'ESTABLISH_DEFINITION = "establish_definition"',
  "def _contribution_for_premise_block(",
  "def build_toda_group_proof_narrative_evidence_contribution_sidecar(",
)

for fragment in required_fragments:
  if fragment not in text:
    raise RuntimeError(
      "Expected 15P structure is missing: " + fragment
    )

import_anchor = (
  "from dataclasses import dataclass\n"
  "from enum import Enum\n"
)

aggregate_import = '''from dataclasses import dataclass
from enum import Enum

from toda_group_proof_narrative_aggregate_semantics import (
  TodaGroupProofNarrativeAggregateSemanticSidecar,
)
'''

if import_anchor not in text:
  raise RuntimeError("Expected import anchor not found.")

text = text.replace(import_anchor, aggregate_import, 1)

builder_start = text.find(
  "def build_toda_group_proof_narrative_evidence_contribution_sidecar("
)

if builder_start < 0:
  raise RuntimeError("EvidenceContribution builder start not found.")

prefix = text[:builder_start]

helper_and_builder = '''def _aggregate_semantic_contribution_for_edge(
  edge: TodaProofEdge,
  block_by_step_id: dict[
    int,
    TodaGroupProofNarrativeBlock,
  ],
  aggregate_semantic_sidecar: (
    TodaGroupProofNarrativeAggregateSemanticSidecar
    | None
  ),
) -> (
  TodaGroupProofNarrativeEvidenceContribution
  | None
):
  if aggregate_semantic_sidecar is None:
    return None

  aggregate_kind_by_step_id = {
    id(semantic.proof_step): semantic.kind
    for semantic in aggregate_semantic_sidecar.step_semantics
  }

  if id(edge.premise_step) not in aggregate_kind_by_step_id:
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


def build_toda_group_proof_narrative_evidence_contribution_sidecar(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  aggregate_semantic_sidecar: (
    TodaGroupProofNarrativeAggregateSemanticSidecar
    | None
  ) = None,
) -> TodaGroupProofNarrativeEvidenceContributionSidecar:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    blocks,
    tuple,
  ):
    raise TypeError(
      "blocks must be a tuple"
    )

  if (
    aggregate_semantic_sidecar is not None
    and aggregate_semantic_sidecar.presentation
    is not presentation
  ):
    raise ValueError(
      "aggregate_semantic_sidecar must belong "
      "to presentation"
    )

  block_by_step_id = (
    _block_by_step_id(
      blocks
    )
  )

  presentation_step_ids = {
    id(node.proof_step)
    for node in presentation.nodes
  }

  if set(block_by_step_id) != presentation_step_ids:
    raise ValueError(
      "blocks must cover presentation nodes "
      "exactly once"
    )

  edge_semantics = []

  for edge in presentation.edges:
    contribution = (
      _aggregate_semantic_contribution_for_edge(
        edge,
        block_by_step_id,
        aggregate_semantic_sidecar,
      )
    )

    if contribution is None:
      contribution = (
        _contribution_for_premise_block(
          block_by_step_id[
            id(edge.premise_step)
          ],
          edge,
        )
      )

    edge_semantics.append(
      TodaGroupProofNarrativeEvidenceContributionSemantic(
        edge=edge,
        contribution=contribution,
      )
    )

  return (
    TodaGroupProofNarrativeEvidenceContributionSidecar(
      presentation=presentation,
      edge_semantics=tuple(edge_semantics),
    )
  )
'''

updated = prefix + helper_and_builder + "\n"
ast.parse(updated)
path.write_text(updated, encoding="utf-8")

print(
  "Applied Phase 144-6-R5-15U-R1 "
  "safe builder replacement."
)
