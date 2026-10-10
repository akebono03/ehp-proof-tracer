"""Read-only ancestry diagnostics for Proposition 5.6 R4-R11 witnesses.

Does not make any provenance decisions or turn missing data into a citation.
"""
from __future__ import annotations

from dataclasses import dataclass

from proof import ProofRule, ProofStep


@dataclass(frozen=True)
class AncestryFinding:
    path: str
    issue: str
    conclusion_type: str
    rule_name: str | None


def diagnose_incomplete_ancestry(root: ProofStep) -> tuple[AncestryFinding, ...]:
    """Report all reachable structural provenance gaps, bounded by node identity."""
    if not isinstance(root, ProofStep):
        raise TypeError("root must be a ProofStep")
    findings: list[AncestryFinding] = []
    seen: set[int] = set()
    active: set[int] = set()

    def visit(node: ProofStep, path: str) -> None:
        identity = id(node)
        if identity in active:
            findings.append(AncestryFinding(path, "CYCLIC_ANCESTRY", type(node.conclusion).__name__, None))
            return
        if identity in seen:
            return
        active.add(identity)
        try:
            inference_name = node.inference_rule.name if node.inference_rule is not None else None
            if node.rule is ProofRule.INFERENCE:
                if node.inference_rule is None:
                    findings.append(AncestryFinding(path, "INFERENCE_RULE_MISSING", type(node.conclusion).__name__, None))
                if not node.premises:
                    findings.append(AncestryFinding(path, "INFERENCE_PREMISES_MISSING", type(node.conclusion).__name__, inference_name))
            elif node.rule is ProofRule.GIVEN:
                if node.premises:
                    findings.append(AncestryFinding(path, "GIVEN_HAS_PREMISES", type(node.conclusion).__name__, inference_name))
            else:
                findings.append(AncestryFinding(path, "UNSUPPORTED_PROOF_RULE", type(node.conclusion).__name__, inference_name))
            for position, premise in enumerate(node.premises):
                child_path = f"{path}/premise[{position}]"
                if not isinstance(premise, ProofStep):
                    findings.append(AncestryFinding(child_path, "NON_PROOFSTEP_PREMISE", type(premise).__name__, None))
                else:
                    visit(premise, child_path)
        finally:
            active.remove(identity)
            seen.add(identity)

    visit(root, "root")
    return tuple(findings)
