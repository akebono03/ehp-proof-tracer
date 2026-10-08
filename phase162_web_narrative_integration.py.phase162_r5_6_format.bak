"""Phase 162 R5: add a separately validated map-isomorphism proof to web narrative."""

from homotopy_groups import TodaEHPExactnessWindow, TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase161_r7_premise_provenance_validation import (
    reconstruct_phase161_r7_validated_goal,
)
from phase162_validated_proof_presentation import (
    build_validated_backward_proof_presentation,
    render_validated_backward_proof_markdown,
)
from probes.probe_phase55_capabilities import build_phase55_representative_result
from probes.probe_phase58_capabilities import build_phase58_representative_result
from proof import ProofRule, ProofStep
from toda_rules import TodaProp42ExactnessStatement


def build_phase162_web_validated_isomorphism_markdown() -> str:
    """Render only after the exact provenance roots pass R7 validation."""
    prop51 = build_phase55_representative_result()["prop51_steps"][0]
    hopf_eta5 = build_phase58_representative_result()["final_hopf_step"]

    pi_3_2 = TodaPrimaryGroup(group_dimension=3, sphere_dimension=2)
    pi_4_2 = TodaPrimaryGroup(group_dimension=4, sphere_dimension=2)
    pi_5_3 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=3)
    pi_5_5 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=5)
    pi_6_3 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=3)
    pi_6_5 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=5)

    windows = (
        (pi_5_3, pi_5_5, pi_3_2, EHP_H_MAP, EHP_DELTA_MAP),
        (pi_4_2, pi_5_3, pi_5_5, EHP_E_MAP, EHP_H_MAP),
        (pi_6_3, pi_6_5, pi_4_2, EHP_H_MAP, EHP_DELTA_MAP),
        (pi_6_5, pi_4_2, pi_5_3, EHP_DELTA_MAP, EHP_E_MAP),
    )
    exactness = tuple(
        ProofStep(
            conclusion=TodaProp42ExactnessStatement(
                window=TodaEHPExactnessWindow(
                    source_term=source,
                    middle_term=middle,
                    target_term=target,
                    first_map=first,
                    second_map=second,
                )
            ),
            premises=(),
            rule=ProofRule.GIVEN,
        )
        for source, middle, target, first, second in windows
    )
    leaves = (prop51, hopf_eta5) + exactness
    trusted = {}
    visited = set()

    def collect(step: ProofStep) -> None:
        key = id(step)
        if key in visited:
            return
        visited.add(key)
        if step.rule is ProofRule.GIVEN:
            trusted[key] = step
        for premise in step.premises:
            collect(premise)

    for leaf in leaves:
        collect(leaf)

    validated = reconstruct_phase161_r7_validated_goal(
        phase161_r5_target_goal(), leaves, tuple(trusted.values())
    )
    presentation = build_validated_backward_proof_presentation(validated)
    return render_validated_backward_proof_markdown(presentation)
