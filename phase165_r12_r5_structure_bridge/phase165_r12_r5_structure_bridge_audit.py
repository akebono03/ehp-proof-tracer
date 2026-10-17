"""R12-R5: diagnose the root expansion; do not report proof completion."""
from __future__ import annotations
import json
from expression import eta
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r10_rule_registry import build_rule_registry
from phase165_r8_rule_provider import DEFAULT_RULE_MODULES
from phase165_r57_r26_generic_search_connection import build_generic_backward_expansion_provider
from proof import Relation, RelationType


def audit():
    registry = build_rule_registry(DEFAULT_RULE_MODULES)
    goal = Relation(TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, eta(3)), RelationType.EQUALITY)
    provider = build_generic_backward_expansion_provider(registry.rules())
    proposals = provider(goal)
    bridge_name = 'finite cyclic structure gives group relation'
    matched = tuple(x for x in proposals if x.rule.name == bridge_name)
    if len(matched) != 1:
        raise AssertionError('expected one generic bridge expansion for pi43 root')
    return {
        'phase': '165 R12-R5',
        'mode': 'ROOT_TYPED_BRIDGE_NOT_PI43_PROOF',
        'registry_entries': len(registry.entries),
        'goal': repr(goal),
        'root_expansion_count': len(proposals),
        'bridge_expansion_count': len(matched),
        'bridge_subgoals': [repr(item) for item in matched[0].subgoals],
        'target_pi43_proof_certified': False,
        'full_pytest_run': False,
    }


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
