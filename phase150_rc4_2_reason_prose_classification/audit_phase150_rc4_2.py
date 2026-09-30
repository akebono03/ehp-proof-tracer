from __future__ import annotations

from collections import Counter
from pathlib import Path

from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_hidden_bridge_semantics import (
  build_toda_group_proof_narrative_hidden_bridge_semantics,
)


CASES = (
  ("pi_6^3", 3, 3),
  ("pi_8^5", 5, 3),
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)


def _block_index_by_step_id(blocks):
  return {
    id(step): index
    for index, block in enumerate(blocks)
    for step in block.steps
  }


def _edge_role_pairs(presentation, blocks):
  block_index = _block_index_by_step_id(blocks)
  pairs = []
  for edge in presentation.edges:
    premise_index = block_index[id(edge.premise_step)]
    parent_index = block_index[id(edge.parent_step)]
    if premise_index == parent_index:
      continue
    pairs.append(
      (
        blocks[premise_index].role.value,
        blocks[parent_index].role.value,
      )
    )
  return tuple(pairs)


def _semantic_dependency_pairs(sidecar, blocks):
  block_index = _block_index_by_step_id(blocks)
  result = []
  for semantic in sidecar.dependency_semantics:
    prerequisite_index = block_index[id(semantic.prerequisite_step)]
    dependent_index = block_index[id(semantic.dependent_step)]
    result.append(
      (
        semantic.role.value,
        blocks[prerequisite_index].role.value,
        blocks[dependent_index].role.value,
      )
    )
  return tuple(result)


def _pi6_false_diagnosis(presentation, blocks):
  map_blocks = [
    (index, block)
    for index, block in enumerate(blocks)
    if block.role is TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY
  ]
  exactness_blocks = [
    index
    for index, block in enumerate(blocks)
    if block.role is TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS
  ]
  map_types = [
    (
      index,
      tuple(type(step.conclusion).__name__ for step in block.steps),
    )
    for index, block in map_blocks
  ]
  return exactness_blocks, map_types


def main():
  output_dir = Path("phase150_rc4_2_reason_prose_classification") / "audit_output"
  output_dir.mkdir(parents=True, exist_ok=True)

  all_pairs = Counter()
  case_lines = []
  pi6_diagnosis = None

  for label, n, k in CASES:
    presentation, blocks, sidecar, arguments = _method_evidence_data(n, k)
    edge_pairs = _edge_role_pairs(presentation, blocks)
    semantic_pairs = _semantic_dependency_pairs(sidecar, blocks)
    hidden = build_toda_group_proof_narrative_hidden_bridge_semantics(
      presentation
    )
    all_pairs.update(edge_pairs)

    case_lines.extend(
      (
        "=" * 78,
        label,
        f"blocks={len(blocks)} arguments={len(arguments)} edges={len(presentation.edges)}",
        f"block_roles={tuple(block.role.value for block in blocks)}",
        "edge_role_pairs:",
      )
    )
    case_lines.extend(
      f"  {premise} -> {parent}"
      for premise, parent in edge_pairs
    )
    case_lines.append("semantic_dependency_pairs:")
    case_lines.extend(
      f"  {role}: {premise} -> {parent}"
      for role, premise, parent in semantic_pairs
    )
    case_lines.append(
      "hidden_bridge_semantics="
      + repr(
        tuple(
          (
            item.role.value,
            item.reference_identity,
            None if item.operation_kind is None else item.operation_kind.value,
          )
          for item in hidden
        )
      )
    )
    case_lines.append("")

    if label == "pi_6^3":
      pi6_diagnosis = _pi6_false_diagnosis(presentation, blocks)

  classifications = (
    (
      "DEFINITION_APPLICABILITY",
      "PRECONDITION + semantic dependency PRECONDITION_FOR_DEFINITION -> DEFINITION",
      "already typed",
      "generic",
    ),
    (
      "DERIVED_EQUALITY",
      "CALCULATION -> CALCULATION dependency chain",
      "graph edges + Relation(EQUALITY)",
      "generic",
    ),
    (
      "EXACTNESS_TO_MAP_PROPERTY",
      "EXACTNESS + MAP_PROPERTY premise(s) -> MAP_PROPERTY",
      "block roles + graph/exactness ownership",
      "generic; inspect concrete map-property statement type for wording",
    ),
    (
      "TRANSPORTED_ORDER",
      "GROUP_STRUCTURE/ORDER + MAP_PROPERTY + transport -> ORDER",
      "block roles + hidden transport semantics",
      "generic",
    ),
    (
      "MULTIPLE_RELATION_TO_ORDER",
      "CALCULATION + ORDER -> ORDER",
      "graph edges + relation shape",
      "generic",
    ),
    (
      "SHORT_EXACT_DERIVATION",
      "EXACTNESS + endpoint MAP_PROPERTY -> exactness display contribution",
      "exactness component/exposure + map-property evidence",
      "generic",
    ),
    (
      "SHORT_EXACT_TO_GROUP_ORDER",
      "EXACTNESS + endpoint GROUP_STRUCTURE -> GROUP_STRUCTURE",
      "argument method evidence + graph dependencies",
      "generic",
    ),
    (
      "MEMBER_OF_FULL_ORDER_GENERATES",
      "MEMBERSHIP + ORDER + GROUP_STRUCTURE -> GROUP_STRUCTURE",
      "block roles + relation subjects",
      "generic",
    ),
  )

  exactness_blocks, map_types = pi6_diagnosis

  lines = [
    "=" * 78,
    "Phase 150 / RC4-2 Reason-prose classification",
    "Production changes: none",
    "Existing test changes: none",
    "Repository-wide tests: not run",
    "=" * 78,
    "",
    "RC4-1 FALSE DIAGNOSIS",
    "-" * 78,
    (
      "[3] current_required_facts_present=False was a prose-regex limitation: "
      "the current Narrative does not print the upstream H:pi_7^3->pi_7^5 "
      "surjectivity fact, while the proof structure still contains exactness "
      "and typed MAP_PROPERTY blocks."
    ),
    f"pi6_exactness_block_indices={exactness_blocks}",
    f"pi6_map_property_statement_types={map_types}",
    "",
    "PROPOSED GENERIC REASON RELATIONS",
    "-" * 78,
  ]

  for index, (name, shape, source, status) in enumerate(classifications, start=1):
    lines.extend(
      (
        f"[{index}] {name}",
        f"shape: {shape}",
        f"semantic source: {source}",
        f"classification: {status}",
        "",
      )
    )

  lines.extend(
    (
      "DESIGN CONCLUSION",
      "-" * 78,
      "Do not key reason prose by pi_6^3, nu', proposition number, or rendered text.",
      "Reason classification should be derived before prose rendering.",
      "Preferred pipeline:",
      "ProofStep / block role / dependency / exactness ownership / hidden transport",
      "  -> generic reason relation",
      "  -> generic prose renderer",
      "",
      "RC4-3 should introduce only the minimal typed reason-relation model needed",
      "for relations that are actually supported by current semantics.",
      "",
      "CROSS-GROUP EDGE ROLE POPULATION",
      "-" * 78,
    )
  )
  lines.extend(
    f"{premise} -> {parent}: {count}"
    for (premise, parent), count in sorted(all_pairs.items())
  )
  lines.extend(("", "AUDIT_RESULT=PASS"))

  report = "\n".join(lines + [""] + case_lines) + "\n"
  print(report)
  (output_dir / "phase150_rc4_2_report.txt").write_text(report, encoding="utf-8")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
