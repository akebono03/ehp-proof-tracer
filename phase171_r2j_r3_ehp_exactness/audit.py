"""R2J-R3: replay H-surjectivity and both cited EHP windows, no GIVEN promotion."""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import (
    TodaDeltaMap, TodaHopfInvariantMap, TodaPrimaryGroup, TodaSuspensionMap,
)
from phase165_r12_r11_prop42_unified import (
    TodaProp42GeneralExactnessStatement, expand_cited_prop42_exactness,
)
from phase165_r12_r20_eta_definition import expand_cited_eta_definition
from phase165_r12_r21_eta_generator_chain import expand_cited_eta_generator
from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase166_r3c_publication_order import precedes_citing_assertion
from phase171_r2h_prop22_cited_hopf.source import expand_cited_prop22_right_formula
from phase171_r2i_eta_hopf_bridge.audit import _available, _checked_chain, _screened_context
from phase171_r2i_eta_hopf_bridge.source import expand_cited_eta_hopf_power
from phase171_r2j_r2_cyclic_hopf_surjective.source import expand_cited_cyclic_hopf_surjectivity
from phase171_r2j_r3_ehp_exactness.source import (
    _delta_e_inputs, _h_delta_inputs, expand_cited_ehp_surjectivity_consequences,
)
from proof import ProofRule
from toda_rules import TodaDeltaZeroStatement, TodaProp42ExactnessStatement
from unified_statement_registry import AssertionOrigin

OUTPUT = Path(__file__).resolve().parent / "output"


def _goals():
    delta = TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(7, 5), TodaPrimaryGroup(5, 2),
    ))
    e_injective = MapInjective(TodaSuspensionMap(
        TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 3),
    ))
    return delta, e_injective


def _scoped_provider(available, proof_target):
    def expand(goal):
        return (
            expand_cited_ehp_surjectivity_consequences(goal)
            + expand_cited_prop42_exactness(goal, available)
            + expand_cited_cyclic_hopf_surjectivity(
                goal, available, proof_target=proof_target,
            )
            + expand_cited_eta_hopf_power(goal, available)
            + expand_cited_prop22_right_formula(goal, available)
            + expand_cited_eta_definition(goal, available)
            + expand_cited_eta_generator(goal)
        )
    return expand


def _walk(root):
    result = []
    seen = set()

    def visit(step):
        if id(step) in seen:
            return
        seen.add(id(step))
        result.append(step)
        for parent in step.premises:
            visit(parent)
    visit(root)
    return tuple(result)


def build_r2j_r3_proof():
    """Build the two zero/injective roots using one screened pi6^3 context."""
    screened, group_goal, citing = _screened_context()
    chain, available = _checked_chain(screened, citing)
    delta, injective = _goals()
    exact_sources = tuple(
        link for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and type(link.step.conclusion) is TodaProp42GeneralExactnessStatement
    )
    if len(exact_sources) != 1:
        raise RuntimeError("one citation-screened Proposition 4.2 general source required")
    entry = exact_sources[0]
    if (screened.registry.assertion(entry.assertion_id).origin is not AssertionOrigin.FIXED_STATEMENT
            or not precedes_citing_assertion(screened, entry.assertion_id, citing)):
        raise RuntimeError("Proposition 4.2 not positioned before the group goal")
    if _h_delta_inputs(delta) is None or _delta_e_inputs(injective) is None:
        raise RuntimeError("EHP consecutive windows have invalid indices")
    if _h_delta_inputs(delta)[0] != MapSurjective(TodaHopfInvariantMap(
            TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5))):
        raise RuntimeError("the H-Delta window uses a wrong Hopf map")
    if _delta_e_inputs(injective)[0] != delta:
        raise RuntimeError("the two EHP windows do not share the same Delta")
    public = shared_expansion_provider(screened, proof_target=group_goal)
    for target in (delta, injective):
        if not any(option.subgoals == expand_cited_ehp_surjectivity_consequences(target)[0].subgoals
                   and option.rule.name == expand_cited_ehp_surjectivity_consequences(target)[0].rule.name
                   for option in public(target)):
            raise RuntimeError("R2J-R3 is not connected to the public shared provider")
    expand = _scoped_provider(available, group_goal)
    delta_root = reconstruct_registered_goal(
        delta, screened, citing, expand, lookup_mode="typed_reference_publication",
    )
    injective_root = reconstruct_registered_goal(
        injective, screened, citing, expand, lookup_mode="typed_reference_publication",
    )
    if (delta_root.rule is not ProofRule.INFERENCE
            or injective_root.rule is not ProofRule.INFERENCE
            or delta_root.conclusion != delta
            or injective_root.conclusion != injective):
        raise RuntimeError("the two EHP conclusions were not inferred")
    ancestry = _walk(injective_root)
    if not any(step.conclusion == chain.conclusion and step.rule is ProofRule.INFERENCE
               for step in ancestry):
        raise RuntimeError("R2I Hopf image is not an inferred ancestor")
    if not any(step.conclusion == delta and step.rule is ProofRule.INFERENCE
               for step in ancestry):
        raise RuntimeError("Delta=0 was not inferred")
    if not any(step.conclusion == _h_delta_inputs(delta)[0]
               and step.rule is ProofRule.INFERENCE for step in ancestry):
        raise RuntimeError("R2J-R2 surjectivity was not inferred")
    expected_windows = (_h_delta_inputs(delta)[1], _delta_e_inputs(injective)[1])
    for window in expected_windows:
        matches = tuple(step for step in ancestry if step.conclusion == window)
        if (len(matches) != 1 or matches[0].rule is not ProofRule.INFERENCE
                or not any(parent.conclusion == entry.step.conclusion
                           and parent.rule is ProofRule.GIVEN for parent in matches[0].premises)):
            raise RuntimeError("specialized exactness lacks the cited universal source")
    leaves = tuple(step for step in ancestry if step.rule is ProofRule.GIVEN)
    permitted = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    if (len(leaves) != 5
            or any(leaf.conclusion not in permitted or leaf.premises for leaf in leaves)
            or sum(leaf.conclusion == entry.step.conclusion for leaf in leaves) != 1):
        raise RuntimeError("wrong number or content of citation-screened GIVEN leaves")
    forbidden = (delta, injective, _h_delta_inputs(delta)[0])
    if any(step.conclusion in forbidden and step.rule is ProofRule.GIVEN for step in ancestry):
        raise RuntimeError("EHP result was promoted into GIVEN")
    if any(step.conclusion == group_goal for step in ancestry):
        raise RuntimeError("pi6^3 target group prematurely imported")
    return delta_root, injective_root, ancestry, entry


def run():
    delta_root, injective_root, ancestry, ref = build_r2j_r3_proof()
    report = {
        "result": "PASS_CITED_DELTA_ZERO_AND_E_INJECTIVE_ONLY",
        "delta_zero": repr(delta_root.conclusion),
        "e_injective": repr(injective_root.conclusion),
        "proposition42_assertion_id": ref.assertion_id,
        "inferences": sum(step.rule is ProofRule.INFERENCE for step in ancestry),
        "given_leaves": sum(step.rule is ProofRule.GIVEN for step in ancestry),
        "given_added": 0,
        "pi63_proven": False,
        "full_pytest": False,
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    report_path = OUTPUT / "audit.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R3_H_SURJECTIVE_ANCESTRY=PASS", flush=True)
    print("PHASE171_R2J_R3_H_DELTA_EXACTNESS=PASS", flush=True)
    print("PHASE171_R2J_R3_DELTA_ZERO=PASS", flush=True)
    print("PHASE171_R2J_R3_DELTA_E_EXACTNESS=PASS", flush=True)
    print("PHASE171_R2J_R3_E_INJECTIVE=PASS", flush=True)
    print("PHASE171_R2J_R3_INFERENCES=" + str(report["inferences"]), flush=True)
    print("PHASE171_R2J_R3_GIVEN_LEAVES=" + str(report["given_leaves"]), flush=True)
    print("PHASE171_R2J_R3_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2J_R3_RESULT=" + report["result"], flush=True)
    print("PHASE171_R2J_R3_REPORT=" + str(report_path), flush=True)


if __name__ == "__main__":
    run()
