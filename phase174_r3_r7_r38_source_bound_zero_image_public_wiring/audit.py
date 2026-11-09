"""R38 public zero-suspension-image chain: proposals versus certified proof."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.install import (
    verify_checkout,
)

ROOT = Path(__file__).resolve().parents[1]


def inspect_public_chain() -> dict[str, object]:
    """Check the real R14 cited law and public R6/R7/R9 candidates."""
    from expression import Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import (
        exact_prior_database_result, precedes_db_goal,
    )
    from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import RULE_NAME as CYCLIC_RULE
    from phase174_r3_r7_r7_composite_zero_audit.rule import RULE_NAME as ZERO_RULE
    from phase174_r3_r7_r9_composition_associativity.rule import RULE_NAME as ASSOC_RULE
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import canonical_annihilator_instance
    from phase174_r3_r7_r12_toda59_annihilator_source.source import CitedFamilyAnnihilator
    from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider import (
        PROVIDER_ID, left_associated, lifted_stable_composition,
    )
    from proof import ProofRule, Relation, RelationType

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    screened = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root,
    )
    fixed_links = tuple(
        link for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == screened.registry.assertion(link.assertion_id).content
    )
    schemas = tuple(link for link in fixed_links
                    if type(link.step.conclusion) is CitedFamilyAnnihilator)
    if len(schemas) != 1:
        raise RuntimeError('R14 independently cited family law not uniquely screened')
    schema_link = schemas[0]
    citation = schema_link.step.inference_rule
    if (citation is None or citation.literature_reference is None
            or citation.literature_reference.locator != '(5.9)'):
        raise RuntimeError('Cited Toda (5.9) origin is missing')
    domain = TodaPrimaryGroup(10, 5)
    target = TodaPrimaryGroup(11, 6)
    source_goal = exact_prior_database_result(5, 5)
    if (type(source_goal) is not Relation
            or source_goal.relation_type is not RelationType.EQUALITY
            or source_goal.lhs != domain
            or not precedes_db_goal(5, 5, 7, 5)):
        raise RuntimeError('R38 candidate is not a strictly earlier typed DB result')
    g = source_goal.rhs.generator
    lifted = lifted_stable_composition(g)
    if lifted is None:
        raise RuntimeError('R38 cannot lift actual prior composite structurally')
    left = left_associated(lifted)
    if left is None:
        raise RuntimeError('R38 actual suspended composite has wrong factorization')
    law = canonical_annihilator_instance(schema_link.step.conclusion, 6)
    if law != Relation(left.left, Zero(), RelationType.EQUALITY):
        raise RuntimeError('R38 source law does not match zero left factor')
    mapping = TodaSuspensionMap(domain, target)
    image_goal = ImageZeroStatement(mapping)
    gen_zero = GeneratorImage(mapping, g, Zero())
    left_goal = GeneratorImage(mapping, g, left)
    right_goal = GeneratorImage(mapping, g, lifted)
    provider = shared_expansion_provider(screened, proof_target=root)
    expected = (
        (image_goal, CYCLIC_RULE),
        (gen_zero, ZERO_RULE),
        (left_goal, ASSOC_RULE),
        (right_goal, 'suspension preserves composition of separately proved maps'),
    )
    matched = []
    for goal, name in expected:
        found = tuple(option for option in provider(goal) if option.rule.name == name)
        if not found:
            raise RuntimeError('R38 public provider lacks expected generic rule: ' + name)
        matched.append(found[0])
    if matched[0].subgoals != (source_goal, gen_zero):
        raise RuntimeError('R6 source prior identity is not preserved')
    if matched[1].subgoals != (left_goal, law):
        raise RuntimeError('R7 zero left-factor source identity is not preserved')
    if matched[2].subgoals != (right_goal,):
        raise RuntimeError('R9 reassociation is not an exact proof subgoal')
    if any(link.step.conclusion in (image_goal, gen_zero, root) for link in fixed_links):
        raise RuntimeError('Forbidden derived or terminal direct GIVEN')
    if any(link.step.conclusion == source_goal for link in fixed_links):
        raise RuntimeError('The database candidate was incorrectly made a source GIVEN')
    ann = provider(law)
    if not any(option.rule.name == 'source-qualified general family annihilator specialization'
               for option in ann):
        raise RuntimeError('Public R14 cited source specialization is missing')
    return {
        'source_locator': '(5.9)',
        'public_source_annihilator_leaves': len(schemas),
        'prior_group_candidate_is_earlier': True,
        'prior_group_is_independent_cited_source': False,
        'zero_image_public_proposals': 1,
        'generator_zero_public_proposals': 1,
        'associativity_public_proposals': 1,
        'composition_factorization_public_proposals': 1,
        'r14_general_source_specialization_proposed': True,
        'direct_generator_or_image_zero_givens': 0,
        'new_givens': 0,
        'new_math_rules': 0,
        'zero_image_proved_by_this_audit': False,
        'upper_delta_surjectivity_proved': False,
        'root_complete': False,
        'web_http_checked': False,
        'full_pytest': False,
        'public_provider_id': PROVIDER_ID,
    }


def report(*, dry_run: bool) -> dict[str, object]:
    state = verify_checkout()
    if not dry_run and state['mode'] != 'INSTALLED':
        raise RuntimeError('Install R38 first')
    live = None if dry_run else inspect_public_chain()
    return {
        'phase': '174-R3-R7-R38',
        'git_state': state,
        'public': live,
        'gate': ('PASS_R38_REVIEWED_SOURCE_PREFLIGHT' if dry_run else
                 'PASS_R38_GENERAL_ZERO_IMAGE_CHAIN_PUBLIC_PROPOSALS_PROOF_PENDING'),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    result = report(dry_run=args.dry_run)
    folder = Path(os.environ.get('LOCALAPPDATA', tempfile.gettempdir())) / (
        'EHPProofTracerAudit/phase174_r3_r7_r38'
    )
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / ('preflight.json' if args.dry_run else 'public_zero_image_chain.json')
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    prefix = 'PHASE174_R3R7R38_'
    for key in ('local_head', 'remote_head', 'source_guard', 'r36_preserved', 'mode'):
        print(prefix + key.upper() + '=' + str(result['git_state'][key]))
    if result['public'] is not None:
        for key, value in result['public'].items():
            if isinstance(value, (str, int, bool)):
                print(prefix + key.upper() + '=' + str(value))
    print(prefix + 'REPORT=' + str(path))
    print(prefix + 'GATE=' + result['gate'])
    print('(END)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
