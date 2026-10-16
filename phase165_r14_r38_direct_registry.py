"""Phase165: register adopted typed Toda references and finish pi3^2 proof."""
from __future__ import annotations

from pathlib import Path
from dataclasses import replace
from proof import InferenceRule, LiteratureReference

from phase163_r4_registry_bridge import MigrationRecord, MigrationStatus, RegistryBridgeResult
from phase165_r14_r35_leaf_binding import known_source_candidates
from phase165_r14_r36_adopted_backward import adopted_leaf_steps
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin,
    LiteratureEntry, ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)


def build_adopted_typed_reference_registry(tex_path: Path) -> RegistryBridgeResult:
    """Bind nine already typed R36 source leaves to the unified registry.

    This treats Toda's adopted TeX and sourced foundational fact as references;
    it does not claim that the original edition was independently checked.
    """
    steps = adopted_leaf_steps(Path(tex_path))
    leaves = tuple(step.conclusion for step in steps)
    known = known_source_candidates(Path(tex_path))
    if len(leaves) != len(steps) or len(leaves) != 9:
        raise ValueError("R36 frontier changed")
    registry = UnifiedStatementRegistry()
    records = []
    links = []
    for index, goal in enumerate(leaves, start=1):
        matches = [step for step in steps if type(step.conclusion) is type(goal) and step.conclusion == goal]
        if len(matches) != 1 or matches[0].rule is not ProofRule.GIVEN:
            raise ValueError("unresolved or non-Reference leaf")
        source = [item for item in known if type(item.goal) is type(goal) and item.goal == goal]
        if len(source) > 1:
            raise ValueError("ambiguous adopted source")
        if source:
            locator = source[0].locator
            source_id = source[0].source_id
            if source_id == "UNRESOLVED_EXACT_REGISTRY_ID":
                # Preserve the known exact citation locator without inventing an archive ID.
                source_id = "Toda translated TeX:Proposition 5.1 (archive ID unresolved)"
        elif bool(getattr(matches[0], "foundational_reference", None)):
            locator = "Foundational: suspension identity"
            source_id = "R17 foundational reference"
        elif "FreeCyclicGroup" in repr(goal):
            locator = "(5.1)"
            source_id = "Toda translated TeX:(5.1)"
        else:
            raise ValueError("unmatched source without explicit provenance")
        ref_id = f"adopted:ref:{index}"
        assertion_id = f"adopted:assertion:{index}"
        registry.add_reference(LiteratureEntry(
            ref_id, ReferenceKind.PROPOSITION if locator.startswith("Proposition")
            else ReferenceKind.EQUATION, locator, source_id=source_id,
        ))
        registry.add_assertion(AssertionEntry(
            assertion_id, ref_id, AssertionKind.STATEMENT, goal,
            origin=AssertionOrigin.FIXED_STATEMENT,
        ))
        # phase165_r42_source_inference: keep the existing GIVEN statement,
        # and attach its source locator to the ProofStep used by the renderer.
        # Foundational references retain their separate provenance mechanism.
        source_step = matches[0]
        if locator.startswith("Proposition ") or locator.startswith("("):
            source_step = replace(
                source_step,
                inference_rule=InferenceRule(
                    name="Toda " + locator,
                    literature_reference=LiteratureReference(
                        label="Toda " + locator, locator=locator,
                    ),
                ),
            )
        links.append(ProofStepLink(assertion_id, step=source_step))
        records.append(MigrationRecord(
            "adopted_typed_reference", locator, assertion_id,
            MigrationStatus.STRUCTURED, "adopted TeX; original edition unverified",
        ))
    return RegistryBridgeResult(registry, tuple(records), tuple(links))




