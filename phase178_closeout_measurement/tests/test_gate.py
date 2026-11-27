import xml.etree.ElementTree as ET

import pytest

from phase178_closeout_measurement.gate import (
    EXPECTED, EXPECTED_K6, inspect_junit, split_scope, validate_k6,
    validate_prior, validate_scope,
)


def test_scope_excludes_stable_and_future():
    active, stable, future = split_scope((*EXPECTED, (8,6), (3,7), (2,0)), lambda n,k:n >= k+2)
    assert active == EXPECTED
    assert stable == ((8,6), (2,0))
    assert future == ((3,7),)
    assert len(active) == 21


def test_duplicate_coordinates_rejected():
    with pytest.raises(RuntimeError, match='DUPLICATE'):
        split_scope(((2,1),(2,1)), lambda n,k:False)


def test_exact_scope_count():
    validate_scope(EXPECTED, range(313), range(497))
    with pytest.raises(RuntimeError):
        validate_scope(EXPECTED[:-1], range(313), range(498))
    with pytest.raises(RuntimeError):
        validate_scope(EXPECTED, range(312), range(498))


def prior():
    return dict(n=3,k=5,status='complete',open_goal_count=0,open_goals=[],root_step_count=1,
                conclusion='typed group',web={'status':'rendered'},complete_invariants_hold=True)


def test_prior_valid():
    validate_prior(3,5,prior())


@pytest.mark.parametrize('key,value', [('n',4),('status','partial'),('open_goal_count',1),('open_goals',['x']),
    ('root_step_count',0),('conclusion',None),('web',{'status':'failed'}),('complete_invariants_hold',False)])
def test_prior_invalid(key,value):
    row=prior()
    row[key]=value
    with pytest.raises(RuntimeError):
        validate_prior(3,5,row)


def k6(n):
    steps,given,inference,citations=EXPECTED_K6[n]
    return dict(summary=dict(n=n,k=6,status='complete',trust_status='VERIFIED',open_goal_count=0,target_given_count=0,
        web_key='generic-complete-proof',complete_invariants_hold=True,web_error=None,proven_step_count=steps),
        root_ancestor_count=steps,given_count=given,inference_count=inference,model_citation_count=citations,
        model_citations=[{} for _ in range(citations)],citation_headings=list(range(1,citations+1)),citation_audit='VERIFIED')


@pytest.mark.parametrize('n',range(2,8))
def test_k6_valid(n):
    validate_k6(n,k6(n))


@pytest.mark.parametrize('key,value', [('status','partial'),('trust_status','UNKNOWN'),('open_goal_count',1),
    ('target_given_count',1),('web_key','generic-partial-proof'),('complete_invariants_hold',False),('web_error','error'),('proven_step_count',0)])
def test_k6_summary_invalid(key,value):
    row=k6(7)
    row['summary'][key]=value
    with pytest.raises(RuntimeError):
        validate_k6(7,row)


@pytest.mark.parametrize('key,value', [('given_count',0),('root_ancestor_count',0),('citation_audit','UNKNOWN'),('model_citations',[]),('citation_headings',[])])
def test_k6_model_invalid(key,value):
    row=k6(7)
    row[key]=value
    with pytest.raises(RuntimeError):
        validate_k6(7,row)


def junit(tmp_path,tag=None):
    suite=ET.Element('testsuite')
    case=ET.SubElement(suite,'testcase',name='test_one')
    if tag:
        ET.SubElement(case,tag)
    path=tmp_path/'test.xml'
    ET.ElementTree(suite).write(path,encoding='utf-8')
    return path


def test_junit_pass(tmp_path):
    assert inspect_junit(junit(tmp_path),0,1,expected_count=1)==1


@pytest.mark.parametrize('tag',['failure','error','skipped'])
def test_junit_nonpass(tmp_path,tag):
    with pytest.raises(RuntimeError):
        inspect_junit(junit(tmp_path,tag),0,1)


def test_junit_exit_or_count(tmp_path):
    path=junit(tmp_path)
    for code,minimum,expected in [(1,1,None),(0,2,None),(0,1,2)]:
        with pytest.raises(RuntimeError):
            inspect_junit(path,code,minimum,expected_count=expected)
