"""Isolated runtime probe: inspect existing R8 factories without proving any goal."""
from __future__ import annotations

import json
from pathlib import Path
import sys


def run(root: Path) -> dict:
    sys.path.insert(0, str(root))
    from phase165_r8_rule_provider import discover_inference_rules, DEFAULT_RULE_MODULES
    from proof import InferenceRule
    result = {'status': 'OK', 'modules': list(DEFAULT_RULE_MODULES), 'rules': [], 'skipped_factories': [], 'skipped_rules': []}
    for module in DEFAULT_RULE_MODULES:
        try:
            rules, report = discover_inference_rules((module,))
        except Exception as exc:
            result['rules'].append({'module': module, 'status': 'IMPORT_OR_DISCOVERY_ERROR', 'error': f'{type(exc).__name__}: {exc}'})
            continue
        result['skipped_factories'].extend(report.skipped_factories)
        result['skipped_rules'].extend(report.skipped_rules)
        # R8 report does not export the factory-to-rule mapping. Do not invent it.
        for index, rule in enumerate(rules):
            patterns = getattr(rule, 'premise_patterns', ())
            conclusion = getattr(rule, 'conclusion_pattern', None)
            result['rules'].append({
                'module': module, 'runtime_index': index, 'name': rule.name,
                'status': 'INSTANTIATED' if isinstance(rule, InferenceRule) else 'UNKNOWN',
                'has_conclusion_pattern': conclusion is not None,
                'premise_count': len(patterns) if patterns is not None else 0,
                'backward_structural_candidate': conclusion is not None and bool(patterns),
                'backward_goal_verified': False, 'proof_reconstructed': False,
                'connection': 'DEFAULT_R8_PROVIDER_PATH_STATIC_ONLY',
            })
    return result


if __name__ == '__main__':
    try:
        result = run(Path(sys.argv[1]).resolve())
    except Exception as exc:
        result = {'status': 'PROBE_ERROR', 'error': f'{type(exc).__name__}: {exc}', 'rules': [], 'skipped_factories': [], 'skipped_rules': []}
    print(json.dumps(result, ensure_ascii=False))
