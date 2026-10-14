"""Read-only compatibility audit for existing pi4^3 inference-rule factories.

This is static evidence, not proof of soundness or runtime integration.
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

FACTORIES = (
    'toda_pi4_3_delta_image_free_cyclic_inference_rule',
    'toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule',
    'toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule',
    'toda_pi4_3_finite_cyclic_inference_rule',
    'toda_pi4_3_eta3_generator_inference_rule',
)


def symbol(node: ast.AST | None) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f'{symbol(node.value)}.{node.attr}'
    if isinstance(node, ast.Call):
        return symbol(node.func)
    if isinstance(node, ast.Constant):
        return repr(node.value)
    if node is None:
        return ''
    try:
        return ast.unparse(node)
    except (ValueError, TypeError):
        return type(node).__name__


def _rule_calls(fn: ast.FunctionDef) -> list[ast.Call]:
    return [item for item in ast.walk(fn)
            if isinstance(item, ast.Call) and symbol(item.func).split('.')[-1] == 'InferenceRule']


def _keyword(call: ast.Call, name: str) -> ast.AST | None:
    return next((kw.value for kw in call.keywords if kw.arg == name), None)


def _patterns(node: ast.AST | None) -> list[dict]:
    if node is None:
        return []
    return [{kw.arg: symbol(kw.value) for kw in item.keywords if kw.arg}
            for item in ast.walk(node)
            if isinstance(item, ast.Call) and symbol(item.func).split('.')[-1] == 'PremisePattern']


def _definitions(tree: ast.Module) -> dict[str, ast.FunctionDef]:
    return {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}


def _calls(fn: ast.FunctionDef) -> list[str]:
    return sorted({symbol(node.func).split('.')[-1] for node in ast.walk(fn)
                   if isinstance(node, ast.Call)})


def _functions_in_shared_provider(tree: ast.Module) -> set[str]:
    result = set()
    for item in ast.walk(tree):
        if isinstance(item, ast.FunctionDef) and item.name in ('shared_expansion_provider', 'expand'):
            result.update(_calls(item))
            for name in ast.walk(item):
                if isinstance(name, ast.Name) and name.id.startswith('expand_'):
                    result.add(name.id)
    return result


def audit(root: Path) -> dict:
    root = Path(root).resolve()
    source = root / 'toda_rules.py'
    shared = root / 'phase165_r52_r9_shared_math.py'
    if not source.is_file() or not shared.is_file():
        raise FileNotFoundError('required root production modules missing')
    source_text = source.read_text(encoding='utf-8-sig')
    source_tree = ast.parse(source_text, filename=str(source))
    shared_tree = ast.parse(shared.read_text(encoding='utf-8-sig'), filename=str(shared))
    defs = _definitions(source_tree)
    provider_symbols = _functions_in_shared_provider(shared_tree)
    records = []
    for factory_name in FACTORIES:
        fn = defs.get(factory_name)
        if fn is None:
            records.append({'factory': factory_name, 'status': 'MISSING_IN_ROOT',
                            'direct_shared_reference': factory_name in provider_symbols})
            continue
        rule_calls = _rule_calls(fn)
        if len(rule_calls) != 1:
            records.append({'factory': factory_name, 'status': 'RULE_FACTORY_SHAPE_REVIEW',
                            'line': fn.lineno, 'rule_constructor_count': len(rule_calls),
                            'direct_shared_reference': factory_name in provider_symbols})
            continue
        call = rule_calls[0]
        rule_name = _keyword(call, 'name')
        guard = _keyword(call, 'match_guard')
        builder = _keyword(call, 'conclusion_builder')
        guard_name = symbol(guard)
        builder_name = symbol(builder)
        related = {}
        for name in (guard_name, builder_name):
            helper = defs.get(name)
            if helper is not None:
                related[name] = {'line': helper.lineno, 'source': ast.get_source_segment(source_text, helper),
                                 'calls': _calls(helper)}
        records.append({
            'factory': factory_name, 'status': 'EXISTING_FORWARD_RULE_NEEDS_REVERSE_ADAPTER_REVIEW',
            'line': fn.lineno, 'rule_name': symbol(rule_name),
            'premise_patterns': _patterns(_keyword(call, 'premise_patterns')),
            'match_guard': guard_name, 'conclusion_builder': builder_name,
            'helper_definitions': related, 'factory_source': ast.get_source_segment(source_text, fn),
            'factory_calls': _calls(fn),
            'direct_shared_reference': factory_name in provider_symbols,
            'has_expansion_entrypoint': any(
                isinstance(node, ast.FunctionDef) and node.name.startswith('expand_')
                and factory_name in _calls(node) for node in ast.walk(source_tree)
            ),
        })
    return {'phase': '165 R52-R22', 'mode': 'READ_ONLY_ACTIVE_RULE_COMPATIBILITY',
            'source_module': 'toda_rules.py', 'shared_module': shared.name,
            'rule_count_requested': len(FACTORIES), 'rule_count_present': sum(
                x['status'] != 'MISSING_IN_ROOT' for x in records),
            'rules': records,
            'conclusion': 'Static comparison only: no rule is wired, replaced, or approved by this audit.',
            'limitations': [
                'Presence does not imply soundness, generality, or backward-search eligibility.',
                'A forward InferenceRule requires a goal-to-premise mapping before use in GoalExpansion.',
                'Matching premise types is necessary, not sufficient: guards and actual typed objects must agree.',
                'Source metadata and root citation gates must still be checked during search.',
                'No full pytest is run.',
            ], 'full_pytest_run': False}


def write_report(root: Path, output: Path) -> dict:
    data = audit(root)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'compatibility.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# Phase 165 R52-R22 既存規則の共通探索適合性', '',
             'これは静的な監査であり、規則の数学的正当性や接続完了を認定しない。', '',
             '| 関数 | 状態 | 規則名 | 前提型 | 共通探索からの直接参照 |',
             '|---|---|---|---|---|']
    for item in data['rules']:
        patterns = ', '.join(x.get('statement_type', '?') for x in item.get('premise_patterns', []))
        lines.append(f"| `{item['factory']}` | {item['status']} | {item.get('rule_name', '')} | {patterns} | {item['direct_shared_reference']} |")
    lines += ['', '## 次の判断', '',
              '- 前提・結論・guard の型が一致する場合に限り既存規則を使う。',
              '- 共通探索への接続は `GoalExpansion(rule, subgoals)` が作れるようになってから行う。',
              '- 命題の結論を GIVEN として流用しない。',
              '- root 以外の過去バックアップは統合対象にしない。', '']
    (output / 'review.md').write_text('\n'.join(lines), encoding='utf-8')
    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = write_report(args.root, args.output)
    print(json.dumps({'phase': result['phase'], 'mode': result['mode'],
                      'rule_count_requested': result['rule_count_requested'],
                      'rule_count_present': result['rule_count_present'],
                      'direct_shared_count': sum(x.get('direct_shared_reference', False) for x in result['rules']),
                      'full_pytest_run': False}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
