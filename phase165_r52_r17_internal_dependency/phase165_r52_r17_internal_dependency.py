"""R52-R17: reuse explicitly completed internal inference proofs, without self-citation."""
from __future__ import annotations

from dataclasses import dataclass

from proof import ProofRule, ProofStep


def same_statement(left: object, right: object) -> bool:
    return type(left) is type(right) and left == right


@dataclass(frozen=True)
class CompletedInternalProof:
    """Caller-supplied completed proof; this container does not certify its mathematics."""
    root: ProofStep

    def __post_init__(self) -> None:
        if not isinstance(self.root, ProofStep) or self.root.rule is not ProofRule.INFERENCE:
            raise ValueError("completed internal proof requires an inference root")
        validate_ancestry(self.root)


def validate_ancestry(root: ProofStep) -> None:
    """Reject structural cycles and any inference depending on its own conclusion."""
    active_ids: set[int] = set()
    visited_ids: set[int] = set()

    def visit(step: ProofStep, ancestors: tuple[object, ...]) -> None:
        identifier = id(step)
        if identifier in active_ids:
            raise ValueError("cyclic ProofStep ancestry")
        if any(same_statement(step.conclusion, earlier) for earlier in ancestors):
            raise ValueError("self-dependent ProofStep ancestry")
        if identifier in visited_ids:
            return
        active_ids.add(identifier)
        for premise in step.premises:
            if not isinstance(premise, ProofStep):
                raise ValueError("internal proof premises must be ProofSteps")
            visit(premise, ancestors + (step.conclusion,))
        active_ids.remove(identifier)
        visited_ids.add(identifier)

    visit(root, ())


def find_reusable_internal_proof(
    target: object,
    current_goal: object,
    completed: tuple[CompletedInternalProof, ...],
) -> ProofStep | None:
    """Reuse an established inference only for a distinct, nondependent goal."""
    if not isinstance(completed, tuple) or not all(isinstance(item, CompletedInternalProof) for item in completed):
        raise TypeError("completed must contain CompletedInternalProof objects")
    if same_statement(target, current_goal):
        return None
    matches: list[ProofStep] = []
    for item in completed:
        root = item.root
        if not same_statement(root.conclusion, target):
            continue
        try:
            validate_ancestry(root)
        except ValueError:
            continue
        if depends_on(root, current_goal):
            continue
        matches.append(root)
    if len(matches) > 1:
        raise ValueError("ambiguous completed internal proofs")
    return matches[0] if matches else None


def depends_on(root: ProofStep, statement: object) -> bool:
    """Check transitive proof-step ancestry, not just direct premise IDs."""
    seen: set[int] = set()

    def visit(step: ProofStep) -> bool:
        identifier = id(step)
        if identifier in seen:
            return False
        seen.add(identifier)
        return any(
            same_statement(child.conclusion, statement) or visit(child)
            for child in step.premises
        )

    return visit(root)
