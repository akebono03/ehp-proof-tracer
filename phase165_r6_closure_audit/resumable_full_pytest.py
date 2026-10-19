"""Resumable final pytest execution for Phase 165; no production mutation."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path: Path, value: dict) -> None:
    """Retry atomic checkpoint updates when Dropbox temporarily locks the file."""
    tmp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
        for attempt in range(40):
            try:
                os.replace(tmp, path)
                return
            except PermissionError:
                if attempt == 39:
                    raise
                time.sleep(0.25)
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except PermissionError:
                pass


def recover_successful_batch(log: Path, expected_count: int) -> bool:
    """Recover a finished but not checkpointed batch from its complete pytest log."""
    if not log.is_file():
        return False
    content = log.read_text(encoding='utf-8', errors='replace')
    # A complete pytest terminal summary must match the batch size exactly.
    return bool(re.search(r'^' + str(expected_count) + r' passed in [0-9.]+s\s*$',
                          content, flags=re.MULTILINE)) and not bool(
        re.search(r'(?m)^(FAILED|ERROR|INTERNALERROR|Traceback)', content))


def run_logged(command: list[str], path: Path, cwd: Path) -> int:
    """Stream stdout immediately to file and console; Ctrl+C kills child."""
    with path.open('w', encoding='utf-8', errors='backslashreplace') as output:
        proc = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True,
                                encoding='utf-8', errors='replace', bufsize=1,
                                env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})
        try:
            assert proc.stdout is not None
            for line in proc.stdout:
                output.write(line)
                output.flush()
                print(line, end='', flush=True)
            return proc.wait()
        except KeyboardInterrupt:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
            raise


def parse_collected_nodes(log: str) -> list[str]:
    # pytest -q --collect-only produces node IDs on separate lines.
    nodes: list[str] = []
    for line in log.splitlines():
        value = line.strip()
        if '::' in value and not value.startswith(('ERROR ', 'FAILED ', 'warnings ')):
            if re.search(r'\btest_[^\s:]+(?:\[[^\]]+\])?$', value):
                nodes.append(value)
    return nodes


def fingerprint(nodes: list[str]) -> str:
    return hashlib.sha256('\n'.join(nodes).encode('utf-8')).hexdigest()


def execute(root: Path, results: Path, chunk_size: int, extra: list[str], defer_failures: bool = False) -> int:
    results.mkdir(parents=True, exist_ok=True)
    state_path = results / 'state.json'
    collection_path = results / 'collection.log'
    state = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}
    if state.get('status') == 'COMPLETE':
        print('Already complete. See state.json.'); return 0
    if state.get('status') == 'FAILED':
        print('Previous run had test failures. Failed batches are preserved.' if defer_failures else
              'Previous run had test failures. Re-running failed/incomplete batches.')

    # Reject stale or incompatible checkpoints before any execution.
    if state.get('scope') and state['scope'] != extra:
        raise RuntimeError('Scope changed; use a new results directory')
    state['scope'] = extra
    # Snapshot the collection at the first run; keep this exact set for resume.
    nodes_path = results / 'nodeids.json'
    if nodes_path.exists():
        nodes = json.loads(nodes_path.read_text(encoding='utf-8'))
    else:
        state.update(status='COLLECTING', started_at=state.get('started_at', utc_now()))
        atomic_json(state_path, state)
        rc = run_logged([sys.executable, '-m', 'pytest', '--collect-only', '-q',
                         '-o', 'addopts='] + extra, collection_path, root)
        if rc != 0:
            state.update(status='COLLECTION_FAILED', collection_exit=rc,
                         updated_at=utc_now(), collection_log=str(collection_path))
            atomic_json(state_path, state)
            return rc
        nodes = parse_collected_nodes(collection_path.read_text(encoding='utf-8'))
        if not nodes:
            state.update(status='COLLECTION_EMPTY', updated_at=utc_now())
            atomic_json(state_path, state)
            return 2
        nodes_path.write_text(json.dumps(nodes, ensure_ascii=False, indent=2), encoding='utf-8')
    digest = fingerprint(nodes)
    if state.get('fingerprint') and digest != state['fingerprint']:
        raise RuntimeError('Node list changed; cannot resume old checkpoint')
    if state.get('chunk_size') and chunk_size != state['chunk_size']:
        raise RuntimeError('Chunk size changed; rerun with previous chunk size')
    groups = [nodes[i:i+chunk_size] for i in range(0, len(nodes), chunk_size)]
    completed = dict(state.get('completed', {}))
    state.update(status='RUNNING', fingerprint=digest, chunk_size=chunk_size,
                 collected_node_count=len(nodes), batch_total=len(groups),
                 updated_at=utc_now(), completed=completed)
    atomic_json(state_path, state)
    try:
        for i, group in enumerate(groups, 1):
            key = str(i)
            # Both successful and failed batches are retained; only successful batches can be skipped.
            if completed.get(key, {}).get('returncode') == 0:
                continue
            if defer_failures and key in completed and completed[key].get('returncode') != 0:
                print(f'DEFERRED FAILED BATCH {i}/{len(groups)}; original log preserved', flush=True)
                continue
            log = results / f'batch_{i:04}.log'
            if key not in completed and recover_successful_batch(log, len(group)):
                completed[key] = dict(returncode=0, node_count=len(group),
                                      log=str(log), finished_at=utc_now(),
                                      recovered_from_log=True)
                state.update(completed=completed, updated_at=utc_now())
                atomic_json(state_path, state)
                print(f'RECOVERED BATCH {i}/{len(groups)} from validated log', flush=True)
                continue
            state.update(current_batch=i, updated_at=utc_now(), status='RUNNING')
            atomic_json(state_path, state)
            print(f'BATCH {i}/{len(groups)}: {len(group)} tests; log={log}', flush=True)
            rc = run_logged([sys.executable, '-m', 'pytest', '-q', '-o', 'addopts='] + group,
                            log, root)
            completed[key] = dict(returncode=rc, node_count=len(group),
                                  log=str(log), finished_at=utc_now())
            state.update(completed=completed, updated_at=utc_now())
            atomic_json(state_path, state)
            if rc != 0:
                state.update(status='FAILED', failed_batch=i, updated_at=utc_now())
                atomic_json(state_path, state)
                if not defer_failures:
                    print(f'FAILED at batch {i}; inspect {log} and rerun to retry.', flush=True)
                    return rc
                print(f'RECORDED FAILURE at batch {i}; continuing, log={log}', flush=True)
    except KeyboardInterrupt:
        state.update(status='INTERRUPTED', updated_at=utc_now())
        atomic_json(state_path, state)
        print('INTERRUPTED. Completed batches preserved. Rerun to resume.', flush=True)
        return 130
    failed = [int(key) for key, item in completed.items() if item.get('returncode') != 0]
    if failed:
        state.update(status='FAILED', current_batch=None, failed_batches=sorted(failed),
                     executed_batches=len(completed), updated_at=utc_now())
        atomic_json(state_path, state)
        print(f'ALL BATCHES VISITED; FAILED BATCHES: {sorted(failed)}; logs retained.', flush=True)
        return 1
    state.update(status='COMPLETE', current_batch=None, failed_batches=[], updated_at=utc_now())
    atomic_json(state_path, state)
    print(f'COMPLETE: {len(nodes)} collected tests, {len(groups)} successful batches.', flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--results', type=Path, required=True)
    parser.add_argument('--chunk-size', type=int, default=40)
    parser.add_argument('--defer-failed-batches', action='store_true',
                        help='Retain failures and continue remaining batches; never report PASS if failures remain')
    args = parser.parse_args()
    if args.chunk_size < 1:
        parser.error('--chunk-size must be positive')
    root = args.root.resolve()
    scope_path = root / 'phase165_r6_audit_results' / 'collection_scope.json'
    if not scope_path.is_file():
        raise RuntimeError('Missing audited collection_scope.json; cannot run unrestricted pytest')
    scope_data = json.loads(scope_path.read_text(encoding='utf-8-sig'))
    declared = scope_data['scope']
    if not isinstance(declared, list) or not declared or not all(isinstance(p, str) and p for p in declared):
        raise RuntimeError('Invalid collection scope')
    scope = [p for p in declared if (root / p).is_file() or (root / p).is_dir()]
    absent = [p for p in declared if p not in scope]
    if absent:
        raise RuntimeError('Audited scope contains missing paths: ' + ', '.join(absent))
    print('PHASE 165 AUDITED SCOPE: ' + str(len(scope)) + ' paths; no whole-tree discovery', flush=True)
    return execute(root, args.results.resolve(), args.chunk_size, scope,
                   defer_failures=args.defer_failed_batches)


if __name__ == '__main__':
    sys.exit(main())
