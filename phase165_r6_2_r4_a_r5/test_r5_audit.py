from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from r5_audit import audit_adapter, audit_shared, classify_goal, markdown

@dataclass(frozen=True)
class Var:
    name: str


def test_no_conclusion_pattern():
    rule=SimpleNamespace(conclusion_pattern=None,premise_patterns=())
    assert classify_goal(rule,1,lambda r,g:None,lambda x:set(),lambda u:None)=='NO_CONCLUSION_PATTERN'


def test_no_match():
    rule=SimpleNamespace(conclusion_pattern=1,premise_patterns=(1,))
    assert classify_goal(rule,2,lambda r,g:None,lambda x:set(),lambda u:None)=='NO_CONCLUSION_MATCH'


def test_unbound_variable():
    p=SimpleNamespace(relation_pattern=None,statement_pattern='template')
    rule=SimpleNamespace(conclusion_pattern=1,premise_patterns=(p,))
    match=SimpleNamespace(bindings=())
    assert classify_goal(rule,1,lambda r,g:match,lambda x:{'missing'},lambda u:None)=='UNBOUND_VARIABLE'


def test_generated_premises():
    p=SimpleNamespace(relation_pattern=None,statement_pattern='template')
    rule=SimpleNamespace(conclusion_pattern=1,premise_patterns=(p,))
    match=SimpleNamespace(bindings=(SimpleNamespace(variable=Var('known')),))
    assert classify_goal(rule,1,lambda r,g:match,lambda x:{'known'},lambda u:(object(),))=='PREMISES_GENERATED'


def test_adapter_static_only(tmp_path):
    f=tmp_path/'adapter.py'
    f.write_text('def expand_existing_pi43_rules(goal):\n    return (GoalExpansion(toda_rule(), (goal,)),)\n',encoding='utf-8')
    d=audit_adapter(f)
    assert d['status']=='FOUND'
    assert len(d['branches'])==1
    assert d['rule_factories'][0]['symbol']=='toda_rule'
    audit_shared(tmp_path,d)
    assert d['shared_provider_status']=='SOURCE_MISSING'


def test_markdown_report():
    report={'status':'OK','goals_examined':2,'reason_totals':{'NO_CONCLUSION_MATCH':2},'adapter':{'status':'FOUND','rule_factories':[],'branches':[]},'rules':[],'limitations':[]}
    assert 'NO_CONCLUSION_MATCH' in markdown(report)
