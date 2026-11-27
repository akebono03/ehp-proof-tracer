from copy import deepcopy

import pytest

from phase178_r24_n7_source_first_audit.audit import SELF_FILES, ancestry, summarize, validate_scope


def test_scope_accepts_only_own_package_commits():
    validate_scope([], [])
    validate_scope(SELF_FILES, [])
    with pytest.raises(RuntimeError, match='UNREVIEWED_COMMITTED_PATHS'):
        validate_scope(['proof.py'], [])
    with pytest.raises(RuntimeError, match='TRACKED_WORKTREE_NOT_CLEAN'):
        validate_scope([], ['proof.py'])


def test_ancestry_shared_and_disconnected():
    nodes = {0:{'premises':[1,2]},1:{'premises':[3]},2:{'premises':[3]},3:{'premises':[]},4:{'premises':[]}}
    assert ancestry(nodes,0) == {0,1,2,3}


@pytest.mark.parametrize('nodes',[{0:{'premises':[1]}},{0:{'premises':[0]}},
                                  {0:{'premises':[1]},1:{'premises':[0]}}])
def test_ancestry_invalid(nodes):
    with pytest.raises(RuntimeError,match='INVALID_PROOF_GRAPH'):
        ancestry(nodes,0)


def partial_fixture():
    return ({'n':7,'k':6,'status':'partial','web_error':None,'web_key':'generic-partial-proof',
             'target_given_count':0,'complete_invariants_hold':True,'open_goal_count':1,
             'trust_status':'NOT_APPLICABLE_PARTIAL'},
            {'open_goals':['goal'],'screened_source_inventory':{'target_group_given_links':[]},
             'frontier':[{'goal':'goal','state':'CANDIDATES_PRESENT',
                          'observed_expansions':[{'options':[{'rule':'candidate'},{'rule':'candidate'}]}]}],
             'provider_calls':[], 'search_context':{}})


def test_partial_candidate_is_not_complete():
    summary, detail = partial_fixture()
    result = summarize(summary,detail)
    assert result['root_complete'] is False
    assert result['frontier'][0]['rules'] == ['candidate']


def test_complete_requires_trust_and_no_open_goals():
    summary, detail = partial_fixture()
    summary.update(status='complete',web_key='generic-complete-proof')
    with pytest.raises(RuntimeError,match='COMPLETE_NOT_VERIFIED'):
        summarize(summary,detail)
    summary.update(trust_status='VERIFIED',open_goal_count=0)
    detail.update(open_goals=[],frontier=[])
    assert summarize(summary,detail)['root_complete'] is True


@pytest.mark.parametrize('key,value', [('target_given_count',1),('complete_invariants_hold',False),('n',6)])
def test_reject_invalid_summary(key,value):
    summary, detail = partial_fixture()
    summary[key] = value
    with pytest.raises(RuntimeError):
        summarize(summary,detail)


def test_reject_screened_root_given():
    summary, detail = partial_fixture()
    changed = deepcopy(detail)
    changed['screened_source_inventory']['target_group_given_links'] = ['root']
    with pytest.raises(RuntimeError,match='SCREENED_ROOT_GIVEN'):
        summarize(summary,changed)
