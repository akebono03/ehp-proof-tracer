from copy import deepcopy

import pytest

from phase178_r14_n5_source_first_audit.audit import ANCHORS, source_evidence, summarize


def source_fixture():
    return '\n'.join((
        ANCHORS[0]+r'\pi^{2n+1}_{n+7}\to\pi^{n}_{n+5} n=4,5,6 単射\end{equation}',
        ANCHORS[1]+r'\pi^{3}_{9}=0,\pi^{4}_{10}=\mathbb Z_8,\pi^{n}_{n+6}=\mathbb Z_2\end{proposition}',
        ANCHORS[2]+r'\Delta(\nu_9)=\pm\,2(\nu_4^{2})\end{equation}',
    ))


def test_source_order():
    assert list(source_evidence(source_fixture())['anchor_lines'].values()) == [1,2,3]
    with pytest.raises(RuntimeError,match='SOURCE_ORDER'):
        source_evidence('\n'.join(reversed(source_fixture().splitlines())))
    with pytest.raises(RuntimeError,match='EQ513'):
        source_evidence(source_fixture().replace(r'\,2',r'\,4'))


def fixture():
    summary={'n':5,'k':6,'status':'partial','web_error':None,'web_key':'generic-partial-proof',
             'target_given_count':0,'complete_invariants_hold':True,'open_goal_count':1,'trust_status':'NOT_APPLICABLE_PARTIAL'}
    goal={'type':'test','repr':'goal'}
    detail={'open_goals':[goal],'frontier':[{'goal':goal,'state':'CANDIDATES_PRESENT',
             'observed_expansions':[{'options':[{'rule':'one'},{'rule':'one'},{'rule':'two'}]}]}],
            'provider_calls':[{}],'screened_source_inventory':{},'search_context':{}}
    return summary,detail


def test_partial_candidates_not_proof():
    summary,detail=fixture()
    output=summarize(summary,detail)
    assert not output['root_complete']
    assert output['frontier'][0]['rules']==['one','two']


@pytest.mark.parametrize('key,value,message',[('n',6,'WRONG_TARGET'),('target_given_count',1,'TARGET_GIVEN'),
    ('status','worker_timeout','UNMEASURED'),('web_error','error','WEB_GAP'),('complete_invariants_hold',False,'TRUST_CONTRACT')])
def test_bad_summary_rejected(key,value,message):
    summary,detail=fixture()
    summary[key]=value
    with pytest.raises(RuntimeError,match=message):
        summarize(summary,detail)


def test_complete_requires_verified_root():
    summary,detail=fixture()
    summary.update(status='complete',open_goal_count=0,web_key='generic-complete-proof',trust_status='VERIFIED')
    detail.update(open_goals=[],frontier=[])
    assert summarize(summary,detail)['root_complete']
    wrong=deepcopy(summary)
    wrong['trust_status']='NOT_VERIFIED_COMPLETE'
    with pytest.raises(RuntimeError,match='COMPLETE_NOT_VERIFIED'):
        summarize(wrong,detail)
