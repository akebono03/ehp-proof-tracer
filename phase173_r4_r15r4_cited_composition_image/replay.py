"""Replay a source-backed composite image in the existing proof engine.

Only actual cited Chapter V stable-family GIVEN steps are allowed as leaves.
The R15R3 canonical formal image inference is a separate, premise-free
inference; the proof construction adds no new GIVEN or direct DB leaf.
"""
from __future__ import annotations

from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10e8_hyoujigen_generic_suspension.chapter_vi_reference import (
    build_cited_chapter_vi_family_definitions,
)
from phase169_r10d2_general_family_definition.family_citation import (
    build_cited_stable_family_definitions,
    expand_cited_stable_family,
)
from phase173_r4_r15r3_formal_suspension_bridge.bridge import (
    expand_canonical_formal_image,
)
from phase173_r4_r15r4_cited_composition_image.bridge import (
    expand_composed_generator_image,
    generator_image,
)
from proof import (
    ProofRule,
    ProofStep,
    apply_inference_match,
    find_inference_matches_for_rule,
)
from unified_statement_registry import AssertionOrigin


def cited_source_steps() -> tuple[ProofStep, ...]:
    """Fetch the existing Chapter V source-verified GIVENs, not CSV assertions."""
    result: list[ProofStep] = []
    for cited in (
        build_cited_stable_family_definitions(),
        build_cited_chapter_vi_family_definitions(),
    ):
        for link in cited.proof_links:
            assertion = cited.registry.assertion(link.assertion_id)
            step = link.step
            if (
                assertion.origin is AssertionOrigin.FIXED_STATEMENT
                and step is not None
                and step.rule is ProofRule.GIVEN
                and step.conclusion == assertion.content
                and not step.premises
            ):
                result.append(step)
    return tuple(result)


def replay_cited_image(goal: object, sources: tuple[ProofStep, ...]) -> ProofStep | None:
    """Derive an image only if every leaf and inference matches an existing rule.

    Return None on missing cited definitions or missing atomic image rules.
    Does not modify the public expansion registry or Web proof results.
    """
    if not isinstance(goal, GeneratorImage) or not isinstance(sources, tuple):
        return None
    if any(step.rule is not ProofRule.GIVEN or step.premises for step in sources):
        return None
    available = tuple(step.conclusion for step in sources)
    if len(set(available)) != len(available):
        return None
    memo: dict[object, ProofStep | None] = {}
    in_progress: set[object] = set()

    def prove(statement: object) -> ProofStep | None:
        if statement in memo:
            return memo[statement]
        if statement in in_progress:
            return None
        for original in sources:
            if statement == original.conclusion and type(statement) is type(original.conclusion):
                memo[statement] = original
                return original
        in_progress.add(statement)
        proposals = (
            expand_canonical_formal_image(statement)
            + expand_cited_stable_family(statement, available)
            + expand_composed_generator_image(statement)
        )
        valid: list[ProofStep] = []
        for proposal in proposals:
            premises = tuple(prove(subgoal) for subgoal in proposal.subgoals)
            if any(premise is None for premise in premises):
                continue
            for match in find_inference_matches_for_rule(proposal.rule, premises):
                candidate = apply_inference_match(match)
                if (
                    candidate.rule is ProofRule.INFERENCE
                    and candidate.conclusion == statement
                    and candidate.premises == premises
                ):
                    valid.append(candidate)
        in_progress.remove(statement)
        # First Successful Proof Search: the first independently replayable
        # derivation is enough. No unnecessary uniqueness requirement.
        result = valid[0] if valid else None
        memo[statement] = result
        return result

    return prove(goal)


def replay_named_image(
    source: object, target: object, sources: tuple[ProofStep, ...]
) -> ProofStep | None:
    """Prove E(source)=target only through checked independent atom images."""
    goal = generator_image(source, target)
    return replay_cited_image(goal, sources) if goal is not None else None


def proof_tree_steps(root: ProofStep) -> tuple[ProofStep, ...]:
    """Traverse the proof premises in postorder without claiming completeness."""
    result: list[ProofStep] = []
    visited: set[int] = set()

    def visit(step: ProofStep) -> None:
        if id(step) in visited:
            return
        visited.add(id(step))
        for premise in step.premises:
            visit(premise)
        result.append(step)

    visit(root)
    return tuple(result)
