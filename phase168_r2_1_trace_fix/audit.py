"""Read-only Phase 168 R2 trace: Toda (5.2) citation and expansion."""
from __future__ import annotations
import json
from pathlib import Path
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r2_toda52_transport import expand_toda52_finite_cyclic_goal
from phase165_r52_r27_r5_literature import Toda52UniversalStatement
from proof import ProofRule


def snapshot(bridge):
    candidates = []
    for a in bridge.registry._assertions.values():
        if isinstance(a.content, Toda52UniversalStatement):
            links = [link for link in bridge.proof_links if link.assertion_id == a.assertion_id]
            candidates.append({"assertion_id": a.assertion_id, "reference_id": a.reference_id,
                               "publication_position": bridge.registry.reference(a.reference_id).publication_position,
                               "component_position": a.component_position,
                               "links": [{"rule": str(getattr(l.step,"rule",None)),
                                          "matched": bool(l.step is not None and l.step.conclusion == a.content)} for l in links]})
    return candidates


def main():
    bridge = build_shared_typed_bridge()
    goal, = registered_group_goal_candidates(bridge, n=2, k=2)
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    assertions = tuple(bridge.registry._assertions.values())
    context_id = citing_id or assertions[0].assertion_id
    screened = screen_shared_proof_context(bridge, goal=goal, citing_assertion_id=context_id,
                                          explicit_publication_target=citing_id is not None)
    fixed_available = tuple(link.step.conclusion for link in screened.proof_links
                            if link.step is not None and link.step.rule is ProofRule.GIVEN
                            and screened.registry.assertion(link.assertion_id).origin.name == 'FIXED_STATEMENT')
    raw = expand_toda52_finite_cyclic_goal(goal, tuple(link.step.conclusion for link in bridge.proof_links
                                  if link.step is not None and isinstance(link.step.conclusion,Toda52UniversalStatement)))
    selected = expand_toda52_finite_cyclic_goal(goal, fixed_available)
    root = shared_expansion_provider(screened, proof_target=goal)(goal)
    result = {"goal":repr(goal),"citing_id":citing_id,"context_id":context_id,
              "full_toda52":snapshot(bridge),"screened_toda52":snapshot(screened),
              "screened_given_toda52_count":sum(isinstance(x,Toda52UniversalStatement) for x in fixed_available),
              "raw_transport_count":len(raw),"screened_transport_count":len(selected),
              "screened_root_rules":[getattr(x.rule,'name',repr(x.rule)) for x in root],
              "screened_transport_subgoals":[[repr(s) for s in x.subgoals] for x in selected],
              "note":"This diagnostic never infers a proof from registered goal data."}
    out=Path(__file__).parent/'results.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('goal','screened_transport_subgoals')},ensure_ascii=False,indent=2))
    print('REPORT:',out)

if __name__=='__main__':
    main()
