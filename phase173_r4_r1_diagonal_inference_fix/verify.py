"""Read-only post-install proof search for the exact Toda (5.6) root."""
from __future__ import annotations

from pathlib import Path

from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import (
    build_shared_typed_bridge, search_shared_group_goal, shared_expansion_provider,
)
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase173_r4_r1_lemma54_source_bridge.source import (
    add_verified_lemma54_source, expand_cited_lemma54_hopf,
)
from phase173_r4_r1_source_bound_56.rule import expand_source_bound_toda56
from proof import ProofRule
from unified_statement_registry import AssertionOrigin


def run_verification(root: Path) -> dict[str, object]:
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=4, k=3)
    if len(goals) != 1:
        raise RuntimeError('Expected exactly one registered pi_7^4 goal')
    goal = goals[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    if citing_id is None:
        raise RuntimeError('Missing published pi_7^4 citation target')
    chapter = (root / 'sources/toda/Toda_05_2.tex').read_text(encoding='utf-8-sig')
    augmented = add_verified_lemma54_source(
        bridge, citing_assertion_id=citing_id, chapter=chapter,
    )
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        augmented, goal=goal, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    ))
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
    )

    def extra(statement: object):
        hopf = expand_cited_lemma54_hopf(statement, available)
        if hopf:
            return hopf
        return expand_source_bound_toda56(
            statement, available, screened, proof_target=goal,
        )

    root_candidates = expand_source_bound_toda56(
        goal, available, screened, proof_target=goal,
    )
    if len(root_candidates) != 1:
        raise RuntimeError('Expected one strictly source-bound root')
    from phase165_r3_recursive_search import SourceBoundGoal
    if not isinstance(root_candidates[0].subgoals[2], SourceBoundGoal):
        raise RuntimeError('Diagonal is not required to be inferred from Toda (5.1)')
    provider = shared_expansion_provider(
        screened, extra_providers=(extra,), proof_target=goal,
    )
    result = search_shared_group_goal(
        n=4, k=3, group_structure=goal.rhs,
        bridge=augmented, citing_assertion_id=citing_id,
        expansion_provider=provider,
    )
    completed = result.status.value == 'complete' and result.conclusion == goal
    roots = tuple(
        step for step in result.proven_steps
        if step.conclusion == goal and step.rule is ProofRule.INFERENCE
        and step.inference_rule is not None
        and step.inference_rule.name == root_candidates[0].rule.name
    )
    certified = bool(completed and len(roots) == 1
                     and len(roots[0].premises) == 4
                     and roots[0].premises[2].rule is ProofRule.INFERENCE
                     and roots[0].premises[3].rule is ProofRule.INFERENCE
                     and roots[0].premises[2].premises
                     and roots[0].premises[2].premises[0].conclusion
                     == root_candidates[0].subgoals[2].source)
    return {
        'status': result.status.value,
        'complete': completed,
        'source_bound_root_count': len(roots),
        'diagonal_inference_certified': certified,
        'open_goal_count': len(result.open_goals),
        'diagnostics': tuple(str(x) for x in result.diagnostics),
    }


def main() -> int:
    from phase173_r4_r1_diagonal_inference_fix.install import preflight
    root = Path.cwd().resolve()
    if preflight(root) != 'ALREADY_INSTALLED':
        raise RuntimeError('Install the reviewed diagonal route before verifying')
    row = run_verification(root)
    print('PHASE173_R4_R1_DIAGONAL_VERIFICATION=PASS')
    print('PHASE173_R4_R1_PROOF_STATUS=' + str(row['status']))
    print('PHASE173_R4_R1_COMPLETE=' + str(row['complete']))
    print('PHASE173_R4_R1_DIAGONAL_INFERENCE_CERTIFIED=' + str(row['diagonal_inference_certified']))
    print('PHASE173_R4_R1_SOURCE_BOUND_ROOTS=' + str(row['source_bound_root_count']))
    print('PHASE173_R4_R1_OPEN_GOALS=' + str(row['open_goal_count']))
    print('PHASE173_R4_R1_DIAGNOSTICS=' + repr(row['diagnostics']))
    if not row['diagonal_inference_certified']:
        raise RuntimeError('A checked Toda (5.6) root proof is not yet complete')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
