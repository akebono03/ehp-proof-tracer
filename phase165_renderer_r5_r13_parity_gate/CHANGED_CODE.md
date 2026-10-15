# 変更コード全文（新規ファイル）

## audit.py

```python
"""R5-R13: read-only compatibility gate for legacy Phase 162 Narrative."""
from __future__ import annotations

import ast
import importlib
import json
import re
import traceback
from datetime import datetime, timezone
from pathlib import Path

LEGACY_MODULE = 'phase162_web_narrative_integration'
CANONICAL_MODULE = 'toda_group_proof_narrative_renderer'
BACKUP = re.compile(r'\.phase\d+_[^/\\]*\.py$', re.I)
ENTRY_POINTS = ('web_group_proof.py', 'main.py', 'cli.py')


def load_tree(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))


def defined(tree: ast.Module, name: str) -> bool:
    return any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name for node in tree.body)


def imported(tree: ast.Module, module: str, symbol: str) -> bool:
    return any(isinstance(node, ast.ImportFrom) and node.module == module and any(alias.name == symbol for alias in node.names) for node in ast.walk(tree))


def canonical_connections(root: Path) -> dict:
    web = load_tree(root / 'web_group_proof.py')
    cli = load_tree(root / 'cli.py')
    main = load_tree(root / 'main.py')
    result = {
        'web_uses_phase165_adapter': imported(web, 'phase165_r52_r3_web_adapter', 'build_partial_web_group_proof_view'),
        'cli_uses_partial_renderer': imported(cli, 'phase165_r52_partial_proof', 'render_partial_proof_markdown'),
        'main_calls_partial_renderer': any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'render_partial_proof_markdown' for node in ast.walk(main)),
    }
    return result


def legacy_dependencies(root: Path) -> dict:
    legacy = load_tree(root / 'phase162_web_narrative_integration.py')
    r3 = load_tree(root / 'phase162_r3_narrative_connection.py')
    replay = load_tree(root / 'phase162_pi5_3_web_replay.py')
    leaves = root / 'phase162_ehp_leaf_inputs.py'
    return {
        'shared_leaves_exist': leaves.is_file(),
        'replay_uses_shared_leaves': imported(replay, 'phase162_ehp_leaf_inputs', '_phase162_ehp_leaves'),
        'legacy_reexports_leaves': imported(legacy, 'phase162_ehp_leaf_inputs', '_phase162_ehp_leaves'),
        'legacy_web_entry_exists': defined(legacy, 'build_phase162_web_validated_isomorphism_markdown'),
        'legacy_web_calls_old_renderer': imported(legacy, 'phase162_r3_narrative_connection', 'render_phase162_r3_narrative'),
        'legacy_r3_entry_exists': defined(r3, 'render_phase162_r3_narrative'),
    }


def classify_exception(exc: BaseException) -> dict:
    return {'status': 'ERROR', 'type': type(exc).__name__, 'message': str(exc)[:500], 'traceback_tail': traceback.format_exception_only(type(exc), exc)[-1].strip()[:500]}


def run_renderer(fn) -> dict:
    try:
        value = fn()
        if not isinstance(value, str):
            return {'status': 'NON_STRING', 'type': type(value).__name__}
        return {'status': 'RENDERED', 'length': len(value), 'sections': [line for line in value.splitlines() if line.startswith('## ')], 'has_unresolved_goal': '未解決 Goal' in value, 'preview': value[:350]}
    except Exception as exc:
        return classify_exception(exc)


def runtime_comparison() -> dict:
    """Try legacy and canonical paths separately. Never infer equality from failures."""
    try:
        old = getattr(importlib.import_module(LEGACY_MODULE), 'build_phase162_web_validated_isomorphism_markdown')
        old_result = run_renderer(old)
    except Exception as exc:
        old_result = classify_exception(exc)
    try:
        search = getattr(importlib.import_module('phase165_r55_nk_only_goal'), 'search_group_from_registered_goal')
        render = getattr(importlib.import_module('phase165_r52_partial_proof'), 'render_partial_proof_markdown')
        new_result = run_renderer(lambda: render(search(n=3, k=2)))
    except Exception as exc:
        new_result = classify_exception(exc)
    comparable = old_result['status'] == 'RENDERED' and new_result['status'] == 'RENDERED'
    return {'legacy': old_result, 'canonical': new_result, 'both_rendered': comparable,
            'semantic_parity_proven': False,
            'decision': 'REVIEW_OUTPUTS_NO_AUTOMATIC_REPLACEMENT' if comparable else 'BLOCKED_RUNTIME_INPUTS_NO_AUTOMATIC_REPLACEMENT'}


def audit(root: Path, *, runtime: bool = True) -> dict:
    root = root.resolve()
    try:
        connections = canonical_connections(root)
        dependencies = legacy_dependencies(root)
    except (OSError, UnicodeError, SyntaxError) as exc:
        return {'phase': '165 R5-R13', 'status': 'PRECONDITION_FAILED', 'error': str(exc), 'full_pytest_run': False}
    guards = {**connections, **dependencies}
    guards['legacy_path_not_in_public_entry_imports'] = all(
        not any(isinstance(node, ast.ImportFrom) and node.module in (LEGACY_MODULE, 'phase162_r3_narrative_connection') for node in ast.walk(load_tree(root / entry)))
        for entry in ENTRY_POINTS
    )
    result = {'phase': '165 R5-R13', 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
              'guards': guards, 'runtime': None, 'full_pytest_run': False,
              'scope': 'read_only; legacy vs canonical pi5^3 display gate'}
    if not all(guards.values()):
        result['status'] = 'PRECONDITION_FAILED'
    else:
        result['runtime'] = runtime_comparison() if runtime else {'status': 'NOT_RUN'}
        result['status'] = 'REVIEW_REQUIRED'
    return result


def report(result: dict) -> str:
    lines = ['# Phase 165 R5-R13 旧 Narrative 置換適合性監査', '', f"判定: **{result['status']}**", '', '## 前提条件']
    for key, val in result.get('guards', {}).items():
        lines.append(f'- {key}: {"PASS" if val else "FAIL"}')
    lines += ['', '## 実行時の表示結果', '']
    r = result.get('runtime')
    if r and 'legacy' in r:
        for k in ('legacy', 'canonical'):
            v = r[k]
            lines.append(f"### {k}: {v['status']}")
            if v['status'] == 'RENDERED':
                lines.append(f"- 文字数: {v['length']}")
                lines.append('- 見出し: ' + ', '.join(v['sections']))
            else:
                lines.append(f"- 原因: {v.get('type', 'unknown')}: {v.get('message', '')}")
            lines.append('')
        lines.append(f"- 比較結果: {r['decision']}")
    else:
        lines.append('実行時比較なし（前提条件未充足または明示的な省略）')
    lines += ['', '## 境界', '- 結果の文字列や見出しの一致は数学的意味の一致を証明しない。',
              '- 旧 Phase 162 の fixture が空の場合は失敗を記録し、旧経路を自動置換しない。',
              '- 既存ソース、テスト、Reference、ProofStep は変更しない。',
              '- 旧 Phase 162 の6件の既知テスト失敗は未解決。',
              '- 全体 pytest は Phase 165 最終段階でのみ実施。', '']
    return '\n'.join(lines)


def main() -> int:
    project = Path(__file__).resolve().parent.parent
    result = audit(project)
    out = Path(__file__).resolve().parent / 'audit_output'
    out.mkdir(exist_ok=True)
    (out / 'audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (out / 'review.md').write_text(report(result), encoding='utf-8')
    print(json.dumps({'status': result['status'], 'guards': result.get('guards', {}),
          'runtime': None if result['runtime'] is None else {key: value.get('status') if isinstance(value, dict) else value for key, value in result['runtime'].items() if key in ('legacy', 'canonical', 'decision', 'semantic_parity_proven')},
          'report': str(out / 'review.md'), 'full_pytest_run': False}, ensure_ascii=False, indent=2))
    return 0 if result['status'] == 'REVIEW_REQUIRED' else 1


if __name__ == '__main__':
    raise SystemExit(main())

```

## test_audit.py

```python
"""Focused tests for the R5-R13 audit; no application fixtures."""
from pathlib import Path

from audit import classify_exception, defined, imported, load_tree, report, run_renderer


def test_imported_symbol_detection(tmp_path: Path):
    path = tmp_path / 'a.py'
    path.write_text('from phase162_ehp_leaf_inputs import _phase162_ehp_leaves\n', encoding='utf-8')
    tree = load_tree(path)
    assert imported(tree, 'phase162_ehp_leaf_inputs', '_phase162_ehp_leaves')
    assert not imported(tree, 'other', '_phase162_ehp_leaves')


def test_bom_is_supported(tmp_path: Path):
    path = tmp_path / 'a.py'
    path.write_bytes(b'\xef\xbb\xbfdef f():\n    return 1\n')
    assert defined(load_tree(path), 'f')


def test_defined_functions():
    import ast
    tree = ast.parse('def first():\n    pass\n')
    assert defined(tree, 'first')
    assert not defined(tree, 'other')


def test_runtime_renderer_produces_sections():
    result = run_renderer(lambda: '## 証明対象\n\n## 証明\n')
    assert result['status'] == 'RENDERED'
    assert result['sections'] == ['## 証明対象', '## 証明']


def test_runtime_renderer_reports_failures_without_success():
    def fail():
        raise IndexError('tuple index out of range')
    result = run_renderer(fail)
    assert result['status'] == 'ERROR'
    assert result['type'] == 'IndexError'


def test_runtime_renderer_rejects_non_string():
    assert run_renderer(lambda: None)['status'] == 'NON_STRING'


def test_exception_classification():
    result = classify_exception(ValueError('invalid'))
    assert result['status'] == 'ERROR'
    assert result['type'] == 'ValueError'


def test_report_handles_blocked_precondition():
    text = report({'status': 'PRECONDITION_FAILED', 'guards': {'missing': False}, 'runtime': None})
    assert 'FAIL' in text
    assert '自動置換しない' in text


def test_report_handles_comparable_output():
    result = {'status': 'REVIEW_REQUIRED', 'guards': {'valid': True}, 'runtime': {
        'legacy': {'status': 'RENDERED', 'length': 5, 'sections': ['## 証明']},
        'canonical': {'status': 'ERROR', 'type': 'ValueError', 'message': 'bad'},
        'decision': 'BLOCKED_RUNTIME_INPUTS_NO_AUTOMATIC_REPLACEMENT'}}
    assert 'ValueError' in report(result)

```

## run.ps1

```powershell
$ErrorActionPreference = 'Stop'
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $folder
$env:PYTHONPATH = "$folder;$project"
Push-Location $project
try {
    python -m pytest -q "$folder\test_audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'R5-R13 focused audit unit tests failed.' }
    python "$folder\audit.py"
    if ($LASTEXITCODE -ne 0) { throw 'R5-R13 preconditions failed. No application files changed.' }
    Write-Host 'R5-R13 comparison evidence saved. Legacy Narrative NOT retired. Full pytest NOT run.'
}
finally { Pop-Location }

```

