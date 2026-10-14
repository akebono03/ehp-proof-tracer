# R25 追加コード全文

変更対象は `audit.py` の `extract_factory`, `consumer_summary`, `audit`, `main` と、`test_audit.py` の4テスト。既存クラス・関数・import の変更なし。

## audit.py

```python
"""Phase 165 R52-R25: inspect compatibility before retiring a legacy pi3^2 rule.

Read-only: does not run legacy bootstraps, apply inference, or modify production.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

LEGACY_NAME = 'toda_pi3_2_free_cyclic_generator_inference_rule'
GENERAL_NAME = 'reverse_free_cyclic_transport_rule'


def extract_factory(source: str, name: str) -> dict:
    tree = ast.parse(source)
    func = next((n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name), None)
    if func is None:
        return {'present': False, 'name': name}
    cls = sorted({n.id for n in ast.walk(func) if isinstance(n, ast.Name)})
    patterns = []
    for node in ast.walk(func):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'PremisePattern':
            for keyword in node.keywords:
                if keyword.arg == 'statement_type':
                    patterns.append(ast.unparse(keyword.value))
    return {'present': True, 'name': name, 'line': func.lineno,
            'premise_types': patterns,
            'has_guard': 'match_guard' in {n.arg for n in ast.walk(func) if isinstance(n, ast.keyword)},
            'has_conclusion_builder': 'conclusion_builder' in {n.arg for n in ast.walk(func) if isinstance(n, ast.keyword)},
            'type_names': [n for n in cls if n.endswith('Statement') or n in ('MapIsomorphism', 'GeneratorImage', 'Relation')]}


def consumer_summary(source: str, name: str) -> dict:
    tree = ast.parse(source)
    factory_calls = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == name]
    imports = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) for a in n.names if a.name == name]
    return {'factory_calls': factory_calls, 'import_lines': imports}


def audit(root: Path) -> dict:
    required = {
        'old_factory': root / 'toda_rules.py',
        'generic_factory': root / 'phase165_r14_r33_final_group.py',
        'bootstrap': root / 'toda_upstream_bootstrap.py',
        'probe': root / 'probes' / 'probe_phase49_capabilities.py',
        'shared_test': root / 'test_phase165_r52_r9_shared_math.py',
    }
    missing = [k for k, p in required.items() if not p.is_file()]
    if missing:
        raise FileNotFoundError('Required active files missing: ' + ', '.join(missing))
    source = {k: p.read_text(encoding='utf-8-sig') for k, p in required.items()}
    legacy = extract_factory(source['old_factory'], LEGACY_NAME)
    general = extract_factory(source['generic_factory'], GENERAL_NAME)
    consumers = {k: consumer_summary(source[k], LEGACY_NAME) for k in ('bootstrap', 'probe')}
    generic_test = 'test_r9_pi32_regenerated_by_shared_mathematical_expansion' in source['shared_test']
    premises_identical = legacy.get('premise_types') == general.get('premise_types')
    active_callers = sum(len(v['factory_calls']) for v in consumers.values())
    # Even identical premise names would not certify matching guards, constructors or public APIs.
    status = 'BLOCKED_OLD_CONSUMERS_REQUIRE_SEMANTIC_MIGRATION' if active_callers else 'REVIEW_REQUIRED_NO_ACTIVE_CALLERS_FOUND'
    return {
        'phase': '165 R52-R25', 'mode': 'READ_ONLY_LEGACY_GENERIC_SEMANTIC_GATE',
        'legacy': legacy, 'general': general, 'consumers': consumers,
        'generic_pi32_test_present': generic_test,
        'premise_type_names_identical': premises_identical,
        'old_factory_call_count': active_callers,
        'status': status,
        'deletion_approved': False, 'production_modified': False, 'full_pytest_run': False,
        'next_obligations': [
            'Compare old and generic rule conclusions and guards on typed proof steps',
            'Migrate legacy bootstrap and probe preserving their public return contracts',
            'Run targeted tests for old bootstrap, probe and new shared search',
            'Only then delete legacy rule and remove imports',
        ],
    }


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    result = audit(root)
    out = Path(__file__).resolve().parent / 'audit_output'
    out.mkdir(exist_ok=True)
    (out / 'migration_gate.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    text = ('# R52-R25: π3² 旧専用規則の置換条件\n\n'
            f"- 判定: **{result['status']}**\n"
            f"- 旧規則の型付き前提: `{result['legacy'].get('premise_types', [])}`\n"
            f"- 一般規則の型付き前提: `{result['general'].get('premise_types', [])}`\n"
            f"- 旧呼出数: {result['old_factory_call_count']}\n"
            '- 本番コードは未変更、専用規則は削除していません。\n'
            '- AST で型名が一致しても数学的等価性は認定しません。\n')
    (out / 'review.md').write_text(text, encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('phase', 'mode', 'premise_type_names_identical', 'old_factory_call_count', 'status', 'deletion_approved', 'full_pytest_run')}, ensure_ascii=False, indent=2))
    print('Review:', out / 'review.md')


if __name__ == '__main__':
    main()

```

## test_audit.py

```python
from pathlib import Path

from audit import audit, consumer_summary, extract_factory


def test_r25_reads_rule_shapes():
    data = extract_factory('def demo():\n return InferenceRule(premise_patterns=(PremisePattern(statement_type=Relation),),match_guard=g,conclusion_builder=b)\n', 'demo')
    assert data['present']
    assert data['premise_types'] == ['Relation']
    assert data['has_guard'] and data['has_conclusion_builder']


def test_r25_records_missing_factory():
    assert extract_factory('def other():\n return 1\n', 'missing')['present'] is False


def test_r25_finds_old_consumers():
    found = consumer_summary('from r import old\na=old()\n', 'old')
    assert found['factory_calls'] == [2]
    assert found['import_lines'] == [1]


def test_r25_requires_semantic_gate_even_for_same_names(tmp_path: Path):
    (tmp_path / 'probes').mkdir()
    (tmp_path / 'toda_rules.py').write_text('def toda_pi3_2_free_cyclic_generator_inference_rule():\n return InferenceRule(premise_patterns=(PremisePattern(statement_type=Relation),), match_guard=g, conclusion_builder=b)\n')
    (tmp_path / 'phase165_r14_r33_final_group.py').write_text('def reverse_free_cyclic_transport_rule():\n return InferenceRule(premise_patterns=(PremisePattern(statement_type=Relation),), match_guard=g, conclusion_builder=b)\n')
    (tmp_path / 'toda_upstream_bootstrap.py').write_text('x=toda_pi3_2_free_cyclic_generator_inference_rule()\n')
    (tmp_path / 'probes' / 'probe_phase49_capabilities.py').write_text('x=1\n')
    (tmp_path / 'test_phase165_r52_r9_shared_math.py').write_text('def test_r9_pi32_regenerated_by_shared_mathematical_expansion():\n pass\n')
    result = audit(tmp_path)
    assert result['premise_type_names_identical']
    assert not result['deletion_approved']
    assert result['old_factory_call_count'] == 1

```

## run.ps1

```powershell
$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $package
Push-Location $package
try {
    python -m pytest -q test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R25 targeted pytest failed' }
    python audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R25 audit failed' }
    Write-Host 'R25 compatibility gate completed; production unchanged; full pytest NOT run.'
} finally { Pop-Location }

```