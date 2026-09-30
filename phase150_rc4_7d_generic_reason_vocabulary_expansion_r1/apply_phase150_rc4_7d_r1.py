from pathlib import Path
import shutil
R=Path.cwd(); P=R/'phase150_rc4_7d_generic_reason_vocabulary_expansion_r1'; F=R/'toda_group_proof_narrative_reasons.py'; G=R/'toda_group_proof_narrative_reason_renderer.py'
for f in (F,G):
 if not f.exists(): raise SystemExit(f'missing: {f}')
 b=P/('backup_'+f.name)
 if not b.exists(): shutil.copy2(f,b)
s=F.read_text(encoding='utf-8')
a='''from toda_group_proof_narrative_semantics import (\n  TodaGroupProofNarrativeDependencySemanticRole,\n  TodaGroupProofNarrativeReferenceApplicationSemantic,\n  TodaGroupProofNarrativeSemanticSidecar,\n)\n'''
b='''from toda_group_proof_narrative_aggregate_semantics import (\n  TodaGroupProofNarrativeAggregateSemanticKind,\n  build_toda_group_proof_narrative_aggregate_semantic_sidecar,\n)\n'''+a
if a not in s: raise SystemExit('import baseline mismatch')
s=s.replace(a,b,1)
a='''  FINAL_GROUP_STRUCTURE = (\n    "final_group_structure"\n  )\n'''; b=a+'''  MAP_STRUCTURE_DERIVATION = (\n    "map_structure_derivation"\n  )\n  GROUP_ORDER_DERIVATION = (\n    "group_order_derivation"\n  )\n  FINAL_RESULT_DERIVATION = (\n    "final_result_derivation"\n  )\n'''
if a not in s: raise SystemExit('enum baseline mismatch')
s=s.replace(a,b,1)
helpers='''def _aggregate_derivation_reason(\n  proof_step: ProofStep,\n  aggregate_kind: TodaGroupProofNarrativeAggregateSemanticKind | None,\n) -> TodaGroupProofNarrativeReason | None:\n  if aggregate_kind is TodaGroupProofNarrativeAggregateSemanticKind.MAP_TRANSPORT:\n    kind = TodaGroupProofNarrativeReasonKind.MAP_STRUCTURE_DERIVATION\n  elif aggregate_kind is TodaGroupProofNarrativeAggregateSemanticKind.GROUP_ORDER_TRANSPORT:\n    kind = TodaGroupProofNarrativeReasonKind.GROUP_ORDER_DERIVATION\n  else:\n    return None\n  if not proof_step.premises:\n    return None\n  return TodaGroupProofNarrativeReason(\n    kind=kind,\n    premise_steps=tuple(proof_step.premises),\n    conclusion_step=proof_step,\n  )\n\n\ndef _final_result_derivation_reason(\n  proof_step: ProofStep,\n) -> TodaGroupProofNarrativeReason | None:\n  conclusion = proof_step.conclusion\n  if (\n    not isinstance(conclusion, Relation)\n    or conclusion.relation_type is not RelationType.EQUALITY\n    or not isinstance(conclusion.rhs, FiniteCyclicGroup)\n    or not proof_step.premises\n  ):\n    return None\n  return TodaGroupProofNarrativeReason(\n    kind=TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION,\n    premise_steps=tuple(proof_step.premises),\n    conclusion_step=proof_step,\n  )\n\n\n'''
anchor='def build_toda_group_proof_narrative_reason_sidecar(\n'
if anchor not in s: raise SystemExit('builder anchor missing')
s=s.replace(anchor,helpers+anchor,1)
a='''  reasons = []\n  reference_applications_by_step_id = {}\n  visible_step_ids = {\n'''; b='''  reasons = []\n  reference_applications_by_step_id = {}\n  aggregate_sidecar = build_toda_group_proof_narrative_aggregate_semantic_sidecar(\n    presentation\n  )\n  aggregate_kind_by_step_id = {\n    id(semantic.proof_step): semantic.kind\n    for semantic in aggregate_sidecar.step_semantics\n  }\n  visible_step_ids = {\n'''
if a not in s: raise SystemExit('builder setup mismatch')
s=s.replace(a,b,1)
a='''    final_group_structure_reason = _final_group_structure_reason(\n      node.proof_step\n    )\n    if final_group_structure_reason is not None:\n      append_if_visible(final_group_structure_reason)\n\n  return TodaGroupProofNarrativeReasonSidecar(\n'''; b='''    final_group_structure_reason = _final_group_structure_reason(\n      node.proof_step\n    )\n    if final_group_structure_reason is not None:\n      append_if_visible(final_group_structure_reason)\n\n    aggregate_reason = _aggregate_derivation_reason(\n      node.proof_step,\n      aggregate_kind_by_step_id.get(id(node.proof_step)),\n    )\n    if aggregate_reason is not None:\n      append_if_visible(aggregate_reason)\n\n    if final_group_structure_reason is None:\n      final_reason = _final_result_derivation_reason(node.proof_step)\n      if final_reason is not None:\n        append_if_visible(final_reason)\n\n  return TodaGroupProofNarrativeReasonSidecar(\n'''
if a not in s: raise SystemExit('builder tail mismatch')
s=s.replace(a,b,1); F.write_text(s,encoding='utf-8')

s=G.read_text(encoding='utf-8'); a='  return None\n\n\ndef insert_toda_group_proof_narrative_reason_prose(\n'; b='''  if reason.kind is TodaGroupProofNarrativeReasonKind.MAP_STRUCTURE_DERIVATION:\n    return (\n      "この完全性、既知の群構造、および写像の像に関する結果を合わせると、"\n      "対象となる写像の像と核が決まる.\\nしたがって、"\n    )\n\n  if reason.kind is TodaGroupProofNarrativeReasonKind.GROUP_ORDER_DERIVATION:\n    return (\n      "この群構造と写像による移送の結果を合わせると、"\n      "対象の群の位数と写像の単射性が決まる.\\nしたがって、"\n    )\n\n  if reason.kind is TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION:\n    return "以上で得た群構造、生成元、および写像に関する結果を合わせると、"\n\n  return None\n\n\ndef insert_toda_group_proof_narrative_reason_prose(\n'''
if a not in s: raise SystemExit('renderer baseline mismatch')
s=s.replace(a,b,1); G.write_text(s,encoding='utf-8')
(R/'tests'/'test_phase150_rc4_7d_generic_reason_vocabulary.py').write_text((P/'test_phase150_rc4_7d_generic_reason_vocabulary.py').read_text(encoding='utf-8'),encoding='utf-8')
print('RC4-7D R1 applied')
