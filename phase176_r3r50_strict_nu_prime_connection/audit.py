"""Observe the real Web path; verify the alias step and its cited ancestry."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

from expression import Composition, MapApplication, Multiple
from homotopy_groups import TodaPrimaryGroup, TodaHopfInvariantMap
from map_facts import EHP_H_MAP
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r14_r6_generic_iso import MapInjective
from phase171_r2h_prop22_cited_hopf.source import TodaProp22RightFormula
from phase176_r3r27r1_toda55_quadruple_isolated.source import Toda55UniversalQuadrupleStatement
from phase176_r3r48_cited_finite_delta_kernel.rule import RULE_NAME as KERNEL_RULE_NAME
from phase176_r3r48_cited_finite_delta_kernel.source import canonical_signed_delta
from phase176_r3r49_hopf_image_frontier.audit import capture_web, source_rows
from phase176_r3r50_strict_nu_prime_connection.notation import RULE_NAME, alias_hopf_input
from proof import ProofRule, Relation


def walk_tree(step):
    visited = []

    def visit(node):
        if any(node is old for old in visited):
            return
        visited.append(node)
        for child in node.premises:
            visit(child)

    visit(step)
    return tuple(visited)


def observe():
    invocation, result, calls, key = capture_web()
    bridge, root = invocation['bridge'], invocation['goal']
    signed = canonical_signed_delta()
    generator = root.rhs.generator
    goal = Relation(MapApplication(EHP_H_MAP, generator), Multiple(4, signed.element))
    rows = [(item, record) for item, record in source_rows(bridge, generator.left)
            if record['locator'] == '(5.3)' and record['strict_nu_prime_alias'] and not record['exact_alpha']]
    if len(rows) != 1:
        raise RuntimeError('EXPECTED_ONE_STRICT_SOURCE_ALIAS')
    cited, record = rows[0]
    canonical = Relation(MapApplication(EHP_H_MAP, Composition(cited.lhs.expression, generator.right)), goal.rhs)
    step = next((s for s in result.proven_steps if s.conclusion == goal), None)
    if (step is None or step.rule is not ProofRule.INFERENCE or step.inference_rule is None
            or step.inference_rule.name != RULE_NAME or len(step.premises) != 1):
        raise RuntimeError('ACTUAL_WEB_HOPF_NOT_PROVED_BY_NOTATION_TRANSPORT')
    premise = step.premises[0]
    if (premise.conclusion != canonical or premise.rule is not ProofRule.INFERENCE
            or alias_hopf_input(goal, canonical) != canonical
            or not any(p is premise for p in result.proven_steps)):
        raise RuntimeError('CANONICAL_PREMISE_NOT_ACCEPTED')
    if not any(g == goal and any(o.rule.name == RULE_NAME and o.subgoals == (canonical,)
                                  for o in opts) for g, opts in calls):
        raise RuntimeError('ACTUAL_PROVIDER_NOT_REACHED')
    if goal in result.open_goals:
        raise RuntimeError('PROVED_HOPF_GOAL_STILL_OPEN')
    tree = walk_tree(step)
    givens = tuple(s for s in tree if s.rule is ProofRule.GIVEN)
    links = tuple(link for link in bridge.proof_links if link.step is not None)
    if any(not any(s is link.step for link in links) for s in givens):
        raise RuntimeError('UNSCREENED_GIVEN_IN_HOPF_TREE')
    for required in (cited, Toda55UniversalQuadrupleStatement(), TodaEtaFamilyGeneralDefinition(), TodaProp22RightFormula()):
        if not any(s.conclusion == required for s in givens):
            raise RuntimeError('CITED_ANCESTOR_MISSING:' + repr(required))
    if not any(link.assertion_id == record['assertion_id'] and any(link.step is s for s in givens) for link in links):
        raise RuntimeError('ORIGINAL_TODA53_LINK_NOT_USED')
    if any(s.conclusion in (goal, canonical, root) for s in givens):
        raise RuntimeError('DERIVED_GOAL_AS_GIVEN')
    kernel = KernelMultipleStatement(signed.map, signed.map.source_group, signed.element, 4)
    injective = MapInjective(TodaHopfInvariantMap(TodaPrimaryGroup(8,3), signed.map.source_group))
    if not any(s.conclusion == kernel and s.rule is ProofRule.INFERENCE and s.inference_rule is not None
               and s.inference_rule.name == KERNEL_RULE_NAME for s in result.proven_steps):
        raise RuntimeError('R3R48_KERNEL_REGRESSION')
    if not any(s.conclusion == injective for s in result.proven_steps):
        raise RuntimeError('HOPF_INJECTIVITY_REGRESSION')
    return {'gate':'PASS_R3R50_ACTUAL_WEB_HOPF_NOTATION_CONNECTED', 'status':result.status.value,
            'web_key':key, 'accepted_step_count':len(result.proven_steps),
            'actual_hopf_proved':True, 'actual_hopf_open':False, 'actual_hopf_goal':repr(goal),
            'canonical_premise':repr(canonical), 'original_toda53_assertion_id':record['assertion_id'],
            'original_toda53_position':record['position'], 'notation_rule':RULE_NAME,
            'hopf_tree_steps':len(tree), 'cited_given_count':len(givens),
            'kernel_preserved':True, 'hopf_injective_preserved':True,
            'root_group_proved':result.status.value == 'complete',
            'open_goals':[repr(g) for g in result.open_goals],
            'new_math_rules':0, 'new_notation_rules':1, 'new_given_registrations':0,
            'full_pytest':'NOT_RUN'}


def main() -> int:
    report = observe()
    folder = Path(os.environ.get('LOCALAPPDATA') or tempfile.gettempdir()) / 'EHPProofTracerAudit' / 'phase176_r3r50_strict_nu_prime_connection'
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / 'report.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    for key,value in report.items():
        print('PHASE176_R3R50_'+key.upper()+'='+json.dumps(value, ensure_ascii=False))
    print('REPORT='+str(path))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
