"""Phase 164 R5-R2: select a proof replay, never render text here.

All selected replays must pass through the same presentation and renderer.
Existing specialized proof construction is preserved in this phase.
"""
from toda_group_result_proof_replay import build_toda_group_result_proof_replay


def build_phase164_r5_r2_common_replay(n: int, k: int, group_result, max_depth: int, mode: str):
    """Select an existing proof root; return replay without Markdown or Web views."""
    if mode == "narrative" and n == 3 and k == 2:
        from phase164_r5_web_registry_connection import build_phase164_r5_web_pi5_3_proof

        replay, _ = build_phase164_r5_web_pi5_3_proof(max_depth=max_depth)
        return replay

    if mode == "narrative" and k == 1 and n in (4, 5):
        from toda_calculation_facade import build_standard_toda_report
        from toda_stable_eta_proof_replay import build_toda_stable_eta_proof_replay

        base_report = build_standard_toda_report(n=3, k=1)
        if len(base_report.candidates) != 1:
            raise ValueError("stable eta proof requires one base group result")
        base_result = base_report.candidates[0].source_candidate.group_result
        derived = build_toda_stable_eta_proof_replay(
            group_result, base_result, max_depth=max(3, max_depth)
        )
        return derived.replay

    return build_toda_group_result_proof_replay(group_result, max_depth=max_depth)
