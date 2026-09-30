from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)


class ProposedReasonKind(Enum):
  DEFINITION_APPLICABILITY = "definition_applicability"
  DERIVED_EQUALITY = "derived_equality"
  EXACTNESS_TO_MAP_PROPERTY = "exactness_to_map_property"
  TRANSPORTED_ORDER = "transported_order"
  MULTIPLE_RELATION_TO_ORDER = "multiple_relation_to_order"
  SHORT_EXACT_DERIVATION = "short_exact_derivation"
  SHORT_EXACT_TO_GROUP_ORDER = "short_exact_to_group_order"
  MEMBER_OF_FULL_ORDER_GENERATES = "member_of_full_order_generates"


@dataclass(frozen=True)
class ProposedReasonRule:
  kind: ProposedReasonKind
  premise_roles: tuple[TodaGroupProofNarrativeMathematicalBlockRole, ...]
  conclusion_role: TodaGroupProofNarrativeMathematicalBlockRole
  requires_typed_dependency: bool
  requires_statement_shape: bool
  requires_exactness_context: bool
  requires_transport_semantic: bool
  rc4_4_status: str


RULES = (
  ProposedReasonRule(
    kind=ProposedReasonKind.DEFINITION_APPLICABILITY,
    premise_roles=(TodaGroupProofNarrativeMathematicalBlockRole.PRECONDITION,),
    conclusion_role=TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION,
    requires_typed_dependency=True,
    requires_statement_shape=False,
    requires_exactness_context=False,
    requires_transport_semantic=False,
    rc4_4_status="implement",
  ),
  ProposedReasonRule(
    kind=ProposedReasonKind.DERIVED_EQUALITY,
    premise_roles=(TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION,),
    conclusion_role=TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION,
    requires_typed_dependency=False,
    requires_statement_shape=True,
    requires_exactness_context=False,
    requires_transport_semantic=False,
    rc4_4_status="implement",
  ),
  ProposedReasonRule(
    kind=ProposedReasonKind.EXACTNESS_TO_MAP_PROPERTY,
    premise_roles=(
      TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS,
      TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY,
    ),
    conclusion_role=TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY,
    requires_typed_dependency=False,
    requires_statement_shape=True,
    requires_exactness_context=True,
    requires_transport_semantic=False,
    rc4_4_status="implement",
  ),
  ProposedReasonRule(
    kind=ProposedReasonKind.TRANSPORTED_ORDER,
    premise_roles=(
      TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE,
      TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY,
    ),
    conclusion_role=TodaGroupProofNarrativeMathematicalBlockRole.ORDER,
    requires_typed_dependency=False,
    requires_statement_shape=True,
    requires_exactness_context=False,
    requires_transport_semantic=True,
    rc4_4_status="defer-unless-existing-transport-identifies-chain",
  ),
  ProposedReasonRule(
    kind=ProposedReasonKind.MULTIPLE_RELATION_TO_ORDER,
    premise_roles=(
      TodaGroupProofNarrativeMathematicalBlockRole.CALCULATION,
      TodaGroupProofNarrativeMathematicalBlockRole.ORDER,
    ),
    conclusion_role=TodaGroupProofNarrativeMathematicalBlockRole.ORDER,
    requires_typed_dependency=False,
    requires_statement_shape=True,
    requires_exactness_context=False,
    requires_transport_semantic=False,
    rc4_4_status="implement",
  ),
  ProposedReasonRule(
    kind=ProposedReasonKind.SHORT_EXACT_DERIVATION,
    premise_roles=(
      TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS,
      TodaGroupProofNarrativeMathematicalBlockRole.MAP_PROPERTY,
    ),
    conclusion_role=TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS,
    requires_typed_dependency=False,
    requires_statement_shape=False,
    requires_exactness_context=True,
    requires_transport_semantic=False,
    rc4_4_status="implement-at-exactness-contribution-boundary",
  ),
  ProposedReasonRule(
    kind=ProposedReasonKind.SHORT_EXACT_TO_GROUP_ORDER,
    premise_roles=(
      TodaGroupProofNarrativeMathematicalBlockRole.EXACTNESS,
      TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE,
    ),
    conclusion_role=TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE,
    requires_typed_dependency=False,
    requires_statement_shape=True,
    requires_exactness_context=True,
    requires_transport_semantic=False,
    rc4_4_status="implement",
  ),
  ProposedReasonRule(
    kind=ProposedReasonKind.MEMBER_OF_FULL_ORDER_GENERATES,
    premise_roles=(
      TodaGroupProofNarrativeMathematicalBlockRole.MEMBERSHIP,
      TodaGroupProofNarrativeMathematicalBlockRole.ORDER,
      TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE,
    ),
    conclusion_role=TodaGroupProofNarrativeMathematicalBlockRole.GROUP_STRUCTURE,
    requires_typed_dependency=False,
    requires_statement_shape=True,
    requires_exactness_context=False,
    requires_transport_semantic=False,
    rc4_4_status="implement",
  ),
)


def main():
  output_dir=Path("phase150_rc4_3_general_rule_design")/"audit_output"
  output_dir.mkdir(parents=True,exist_ok=True)

  presentation, blocks, sidecar, arguments = _method_evidence_data(3,3)
  role_population={role:0 for role in TodaGroupProofNarrativeMathematicalBlockRole}
  for block in blocks:
    role_population[block.role]+=1

  lines=[
    "="*78,
    "Phase 150 / RC4-3 General rule design",
    "Production changes: none",
    "Existing test changes: none",
    "Repository-wide tests: not run",
    "="*78,
    "",
    "PROPOSED PRODUCTION MODEL",
    "-"*78,
    "New module for RC4-4:",
    "  toda_group_proof_narrative_reasons.py",
    "",
    "Minimal production types:",
    "  TodaGroupProofNarrativeReasonKind(Enum)",
    "  TodaGroupProofNarrativeReason(dataclass)",
    "  TodaGroupProofNarrativeReasonSidecar(dataclass)",
    "  build_toda_group_proof_narrative_reason_sidecar(...)",
    "",
    "Reason record fields:",
    "  kind: TodaGroupProofNarrativeReasonKind",
    "  premise_steps: tuple[ProofStep, ...]",
    "  conclusion_step: ProofStep",
    "  owner_argument_index: int | None",
    "",
    "Important separation:",
    "  OrderedContribution = what/where to display (RC3)",
    "  Reason = why a conclusion follows (RC4)",
    "  Renderer = how to say that reason in prose (RC4)",
    "",
    "PROPOSED RULES",
    "-"*78,
  ]

  for index, rule in enumerate(RULES,start=1):
    lines.extend([
      f"[{index}] {rule.kind.value}",
      "premise_roles="+repr(tuple(x.value for x in rule.premise_roles)),
      f"conclusion_role={rule.conclusion_role.value}",
      f"requires_typed_dependency={rule.requires_typed_dependency}",
      f"requires_statement_shape={rule.requires_statement_shape}",
      f"requires_exactness_context={rule.requires_exactness_context}",
      f"requires_transport_semantic={rule.requires_transport_semantic}",
      f"rc4_4_status={rule.rc4_4_status}",
      "",
    ])

  lines.extend([
    "SAFETY / GENERALITY GUARDS",
    "-"*78,
    "1. Never classify by n, k, pi_6^3, nu', proposition number, or rendered text.",
    "2. Never classify a raw role pair alone when multiple mathematical meanings are possible.",
    "3. Require statement shape for equality/order/generator deductions.",
    "4. Require exactness ownership/context for exactness-derived reasons.",
    "5. Do not generate a reason from OTHER blocks.",
    "6. Do not invent EHP map names or semantic labels; RC5 owns naming.",
    "7. Reason generation must not change contribution placement/order.",
    "8. Unsupported/ambiguous relations produce no reason, not fallback prose.",
    "",
    "RC4-4 MINIMAL IMPLEMENTATION BOUNDARY",
    "-"*78,
    "Implement the typed reason sidecar and only rules whose current semantic inputs",
    "are sufficient. Keep transported_order guarded by existing typed transport",
    "semantics; otherwise omit it rather than infer from names.",
    "",
    "Renderer integration should be additive: existing Narrative remains valid when",
    "no reason is classified. RC3 OrderedContribution APIs remain unchanged.",
    "",
    "PI_6^3 CURRENT ROLE POPULATION",
    "-"*78,
  ])
  lines.extend(
    f"{role.value}={count}"
    for role,count in role_population.items()
    if count
  )
  lines.extend([
    "",
    "DESIGN_RESULT=PASS",
    "NEXT=RC4-4 Minimal implementation",
  ])

  report="\n".join(lines)+"\n"
  print(report)
  (output_dir/"phase150_rc4_3_design.txt").write_text(report,encoding="utf-8")
  return 0


if __name__=="__main__":
  raise SystemExit(main())
