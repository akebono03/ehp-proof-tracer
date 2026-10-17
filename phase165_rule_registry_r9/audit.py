"""Phase 165 R9: read-only inventory of active typed inference rules."""
from __future__ import annotations

import ast
import inspect
import json
from collections import defaultdict
from pathlib import Path

from phase165_r8_rule_provider import DEFAULT_RULE_MODULES, discover_inference_rules
from proof import PatternVariable, PremisePattern

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).with_name('audit_result.json')


def pattern_variables(value: object) -> set[str]:
    """Collect named pattern variables without interpreting mathematical values."""
    if isinstance(value, PatternVariable):
        return {value.name}
    if isinstance(value, (list, tuple)):
        result = set()
        for v in value:
            result.update(pattern_variables(v))
        return result
    if hasattr(value, '__dataclass_fields__'):
        result = set()
        for key in value.__dataclass_fields__:
            result.update(pattern_variables(getattr(value, key)))
        return result
    return set()


def factory_inventory():
    """Enumerate factories, including those excluded for required arguments."""
    from importlib import import_module
    rows = []
    for module_name in DEFAULT_RULE_MODULES:
        module = import_module(module_name)
        for name, value in sorted(vars(module).items()):
            if not (name.endswith('_inference_rule') and callable(value)
                    and getattr(value, '__module__', None) == module.__name__):
                continue
            signature = inspect.signature(value)
            required = [p.name for p in signature.parameters.values()
                        if p.default is inspect.Parameter.empty
                        and p.kind in (inspect.Parameter.POSITIONAL_ONLY,
                                       inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                       inspect.Parameter.KEYWORD_ONLY)]
            runtime_name = None
            if not required:
                try:
                    runtime_name = value().name
                except (TypeError, ValueError, RuntimeError, AttributeError):
                    pass
            rows.append({'module': module_name, 'factory': name,
                         'rule_id_candidate': f'{module_name}.{name}',
                         'required_arguments': required, 'runtime_rule_name': runtime_name})
    return rows


def source_connections():
    """AST-only inspection: no deprecated catalog construction."""
    paths = ['phase165_r8_rule_provider.py',
             'phase165_r57_r26_generic_search_connection.py',
             'phase165_r52_r9_shared_math.py', 'rule_catalog.py']
    result = {}
    for name in paths:
        path = ROOT / name
        if not path.is_file():
            result[name] = {'present': False}
            continue
        tree = ast.parse(path.read_text(encoding='utf-8-sig'))
        calls = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                fn = node.func
                text = fn.id if isinstance(fn, ast.Name) else fn.attr if isinstance(fn, ast.Attribute) else ''
                if text in ('discover_inference_rules', 'build_generic_backward_expansion_provider',
                            'shared_expansion_provider', 'build_standard_production_applicability_catalog',
                            'register', 'build_production_rule_provider'):
                    calls.append({'function': text, 'line': node.lineno})
        result[name] = {'present': True, 'calls': calls}
    return result


def main():
    rules, discovery = discover_inference_rules()
    factories = factory_inventory()
    ids_by_name = defaultdict(list)
    for row in factories:
        if row['runtime_rule_name'] is not None:
            ids_by_name[row['runtime_rule_name']].append(row['rule_id_candidate'])
    records = []
    names = defaultdict(list)
    signatures = defaultdict(list)
    for index, rule in enumerate(rules):
        # Map by actual instantiated rule name, not by index: factories may be skipped.
        factory_id = ids_by_name[rule.name].pop(0) if ids_by_name[rule.name] else None
        conclusion = rule.conclusion_pattern
        bound = pattern_variables(conclusion)
        required = set()
        for premise in rule.premise_patterns:
            if isinstance(premise, PremisePattern):
                value = premise.relation_pattern if premise.relation_pattern is not None else premise.statement_pattern
                required.update(pattern_variables(value))
        fully_bound = bool(conclusion is not None and set(required).issubset(bound))
        record = {'index': index, 'rule_id_candidate': factory_id, 'rule_name': rule.name,
                  'premise_count': len(rule.premise_patterns),
                  'conclusion_pattern_present': conclusion is not None,
                  'guard_present': rule.match_guard is not None,
                  'backward_pattern_variables_bound': fully_bound,
                  'backward_status': ('PATTERN_CANDIDATE_ONLY' if fully_bound
                                      else 'NO_CONCLUSION_PATTERN' if conclusion is None
                                      else 'REQUIRES_BINDING_OR_WITNESS'),
                  'pattern_signature': repr((conclusion, rule.premise_patterns))}
        records.append(record)
        names[rule.name].append(factory_id)
        signatures[record['pattern_signature']].append(factory_id)
    all_ids = [x['rule_id_candidate'] for x in factories]
    report = {'phase': '165 R9 unified rule management inventory',
              'mode': 'READ_ONLY_ACTIVE_R8_WITH_STATIC_CONNECTIONS',
              'catalog_retired_not_invoked': True,
              'scope': 'Active R8 factories; not a mathematically complete rule registry',
              'discovered_count': len(rules),
              'factory_count': len(factories),
              'requires_input_count': sum(bool(x['required_arguments']) for x in factories),
              'candidate_rule_ids_unique': len(all_ids) == len(set(all_ids)),
              'duplicate_rule_names': [v for v in names.values() if len(v) > 1],
              'duplicate_pattern_candidates': [v for v in signatures.values() if len(v) > 1],
              'backward_pattern_candidates': sum(x['backward_pattern_variables_bound'] for x in records),
              'sources': source_connections(), 'factories': factories, 'rules': records,
              'skipped_factories': list(discovery.skipped_factories),
              'limitations': ['Rule ID candidates are module+factory, not yet persisted canonical IDs.',
                              'Pattern matching and search proof success are not established.',
                              'Static source references do not certify runtime connection.',
                              'Semantic duplicates require human mathematical review.'],
              'full_pytest_run': False}
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('phase','discovered_count','factory_count',
                                            'requires_input_count','candidate_rule_ids_unique',
                                            'backward_pattern_candidates','full_pytest_run')},
                     ensure_ascii=False, indent=2))
    print('Audit saved:', OUTPUT)
    return report


if __name__ == '__main__':
    main()
