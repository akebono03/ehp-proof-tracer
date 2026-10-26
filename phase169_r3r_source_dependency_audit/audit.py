"""Read-only structural audit of Proposition 5.1 and EHP proof prerequisites.

This module does not alter a ProofStep, registry, source code, or reference.
"""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r57_r8_eta_specialization import specialize_eta_group_relation
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from proof import ProofRule, Relation
from toda_rules import (
    TodaDeltaInjectiveStatement,
    TodaHopfInvariantSurjectiveStatement,
    TodaProp51FiniteDimensionalStatement,
)

OUTPUT = Path(__file__).resolve().parent / "output"


def _ancestry(root):
    seen = set()
    pending = [root]
    nodes = []
    while pending:
        step = pending.pop()
        if id(step) in seen:
            continue
        seen.add(id(step))
        nodes.append(step)
        pending.extend(step.premises)
    return tuple(nodes)


def _step_details(step, model):
    indices = tuple(i for i, item in enumerate(model.steps) if item is step)
    if not indices:
        indices = tuple(i for i, item in enumerate(model.steps) if item == step)
    return {
        "type": type(step.conclusion).__name__,
        "rule": step.rule.value,
        "step_indices": indices,
        "citation_numbers": tuple(dict.fromkeys(
            number for i in indices for number in model.step_citation_numbers[i]
        )),
        "premise_types": tuple(type(parent.conclusion).__name__ for parent in step.premises),
        "premise_rules": tuple(parent.rule.value for parent in step.premises),
        "conclusion_repr": repr(step.conclusion),
    }


def report():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(n=3, k=2, bridge=bridge, context_sink=contexts.append)
    if not contexts:
        raise RuntimeError("Search returned no screened context")
    model = build_linked_proof_narrative_model(result, contexts[-1])
    if model.root_index is None:
        raise RuntimeError("Root proof step could not be located")
    root = model.steps[model.root_index]
    root_nodes = _ancestry(root)
    sources = tuple(step for step in root_nodes
                    if step.rule is ProofRule.GIVEN
                    and isinstance(step.conclusion, TodaProp51FiniteDimensionalStatement))
    delta = tuple(step for step in root_nodes
                  if isinstance(step.conclusion, TodaDeltaInjectiveStatement))
    hopf = tuple(step for step in root_nodes
                 if isinstance(step.conclusion, TodaHopfInvariantSurjectiveStatement))
    reference_rows = [{
        "number": citation.number,
        "locator": citation.reference.locator or citation.reference.label,
        "assertion_ids": citation.assertion_ids,
        "step_indices": citation.step_indices,
        "statement_bodies": citation.statement_bodies,
    } for citation in model.citations]
    prop51 = sources[0].conclusion if len(sources) == 1 else None
    pi65 = TodaPrimaryGroup(6, 5)
    eta_group = None
    if prop51 is not None:
        try:
            eta_group = specialize_eta_group_relation(prop51.higher_eta_group_relation, 5)
        except (TypeError, ValueError):
            eta_group = None
    pi55 = TodaPrimaryGroup(5, 5)
    proven_pi55 = tuple(step for step in root_nodes
                       if isinstance(step.conclusion, Relation)
                       and step.conclusion.lhs == pi55)
    cited_pi55 = tuple(step for step in root_nodes
                      if step.rule is ProofRule.GIVEN
                      and isinstance(step.conclusion, Relation)
                      and step.conclusion.lhs == pi55)
    data = {
        "phase": "169-R3R",
        "mode": "AUDIT_ONLY",
        "status": result.status.value,
        "model_steps": len(model.steps),
        "root_ancestry_count": len(root_nodes),
        "citation_rows": reference_rows,
        "proposition_5_1_composite_given_count": len(sources),
        "proposition_5_1_composite": (
            _step_details(sources[0], model) if len(sources) == 1 else None
        ),
        "proposition_5_1_components": ({
            "pi3_2_group_relation": repr(prop51.pi3_2_group_relation),
            "eta2_hopf_relation": repr(prop51.eta2_hopf_relation),
            "delta_iota5_relation": repr(prop51.delta_iota5_relation),
            "higher_eta_group_relation": repr(prop51.higher_eta_group_relation),
        } if prop51 is not None else {}),
        "pi_6_5_source_specialization_available": (
            eta_group is not None and eta_group.lhs == pi65
        ),
        "pi_6_5_source_specialization": repr(eta_group),
        "pi_6_5_independent_derived_relation_steps": tuple(
            _step_details(step, model) for step in root_nodes
            if isinstance(step.conclusion, Relation)
            and step.conclusion.lhs == pi65 and step.rule is ProofRule.INFERENCE
        ),
        "delta_injective": tuple(_step_details(step, model) for step in delta),
        "hopf_surjective": tuple(_step_details(step, model) for step in hopf),
        "pi_5_5_derived_relation_steps": tuple(_step_details(step, model) for step in proven_pi55),
        "pi_5_5_cited_given_relation_steps": tuple(_step_details(step, model) for step in cited_pi55),
        "toda_5_1_reference_in_model": any(
            item["locator"] == "(5.1)" for item in reference_rows
        ),
        "boundaries": (
            "A Proposition 5.1 component is literature data; projection must not invent a ProofStep.",
            "The pi_5^5 diagonal group requires its own cited (5.1) or another verified proof ancestor.",
            "The single Delta-injectivity proof premise must be inspected before claiming a complete explanation.",
            "The web's complete status is recorded without modifying or re-verifying the result.",
        ),
    }
    return data


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    data = report()
    (OUTPUT / "r3r_audit.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    keys = (
        "status", "model_steps", "root_ancestry_count",
        "proposition_5_1_composite_given_count", "pi_6_5_source_specialization_available",
        "toda_5_1_reference_in_model",
    )
    for key in keys:
        print("R3R_" + key.upper() + "=" + str(data[key]))
    print("R3R_DELTA_INJECTIVE=" + json.dumps(data["delta_injective"], ensure_ascii=False))
    print("R3R_HOPF_SURJECTIVE=" + json.dumps(data["hopf_surjective"], ensure_ascii=False))
    print("R3R_PI55_DERIVED_STEP_COUNT=" + str(len(data["pi_5_5_derived_relation_steps"])))
    print("R3R_PI55_GIVEN_STEP_COUNT=" + str(len(data["pi_5_5_cited_given_relation_steps"])))
    for row in data["citation_rows"]:
        print("R3R_REF=" + str(row["number"]) + " " + row["locator"]
              + " BODIES=" + str(len(row["statement_bodies"])))
    print("R3R_REPORT=" + str(OUTPUT / "r3r_audit.json"))
    print("R3R_AUDIT_ONLY=True")
    print("R3R_FULL_PYTEST_RUN=False")


if __name__ == "__main__":
    main()
