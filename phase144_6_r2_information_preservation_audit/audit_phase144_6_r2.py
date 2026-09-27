from __future__ import annotations

import re

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
    build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
    build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
    render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_renderer import (
    _render_phase134_3_pi6_3_narrative_markdown,
    render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
    build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay


def build_data(depth: int):
    report = build_standard_toda_report(n=3, k=3)
    group_result = report.candidates[0].source_candidate.group_result
    replay = build_toda_group_result_proof_replay(
        group_result,
        max_depth=depth,
    )
    presentation = build_toda_group_proof_presentation(replay)
    sidecar = build_toda_group_proof_narrative_semantic_sidecar(
        presentation
    )
    blocks = build_toda_group_proof_narrative_blocks(
        presentation,
        semantic_sidecar=sidecar,
    )
    arguments = build_toda_group_proof_narrative_arguments(
        presentation,
        blocks,
        sidecar,
    )
    generic = render_toda_group_proof_narrative_multi_argument_markdown(
        presentation,
        blocks,
        sidecar,
        arguments,
    )
    public = render_toda_group_proof_narrative_markdown(presentation)
    return presentation, sidecar, blocks, arguments, generic, public


def statement_text(step) -> str:
    return repr(step.conclusion).replace("\n", " ")


def summarize(depth: int) -> None:
    presentation, sidecar, blocks, arguments, generic, public = build_data(depth)
    print("=" * 78)
    print(f"DEPTH {depth}")
    print("=" * 78)
    print(f"nodes={len(presentation.nodes)}")
    print(f"edges={len(presentation.edges)}")
    print(f"premise_semantics={len(sidecar.premise_semantics)}")
    print(f"step_semantics={len(sidecar.step_semantics)}")
    print(f"dependency_semantics={len(sidecar.dependency_semantics)}")
    print(f"blocks={len(blocks)}")
    print(f"arguments={len(arguments)}")
    print(f"generic_chars={len(generic)}")
    print(f"public_chars={len(public)}")
    print(f"generic_equals_public={generic == public}")
    print()

    print("Semantic sidecar")
    print("-" * 78)
    for semantic in sidecar.premise_semantics:
        print(
            "premise:",
            semantic.role.value,
            "|",
            statement_text(semantic.edge.premise_step)[:220],
        )
    for semantic in sidecar.step_semantics:
        print(
            "step:",
            semantic.role.value,
            "|",
            statement_text(semantic.proof_step)[:220],
        )
    for semantic in sidecar.dependency_semantics:
        print(
            "dependency:",
            semantic.role.value,
            "| prerequisite=",
            statement_text(semantic.prerequisite_step)[:120],
            "| dependent=",
            statement_text(semantic.dependent_step)[:120],
        )
    print()

    print("Block inventory")
    print("-" * 78)
    for index, block in enumerate(blocks):
        print(
            f"B{index:02d}",
            block.role.value,
            f"steps={len(block.steps)}",
        )
        for step in block.steps:
            text = statement_text(step)
            if (
                "eta_2" in text
                or "eta_3" in text
                or "eta_4" in text
                or "TodaProp5" in text
            ):
                print("   ", text[:260])
    print()

    print("Argument inventory")
    print("-" * 78)
    for index, argument in enumerate(arguments):
        print(
            f"A{index:02d}",
            argument.role.value,
            "| conclusion_role=",
            argument.conclusion_block.role.value,
            "| conclusion_steps=",
            len(argument.conclusion_block.steps),
        )
    print()

    print("Rendered-information probes")
    print("-" * 78)
    probes = {
        "definition_sentence": r"$\nu'$ を定める.",
        "eta2_eta3_eta4": r"\eta_{2}\eta_{3}\eta_{4}",
        "eta3_eta4": r"\eta_{3}\eta_{4}",
        "reference_R1": "[R1]",
        "reference_R2": "[R2]",
        "reference_R3": "[R3]",
        "reference_R4": "[R4]",
        "reference_R5": "[R5]",
        "equation_ref_1_2": "(1) と (2) より、",
        "equation_ref_4_5": "(4) と (5) より、",
    }
    for name, needle in probes.items():
        print(
            f"{name}: generic={needle in generic}, public={needle in public}"
        )
    print(
        "generic_tags=",
        re.findall(r"\\tag\{(\d+)\}", generic),
    )
    print(
        "public_tags=",
        re.findall(r"\\tag\{(\d+)\}", public),
    )
    print()


def legacy_depth2() -> None:
    presentation, _, _, _, _, _ = build_data(2)
    legacy = _render_phase134_3_pi6_3_narrative_markdown(presentation)
    print("=" * 78)
    print("LEGACY DEPTH 2")
    print("=" * 78)
    for label in ("R1", "R2", "R3", "R4", "R5"):
        print(f"[{label}]={f'[{label}]' in legacy}")
    print("tags=", re.findall(r"\\tag\{(\d+)\}", legacy))
    print(
        "eta2_eta3_eta4=",
        r"\eta_{2}\eta_{3}\eta_{4}" in legacy,
    )
    print(
        "eta3_eta4=",
        r"\eta_{3}\eta_{4}" in legacy,
    )
    print()


def main() -> int:
    print("=" * 78)
    print("Phase 144-6-R2: pi_6^3 legacy/generic information-preservation audit")
    print("=" * 78)
    print("AUDIT ONLY: no production files are modified.")
    print()
    legacy_depth2()
    summarize(2)
    summarize(3)
    print("=" * 78)
    print("Interpretation checklist")
    print("=" * 78)
    print("1. Are R1-R5 present in legacy but absent from generic/public?")
    print("2. Are equation tags/refs lost at depth 2 but recovered at depth 3?")
    print("3. Which Semantic/Block/Argument roles own eta-composite supporting facts?")
    print("4. Does the Semantic sidecar preserve theorem-reference identity/numbering?")
    print("5. Does public output equal the generic multi-argument renderer?")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
