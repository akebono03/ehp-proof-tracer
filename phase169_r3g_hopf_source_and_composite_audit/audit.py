"""Phase 169 R3G: inspect two genuine EHP proof blockers without patching sources.

This is an AUDIT_ONLY tool. A source statement, registry entry, proposal,
and proven ProofStep are deliberately recorded as distinct statuses.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

from homotopy_groups import (
    TodaDeltaMap,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
)
from phase165_r14_r5_ehp_connection import expand_registered_ehp_terminal_goal
from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase166_r3c_publication_order import precedes_citing_assertion
from proof import ProofRule, Relation
from toda_rules import (
    TodaDeltaInjectiveStatement,
    TodaHopfInvariantSurjectiveStatement,
    TodaProp51FiniteDimensionalStatement,
)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def _references_for_exact_content(bridge, content):
    found = []
    for assertion in bridge.registry._assertions.values():
        if type(assertion.content) is not type(content) or assertion.content != content:
            continue
        ref = bridge.registry.reference(assertion.reference_id)
        found.append({
            "assertion_id": assertion.assertion_id,
            "locator": ref.locator,
            "origin": assertion.origin.value,
            "component_position": assertion.component_position,
            "publication_position": ref.publication_position,
        })
    return found


def _screened_steps(screened, goal):
    result = []
    for link in screened.proof_links:
        if link.step is None:
            continue
        if type(link.step.conclusion) is type(goal) and link.step.conclusion == goal:
            result.append({
                "assertion_id": link.assertion_id,
                "proof_rule": link.step.rule.value,
                "premise_count": len(link.step.premises),
            })
    return result


def _try_reconstruct(goal, screened, citing_id, provider):
    try:
        step = reconstruct_registered_goal(
            goal, screened, citing_id, provider,
            lookup_mode="typed_reference_publication",
        )
    except RegisteredGoalUnresolved as exc:
        return {"status": "unresolved", "reason": str(exc)[:500]}
    return {
        "status": "proved",
        "proof_rule": step.rule.value,
        "premises": len(step.premises),
        "conclusion_exact": step.conclusion == goal,
    }


def _historical_metadata(bridge, screened, citing_id):
    rows = []
    for entry in bridge.registry._assertions.values():
        reference = bridge.registry.reference(entry.reference_id)
        if reference.locator != "(5.3)":
            continue
        rows.append({
            "assertion_id": entry.assertion_id,
            "type": type(entry.content).__name__,
            "origin": entry.origin.value,
            "publication_position": reference.publication_position,
            "component_position": entry.component_position,
            "prior_to_pi53": precedes_citing_assertion(
                bridge, entry.assertion_id, citing_id,
            ),
            "screened_as_given": any(
                link.assertion_id == entry.assertion_id
                and link.step is not None
                and link.step.rule is ProofRule.GIVEN
                for link in screened.proof_links
            ),
        })
    return rows


def audit() -> int:
    bridge = build_shared_typed_bridge()
    contexts = []
    lower = search_group_from_registered_goal(n=2, k=2, bridge=bridge)
    upper = search_group_from_registered_goal(
        n=3, k=2, bridge=bridge, context_sink=contexts.append,
    )
    if lower.status is not ProofSearchStatus.COMPLETE:
        raise AssertionError("pi_4^2 previous complete proof is unavailable")
    if len(contexts) != 1:
        raise AssertionError("expected one actual pi_5^3 screened context")
    screened = contexts[0]
    upper_goals = registered_group_goal_candidates(bridge, n=3, k=2)
    if len(upper_goals) != 1:
        raise AssertionError("pi_5^3 registered goal not unique")
    target = upper_goals[0]
    target_rows = _references_for_exact_content(bridge, target)
    if len(target_rows) != 1:
        raise AssertionError("pi_5^3 typed citing assertion not unique")
    citing_id = target_rows[0]["assertion_id"]
    provider = shared_expansion_provider(screened, proof_target=target)
    given_contents = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    hopf_terminal = TodaHopfInvariantSurjectiveStatement(
        TodaHopfInvariantMap(TodaPrimaryGroup(6, 3), TodaPrimaryGroup(6, 5)),
    )
    delta_terminal = TodaDeltaInjectiveStatement(
        TodaDeltaMap(TodaPrimaryGroup(5, 5), TodaPrimaryGroup(3, 2)),
    )
    options_h = expand_registered_ehp_terminal_goal(hopf_terminal, given_contents)
    options_d = expand_registered_ehp_terminal_goal(delta_terminal, given_contents)
    live_h = provider(hopf_terminal)
    live_d = provider(delta_terminal)
    if len(options_h) != 1 or len(options_d) != 1:
        raise AssertionError("R3F3 terminal proposals must each be unique")
    if not any(
        item.rule.name == options_h[0].rule.name and item.subgoals == options_h[0].subgoals
        for item in live_h
    ) or not any(
        item.rule.name == options_d[0].rule.name and item.subgoals == options_d[0].subgoals
        for item in live_d
    ):
        raise AssertionError("R3F3 terminal proposals not connected to live provider")
    hopf_relation, composite = options_h[0].subgoals
    (delta_composite,) = options_d[0].subgoals
    if not isinstance(hopf_relation, Relation):
        raise AssertionError("Hopf predecessor is not a typed Relation")
    if not isinstance(composite, TodaProp51FiniteDimensionalStatement):
        raise AssertionError("Proposition 5.1 predecessor has unexpected type")
    if delta_composite != composite:
        raise AssertionError("two terminal branches require different composite predicates")

    manuscript = (ROOT / "sources" / "toda" / "Toda_05_2.tex").read_text(encoding="utf-8")
    marker = r"\label{eq:5.3}"
    entry = manuscript.find(marker)
    if entry < 0 or r"H(\nu')=\eta_5" not in manuscript[entry:entry+260]:
        raise AssertionError("adopted (5.3) Hopf formula not located in reviewed source")
    equation = manuscript[entry:manuscript.find(r"\end{equation}", entry)]
    statement_rows = _references_for_exact_content(bridge, hopf_relation)
    composite_rows = _references_for_exact_content(bridge, composite)
    metadata = _historical_metadata(bridge, screened, citing_id)
    if not metadata:
        raise AssertionError("(5.3) source component metadata unexpectedly missing")
    # No inference step is silently produced: an eligible GIVEN for the entire
    # Proposition 5.1 composite remains a GIVEN until a sound rule proves it.
    prop51_screened = _screened_steps(screened, composite)
    hopf_screened = _screened_steps(screened, hopf_relation)
    required = [p.proof_rule for p in options_h[0].rule.premise_patterns]
    required_d = [p.proof_rule for p in options_d[0].rule.premise_patterns]
    if required != [ProofRule.INFERENCE, ProofRule.INFERENCE] or required_d != [ProofRule.INFERENCE]:
        raise AssertionError("historical terminal inference provenance unexpectedly changed")
    hopf_attempt = _try_reconstruct(hopf_relation, screened, citing_id, provider)
    comp_attempt = _try_reconstruct(composite, screened, citing_id, provider)
    report = {
        "phase": "169-R3G",
        "mode": "AUDIT_ONLY",
        "git_head": __import__("subprocess").run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
            capture_output=True, check=True,
        ).stdout.strip(),
        "lower_status": lower.status.value,
        "upper_status": upper.status.value,
        "upper_proven_steps": len(upper.proven_steps),
        "pi5_citing_id": citing_id,
        "source_53": {
            "label_found": True,
            "literal_hopf_formula_found": True,
            "snippet": equation[:300],
            "registry_entries": metadata,
            "entry_types": dict(Counter(item["type"] for item in metadata)),
        },
        "hopf_relation": {
            "goal_repr": repr(hopf_relation),
            "exact_registry_assertions": statement_rows,
            "screened_exact_given": hopf_screened,
            "live_provider_proposals": len(provider(hopf_relation)),
            "reconstruction": hopf_attempt,
        },
        "prop51_composite": {
            "exact_registry_assertions": composite_rows,
            "screened_exact_given": prop51_screened,
            "live_provider_proposals": len(provider(composite)),
            "reconstruction": comp_attempt,
        },
        "terminal_premise_rules": {
            "hopf_surjective": [item.value for item in required],
            "delta_injective": [item.value for item in required_d],
        },
        "new_givens": 0,
        "source_modified": False,
        "completion_claim": False,
    }
    output = HERE / "output" / "source_and_composite.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"LOWER_STATUS={report['lower_status']}")
    print(f"UPPER_STATUS={report['upper_status']}")
    print(f"UPPER_PROVEN_STEPS={report['upper_proven_steps']}")
    print("TODA53_METADATA_TYPES=" + repr(report["source_53"]["entry_types"]))
    print("HOPF_SOURCE_EXACT_TYPED_ASSERTIONS=" + str(len(statement_rows)))
    print("HOPF_SOURCE_SCREENED_GIVEN=" + str(len(hopf_screened)))
    print("HOPF_SOURCE_PROVIDER_PROPOSALS=" + str(report["hopf_relation"]["live_provider_proposals"]))
    print("HOPF_SOURCE_RECONSTRUCTION=" + repr(hopf_attempt))
    print("PROP51_COMPOSITE_SCREENED_GIVEN=" + str(len(prop51_screened)))
    print("PROP51_COMPOSITE_PROVIDER_PROPOSALS=" + str(report["prop51_composite"]["live_provider_proposals"]))
    print("PROP51_COMPOSITE_RECONSTRUCTION=" + repr(comp_attempt))
    print("TERMINAL_REQUIRED_RULES=" + repr(report["terminal_premise_rules"]))
    print("REPORT=" + str(output))
    print("R3G_AUDIT_COMPLETE: source citation and inference are distinct; full suite NOT run")
    return 0


if __name__ == "__main__":
    raise SystemExit(audit())
