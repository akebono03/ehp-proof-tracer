"""R2J-R2: prove H surjective from a cited cyclic group generator image.

R2I is reconstructed inside this proof, not imported as a completed proof
or inserted as a leaf. This audit does not assert Delta=0 or pi_6^3.
"""
from __future__ import annotations

import json
from pathlib import Path

from expression import Composition, MapApplication
from homotopy_groups import TodaHopfInvariantMap, TodaPrimaryGroup
from map_facts import EHP_H_MAP
from phase165_r12_r20_eta_definition import expand_cited_eta_definition
from phase165_r12_r21_eta_generator_chain import expand_cited_eta_generator
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase166_r3c_publication_order import precedes_citing_assertion
from phase168_r2_8_4_generic_specialization.specialization import specialize_registered_higher_stem
from phase171_r2h_prop22_cited_hopf.source import expand_cited_prop22_right_formula
from phase171_r2i_eta_hopf_bridge.audit import _available, _checked_chain, _screened_context
from phase171_r2i_eta_hopf_bridge.source import expand_cited_eta_hopf_power
from phase171_r2j_r2_cyclic_hopf_surjective.source import (
    _valid_surjective_pair,
    expand_cited_cyclic_hopf_surjectivity,
)
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin

OUTPUT = Path(__file__).resolve().parent / "output"
SOURCE = Path(__file__).resolve().parent.parent / "sources" / "toda" / "Toda_05_2.tex"


def _verify_adopted_prop53_text() -> None:
    """Check the reviewed transcription; do not claim original-edition verification."""
    text = SOURCE.read_text(encoding="utf-8-sig")
    begin = text.find(r"\begin{proposition}\label{prop:5.3}")
    end = text.find(r"\end{proposition}", begin)
    if begin < 0 or end <= begin:
        raise RuntimeError("adopted Proposition 5.3 source block missing")
    clause = text[begin:end]
    if any(piece not in clause for piece in (
        r"\pi^{n}_{n+2}", r"\eta_n^{2}", r"\mathbb Z_2", r"n\ge2",
    )):
        raise RuntimeError("adopted Proposition 5.3 theorem text is incomplete")


def _scoped_provider(available: tuple[object, ...], goal: MapSurjective):
    """Exact known obligations; no historical completed-proof import."""
    def expand(current: object):
        return (
            expand_cited_cyclic_hopf_surjectivity(
                current, available, proof_target=goal,
            )
            + expand_cited_eta_hopf_power(current, available)
            + expand_cited_prop22_right_formula(current, available)
            + expand_cited_eta_definition(current, available)
            + expand_cited_eta_generator(current)
        )
    return expand


def build_cited_r2j_r2_proof():
    """Reconstruct the proof tree from four screened, earlier cited leaves."""
    _verify_adopted_prop53_text()
    screened, group_goal, citing = _screened_context()
    chain, available = _checked_chain(screened, citing)
    hopf = TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5),
    )
    goal = MapSurjective(hopf)
    expected_image = chain.conclusion
    if (expected_image.lhs != MapApplication(
            EHP_H_MAP, Composition(chain.alpha, chain.eta_next),
        ) or not isinstance(expected_image.rhs, Composition)):
        raise RuntimeError("R2I Hopf image has the wrong type")
    proposals = expand_cited_cyclic_hopf_surjectivity(
        goal, available, proof_target=group_goal,
    )
    if len(proposals) != 1 or proposals[0].subgoals[1] != expected_image:
        raise RuntimeError("generator-in-image proposal not uniquely screened")
    prior_group = proposals[0].subgoals[0]
    if not _valid_surjective_pair(goal, prior_group, expected_image):
        raise RuntimeError("cyclic generator/element identity mismatch")
    source_links = []
    for link in screened.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        if not isinstance(link.step.conclusion, Relation):
            continue
        specialized = specialize_registered_higher_stem(
            link.step.conclusion, 5,
        )
        if specialized != prior_group:
            continue
        assertion = screened.registry.assertion(link.assertion_id)
        ref = screened.registry.reference(assertion.reference_id)
        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or ref.locator != "Proposition 5.3"
                or not precedes_citing_assertion(
                    screened, link.assertion_id, citing,
                )):
            raise RuntimeError("Proposition 5.3 is not an earlier fixed source")
        source_links.append(link)
    if len(source_links) != 1:
        raise RuntimeError("exactly one screened Proposition 5.3 source required")
    public_options = shared_expansion_provider(
        screened, proof_target=group_goal,
    )(goal)
    if not any(
        option.subgoals == proposals[0].subgoals
        and option.rule.name == proposals[0].rule.name
        for option in public_options
    ):
        raise RuntimeError("R2J rule not connected to shared provider")
    proof = reconstruct_registered_goal(
        goal, screened, citing, _scoped_provider(available, goal),
        lookup_mode="typed_reference_publication",
    )
    if (proof.rule is not ProofRule.INFERENCE
            or proof.conclusion != goal
            or len(proof.premises) != 2
            or any(p.rule is not ProofRule.INFERENCE for p in proof.premises)
            or proof.premises[0].conclusion != prior_group
            or proof.premises[1].conclusion != expected_image):
        raise RuntimeError("H surjectivity was not reconstructed from two inferences")
    nodes = []
    seen = set()

    def visit(step):
        if id(step) in seen:
            return
        seen.add(id(step))
        nodes.append(step)
        for parent in step.premises:
            visit(parent)

    visit(proof)
    leaves = [step for step in nodes if step.rule is ProofRule.GIVEN]
    sources = tuple(link.step.conclusion for link in screened.proof_links
                    if link.step is not None and link.step.rule is ProofRule.GIVEN)
    if (len(leaves) != 4
            or any(leaf.premises for leaf in leaves)
            or any(leaf.conclusion not in sources for leaf in leaves)
            or sum(leaf.conclusion == source_links[0].step.conclusion
                   for leaf in leaves) != 1):
        raise RuntimeError("unexpected or fabricated GIVEN in H surjectivity proof")
    if any(step.conclusion == group_goal for step in nodes):
        raise RuntimeError("pi_6^3 group structure improperly inserted")
    if any(step.rule is ProofRule.GIVEN
           and step.conclusion in (prior_group, expected_image, goal)
           for step in nodes):
        raise RuntimeError("derived group/Hopf/map fact promoted to GIVEN")
    return proof, prior_group, chain, tuple(nodes), source_links[0]


def run() -> None:
    proof, group, chain, nodes, link = build_cited_r2j_r2_proof()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    report = {
        "result": "PASS_CITED_H_SURJECTIVE_ONLY",
        "hopf_map": repr(proof.conclusion.map),
        "group": repr(group),
        "r2i_image": repr(chain.conclusion),
        "prop53_assertion_id": link.assertion_id,
        "inferences": sum(step.rule is ProofRule.INFERENCE for step in nodes),
        "given_leaves": sum(step.rule is ProofRule.GIVEN for step in nodes),
        "given_conclusions": [repr(step.conclusion) for step in nodes
                              if step.rule is ProofRule.GIVEN],
        "delta_zero_proven": False,
        "pi63_proven": False,
        "adopted_prop53_text_matched": True,
        "original_edition_verified": False,
        "registration_status_not_upgraded": True,
        "full_pytest": False,
    }
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE171_R2J_R2_PROP53_SPECIALIZATION=PASS", flush=True)
    print("PHASE171_R2J_R2_R2I_INFERRED_ANCESTRY=PASS", flush=True)
    print("PHASE171_R2J_R2_CYCLIC_GENERATOR_IN_IMAGE=PASS", flush=True)
    print("PHASE171_R2J_R2_H_SURJECTIVE=PASS", flush=True)
    print("PHASE171_R2J_R2_GIVEN_LEAVES=" + str(report["given_leaves"]), flush=True)
    print("PHASE171_R2J_R2_INFERENCES=" + str(report["inferences"]), flush=True)
    print("PHASE171_R2J_R2_DELTA_ZERO_PROVEN=False", flush=True)
    print("PHASE171_R2J_R2_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2J_R2_RESULT=PASS_CITED_H_SURJECTIVE_ONLY", flush=True)
    print("PHASE171_R2J_R2_REPORT=" + str(OUTPUT / "audit.json"), flush=True)


if __name__ == "__main__":
    run()
