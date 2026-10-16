"""R35: inventory and safely associate strict-search leaves with known source claims.

This is a locator map, not verification or a registry certification.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from phase165_r14_r33_final_group import pi33_cyclic_step, hopf_eta2_image_step
from phase165_r14_r31_hopf_injective import (
    toda51_pi21_zero_step, prop42_e_h_exactness_step,
)
from phase165_r14_r30_hopf_surjective import prop42_h_delta_exactness_step
from phase165_r14_r29_delta_derived import Prop42ApplicationPolicy
from phase165_r14_r26_prop42_typed import (
    bind_proposition42, adopted_tex_proofstep,
)
from phase165_r14_r24_delta_connection import reviewed_r23_isomorphism
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from proof import ProofRule, ProofStep


@dataclass(frozen=True)
class LeafBindingCandidate:
    goal: object
    locator: str
    source_id: str
    evidence: str
    certification: str = "unverified_source_claim"




def known_source_candidates(tex_path: Path) -> tuple[LeafBindingCandidate, ...]:
    """Use the already implemented source-specific R23/R26/R30/R31/R33 factories.

    The factories produce provisional GIVEN claims, NOT registry eligible leaves.
    """
    policy = Prop42ApplicationPolicy(use_unrestricted_statement_as_written=True)
    bridge, _ = build_phase165_r5_manifest_bridge()
    r23_iso, _ = reviewed_r23_isomorphism(Path(tex_path))
    prop42_delta_e = adopted_tex_proofstep(
        bind_proposition42(bridge, n=1, i=2, index_scope_confirmed=True)
    )
    candidates = (
        (pi33_cyclic_step(tex_path), "(5.1)", "phase163:archive:toda:(5.1)", "diagonal group"),
        (hopf_eta2_image_step(), "Proposition 5.1", "UNRESOLVED_EXACT_REGISTRY_ID", "Hopf generator image"),
        (toda51_pi21_zero_step(tex_path), "(5.1)", "phase163:archive:toda:(5.1)", "pi_2(S^1)=0"),
        (prop42_e_h_exactness_step(policy), "Proposition 4.2", "phase163:archive:toda:tex:ch4:0005", "E to H exactness"),
        (prop42_h_delta_exactness_step(policy), "Proposition 4.2", "phase163:archive:toda:tex:ch4:0005", "H to Delta exactness"),
        (prop42_delta_e, "Proposition 4.2", "phase163:archive:toda:tex:ch4:0005", "Delta to E exactness"),
    )
    result = []
    for step, locator, source_id, evidence in candidates:
        if not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN:
            raise ValueError("expected source-specific provisional leaf")
        result.append(LeafBindingCandidate(step.conclusion, locator, source_id, evidence))
    # The R23 suspension is a derived premise and must NOT be mapped as a source leaf.
    if r23_iso.rule is not ProofRule.INFERENCE:
        raise ValueError("R23 derived suspension premise changed")
    return tuple(result)


