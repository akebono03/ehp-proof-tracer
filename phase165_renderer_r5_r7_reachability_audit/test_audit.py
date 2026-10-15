"""Unit tests for conservative source-only reachability audit."""
from pathlib import Path
from audit import scan, shortest_path, sources, analyze


def test_shortest_path_direct():
    assert shortest_path({'a': {'b'}, 'b': set()}, 'a', 'b') == ['a','b']


def test_shortest_path_missing():
    assert shortest_path({'a': set(), 'b': set()}, 'a', 'b') is None


def test_scan_import_from_and_calls(tmp_path: Path):
    (tmp_path/'a.py').write_text('from b import go\ndef run():\n    return go()\n',encoding='utf-8')
    (tmp_path/'b.py').write_text('def go():\n    return 1\n',encoding='utf-8')
    result=scan(tmp_path)
    assert 'b.py' in result['graph']['a.py']
    assert {'source':'a.py','target':'b.py','symbol':'go','line':3} in result['calls']


def test_scan_import_as_and_bom(tmp_path: Path):
    (tmp_path/'a.py').write_bytes(b'\xef\xbb\xbffrom b import go as f\nf()\n')
    (tmp_path/'b.py').write_text('def go():\n    pass\n', encoding='utf-8')
    result=scan(tmp_path)
    assert not result['parse_errors']
    assert result['calls'][0]['symbol']=='go'


def test_source_scope_excludes_backup_and_audit(tmp_path: Path):
    for name in ['a.py','a.phase165_backup.py','audit_old.py','probe_x.py']:
        (tmp_path/name).write_text('pass\n',encoding='utf-8')
    assert [p.name for p in sources(tmp_path)] == ['a.py']


def test_audit_does_not_claim_runtime_certification(tmp_path: Path):
    (tmp_path/'web_group_proof.py').write_text('import toda_group_proof_narrative_renderer\n', encoding='utf-8')
    (tmp_path/'toda_group_proof_narrative_renderer.py').write_text('pass\n', encoding='utf-8')
    result=analyze(tmp_path)
    assert result['checks']['web_group_proof_reaches_canonical_module']
    assert result['status']=='REVIEW_REQUIRED'
    assert 'dynamic imports' in ' '.join(result['limitations'])
