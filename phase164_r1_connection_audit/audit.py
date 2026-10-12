from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path.cwd()
TARGETS = {
    'registry': 'unified_statement_registry.py',
    'bridge': 'phase163_r4_registry_bridge.py',
    'archive': 'phase163_source_archive_registry.py',
    'goal': 'phase161_r5_backward_proof_reconstruction.py',
    'matching': 'phase161_r4_literature_premise_matching.py',
    'provenance': 'phase161_r7_premise_provenance_validation.py',
    'proof': 'proof.py',
    'inference': 'repository_inference.py',
    'renderer': 'phase162_validated_proof_presentation.py',
}
TESTS = (
    'tests/test_phase163_r2_unified_registry.py',
    'tests/test_phase163_r3_registry_validation.py',
    'tests/test_phase163_r4_registry_bridge.py',
    'tests/test_phase161_r5_backward_proof_reconstruction.py',
)


def definitions(tree: ast.AST) -> list[str]:
    return [node.name for node in ast.walk(tree) if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))]


def main() -> int:
    if not (ROOT / 'unified_statement_registry.py').is_file():
        raise SystemExit('Run from repository root, not package folder.')
    files = {}
    for name, relative in TARGETS.items():
        path = ROOT / relative
        if not path.is_file():
            files[name] = {'path': relative, 'present': False}
            continue
        source = path.read_text(encoding='utf-8-sig')
        tree = ast.parse(source, filename=relative)
        files[name] = {'path': relative, 'present': True, 'lines': len(source.splitlines()), 'definitions': definitions(tree)}
    report = {
        'phase': '164 R1',
        'mode': 'READ_ONLY_CONNECTION_AUDIT',
        'repo_root': str(ROOT),
        'modules': files,
        'targeted_tests': [{'path': p, 'present': (ROOT / p).is_file()} for p in TESTS],
        'source_files_modified': False,
        'full_pytest_run': False,
        'r2_policy_questions': [
            'Source archive records are not proof eligible.',
            'Boundary metadata is not a typed mathematical premise.',
            'Publication and availability positions must not be inferred.',
            'Proof-internal ancestry must not be promoted to a fixed reference.',
            'GIVEN-root identity validates provenance structure, not mathematical truth.',
        ],
    }
    output = ROOT / 'phase164_r1_output'
    output.mkdir(exist_ok=True)
    (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Phase 164 R1 — 接続監査', '', '既存 Production コードへの変更なし。', '', '## モジュール', '']
    for name, item in files.items():
        lines.append(f"- {name}: `{item['path']}` — {'確認可能' if item['present'] else '欠落'}")
    lines.extend(['', '## 接続設計', '', '1. R2 で引用資格を判定する独立した境界を設ける。', '2. R3 では既存 ProofStep を渡す経路を利用し、新しい探索器を作らない。', '3. `SOURCE_ARCHIVE`、metadata-only、未確認の掲載順は自動承認しない。', '4. `PROOF_INTERNAL` は祖先証明の検査なしに文献固定事実へ昇格しない。', '5. R4 では E:π₄²→π₅³ の7規則と4つの完全性証人を維持する。', '', '## テスト候補', ''])
    lines.extend(f"- `{x['path']}`: {'あり' if x['present'] else '欠落'}" for x in report['targeted_tests'])
    lines.extend(['', '全体 pytest は未実行。数学的真偽や引用資格の確定は R1 の対象外。', ''])
    (output / 'report.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'phase': report['phase'], 'mode': report['mode'], 'modules_found': sum(x['present'] for x in files.values()), 'modules_total': len(files), 'test_files_found': sum(x['present'] for x in report['targeted_tests']), 'full_pytest_run': False, 'report': str(output / 'report.md')}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
