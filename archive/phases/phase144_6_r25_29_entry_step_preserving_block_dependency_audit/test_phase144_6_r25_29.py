import pytest
from phase144_6_r25_29_entry_step_preserving_block_dependency_audit.audit_phase144_6_r25_29 import TARGETS,_summaries_for_target

@pytest.mark.parametrize("n,k",TARGETS)
def test_phase144_6_r25_29_simulation_keeps_conclusion_once_and_last(n,k):
  _,blocks,arguments,rows=_summaries_for_target(n,k)
  for row in rows:
    conclusion_index=next(i for i,b in enumerate(blocks) if b is arguments[row["argument_index"]].conclusion_block)
    simulated=row["simulated_indices"]
    assert simulated
    assert simulated[-1]==conclusion_index
    assert simulated.count(conclusion_index)==1

@pytest.mark.parametrize("n,k",TARGETS)
def test_phase144_6_r25_29_simulation_stops_at_other_argument_conclusions(n,k):
  _,blocks,arguments,rows=_summaries_for_target(n,k)
  conclusions=tuple(next(i for i,b in enumerate(blocks) if b is a.conclusion_block) for a in arguments)
  for row in rows:
    body=frozenset(row["simulated_indices"][:-1])
    assert all(ci not in body for oi,ci in enumerate(conclusions) if oi!=row["argument_index"])

def test_phase144_6_r25_29_pi6_3_preserves_primary_exactness_material():
  _,_,_,rows=_summaries_for_target(3,3)
  group=next(r for r in rows if r["role"]=="establish_group_structure")
  order=next(r for r in rows if r["role"]=="establish_order")
  assert group["simulated_exactness"]>=3
  assert order["simulated_exactness"]>=1

def test_phase144_6_r25_29_large_targets_show_strict_reduction():
  for n,k in ((8,7),(9,7)):
    _,_,_,rows=_summaries_for_target(n,k)
    assert any(r["current_blocks"]>=900 and r["simulated_blocks"]<r["current_blocks"] for r in rows)
