import importlib.util
import json
from pathlib import Path
from unittest.mock import patch

MODULE = Path(__file__).with_name('resumable_full_pytest.py')
spec = importlib.util.spec_from_file_location('phase165_continue_runner', MODULE)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def test_deferred_failed_batch_preserves_log_and_runs_later(tmp_path):
    root = tmp_path / 'repo'
    results = tmp_path / 'results'
    root.mkdir()
    results.mkdir()
    nodes = [f'tests/test_sample.py::test_{i}' for i in range(3)]
    (results / 'nodeids.json').write_text(json.dumps(nodes), encoding='utf-8')
    failing_log = results / 'batch_0001.log'
    failing_log.write_text('FAILED test_0\n1 failed in 0.1s\n', encoding='utf-8')
    (results / 'state.json').write_text(json.dumps({
        'scope': ['tests'], 'chunk_size': 1, 'fingerprint': runner.fingerprint(nodes),
        'status': 'FAILED', 'completed': {'1': {'returncode': 1, 'node_count': 1, 'log': str(failing_log)}}
    }), encoding='utf-8')
    executed = []

    def fake_run(command, path, cwd):
        executed.append(path.name)
        path.write_text('1 passed in 0.1s\n', encoding='utf-8')
        return 0

    with patch.object(runner, 'run_logged', side_effect=fake_run):
        result = runner.execute(root, results, 1, ['tests'], defer_failures=True)
    state = json.loads((results / 'state.json').read_text(encoding='utf-8'))
    assert result == 1
    assert executed == ['batch_0002.log', 'batch_0003.log']
    assert state['status'] == 'FAILED'
    assert state['failed_batches'] == [1]
    assert state['completed']['1']['returncode'] == 1
    assert 'FAILED test_0' in failing_log.read_text(encoding='utf-8')
    assert state['completed']['2']['returncode'] == 0
    assert state['completed']['3']['returncode'] == 0


def test_default_still_retries_failure_and_stops(tmp_path):
    root = tmp_path / 'repo'
    results = tmp_path / 'results'
    root.mkdir()
    results.mkdir()
    nodes = [f'tests/test_sample.py::test_{i}' for i in range(2)]
    (results / 'nodeids.json').write_text(json.dumps(nodes), encoding='utf-8')
    (results / 'state.json').write_text(json.dumps({
        'scope': ['tests'], 'chunk_size': 1, 'fingerprint': runner.fingerprint(nodes),
        'status': 'FAILED', 'completed': {'1': {'returncode': 1}}
    }), encoding='utf-8')
    called = []
    def fake_run(command, path, cwd):
        called.append(path.name)
        path.write_text('1 failed in 0.1s\n', encoding='utf-8')
        return 1
    with patch.object(runner, 'run_logged', side_effect=fake_run):
        result = runner.execute(root, results, 1, ['tests'])
    assert result == 1
    assert called == ['batch_0001.log']
