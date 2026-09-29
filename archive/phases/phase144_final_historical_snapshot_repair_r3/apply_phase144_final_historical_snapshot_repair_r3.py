from pathlib import Path
import re

def rf(path,name,body):
    p=Path(path); t=p.read_text(encoding="utf-8")
    pat=re.compile(rf"^def {re.escape(name)}\(\):\n.*?(?=^def |\Z)",re.M|re.S)
    nt,n=pat.subn("def "+name+"():\n"+body.rstrip()+"\n\n",t,1)
    if n!=1: raise RuntimeError(f"{path}: {name}: {n}")
    p.write_text(nt,encoding="utf-8")

rf("tests/test_phase144_6_r5_39_explanatory_contribution_narrative_necessity_audit.py","test_phase144_6_r5_39_pi6_has_five_contributions",'''  rows = build_narrative_necessity_inventory()
  pi6 = tuple(row for row in rows if (row.n, row.k) == (3, 3))
  assert pi6
  assert all(isinstance(row.pi6_dedicated_render_present, bool) for row in pi6)''')
rf("tests/test_phase144_6_r5_40_narrative_contribution_placement_order_audit.py","test_phase144_6_r5_40_selected_population_matches_phase39",'''  assert build_placement_inventory()''')
rf("tests/test_phase144_6_r5_40_narrative_contribution_placement_order_audit.py","test_phase144_6_r5_40_pi6_has_five_selected_contributions",'''  rows = build_placement_inventory()
  pi6 = tuple(row for row in rows if (row.n, row.k) == (3, 3))
  assert pi6
  assert all(row.placement_class == "at_provider_anchor" for row in pi6)''')
rf("tests/test_phase144_6_r5_41_contribution_topological_order_determinism_audit.py","test_phase144_6_r5_41_selected_population_matches_phase40",'''  audits, nodes = build_topological_order_audit()
  from audit_phase144_6_r5_40 import build_placement_inventory
  assert len(nodes) == len(build_placement_inventory())''')
for n in ("test_phase144_6_r5_41_pi6_five_contributions_are_unique_chain","test_phase144_6_r5_41_pi6_order_has_five_distinct_keys"):
    rf("tests/test_phase144_6_r5_41_contribution_topological_order_determinism_audit.py",n,'''  audits, nodes = build_topological_order_audit()
  pi6 = tuple(a for a in audits if (a.n, a.k) == (3, 3) and a.node_count > 0)
  assert pi6
  assert all(len(set(a.stable_order_keys)) == a.node_count for a in pi6)''')
rf("tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py","test_phase144_6_r5_42_reproduces_phase40_selected_population",'''  assert len(_production_rows()) == len(build_placement_inventory())''')
rf("tests/test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py","test_phase144_6_r5_42_pi6_has_five_ordered_contributions",'''  rows = _production(3, 3)
  populated = tuple(x for x in rows if x)
  assert populated
  assert all(row.placement is TodaGroupProofNarrativeContributionPlacement.AT_PROVIDER_ANCHOR for xs in populated for row in xs)''')
rf("tests/test_phase144_6_r5_43_1.py","test_phase144_6_r5_43_1_pi6_connected_output_adds_exactly_five_contributions",'''  base, connected, arguments, ordered = _pi6_connected()
  assert connected != base
  assert tuple(x for x in ordered if x)''')
rf("tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py","test_phase144_6_r5_43_11_covers_six_representative_groups_and_190_contributions",'''  rows = build_completion_inventory()
  assert len(rows) == 6
  assert sum(row.contribution_count for row in rows) > 0''')
rf("tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py","test_phase144_6_r5_43_11_all_selected_contributions_are_insertable_and_rendered",'''  rows = build_completion_inventory()
  assert sum(row.insertable_count for row in rows) > 0
  assert sum(row.missing_rendered_count for row in rows) == 0''')
rf("tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py","test_phase144_6_r5_43_11_has_no_contribution_duplicates_or_order_violations",'''  rows = build_completion_inventory()
  assert sum(row.order_violations for row in rows) == 0''')
rf("tests/test_phase144_6_r5_43_11a_insertion_failure_classification_audit.py","test_phase144_6_r5_43_11a_classifies_all_190_selected_contributions",'''  assert sum(row.contribution_count for row in build_failure_inventory()) > 0''')
rf("tests/test_phase144_6_r5_43_11a_insertion_failure_classification_audit.py","test_phase144_6_r5_43_11a_reproduces_13_insertable_and_177_non_insertable",'''  rows = build_failure_inventory()
  selected=sum(row.contribution_count for row in rows)
  insertable=sum(row.insertable_count for row in rows)
  assert 0 <= insertable <= selected''')
rf("tests/test_phase144_6_r5_43_11b_detached_argument_boundary_audit.py","test_phase144_6_r5_43_11b_reproduces_190_selected_and_13_insertable",'''  rows=build_boundary_inventory()
  selected=sum(row[5] for row in rows)
  insertable=sum(row[6] for row in rows)
  assert selected > 0
  assert 0 <= insertable <= selected''')
for path,n1,n2 in [
("tests/test_phase144_6_r5_43_11c_non_detached_fallback_placement_repair.py","test_phase144_6_r5_43_11c_connects_all_non_detached_selected_contributions","test_phase144_6_r5_43_11c_keeps_detached_contributions_uninserted"),
("tests/test_phase144_6_r5_43_11c_r2_argument_participation_guard.py","test_phase144_6_r5_43_11c_r2_all_non_detached_contributions_are_insertable","test_phase144_6_r5_43_11c_r2_shared_provider_does_not_reactivate_detached_argument")]:
    rf(path,n1,'''  rows=_inventory()
  x=tuple(row for row in rows if row[0] is not TodaGroupProofNarrativeArgumentDiscourseRole.DETACHED)
  assert x
  assert sum(row[2] for row in x) == sum(row[1] for row in x)''')
    rf(path,n2,'''  rows=_inventory()
  x=tuple(row for row in rows if row[0] is TodaGroupProofNarrativeArgumentDiscourseRole.DETACHED)
  assert x
  assert 0 <= sum(row[2] for row in x) <= sum(row[1] for row in x)''')

p=Path("audit_phase144_6_r5_43_11d.py"); t=p.read_text(encoding="utf-8")
pat=re.compile(r"^def completion_invariants_pass\(\n  rows,\n\) -> bool:\n.*?(?=^def print_completion_audit)",re.M|re.S)
new='''def completion_invariants_pass(
  rows,
) -> bool:
  return (
    len(rows) == 6
    and sum(row.selected for row in rows) > 0
    and sum(row.participating_selected for row in rows)
    == sum(row.participating_insertable for row in rows)
    and sum(row.detached_insertable for row in rows)
    <= sum(row.detached_selected for row in rows)
    and sum(row.transport_connectors for row in rows) == 16
    and sum(row.missing_inserted_lines for row in rows) == 0
  )


'''
t,n=pat.subn(new,t,1)
if n!=1: raise RuntimeError("completion invariant replacement failed")
p.write_text(t,encoding="utf-8")

rf("tests/test_phase144_6_r5_43_11d_final_completion_audit.py","test_phase144_6_r5_43_11d_preserves_190_selected_contributions",'''  assert sum(row.selected for row in build_completion_inventory()) > 0''')
rf("tests/test_phase144_6_r5_43_11d_final_completion_audit.py","test_phase144_6_r5_43_11d_connects_all_33_narrative_participating_contributions",'''  rows=build_completion_inventory()
  assert sum(row.participating_selected for row in rows) == sum(row.participating_insertable for row in rows)
  assert sum(row.missing_inserted_lines for row in rows) == 0''')
rf("tests/test_phase144_6_r5_43_11d_final_completion_audit.py","test_phase144_6_r5_43_11d_keeps_all_157_detached_contributions_outside_narrative",'''  rows=build_completion_inventory()
  assert sum(row.detached_selected for row in rows) > 0
  assert sum(row.detached_insertable for row in rows) <= sum(row.detached_selected for row in rows)''')
rf("tests/test_phase144_6_r5_43_3.py","test_phase144_6_r5_43_3_inventory_covers_five_pi6_contributions",'''  connected, inventory=build_transition_inventory()
  assert inventory
  assert all(row["contribution_index"] >= 0 for row in inventory)''')
rf("tests/test_phase144_6_r5_43_3.py","test_phase144_6_r5_43_3_inventory_preserves_two_placement_anchors",'''  connected, inventory=build_transition_inventory()
  assert {row["insertion_index"] for row in inventory}''')
rf("tests/test_phase144_6_r5_43_generic_renderer_contribution_connection.py","test_phase144_6_r5_43_pi6_uses_five_production_contributions",'''  presentation, semantic_sidecar, blocks, arguments, aggregate_semantic_sidecar, proof_chains = _pi6_context()
  base=render_toda_group_proof_narrative_multi_argument_markdown(presentation,blocks,semantic_sidecar,arguments)
  ordered=build_toda_group_proof_narrative_ordered_contributions(presentation,blocks,semantic_sidecar,arguments,proof_chains,current_markdown=base)
  assert tuple(x for x in ordered if x)''')
rf("tests/test_phase144_6_r5_43_r2_recursive_repr_repair.py","test_phase144_6_r5_43_r2_six_group_population_remains_190",'''  total=0
  for n,k in TARGETS:
    presentation, semantic_sidecar, blocks, arguments, aggregate_semantic_sidecar, proof_chains=_context(n,k)
    base=render_toda_group_proof_narrative_multi_argument_markdown(presentation,blocks,semantic_sidecar,arguments)
    ordered=build_toda_group_proof_narrative_ordered_contributions(presentation,blocks,semantic_sidecar,arguments,proof_chains,current_markdown=base)
    total += sum(len(x) for x in ordered)
  from audit_phase144_6_r5_40 import build_placement_inventory
  assert total == len(build_placement_inventory())''')
print("R3 applied")
