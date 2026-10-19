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
from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path: Path, value: dict) -> None:
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    os.replace(tmp, path)


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


def execute(root: Path, results: Path, chunk_size: int, extra: list[str]) -> int:
    results.mkdir(parents=True, exist_ok=True)
    state_path = results / 'state.json'
    collection_path = results / 'collection.log'
    state = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}
    if state.get('status') == 'COMPLETE':
        print('Already complete. See state.json.'); return 0
    if state.get('status') == 'FAILED':
        print('Previous run had test failures. Re-running failed/incomplete batches.')

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
            log = results / f'batch_{i:04}.log'
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
                print(f'FAILED at batch {i}; inspect {log} and rerun to retry.', flush=True)
                return rc
    except KeyboardInterrupt:
        state.update(status='INTERRUPTED', updated_at=utc_now())
        atomic_json(state_path, state)
        print('INTERRUPTED. Completed batches preserved. Rerun to resume.', flush=True)
        return 130
    state.update(status='COMPLETE', current_batch=None, updated_at=utc_now())
    atomic_json(state_path, state)
    print(f'COMPLETE: {len(nodes)} collected tests, {len(groups)} successful batches.', flush=True)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--results', type=Path, required=True)
    parser.add_argument('--chunk-size', type=int, default=40)
    args = parser.parse_args()
    if args.chunk_size < 1:
        parser.error('--chunk-size must be positive')
    return execute(args.root.resolve(), args.results.resolve(), args.chunk_size, [])


if __name__ == '__main__':
    sys.exit(main())
