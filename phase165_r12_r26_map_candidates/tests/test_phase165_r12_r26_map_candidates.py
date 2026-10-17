from homotopy_groups import TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement, QuotientIsomorphismStatement
from phase165_r12_r26_map_candidates import expand_cited_eta_quotient
from toda_rules import toda_eta_family_definition_statement


def test_cited_family_derives_typed_map_obligations():
    eta = toda_eta_family_definition_statement(3).element
    goal = CyclicStructureStatement(TodaPrimaryGroup(4, 3), eta, 2)
    options = expand_cited_eta_quotient(goal, 1)
    assert len(options) == 1
    q, source = options[0].subgoals
    assert isinstance(q, QuotientIsomorphismStatement)
    assert q.domain == TodaPrimaryGroup(3, 2)
    assert q.codomain == goal.group
    assert source.group == q.domain and source.order is None


def test_missing_or_ambiguous_citation_refused():
    eta = toda_eta_family_definition_statement(3).element
    goal = CyclicStructureStatement(TodaPrimaryGroup(4, 3), eta, 2)
    assert expand_cited_eta_quotient(goal, 0) == ()
    assert expand_cited_eta_quotient(goal, 2) == ()


def test_unrelated_groups_and_generators_refused():
    eta = toda_eta_family_definition_statement(3).element
    assert expand_cited_eta_quotient(CyclicStructureStatement(TodaPrimaryGroup(5, 3), eta, 2), 1) == ()
    assert expand_cited_eta_quotient(CyclicStructureStatement(TodaPrimaryGroup(4, 3), object(), 2), 1) == ()
