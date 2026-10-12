"""Phase 161 R7: verify ancestry before backward-driven reconstruction.

Trusted GIVEN roots are an explicit caller-provided trust boundary. This code
verifies inference derivations, not the external truth of those roots.
"""

from dataclasses import dataclass

from phase161_r5_backward_proof_reconstruction import (
    BackwardReconstructionResult,
    reconstruct_phase161_r5_goal,
)
from proof import (
    ProofRule,
    ProofStep,
    apply_inference_match,
    find_inference_matches_for_rule,
)


@dataclass(frozen=True)
class PremiseProvenanceReport:
    verified_steps: int
    verified_inferences: int
    trusted_roots_used: tuple[ProofStep, ...]


@dataclass(frozen=True)
class ValidatedBackwardReconstruction:
    reconstruction: BackwardReconstructionResult
    provenance: PremiseProvenanceReport


def validate_phase161_r7_provenance(
    steps: tuple[ProofStep, ...],
    trusted_given_roots: tuple[ProofStep, ...],
) -> PremiseProvenanceReport:
    """Check reachable proof ancestry using exact premise identities and rules.

    A trusted root must be the same ProofStep object, not merely an equal
    dataclass value. No inference with missing premises is accepted.
    """
    if not isinstance(steps, tuple) or any(not isinstance(s, ProofStep) for s in steps):
        raise TypeError("steps must be a tuple of ProofStep")
    if not isinstance(trusted_given_roots, tuple) or any(
        not isinstance(s, ProofStep) for s in trusted_given_roots
    ):
        raise TypeError("trusted_given_roots must be a tuple of ProofStep")
    if any(s.rule is not ProofRule.GIVEN or s.premises for s in trusted_given_roots):
        raise ValueError("Trusted roots must be premise-free GIVEN steps")

    trusted_ids = {id(s) for s in trusted_given_roots}
    visiting = set()
    verified = set()
    inferences = set()
    roots = {}

    def visit(step: ProofStep) -> None:
        identity = id(step)
        if identity in verified:
            return
        if identity in visiting:
            raise ValueError("Cyclic proof ancestry")
        visiting.add(identity)
        try:
            if step.rule is ProofRule.GIVEN:
                if step.premises or identity not in trusted_ids:
                    raise ValueError("Untrusted GIVEN provenance root")
                roots[identity] = step
            elif step.rule is ProofRule.INFERENCE:
                if step.inference_rule is None or not step.premises:
                    raise ValueError("Unjustified INFERENCE ancestry")
                if any(not isinstance(p, ProofStep) for p in step.premises):
                    raise ValueError("Inference contains non-ProofStep premises")
                for premise in step.premises:
                    visit(premise)
                matches = (
                    candidate
                    for candidate in find_inference_matches_for_rule(
                        step.inference_rule, step.premises
                    )
                    if len(candidate.premises) == len(step.premises)
                    and all(a is b for a, b in zip(candidate.premises, step.premises))
                )
                if not any(
                    apply_inference_match(match).conclusion == step.conclusion
                    for match in matches
                ):
                    raise ValueError("Inference does not follow from recorded premises")
                inferences.add(identity)
            else:
                raise ValueError("Unsupported proof-rule provenance")
            verified.add(identity)
        finally:
            visiting.remove(identity)

    for step in steps:
        visit(step)
    return PremiseProvenanceReport(
        verified_steps=len(verified),
        verified_inferences=len(inferences),
        trusted_roots_used=tuple(roots.values()),
    )


def reconstruct_phase161_r7_validated_goal(
    goal: object,
    available_leaf_steps: tuple[ProofStep, ...],
    trusted_given_roots: tuple[ProofStep, ...],
) -> ValidatedBackwardReconstruction:
    """Reject unverified inputs, reconstruct via R5, and audit final ancestry."""
    validate_phase161_r7_provenance(available_leaf_steps, trusted_given_roots)
    result = reconstruct_phase161_r5_goal(goal, available_leaf_steps)
    report = validate_phase161_r7_provenance((result.final_step,), trusted_given_roots)
    return ValidatedBackwardReconstruction(reconstruction=result, provenance=report)
