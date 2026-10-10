# Phase 163 R4-R3 変更内容と全文

既存ファイルの変更なし。新規2 Pythonファイル、run.ps1を追加。
実行対象: tests/test_phase163_r4_r3_statement_mapping.py のみ。全体 pytest は行わない。

## 変更ファイル、クラス、関数

- phase163_r4_r3_statement_mapping.py: `_name`, `_literal_dict`, `_dict_assignments`, `_components`, `_rule_sites`, `analyze`, `write_audit`（すべて新規）
- tests/test_phase163_r4_r3_statement_mapping.py: 6 テスト関数（すべて新規）
- run.ps1: インストール・focused pytest・監査実行（新規）

## 制約と判定

- `candidate_mapped_metadata_only` は命題内容の一致ではなく規則名の対応候補。
- 同一命題・特殊化・引用可能位置・Definition の完全性は未確定。
- `InferenceRule` の動的生成名は `dynamic_name_unverified` として保存。
- 対象ファイルは一部の規則ファイルに限定。すべての登録経路の完了を主張しない。
- 次段階では実際の Statement object と ProofStep provenance を照合する。

## phase163_r4_r3_statement_mapping.py

```python
"""Read-only Phase 163 R4-R3 structural mapping audit.

A rule-name mapping is a candidate correspondence, never a proof of
mathematical equality or citation availability.
"""
from __future__ import annotations

import ast
import csv
import json
from collections import Counter
from pathlib import Path


def _name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _literal_dict(node: ast.AST) -> dict[str, str | None]:
    try:
        value = ast.literal_eval(node)
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        return {}
    if not isinstance(value, dict):
        return {}
    return {k: v for k, v in value.items()
            if isinstance(k, str) and (v is None or isinstance(v, str))}


def _dict_assignments(tree: ast.Module, variable: str) -> dict[str, str | None]:
    result: dict[str, str | None] = {}
    # Top-level only; avoid inspecting shadowed local assignments.
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == variable
            for target in node.targets
        ):
            result = _literal_dict(node.value)
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call = node.value
            if (_name(call.func) == 'update' and
                    isinstance(call.func, ast.Attribute) and
                    isinstance(call.func.value, ast.Name) and
                    call.func.value.id == variable and len(call.args) == 1):
                result.update(_literal_dict(call.args[0]))
    return result


def _components(tree: ast.Module) -> dict[tuple[str, str], dict[str, object]]:
    records: dict[tuple[str, str], dict[str, object]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or _name(node.func) != 'TodaFixedStatementComponent':
            continue
        keywords = {keyword.arg: keyword.value for keyword in node.keywords if keyword.arg}
        try:
            locator = ast.literal_eval(keywords['reference_locator'])
            key = ast.literal_eval(keywords['component_key'])
        except (KeyError, TypeError, ValueError, SyntaxError):
            continue
        if not isinstance(locator, str) or not isinstance(key, str):
            continue
        role = keywords.get('statement_role')
        role_name = _name(role) if role is not None else None
        position = keywords.get('order')
        try:
            order = ast.literal_eval(position) if position is not None else None
        except (ValueError, TypeError, SyntaxError):
            order = None
        record_key = (locator, key)
        if record_key in records:
            raise ValueError(f'duplicate boundary component: {record_key}')
        records[record_key] = {'locator': locator, 'key': key, 'role': role_name,
                               'component_order': order, 'line': node.lineno}
    return records


def _rule_sites(tree: ast.Module, filename: str) -> list[dict[str, object]]:
    result = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or _name(node.func) != 'InferenceRule':
            continue
        name_node = next((k.value for k in node.keywords if k.arg == 'name'), None)
        rule_name = None
        if name_node is not None:
            try:
                literal = ast.literal_eval(name_node)
                if isinstance(literal, str):
                    rule_name = literal
            except (ValueError, TypeError, SyntaxError):
                pass
        result.append({'file': filename, 'line': node.lineno, 'name': rule_name})
    return result


def analyze(boundary_source: str, rule_sources: dict[str, str]) -> dict[str, object]:
    boundary = ast.parse(boundary_source)
    components = _components(boundary)
    component_mapping = _dict_assignments(boundary, '_FIXED_RULE_COMPONENT_KEYS')
    locator_mapping = _dict_assignments(boundary, '_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME')
    rows: list[dict[str, object]] = []
    for rule_name in sorted(set(component_mapping) | set(locator_mapping)):
        key = component_mapping.get(rule_name)
        locator = locator_mapping.get(rule_name)
        if locator is None:
            status = 'locator_unresolved'
        elif key is None:
            status = 'aggregate_or_no_component'
        elif (locator, key) not in components:
            status = 'component_not_in_catalog'
        else:
            status = 'candidate_mapped_metadata_only'
        rows.append({'rule_name': rule_name, 'locator': locator or '',
                     'component_key': key or '', 'status': status,
                     'source': 'boundary_rule_name_mapping'})
    sites: list[dict[str, object]] = []
    for filename, source in sorted(rule_sources.items()):
        sites.extend(_rule_sites(ast.parse(source, filename=filename), filename))
    mapped_names = {str(row['rule_name']) for row in rows}
    rule_sites = []
    for site in sites:
        rule_sites.append({**site, 'status': 'dynamic_name_unverified' if site['name'] is None
                           else ('listed_in_boundary_mapping' if site['name'] in mapped_names
                                 else 'not_listed_in_boundary_mapping')})
    mapped_components = {(str(row['locator']), str(row['component_key'])) for row in rows
                         if row['status'] == 'candidate_mapped_metadata_only'}
    unlinked_components = [{**item, 'status': 'no_explicit_rule_name_mapping'}
                           for identity, item in sorted(components.items())
                           if identity not in mapped_components]
    return {
        'mapping_rows': rows,
        'rule_sites': rule_sites,
        'unlinked_components': unlinked_components,
        'counts': {
            'boundary_components': len(components),
            'boundary_rule_mapping_names': len(rows),
            'rule_constructor_sites': len(sites),
            'unlinked_boundary_components': len(unlinked_components),
            'mapping_status': dict(sorted(Counter(str(r['status']) for r in rows).items())),
            'site_status': dict(sorted(Counter(str(r['status']) for r in rule_sites).items())),
        },
    }


def write_audit(root: Path, output: Path) -> dict[str, object]:
    boundary_path = root / 'toda_literature_statement_boundary.py'
    if not boundary_path.is_file():
        raise FileNotFoundError(boundary_path)
    rule_names = ('toda_rules.py', 'hopf_rules.py', 'stable_rules.py', 'ehp_rules.py',
                  'scalar_rules.py', 'relation_rules.py', 'set_rules.py')
    sources = {p: (root / p).read_text(encoding='utf-8-sig')
               for p in rule_names if (root / p).is_file()}
    if 'toda_rules.py' not in sources:
        raise FileNotFoundError(root / 'toda_rules.py')
    result = analyze(boundary_path.read_text(encoding='utf-8-sig'), sources)
    output.mkdir(parents=True, exist_ok=True)
    for filename, key, fields in (
        ('rule_mapping.csv', 'mapping_rows', ['rule_name', 'locator', 'component_key', 'status', 'source']),
        ('rule_sites.csv', 'rule_sites', ['file', 'line', 'name', 'status']),
        ('unlinked_components.csv', 'unlinked_components', ['locator', 'key', 'role', 'component_order', 'line', 'status']),
    ):
        with (output / filename).open('w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(result[key])
    summary = {'scope': sorted(sources), 'counts': result['counts'],
               'limitations': [
                   'Only literal InferenceRule names and literal mapping dictionaries are inspected.',
                   'Constructor sites are not instantiated runtime rules or unique theorems.',
                   'A boundary mapping is not verified mathematical Statement equality.',
                   'Definitions, indirect registrations, dynamic names and proof positions remain unverified.',
                   'No citation availability or semantic equivalence is inferred.',
                   'Existing registries, proof search and renderer are untouched.',
               ]}
    (output / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Phase 163 R4-R3 — Statement 実体と文献境界の対応監査', '',
             '## 監査範囲', *[f'- {p}' for p in summary['scope']], '',
             '## 集計（命題数ではない）',
             *[f'- {name}: {value}' for name, value in result['counts'].items() if not isinstance(value, dict)],
             '', '## 対応状態']
    lines.extend(f'- {k}: {v}' for k, v in result['counts']['mapping_status'].items())
    lines.extend(['', '## InferenceRule 生成箇所の状態'])
    lines.extend(f'- {k}: {v}' for k, v in result['counts']['site_status'].items())
    lines.extend(['', '## 注意・未解決事項', *[f'- {v}' for v in summary['limitations']],
                  '', '**これは対応候補の監査であり、全命題統合の完了ではない。**',
                  '全体 pytest は Phase 163 の最後まで実施しない。'])
    (output / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return summary


if __name__ == '__main__':
    summary = write_audit(Path.cwd(), Path.cwd() / 'phase163_r4_r3_output')
    print('Phase 163 R4-R3 candidate mapping audit:', summary['counts'])
    print('Saved: phase163_r4_r3_output/report.md and CSV files')
    print('No project source changes; full pytest suite not run.')
```

## tests/test_phase163_r4_r3_statement_mapping.py

```python
import pytest

from phase163_r4_r3_statement_mapping import analyze, write_audit


BOUNDARY = '''
_FIXED_RULE_COMPONENT_KEYS = {"known rule": "a", "aggregate": None}
_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME = {"known rule": "Proposition 1", "aggregate": "Proposition 1"}
_FIXED_RULE_COMPONENT_KEYS.update({"missing": "nope"})
_REFERENCE_LOCATOR_BY_FIXED_RULE_NAME.update({"missing": "Proposition 1"})
TodaFixedStatementComponent(reference_locator="Proposition 1", component_key="a", statement_role=Role.RELATION, order=1)
TodaFixedStatementComponent(reference_locator="Proposition 1", component_key="b", statement_role=Role.RELATION, order=None)
'''
RULES = '''
InferenceRule(name="known rule")
InferenceRule(name="not listed")
InferenceRule(name=make_name())
'''


def test_correspondence_and_unlinked_component():
    result = analyze(BOUNDARY, {'toda_rules.py': RULES})
    status = {r['rule_name']: r['status'] for r in result['mapping_rows']}
    assert status == {'aggregate': 'aggregate_or_no_component',
                      'known rule': 'candidate_mapped_metadata_only',
                      'missing': 'component_not_in_catalog'}
    assert len(result['unlinked_components']) == 1
    assert result['unlinked_components'][0]['key'] == 'b'


def test_dynamic_and_unlisted_rule_names_are_not_assumed_mapped():
    result = analyze(BOUNDARY, {'toda_rules.py': RULES})
    assert result['counts']['site_status'] == {
        'dynamic_name_unverified': 1, 'listed_in_boundary_mapping': 1,
        'not_listed_in_boundary_mapping': 1}


def test_missing_locator_remains_unresolved():
    result = analyze('_FIXED_RULE_COMPONENT_KEYS = {"r": "c"}', {})
    assert result['mapping_rows'][0]['status'] == 'locator_unresolved'


def test_duplicate_component_identity_rejected():
    source = '''
TodaFixedStatementComponent(reference_locator="P", component_key="k")
TodaFixedStatementComponent(reference_locator="P", component_key="k")
'''
    with pytest.raises(ValueError, match='duplicate boundary component'):
        analyze(source, {})


def test_output_contains_detail_csv_and_report(tmp_path):
    (tmp_path / 'toda_literature_statement_boundary.py').write_text(BOUNDARY, encoding='utf-8')
    (tmp_path / 'toda_rules.py').write_text(RULES, encoding='utf-8')
    summary = write_audit(tmp_path, tmp_path / 'out')
    assert summary['counts']['boundary_components'] == 2
    for name in ('report.md', 'summary.json', 'rule_mapping.csv',
                 'rule_sites.csv', 'unlinked_components.csv'):
        assert (tmp_path / 'out' / name).exists()


def test_absent_core_file_fails_explicitly(tmp_path):
    with pytest.raises(FileNotFoundError):
        write_audit(tmp_path, tmp_path / 'out')
```

## run.ps1

```powershell
$ErrorActionPreference = "Stop"
$ProjectRoot = (Get-Location).Path
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item -LiteralPath (Join-Path $PackageRoot 'phase163_r4_r3_statement_mapping.py') -Destination (Join-Path $ProjectRoot 'phase163_r4_r3_statement_mapping.py') -Force
$Tests = Join-Path $ProjectRoot 'tests'
New-Item -Path $Tests -ItemType Directory -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $PackageRoot 'tests/test_phase163_r4_r3_statement_mapping.py') -Destination (Join-Path $Tests 'test_phase163_r4_r3_statement_mapping.py') -Force
python -m pytest -q tests/test_phase163_r4_r3_statement_mapping.py
if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
python phase163_r4_r3_statement_mapping.py
if ($LASTEXITCODE -ne 0) { throw 'Audit failed' }
Write-Host 'Phase 163 R4-R3 read-only mapping audit complete. Full suite not run.'
```
