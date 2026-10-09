"""Build an isolated proof replay from a verified concrete eta transport.

Does not modify a repository entry or the public renderer.
"""

from dataclasses import dataclass

from proof_repository import ProofRepositoryEntry
from toda_group_result import TodaGroupResult, normalize_toda_group_result
from toda_group_result_proof_replay import (
    TodaGroupResultProofReplayResult,
    build_toda_group_result_proof_replay,
)
from toda_group_proof_presentation import (
    TodaGroupProofPresentation,
    build_toda_group_proof_presentation,
)
from toda_stable_concrete_transport_proof import (
    build_toda_stable_concrete_transport_proof,
)
from toda_stable_eta_generator_normalization import (
    TodaStableEtaNormalizedProof,
    build_toda_stable_eta_normalized_proof,
)


@dataclass(frozen=True)
class TodaStableEtaReplayIntegration:
    original_result: TodaGroupResult
    derived_proof: TodaStableEtaNormalizedProof
    derived_result: TodaGroupResult
    replay: TodaGroupResultProofReplayResult
    presentation: TodaGroupProofPresentation


def build_toda_stable_eta_proof_replay(
    target_result: TodaGroupResult,
    base_result: TodaGroupResult,
    max_depth: int = 3,
) -> TodaStableEtaReplayIntegration:
    """Replay eta transport from its own derived root, without root substitution.

    Only the concrete 1-stem normalization supported by the preceding R4-B2
    module is accepted. The supplied target root is comparison data, never a
    premise in the constructed derivation.
    """
    if not isinstance(target_result, TodaGroupResult):
        raise TypeError("target_result must be a TodaGroupResult")
    if not isinstance(base_result, TodaGroupResult):
        raise TypeError("base_result must be a TodaGroupResult")
    if isinstance(max_depth, bool) or not isinstance(max_depth, int) or max_depth < 0:
        raise ValueError("max_depth must be a nonnegative integer")

    transport = build_toda_stable_concrete_transport_proof(
        target_result, base_result
    )
    normalized = build_toda_stable_eta_normalized_proof(transport)
    derived_step = normalized.normalized_step
    conclusion = derived_step.conclusion
    if conclusion.lhs != target_result.target:
        raise ValueError("derived group does not match the requested target")
    if conclusion.rhs.order != target_result.group_structure.order:
        raise ValueError("derived group order disagrees with the target")
    source = target_result.source_entry
    ephemeral_entry = ProofRepositoryEntry(
        key=f"phase162.r4b2.derived.{source.key}",
        step=derived_step,
        phase="162-R4-B2",
        theorem=source.theorem,
    )
    derived_result = normalize_toda_group_result(ephemeral_entry)
    replay = build_toda_group_result_proof_replay(
        derived_result, max_depth=max_depth
    )
    presentation = build_toda_group_proof_presentation(replay)
    return TodaStableEtaReplayIntegration(
        original_result=target_result,
        derived_proof=normalized,
        derived_result=derived_result,
        replay=replay,
        presentation=presentation,
    )
