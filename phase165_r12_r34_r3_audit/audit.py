"""Read-only R12-R34-R3 foundational leaf audit."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r14_r16_foundational_suspension import (
    FOUNDATIONAL_SUSPENSION_IDENTITY,
    instantiate_foundational_identity_suspension,
)
from phase165_r14_r17_foundational_proofstep import derive_foundational_suspension_step
from proof import ProofRule


def audit() -> dict[str, object]:
    claim = instantiate_foundational_identity_suspension(1)
    statement = claim.statement
    step = derive_foundational_suspension_step(statement)
    if not isinstance(statement, GeneratorSuspension):
        raise AssertionError("wrong statement type")
    if step is None or step.rule is not ProofRule.GIVEN:
        raise AssertionError("foundational GIVEN unavailable")
    if step.conclusion != statement or step.premises:
        raise AssertionError("foundational leaf mismatch")
    if step.foundational_reference != FOUNDATIONAL_SUSPENSION_IDENTITY:
        raise AssertionError("foundational citation missing")
    if statement.source_generator.name != "ι₁" or statement.target_generator.name != "ι₂":
        raise AssertionError("unexpected generator arguments")
    return {
        "phase": "165 R12-R34-R3",
        "status": "FOUNDATIONAL_LEAF_CONFIRMED_RUNTIME_TREE_ANCESTRY_NOT_YET_VERIFIED",
        "statement_type": type(statement).__name__,
        "source_generator": statement.source_generator.name,
        "target_generator": statement.target_generator.name,
        "statement": "E(ι₁)=ι₂",
        "rule": step.rule.name,
        "foundational_reference": step.foundational_reference.key,
        "provenance_attached_to_constructed_leaf": True,
        "actual_pi43_proof_tree_checked": False,
        "pi32_ancestor_of_displayed_leaf_confirmed": False,
        "renderer_modified": False,
        "full_pytest_run": False,
        "next_phase": "R12-R34-R4: shared renderer ordering and prior-proof folding",
    }


def main() -> None:
    output = Path(__file__).resolve().parent / "audit_result.json"
    report = audit()
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Audit saved:", output)


if __name__ == "__main__":
    main()
