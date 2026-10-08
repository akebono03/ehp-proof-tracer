import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap, TodaSuspensionIsomorphismStatement, TodaEHPExactnessWindow
from map_facts import EHP_E_MAP, EHP_H_MAP, EHP_DELTA_MAP
from proof import ProofRule, match_premise_pattern
from proof_repository import ProofRepository, ProofRepositoryEntry
from repository_proof_scope import build_repository_proof_scope
from repository_inference import build_depth_two_producer_search_report, execute_depth_two_producer_search
from rule_catalog import InferenceRuleCatalog, InferenceRuleCatalogEntry
from standard_production_repository import build_standard_production_proof_repository
from standard_production_applicability_catalog import build_standard_production_applicability_catalog
from toda_rules import TodaProp42ExactnessStatement, TodaProp51FiniteDimensionalStatement

FAMILIES = (
    'toda_53_n3_prop51_delta_injective_inference_rule',
    'toda_53_n3_delta_injective_hopf_zero_inference_rule',
    'toda_53_n3_hopf_zero_suspension_surjective_inference_rule',
    'toda_53_n3_hopf_eta5_surjective_inference_rule',
    'toda_53_n3_hopf_surjective_delta_zero_inference_rule',
    'toda_53_n3_delta_zero_suspension_injective_inference_rule',
    'toda_53_n3_suspension_isomorphism_inference_rule',
)


def factory_name(rule):
    builder = getattr(rule, 'conclusion_builder', None)
    qualname = getattr(builder, '__qualname__', '')
    if '.<locals>.' not in qualname:
        return None
    return qualname.split('.<locals>.', 1)[0].rsplit('.', 1)[-1]


def unique_conclusions(nodes):
    result = []
    for node in nodes:
        step = node.proof_step
        if not any(previous.conclusion == step.conclusion for previous in result):
            result.append(step)
    return result


def matching_steps(steps, pattern):
    return [step for step in steps if match_premise_pattern(pattern, step) is not None]


def main():
    production = build_standard_production_proof_repository()
    catalog = build_standard_production_applicability_catalog()
    scope = build_repository_proof_scope(production)
    source = TodaPrimaryGroup(group_dimension=4, sphere_dimension=2)
    target = TodaPrimaryGroup(group_dimension=5, sphere_dimension=3)
    goal = TodaSuspensionIsomorphismStatement(map=TodaSuspensionMap(source_group=source, target_group=target))
    # This trial covers exactly the n=3 EHP family. It is not an n-general planner.
    if (source.group_dimension, source.sphere_dimension, target.group_dimension, target.sphere_dimension) != (4, 2, 5, 3):
        raise ValueError('Unsupported EHP dimension family')

    selected_rules = []
    evidence = []
    for name in FAMILIES:
        matches = [e for e in catalog.entries() if factory_name(e.rule) == name]
        # Choose a stable representative without inspecting the goal's proof ancestry.
        chosen = matches[0] if matches else None
        evidence.append({'factory': name, 'candidate_count': len(matches), 'selected_key': chosen.key if chosen else None})
        if chosen is None:
            return emit({'status': 'MISSING_RULE_FAMILY', 'rule_candidates': evidence})
        selected_rules.append(chosen)

    # Compute EHP windows from the goal's source/target dimensions, never from a completed proof.
    pi_5_5 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=5)
    pi_3_2 = TodaPrimaryGroup(group_dimension=3, sphere_dimension=2)
    pi_6_3 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=3)
    pi_6_5 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=5)
    windows = (
        (target, pi_5_5, pi_3_2, EHP_H_MAP, EHP_DELTA_MAP),
        (source, target, pi_5_5, EHP_E_MAP, EHP_H_MAP),
        (pi_6_3, pi_6_5, source, EHP_H_MAP, EHP_DELTA_MAP),
        (pi_6_5, source, target, EHP_DELTA_MAP, EHP_E_MAP),
    )
    wanted = [TodaProp42ExactnessStatement(window=TodaEHPExactnessWindow(
        source_term=a, middle_term=b, target_term=c, first_map=d, second_map=e,
    )) for a, b, c, d, e in windows]
    distinct = unique_conclusions(scope.nodes)
    exactness = []
    for w in wanted:
        matches = [s for s in distinct if s.conclusion == w]
        exactness.append(matches[0] if matches else None)

    # First leaf rule requires Proposition 5.1; second leaf rule uses a Hopf relation
    # and the corresponding cyclic group statement. Preserve the second leaf's
    # exact premise pattern instead of matching its source proof trace.
    p51 = selected_rules[0].rule.premise_patterns
    p_hopf = selected_rules[3].rule.premise_patterns
    prop_candidates = [s for s in distinct if isinstance(s.conclusion, TodaProp51FiniteDimensionalStatement)
                       and any(match_premise_pattern(p, s) is not None for p in p51)]
    hopf_candidates = [s for s in distinct if s not in prop_candidates
                       and any(match_premise_pattern(p, s) is not None for p in p_hopf)]
    # Compare the RHS mathematical expression, not its rendered prose.
    eta5 = HomotopyElement(name='η₅', dimension=5, source=6, target=5,
                           generator=GeneratorSymbol(family='η', index=5))
    eta_candidates = [s for s in hopf_candidates
                      if s.conclusion.__class__.__name__ == 'Relation'
                      and getattr(s.conclusion, 'rhs', None) == eta5]
    details = {
        'scope': 'Goal dimensions -> n3 rule family + EHP exactness; no target ancestry selected',
        'production_root_count': len(production.entries()),
        'production_scope_count': len(scope.nodes),
        'production_catalog_count': len(catalog.entries()),
        'goal': str(goal),
        'rule_candidates': evidence,
        'exactness_found': [x is not None for x in exactness],
        'proposition_candidate_count': len(prop_candidates),
        'hopf_relation_candidate_count': len(eta_candidates),
        'limitations': [
            'This is a goal-dimension-specific candidate profile, not general automatic rule discovery.',
            'Search opt-in applies only to an isolated temporary catalog; not a safety certification.',
            'Proposition and Hopf premise disambiguation may remain unresolved.',
        ],
    }
    if any(x is None for x in exactness) or not prop_candidates or not eta_candidates:
        details['status'] = 'MISSING_GOAL_RELEVANT_PREMISE'
        return emit(details)
    # Test candidate pairs, without choosing a pair from the final proof ancestry.
    outcomes = []
    for prop in prop_candidates[:8]:
        for hopf in eta_candidates[:20]:
            isolated_repository = ProofRepository()
            for i, step in enumerate([prop, hopf, *exactness]):
                isolated_repository.register(ProofRepositoryEntry(key=f'phase161.goal.premise.{i}', step=step))
            isolated_catalog = InferenceRuleCatalog()
            for i, entry in enumerate(selected_rules):
                isolated_catalog.register(InferenceRuleCatalogEntry(
                    key=f'phase161.goal.rule.{i}', rule=entry.rule,
                    conclusion_type=entry.conclusion_type, fixed_point_safe=True,
                    goal_compatibility=entry.goal_compatibility,
                    relevance_category=entry.relevance_category,
                ))
            report = build_depth_two_producer_search_report(isolated_repository, isolated_catalog, goal, max_depth=3)
            record = {'search_status': report.status.value, 'prop_rule': getattr(prop.inference_rule, 'name', None),
                      'hopf_rule': getattr(hopf.inference_rule, 'name', None)}
            if report.status.value == 'success':
                execution = execute_depth_two_producer_search(isolated_repository, isolated_catalog, goal, max_depth=3)
                record['goal_derived'] = execution.repository_inference_result is not None and execution.repository_inference_result.goal_step is not None
                outcomes.append(record)
                if record['goal_derived']:
                    details['status'] = 'GOAL_DERIVED_WITHOUT_TARGET_ANCESTRY_SELECTION'
                    details['successful_pair'] = record
                    details['pairs_examined'] = len(outcomes)
                    return emit(details)
            outcomes.append(record)
    details['status'] = 'NO_VALID_PREMISE_PAIR_FOUND'
    details['pairs_examined'] = len(outcomes)
    details['pair_statuses'] = outcomes[:20]
    return emit(details)


def emit(data):
    text = json.dumps(data, ensure_ascii=False, indent=2, default=str)
    print(text)
    (ROOT / 'phase161_goal_driven_selection_probe.json').write_text(text + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
