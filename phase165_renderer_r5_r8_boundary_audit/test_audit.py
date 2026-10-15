"""Focused tests for the R5-R8 inspection algorithm."""
from pathlib import Path

from audit import investigate, render_report, shortest_path, active_sources


def test_shortest_path_tracks_import_chain():
    graph = {'a.py': {'b.py'}, 'b.py': {'c.py'}, 'c.py': set()}
    assert shortest_path(graph, 'a.py', 'c.py') == ['a.py', 'b.py', 'c.py']


def test_shortest_path_rejects_disconnected_modules():
    graph = {'a.py':set(), 'b.py':set()}
    assert shortest_path(graph,'a.py','b.py') is None


def test_active_sources_does_not_include_backups(tmp_path: Path):
    for name in ('web_group_proof.py','web_group_proof.phase165_r48_backup.py','audit_old.py'):
        (tmp_path/name).write_text('pass\n',encoding='utf-8')
    assert [p.name for p in active_sources(tmp_path)] == ['web_group_proof.py']


def test_investigate_finds_legacy_callers_and_public_isolation(tmp_path: Path):
    (tmp_path/'web_group_proof.py').write_text('from canonical import entry\n\ndef route():\n    return entry()\n',encoding='utf-8')
    (tmp_path/'canonical.py').write_text('def entry():\n    return 1\n',encoding='utf-8')
    (tmp_path/'phase162_web_narrative_integration.py').write_text('from phase162_r3_narrative_connection import render_phase162_r3_narrative\n\ndef old():\n    return render_phase162_r3_narrative()\n',encoding='utf-8')
    (tmp_path/'phase162_r3_narrative_connection.py').write_text('def render_phase162_r3_narrative():\n    return "old"\n',encoding='utf-8')
    result=investigate(tmp_path)
    assert result['checks']['legacy_phase162_web_has_no_public_import_route']
    assert len(result['legacy_import_calls']) == 1
    assert result['legacy_import_calls'][0]['symbol']=='render_phase162_r3_narrative'


def test_investigate_detects_public_import_of_legacy(tmp_path: Path):
    (tmp_path/'web_group_proof.py').write_text('from phase162_web_narrative_integration import old\n',encoding='utf-8')
    (tmp_path/'phase162_web_narrative_integration.py').write_text('def old():\n    return 1\n',encoding='utf-8')
    data=investigate(tmp_path)
    assert not data['checks']['legacy_phase162_web_has_no_public_import_route']


def test_report_contains_actual_paths_and_limitations(tmp_path: Path):
    (tmp_path/'web_group_proof.py').write_text('pass\n',encoding='utf-8')
    report=render_report(investigate(tmp_path))
    assert '公開入口' in report
    assert '限界' in report
    assert 'web_group_proof.py' in report
