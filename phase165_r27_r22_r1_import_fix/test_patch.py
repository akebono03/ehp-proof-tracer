from types import SimpleNamespace

import web_group_query as module
from homotopy_groups import FiniteCyclicGroup
from phase165_r52_partial_proof import GroupStructureStatus, ProofSearchStatus, make_partial_proof_result
from proof import Relation, RelationType
from toda_calculation_result import TodaCalculationStatus


def test_r22_unproved_group_does_not_claim_found(monkeypatch):
    monkeypatch.setattr(module, 'search_group_structure_automatically',
                        lambda n, k: make_partial_proof_result(n=n,k=k,status=ProofSearchStatus.SEARCH_FAILED,diagnostics=('unproved',)))
    result=module.build_standard_web_group_query_view(3,1)
    assert result.status is TodaCalculationStatus.NOT_FOUND
    assert result.result_latex is None
    assert result.proof_available is False


def test_r22_complete_group_uses_existing_renderer(monkeypatch):
    from homotopy_groups import TodaPrimaryGroup
    target=TodaPrimaryGroup(group_dimension=4,sphere_dimension=3)
    conclusion=Relation(lhs=target,rhs=FiniteCyclicGroup(order=2,generator='eta_3'),relation_type=RelationType.EQUALITY)
    monkeypatch.setattr(module,'search_group_structure_automatically',lambda n,k:SimpleNamespace(status=ProofSearchStatus.COMPLETE,structure_status=GroupStructureStatus.KNOWN,conclusion=conclusion))
    result=module.build_standard_web_group_query_view(3,1)
    assert result.status is TodaCalculationStatus.FOUND
    assert result.result_latex is not None
    assert result.proof_available is True


def test_r22_old_builder_is_absent_from_query_source():
    from pathlib import Path
    code=Path(module.__file__).read_text(encoding='utf-8')
    assert 'build_standard_toda_report' not in code
    assert 'search_group_structure_automatically' in code
