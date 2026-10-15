"""Phase 165 R57-R22: read-only local source and adapter-dependency audit."""
from __future__ import annotations

import ast
import json
from pathlib import Path

FILES = (
    'proof.py',
    'phase165_r3_recursive_search.py',
    'phase165_r52_r9_shared_math.py',
    'phase165_r52_r23_existing_rule_adapter.py',
    'phase165_r57_r18_generator_substitution.py',
    'phase165_r57_r19_delta_image_backward.py',
    'phase165_r57_r20_general_specialization.py',
    'phase165_r14_r14_diagonal_and_prop42.py',
)


def function_names(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    return [node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]


def static_audit(root: Path) -> dict:
    missing = [name for name in FILES if not (root / name).is_file()]
    if missing:
        raise FileNotFoundError('Missing required repository files: ' + ', '.join(missing))
    found = {name: function_names(root / name) for name in FILES}
    search = (root / 'phase165_r3_recursive_search.py').read_text(encoding='utf-8')
    shared = (root / 'phase165_r52_r9_shared_math.py').read_text(encoding='utf-8')
    adapter = (root / 'phase165_r52_r23_existing_rule_adapter.py').read_text(encoding='utf-8')
    proof = (root / 'proof.py').read_text(encoding='utf-8')
    probes = {
        'search_recurses_over_provider_subgoals': 'expansion_provider(target)' in search and 'resolve(child)' in search,
        'search_forward_checks_inference': 'find_inference_matches_for_rule(expansion.rule, premises)' in search and 'derive_inference_proof_step(match)' in search,
        'shared_provider_calls_pi43_adapter': 'expand_existing_pi43_rules,' in shared,
        'pi43_adapter_contains_target_specific_goals': 'TodaPrimaryGroup(4, 3)' in adapter,
        'inference_rule_has_conclusion_pattern': 'conclusion_pattern: Any' in proof,
        'inference_rule_has_conclusion_builder': 'conclusion_builder: Any' in proof,
        'generic_scalar_specialization_exists': 'specialize_typed_statement' in found['phase165_r57_r20_general_specialization.py'],
        'delta_image_reverse_exists': 'expand_registered_delta_image_goal' in found['phase165_r57_r19_delta_image_backward.py'],
        'finite_cyclic_substitution_exists': 'finite_cyclic_generator_substitution_rule' in found['phase165_r57_r18_generator_substitution.py'],
    }
    return {'phase': '165 R57-R22', 'mode': 'READ_ONLY_STATIC', 'files': list(FILES),
            'functions': found, 'checks': probes, 'full_pytest_run': False,
            'note': 'Static checks are presence checks, not evidence that proof goals are derivable.'}


def adapter_frontier_probe(root: Path) -> dict:
    """Import the existing adapter only; no repository files are modified."""
    import sys
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from expression import Suspension
    from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup
    from proof import Relation
    from phase165_r52_r23_existing_rule_adapter import _objects, expand_existing_pi43_rules
    import toda_rules as rules
    source, target, _, e, delta, eta2, eta3, twice = _objects()
    goals = {
        'named_generator': Relation(target, FiniteCyclicGroup(2, eta3)),
        'finite_quotient': Relation(target, FiniteCyclicGroup(2, Suspension(expression=eta2))),
        'suspension_kernel': rules.TodaSuspensionKernelFreeCyclicStatement(e, FreeCyclicGroup(twice)),
        'suspension_surjective': rules.TodaSuspensionSurjectiveStatement(e),
        'delta_image': rules.TodaDeltaImageFreeCyclicStatement(delta, FreeCyclicGroup(twice)),
    }
    return {name: {'goal': repr(goal), 'adapter_count': len(expand_existing_pi43_rules(goal)),
                   'rule_names': [x.rule.name for x in expand_existing_pi43_rules(goal)],
                   'subgoals': [[repr(sub) for sub in x.subgoals] for x in expand_existing_pi43_rules(goal)]}
            for name, goal in goals.items()}


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    static = static_audit(root)
    try:
        dynamic = {'status': 'OBSERVED', 'goals': adapter_frontier_probe(root)}
    except Exception as exc:
        dynamic = {'status': 'UNAVAILABLE', 'reason': f'{type(exc).__name__}: {exc}'}
    result = dict(static, adapter_probe=dynamic)
    output = Path(__file__).resolve().parent / 'audit_results.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
