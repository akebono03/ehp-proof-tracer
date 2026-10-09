"""Phase 162 R3-A: audit R2 proof-tree to the existing Presentation.

No narrative, historical Markdown, or completed pi_5^3 ProofStep is read.
This script is intentionally a read-only audit of production objects.
"""

import json
from collections import Counter, deque
from pathlib import Path

from expression import Composition
from homotopy_groups import TodaSuspensionMap
from phase162_r2_existing_proof_connection import reconstruct_phase162_r2_from_existing_proofs
from proof import ProofRule, ProofStep, Relation, RelationType
from proof_repository import ProofRepositoryEntry
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result import normalize_toda_group_result
from toda_group_result_proof_replay import build_complete_toda_group_result_proof_replay
from toda_proof_dependency import extract_toda_recursive_proof_provenance
from toda_rules import toda_eta_family_definition_statement
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from tests.test_phase59_toda52_pi4_2_transport import build_phase59_2_data


def build_r2_fixture():
    """Use independently constructed premises, never a completed target proof."""
    source_data = build_phase59_2_data()
    ehp_data = build_phase59_3_data()
    source_step = source_data["result_steps"][0]
    eta3 = toda_eta_family_definition_statement(3)
    eta4 = toda_eta_family_definition_statement(4)
    eta_steps = (
        ProofStep(conclusion=eta3, premises=(), rule=ProofRule.GIVEN),
        ProofStep(conclusion=eta4, premises=(), rule=ProofRule.GIVEN),
    )
    suspension_map = TodaSuspensionMap(
        source_group=source_step.conclusion.lhs,
        target_group=ehp_data["expected_suspension_isomorphism"].map.target_group,
    )
    target_generator = Composition(left=eta3.element, right=eta4.element)
    goal = Relation(
        lhs=suspension_map.target_group,
        rhs=type(source_step.conclusion.rhs)(order=2, generator=target_generator),
        relation_type=RelationType.EQUALITY,
    )
    provided_steps = (source_step,) + eta_steps + ehp_data["premise_steps"]
    trusted = {}
    seen = set()

    def visit(step):
        if id(step) in seen:
            return
        seen.add(id(step))
        if step.rule is ProofRule.GIVEN:
            trusted[id(step)] = step
        for premise in step.premises:
            if not isinstance(premise, ProofStep):
                raise AssertionError("Non-ProofStep premise in input ancestry")
            visit(premise)

    for step in provided_steps:
        visit(step)
    result = reconstruct_phase162_r2_from_existing_proofs(
        goal=goal,
        suspension_map=suspension_map,
        source_structure_steps=(source_step,),
        eta_definition_steps=eta_steps,
        ehp_leaf_steps=ehp_data["premise_steps"],
        trusted_given_roots=tuple(trusted.values()),
    )
    return result


def audit_presentation():
    r2 = build_r2_fixture()
    final = r2.reconstruction.final_step
    entry = ProofRepositoryEntry(key="phase162_r3a_audit_pi5_3", step=final, phase="162")
    group = normalize_toda_group_result(entry)
    replay = build_complete_toda_group_result_proof_replay(group)
    presentation = build_toda_group_proof_presentation(replay)
    provenance = extract_toda_recursive_proof_provenance(group)

    assert group.proof_step is final
    assert group.source_entry is entry
    assert replay.root_step is final
    assert replay.source_entry is entry
    assert replay.group_result is group
    assert presentation.root_step is final
    assert presentation.source_replay is replay
    assert presentation.nodes is replay.steps
    assert len(final.premises) == 3
    assert final.premises[1] is r2.source_structure_step
    assert final.premises[2] is r2.generator_image_step

    original_node_ids = {id(node.proof_step) for node in provenance.nodes}
    replay_node_ids = {id(node.proof_step) for node in presentation.nodes}
    assert original_node_ids == replay_node_ids, "Lost or added proof nodes"
    assert len(replay_node_ids) == len(presentation.nodes), "Duplicated proof node"

    expected_edges = {
        (id(edge.parent_step), id(edge.premise_step), edge.premise_index)
        for edge in provenance.edges
    }
    actual_edges = {
        (id(edge.parent_step), id(edge.premise_step), edge.premise_index)
        for edge in presentation.edges
    }
    assert expected_edges == actual_edges, "Lost or added premise edges"
    assert len(actual_edges) == len(presentation.edges), "Duplicated proof edge"

    depth_by_id = {id(node.proof_step): node.shortest_depth for node in provenance.nodes}
    assert all(node.depth == depth_by_id[id(node.proof_step)] for node in replay.steps)
    assert replay.max_depth == max(depth_by_id.values())
    for edge in presentation.edges:
        assert edge.parent_step.premises[edge.premise_index] is edge.premise_step

    reachable = set()
    queue = deque([final])
    while queue:
        step = queue.popleft()
        if id(step) in reachable:
            continue
        reachable.add(id(step))
        queue.extend(step.premises)
    assert reachable == replay_node_ids, "Presentation does not match root ancestry"

    roles = Counter(node.role.value for node in presentation.nodes)
    report = {
        "status": "PASS",
        "goal_conclusion_type": type(final.conclusion).__name__,
        "root_inference_rule": final.inference_rule.name if final.inference_rule else None,
        "node_count": len(presentation.nodes),
        "edge_count": len(presentation.edges),
        "max_depth": replay.max_depth,
        "given_count": sum(node.proof_step.rule is ProofRule.GIVEN for node in presentation.nodes),
        "inference_count": sum(node.proof_step.rule is ProofRule.INFERENCE for node in presentation.nodes),
        "roles": dict(sorted(roles.items())),
        "root_premise_count": len(final.premises),
        "root_and_entry_identity": True,
        "all_nodes_preserved": True,
        "all_edges_preserved": True,
        "premise_object_identity_preserved": True,
        "provenance_verified_steps": r2.provenance.verified_steps,
        "provenance_verified_inferences": r2.provenance.verified_inferences,
    }
    return report


def main():
    report = audit_presentation()
    output = Path("phase162_r3a_presentation_audit_report.json")
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Audit report:", output.resolve())


if __name__ == "__main__":
    main()
