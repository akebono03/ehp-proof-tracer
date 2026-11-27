import pytest

from phase178_r29_final_6stem_audit.audit import (
    TARGETS, validate_summary, validate_citations, validate_boundary,
)


def summary(n=7):
    return dict(n=n,k=6,status='complete',trust_status='VERIFIED',open_goal_count=0,
                target_given_count=0,web_error=None,complete_invariants_hold=True,
                web_key='generic-complete-proof',proven_step_count=18,reference_count=0)


@pytest.mark.parametrize('n', range(2,8))
def test_active_scope(n):
    assert (n,6) in TARGETS
    validate_summary(n,summary(n))


@pytest.mark.parametrize('key,value', [('n',8),('status','partial'),('trust_status','UNKNOWN'),
    ('open_goal_count',1),('target_given_count',1),('web_error','error'),
    ('complete_invariants_hold',False),('web_key','generic-partial-proof'),
    ('proven_step_count',0),('reference_count',-1),('reference_count',True)])
def test_reject_active_regression(key,value):
    with pytest.raises(RuntimeError):
        validate_summary(7,dict(summary(),**{key:value}))


def test_boundary_is_not_active():
    assert (8,6) not in TARGETS
    with pytest.raises(RuntimeError):
        validate_summary(8,summary(8))


def citations():
    return [dict(number=1,locator='source A',step_indices=[0,2]),
            dict(number=2,locator='source B',step_indices=[0,1])]


def test_multiple_citations_per_given_and_shared_sources_are_valid():
    validate_citations({0,1,2},{0,1},[(1,2),(2,),(1,)],citations(),[1,2])


@pytest.mark.parametrize('case',['missing','outside','binding','uncovered','unknown','heading'])
def test_reject_invalid_citation_contract(case):
    scope,givens,numbers,cs,headings = {0,1,2},{0,1},[(1,2),(2,),(1,)],citations(),[1,2]
    if case == 'missing':
        cs = []
    elif case == 'outside':
        cs[1]['step_indices'] = [0,3]
    elif case == 'binding':
        numbers[2] = ()
    elif case == 'uncovered':
        cs[1]['step_indices'] = [0]
        numbers[1] = ()
    elif case == 'unknown':
        numbers[2] = (1,3)
    else:
        headings = [1,1]
    with pytest.raises(RuntimeError):
        validate_citations(scope,givens,numbers,cs,headings)


def boundary():
    return dict(gate='PASS_R27_STABLE_BOUNDARY_AUDIT_OPEN',status='partial',
                web_key='generic-partial-proof',trust_verified=False,target_given_count=0,open_goal_count=8)


def test_deferred_partial_boundary():
    validate_boundary(boundary())


@pytest.mark.parametrize('key,value',[('gate','FAIL_R27'),('status','complete'),
    ('web_key','generic-complete-proof'),('trust_verified',True),('target_given_count',1),('open_goal_count',0)])
def test_boundary_change_requires_review(key,value):
    with pytest.raises(RuntimeError):
        validate_boundary(dict(boundary(),**{key:value}))
