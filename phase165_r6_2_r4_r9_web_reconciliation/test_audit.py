from audit import capture_result, safe_stage, render_md
from types import SimpleNamespace


def test_capture_complete_fields():
    result = SimpleNamespace(status='complete', conclusion=1, proven_steps=(SimpleNamespace(conclusion=1, rule='x'),), open_goals=(), diagnostics=(), references=('r',))
    captured = capture_result(result)
    assert captured['proven_step_count'] == 1
    assert captured['references'] == ['r']


def test_capture_unresolved():
    result = SimpleNamespace(status='search_failed', conclusion=None, proven_steps=(), open_goals=('g',), diagnostics=('reason',), references=())
    assert capture_result(result)['open_goals'] == ["'g'"]


def test_safe_stage_ok():
    assert safe_stage('a', lambda: 5)['value'] == 5


def test_safe_stage_error():
    def fail():
        raise ValueError('bad')
    result = safe_stage('x', fail)
    assert result['error_type'] == 'ValueError'


def test_render_md():
    report = {'status':'WEB_CANONICAL_RECONCILIATION_AUDITED','target_count':1,'registry_assertions':2,'proof_links':1,'stages':{'x':{'ok':True,'complete':False,'result':{'status':'failed','proven_step_count':0,'diagnostics':['x'],'open_goals':[1]}}}}
    assert 'ProofStep: 0' in render_md(report)
