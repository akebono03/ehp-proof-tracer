from __future__ import annotations

from dataclasses import fields, is_dataclass

from proof import LiteratureReference, Relation
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_blocks import (
    TodaGroupProofNarrativeMathematicalBlockRole,
    build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
    build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay


def build_presentation(depth: int = 3):
    report = build_standard_toda_report(n=3, k=3)
    group_result = report.candidates[0].source_candidate.group_result
    replay = build_toda_group_result_proof_replay(
        group_result,
        max_depth=depth,
    )
    return build_toda_group_proof_presentation(replay)


def literature_values(value, path="conclusion", seen=None):
    if seen is None:
        seen = set()
    if id(value) in seen:
        return
    seen.add(id(value))

    if isinstance(value, LiteratureReference):
        yield path, value
        return

    if isinstance(value, Relation):
        if isinstance(value.source, LiteratureReference):
            yield path + ".source", value.source
        elif isinstance(value.source, str):
            yield path + ".source", value.source

    if is_dataclass(value):
        for field in fields(value):
            child = getattr(value, field.name)
            yield from literature_values(
                child,
                path + "." + field.name,
                seen,
            )
        return

    if isinstance(value, (tuple, list)):
        for index, child in enumerate(value):
            yield from literature_values(
                child,
                f"{path}[{index}]",
                seen,
            )


def rule_text(step):
    rule = step.inference_rule
    if rule is None:
        return "<none>", "<none>"
    return rule.name, repr(rule.description)


def main() -> int:
    presentation = build_presentation()
    sidecar = build_toda_group_proof_narrative_semantic_sidecar(
        presentation
    )
    blocks = build_toda_group_proof_narrative_blocks(
        presentation,
        semantic_sidecar=sidecar,
    )

    print("=" * 78)
    print("Phase 144-6-R3: provenance/source recovery audit")
    print("=" * 78)
    print("AUDIT ONLY: no production source changes")
    print(f"nodes={len(presentation.nodes)}")
    print(f"edges={len(presentation.edges)}")
    print()

    print("REFERENCE steps")
    print("-" * 78)
    reference_index = 0
    for block_index, block in enumerate(blocks):
        if block.role is not TodaGroupProofNarrativeMathematicalBlockRole.REFERENCE:
            continue
        for step_index, step in enumerate(block.steps):
            reference_index += 1
            name, description = rule_text(step)
            values = tuple(literature_values(step.conclusion))
            print(f"candidate={reference_index} block=B{block_index:02d} step={step_index}")
            print(f"statement_type={type(step.conclusion).__name__}")
            print(f"rule_name={name}")
            print(f"rule_description={description}")
            print(f"step_note={repr(step.note)}")
            print(f"literature_values={values}")
            print()

    print("All presentation steps carrying explicit source/literature metadata")
    print("-" * 78)
    count = 0
    for node_index, node in enumerate(presentation.nodes):
        step = node.proof_step
        values = tuple(literature_values(step.conclusion))
        if not values:
            continue
        count += 1
        name, description = rule_text(step)
        print(f"N{node_index:02d} depth={node.depth if hasattr(node, 'depth') else node.shortest_depth}")
        print(f"statement_type={type(step.conclusion).__name__}")
        print(f"rule_name={name}")
        print(f"rule_description={description}")
        print(f"step_note={repr(step.note)}")
        print(f"literature_values={values}")
        print()
    print(f"explicit_source_step_count={count}")
    print()

    print("Rule-name theorem/lemma locator inventory")
    print("-" * 78)
    for node_index, node in enumerate(presentation.nodes):
        step = node.proof_step
        name, description = rule_text(step)
        lowered = name.lower()
        if (
            "toda" in lowered
            or "proposition" in lowered
            or "lemma" in lowered
        ):
            print(
                f"N{node_index:02d} "
                f"{type(step.conclusion).__name__}: {name}"
            )
    print()

    print("=" * 78)
    print("Decision questions")
    print("=" * 78)
    print("1. Do REFERENCE steps carry LiteratureReference/source metadata?")
    print("2. Do rule descriptions contain stable human theorem titles?")
    print("3. Is Proposition 2.2 represented by any presentation ProofStep?")
    print("4. Which legacy references exist only in renderer-authored prose?")
    print("5. Can R3 safely build ReferenceEntry without parsing rule names?")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
