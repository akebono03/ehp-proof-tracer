import pytest
from phase144_6_r25_30_group_structure_definition_entry_branch_ownership_audit.audit_phase144_6_r25_30 import TARGETS,_argument_rows,LARGE_BRANCH_BLOCK_THRESHOLD

@pytest.mark.parametrize("n,k",TARGETS)
def test_phase144_6_r25_30_audits_only_group_structure_and_definition(n,k):
  _,_,_,rows=_argument_rows(n,k)
  assert rows
  assert all(row["role"] in ("establish_group_structure","establish_definition") for row in rows)

@pytest.mark.parametrize("n,k",TARGETS)
def test_phase144_6_r25_30_child_closure_never_exceeds_entry_closure(n,k):
  _,_,_,rows=_argument_rows(n,k)
  for row in rows:
    for entry in row["entries"]:
      assert all(child["blocks"]<=entry["blocks"] for child in entry["children"])
      assert all(child["steps"]<=entry["steps"] for child in entry["children"])

def test_phase144_6_r25_30_reproduces_remaining_giant_entry_branches():
  for n,k in ((8,7),(9,7)):
    _,_,_,rows=_argument_rows(n,k)
    assert any(
      entry["blocks"]>=LARGE_BRANCH_BLOCK_THRESHOLD
      for row in rows
      for entry in row["entries"]
    )
