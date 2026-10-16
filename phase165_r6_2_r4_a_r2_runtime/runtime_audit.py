"""R4-A-R2 read-only report combining R4-A AST data and bounded runtime R8 discovery."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

from inventory_r4a import audit


def collect(root: Path, *, timeout: int = 90) -> dict:
    root = root.resolve()
    static = audit(root)
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONNOUSERSITE'] = '1'
    command = [sys.executable, '-B', str(Path(__file__).with_name('runtime_probe.py')), str(root)]
    try:
        proc = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True, timeout=timeout, check=False)
        if proc.returncode != 0:
            runtime = {'status': 'PROCESS_ERROR', 'error': proc.stderr[-3000:], 'rules': [], 'skipped_factories': [], 'skipped_rules': []}
        else:
            try:
                runtime = json.loads(proc.stdout)
            except json.JSONDecodeError:
                runtime = {'status': 'OUTPUT_ERROR', 'error': proc.stdout[-1500:] + proc.stderr[-1500:], 'rules': [], 'skipped_factories': [], 'skipped_rules': []}
    except subprocess.TimeoutExpired:
        runtime = {'status': 'TIMEOUT', 'error': f'probe exceeded {timeout}s', 'rules': [], 'skipped_factories': [], 'skipped_rules': []}
    static_candidates = [d for d in static['definitions'] if d['r8_factory_eligible_by_ast']]
    by_module = {}
    for d in static_candidates:
        by_module.setdefault(Path(d['file']).stem, []).append(d['id'])
    runtime['ast_candidate_ids_by_module'] = by_module
    runtime['count_comparison'] = {
        'ast_eligible_factories': len(static_candidates),
        'runtime_instantiated_rules': sum(r.get('status') == 'INSTANTIATED' for r in runtime['rules']),
        'runtime_structural_backward_candidates': sum(r.get('backward_structural_candidate', False) for r in runtime['rules']),
        'runtime_goal_verified': 0,
        'runtime_proof_verified': 0,
        'unresolved_factory_identity': 'R8 returns rule names, not source factory IDs; counts cannot establish a one-to-one match.',
    }
    return {
        'phase': '165 R6-2 R4-A-R2', 'mode': 'READ_ONLY_RUNTIME_DISCOVERY',
        'root': str(root), 'static_summary': static['summary'],
        'connections': static['connections']['paths'], 'runtime': runtime,
        'limitations': [
            'Importing existing production modules can execute their import-time code; probe itself performs no writes.',
            'PYTHONDONTWRITEBYTECODE prevents bytecode writes only, not side effects of imported project modules.',
            'Instantiated rules are not automatically backward applicable to concrete Goals.',
            'Static call edges do not certify runtime search reachability.',
            'No forward proof, mathematical soundness, Goal applicability, or passing existing test is inferred.',
            'Module-by-module R8 discovery may differ from default all-module discovery if modules have cross-import side effects.',
        ],
    }


def markdown(data: dict) -> str:
    c = data['runtime']['count_comparison']
    lines = ['# Phase 165 R6-2 R4-A-R2 実行時収集監査', '',
             f"- 状態: `{data['runtime']['status']}`", f"- 対象: `{data['root']}`", '',
             '## 件数', '', '| 指標 | 件数 |', '|---|---:|',
             f"| R4-A AST 収集対象候補 | {c['ast_eligible_factories']} |",
             f"| 実行時生成された規則 | {c['runtime_instantiated_rules']} |",
             f"| 逆向きパターンの構造候補 | {c['runtime_structural_backward_candidates']} |",
             '| 具体 Goal に対する逆向き適用実証 | 0（未実施） |',
             '| 完成証明の再構成実証 | 0（未実施） |', '',
             '## R8 実行時規則（factory 名との直接対応は未確定）', '',
             '| モジュール | 規則名 | 結論パターン | 前提数 | 逆向き構造候補 |', '|---|---|---|---:|---|']
    for r in data['runtime']['rules']:
        lines.append(f"| `{r.get('module','')}` | `{str(r.get('name','')).replace('|','\\|')}` | {'あり' if r.get('has_conclusion_pattern') else 'なし'} | {r.get('premise_count','—')} | {'候補' if r.get('backward_structural_candidate') else '未確認'} |".replace('\\|', '/'))
    lines += ['', '## 除外 factory', '']
    lines += [f'- `{x}`' for x in data['runtime']['skipped_factories']]
    lines += ['', '## 制約', ''] + [f'- {x}' for x in data['limitations']]
    lines += ['', '## 次段階', '', 'R4-A-R3：source factory の実行時同定、具体的 Goal ごとの逆向き適用、探索到達性を証明成功と分離して検査する。', '']
    return '\n'.join(lines)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--timeout', type=int, default=90)
    args = p.parse_args()
    result = collect(args.root, timeout=args.timeout)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'runtime_capability.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (args.out / 'runtime_capability.md').write_text(markdown(result), encoding='utf-8')
    print(json.dumps({'status': result['runtime']['status'], 'counts': result['runtime']['count_comparison'], 'out': str(args.out)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
