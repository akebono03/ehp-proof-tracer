# R52-R21 変更一覧とコード全文

新規ファイルのみ。既存クラス・関数・importは変更なし。

- `phase165_r52_r21_rule_inventory.py`: `_name`, `_functions`, `_names_called`, `_rule_name`, `_production_files`, `audit_rule_inventory`, `write_audit`, `main`（すべて新規）。
- `test_phase165_r52_r21_rule_inventory.py`: テスト関数4件と import（すべて新規）。
- `run.ps1`: 実行コマンド（新規）。
- `README.md`: 英語のパッケージ説明（新規）。

実行する pytest: `python -m pytest -q <package>/test_phase165_r52_r21_rule_inventory.py`。全体 pytest は Phase 最後のみ。

完了条件: 読み取り専用で AST 定義一覧・呼び出し候補・共通接続の直接参照が出力される。間接参照は未接続と断定しない。次 Phase では監査結果を人手で分類し、既存規則の再利用可能性を検討。

## `phase165_r52_r21_rule_inventory.py` 全文

```python
"""Read-only AST inventory of inference-rule factories and shared-search wiring."""
from __future__ import annotations

import argparse
import ast
import csv
import json
from collections import Counter
from pathlib import Path

EXCLUDED_DIRS = {'.git', '.venv', 'venv', '__pycache__', 'node_modules', '.pytest_cache', 'build', 'dist'}
FACTORY_CALLS = {'InferenceRule'}


def _name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return _name(node.value) + '.' + node.attr
    return ''


def _functions(tree: ast.AST):
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield node


def _names_called(node: ast.AST) -> set[str]:
    return {_name(call.func) for call in ast.walk(node) if isinstance(call, ast.Call)}


def _rule_name(call: ast.Call) -> str:
    for keyword in call.keywords:
        if keyword.arg == 'name' and isinstance(keyword.value, ast.Constant) and isinstance(keyword.value.value, str):
            return keyword.value.value
    return '<dynamic rule name>'


def _production_files(root: Path) -> list[Path]:
    result = []
    for file in root.rglob('*.py'):
        parts = file.relative_to(root).parts
        if any(part in EXCLUDED_DIRS for part in parts):
            continue
        if file.name.startswith(('test_', 'conftest')):
            continue
        if any(part.startswith('phase') and ('backup' in part.lower() or 'output' in part.lower()) for part in parts[:-1]):
            continue
        if any(token in file.name.lower() for token in ('.bak', '_backup', 'pre_cleanup', '_pre_fix')):
            continue
        result.append(file)
    return sorted(result)


def audit_rule_inventory(root: Path) -> dict:
    root = Path(root).resolve()
    rules = []
    callers: dict[str, list[str]] = {}
    parses = []
    functions = []
    shared_providers = set()
    shared_file = root / 'phase165_r52_r9_shared_math.py'
    if shared_file.exists():
        tree = ast.parse(shared_file.read_text(encoding='utf-8-sig'), filename=str(shared_file))
        for fn in _functions(tree):
            if fn.name == 'shared_expansion_provider':
                shared_providers = {n.split('.')[-1] for n in _names_called(fn)}
                # Also retain explicit provider references passed as tuple elements.
                for item in ast.walk(fn):
                    if isinstance(item, (ast.Name, ast.Attribute)):
                        shared_providers.add(_name(item).split('.')[-1])
    for path in _production_files(root):
        relative = str(path.relative_to(root)).replace('\\', '/')
        try:
            tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
        except (SyntaxError, UnicodeError) as error:
            parses.append({'file': relative, 'error': str(error)})
            continue
        for fn in _functions(tree):
            calls = _names_called(fn)
            functions.append({'file': relative, 'name': fn.name, 'calls': calls})
            for name in calls:
                callers.setdefault(name.split('.')[-1], []).append(f'{relative}:{fn.lineno}:{fn.name}')
            for call in ast.walk(fn):
                if isinstance(call, ast.Call) and _name(call.func).split('.')[-1] in FACTORY_CALLS:
                    rules.append({'file': relative, 'function': fn.name, 'line': call.lineno,
                                  'rule_name': _rule_name(call)})
    for rule in rules:
        fn = rule['function']
        sites = sorted(set(callers.get(fn, [])))
        # Static reachability: only direct named provider calls are verified.
        if fn in shared_providers:
            status = 'DIRECT_SHARED_PROVIDER_REFERENCE'
        elif any(s.split(':')[0] == 'phase165_r52_r9_shared_math.py' for s in sites):
            status = 'DIRECT_SHARED_CALL'
        elif sites:
            status = 'OTHER_CALLERS_NO_DIRECT_SHARED_LINK'
        else:
            status = 'NO_STATIC_CALLERS'
        rule.update(status=status, caller_count=len(sites), caller_examples=sites[:8])
    providers = []
    for f in functions:
        if f['name'] in shared_providers:
            providers.append({'file': f['file'], 'function': f['name']})
    return {'phase': '165 R52-R21', 'mode': 'READ_ONLY_AST_CANDIDATE_INVENTORY',
            'root': str(root), 'scanned_production_files': len(_production_files(root)),
            'rule_factory_calls': len(rules), 'status_counts': dict(Counter(x['status'] for x in rules)),
            'shared_provider_names': sorted(shared_providers), 'provider_definition_matches': providers,
            'parse_errors': parses, 'rules': rules,
            'limitations': [
                'A factory call is not necessarily a distinct semantic rule; dynamic rules and aliases may be missed.',
                'OTHER_CALLERS_NO_DIRECT_SHARED_LINK is a candidate for review, NOT proof of disconnection.',
                'AST cannot establish indirect imports, decorators, dispatch, rule soundness or actual reachability.',
                'Files under backup/output folders are excluded; check historical rules separately.',
                'No production sources, Registry entries, or pytest configuration are modified.'
            ], 'full_pytest_run': False}


def write_audit(root: Path, output: Path) -> dict:
    report = audit_rule_inventory(root)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'inventory.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with (output / 'rules.csv').open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=['file', 'function', 'line', 'rule_name', 'status', 'caller_count', 'caller_examples'])
        writer.writeheader()
        for rule in report['rules']:
            writer.writerow({**rule, 'caller_examples': ' | '.join(rule['caller_examples'])})
    lines = ['# Phase 165 R52-R21 推論規則棚卸し', '', '## 集計', '',
             f"- 走査ファイル数: {report['scanned_production_files']}",
             f"- `InferenceRule(...)` 構築箇所: {report['rule_factory_calls']}"]
    for status, count in sorted(report['status_counts'].items()):
        lines.append(f'- {status}: {count}')
    lines += ['', '## 重点確認：商群・核・像・完全性', '']
    words = ('quotient', 'kernel', 'image', 'exact', 'surject', 'cyclic', 'pi4_3', 'pi_4^3')
    for rule in report['rules']:
        if any(w in (rule['file'] + ' ' + rule['rule_name'] + ' ' + rule['function']).lower() for w in words):
            lines.append(f"- `{rule['file']}:{rule['line']}` `{rule['function']}` — {rule['rule_name']} — **{rule['status']}**")
    lines += ['', '## 解釈上の注意', ''] + ['- ' + line for line in report['limitations']]
    (output / 'review.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = write_audit(args.root, args.output)
    print(json.dumps({key: result[key] for key in ('phase', 'mode', 'scanned_production_files', 'rule_factory_calls', 'status_counts', 'full_pytest_run')}, ensure_ascii=False, indent=2))
    print('Review:', args.output / 'review.md')
    print('Details:', args.output / 'rules.csv')


if __name__ == '__main__':
    main()

```

## `test_phase165_r52_r21_rule_inventory.py` 全文

```python
from pathlib import Path

from phase165_r52_r21_rule_inventory import audit_rule_inventory, write_audit


def test_r21_categorizes_rule_factories_without_importing_production(tmp_path: Path):
    (tmp_path / 'example.py').write_text('''from proof import InferenceRule\ndef first_rule():\n    return InferenceRule(name="first")\ndef unused_rule():\n    return InferenceRule(name="unused")\ndef another():\n    return first_rule()\n''', encoding='utf-8')
    (tmp_path / 'phase165_r52_r9_shared_math.py').write_text('''def shared_expansion_provider():\n    first_rule()\n''', encoding='utf-8')
    result = audit_rule_inventory(tmp_path)
    keyed = {r['function']: r for r in result['rules']}
    assert keyed['first_rule']['status'] == 'DIRECT_SHARED_PROVIDER_REFERENCE'
    assert keyed['unused_rule']['status'] == 'NO_STATIC_CALLERS'


def test_r21_does_not_label_indirect_rules_as_proven_unconnected(tmp_path: Path):
    (tmp_path / 'example.py').write_text('''def old_rule():\n    return InferenceRule(name="old")\ndef wrapper():\n    return old_rule()\n''', encoding='utf-8')
    result = audit_rule_inventory(tmp_path)
    assert result['rules'][0]['status'] == 'OTHER_CALLERS_NO_DIRECT_SHARED_LINK'
    assert 'NOT proof of disconnection' in result['limitations'][1]


def test_r21_emits_json_csv_and_review(tmp_path: Path):
    (tmp_path / 'a.py').write_text('''def r():\n    return InferenceRule(name="quotient")\n''', encoding='utf-8')
    output = tmp_path / 'audit'
    result = write_audit(tmp_path, output)
    assert result['rule_factory_calls'] == 1
    assert all((output / name).exists() for name in ('inventory.json', 'rules.csv', 'review.md'))
    assert result['full_pytest_run'] is False


def test_r21_skips_tests_and_backup_paths(tmp_path: Path):
    (tmp_path / 'test_x.py').write_text('''def t():\n    InferenceRule(name="test")\n''', encoding='utf-8')
    folder = tmp_path / 'phase159_backup'
    folder.mkdir()
    (folder / 'old.py').write_text('''def t():\n    InferenceRule(name="backup")\n''', encoding='utf-8')
    assert audit_rule_inventory(tmp_path)['rule_factory_calls'] == 0

```

## `run.ps1` 全文

```powershell
$ErrorActionPreference = 'Stop'
$project = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = "$package;$project"
python -m pytest -q "$package/test_phase165_r52_r21_rule_inventory.py"
if ($LASTEXITCODE -ne 0) { throw 'R21 targeted pytest failed' }
python "$package/phase165_r52_r21_rule_inventory.py" --root "$project" --output "$package/audit_output"
if ($LASTEXITCODE -ne 0) { throw 'R21 inventory failed' }
Write-Output 'R21 read-only inventory completed; full pytest NOT run.'

```

## `README.md` 全文

```markdown
# Phase 165 R52-R21 — Existing Inference Rule Inventory

This package provides a read-only AST-based inventory of `InferenceRule(...)` construction sites and their statically visible callers. It compares rule factories with the shared backward search provider without assuming that an absence of a direct call means an unused rule. Run `run.ps1` from the project root after extraction. The script runs targeted tests and writes `audit_output/inventory.json`, `rules.csv`, and `review.md` next to the package. No existing implementation is patched; no complete pytest suite is run. This inventory is only the first pass: indirect calls, dynamic dispatch and historical backup sources require separate manual review.

```