"""R3R8 contract tests; real checkout validation happens in the worker."""
from __future__ import annotations

import json

import pytest

from phase176_r3r8_lemma57_provider_binding import audit


def test_source_contract_accepts_fixture(tmp_path) -> None:
    for name, anchors in audit.SOURCES.items():
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('\n'.join(anchors), encoding='utf-8')
    assert set(audit.check_sources(tmp_path)) == set(audit.SOURCES)


def test_source_contract_rejects_missing_anchor(tmp_path) -> None:
    for name in audit.SOURCES:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('changed source', encoding='utf-8')
    with pytest.raises(RuntimeError, match='SOURCE_ANCHORS_MISSING'):
        audit.check_sources(tmp_path)


def test_source_bound_provider_rejects_empty_sources() -> None:
    with pytest.raises(ValueError, match='ONE_SCREENED_SOURCE_STEP_REQUIRED'):
        audit.source_bound_provider(lambda goal: (), (), object, lambda goal, refs: ())


def test_source_bound_provider_rejects_non_tuple_sources() -> None:
    with pytest.raises(ValueError, match='ONE_SCREENED_SOURCE_STEP_REQUIRED'):
        audit.source_bound_provider(lambda goal: (), [], object, lambda goal, refs: ())


def test_source_bound_provider_rejects_false_step(monkeypatch) -> None:
    import sys
    from types import SimpleNamespace

    class StubProofStep:
        pass

    monkeypatch.setitem(sys.modules, 'proof', SimpleNamespace(
        ProofStep=StubProofStep,
        ProofRule=SimpleNamespace(GIVEN='given'),
    ))
    with pytest.raises(ValueError, match='INVALID_SCREENED_SOURCE_STEP'):
        audit.source_bound_provider(lambda goal: (), ('string not a ProofStep',), str, lambda goal, refs: ())


def test_worker_rejects_false_completion(monkeypatch) -> None:
    import subprocess

    class Result:
        returncode = 0
        stdout = audit.MARKER + json.dumps({
            'new_given': 0,
            'new_mathematical_rules': 0,
            'root_proof_complete': True,
            'production_provider_modified': False,
            'isolated_base_proof_step_inferred': True,
        })
        stderr = ''

    monkeypatch.setattr(subprocess, 'run', lambda *args, **kwargs: Result())
    with pytest.raises(RuntimeError, match='WORKER_FALSE_PROOF_CLAIM'):
        audit.worker(5)


def test_dry_run_does_not_execute_worker(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(audit, 'preflight', lambda: {'head': 'test'})
    monkeypatch.setattr(audit, 'worker', lambda timeout: pytest.fail('worker called'))
    monkeypatch.setenv('LOCALAPPDATA', str(tmp_path))
    assert audit.execute(True, 5) == 0
    report = json.loads((tmp_path / 'EHPProofTracerAudit' / audit.PACKAGE / 'report.json').read_text(encoding='utf-8'))
    assert report['full_pytest'] == 'NOT_RUN'
    assert report['new_given'] == 0
    assert report['root_proof_complete'] is False
