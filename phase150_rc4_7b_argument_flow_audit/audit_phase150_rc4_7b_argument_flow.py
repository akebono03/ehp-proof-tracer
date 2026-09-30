from toda_calculation_facade import build_standard_toda_report
from toda_group_result_proof_replay import build_complete_toda_group_result_proof_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_sidecar
from toda_group_proof_narrative_blocks import build_toda_group_proof_narrative_blocks
from toda_group_proof_narrative_arguments import (
    build_toda_group_proof_narrative_arguments,
    extract_toda_group_proof_narrative_argument_conclusion_step,
    extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_group_proof_narrative_argument_local_body import (
    extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from toda_group_proof_narrative_references import (
    build_toda_group_proof_narrative_reference_entries,
)

TARGETS = (
    (4, 6, "pi_10^4"),
    (5, 7, "pi_12^5"),
    (8, 7, "pi_15^8"),
    (9, 7, "pi_16^9"),
)


def rule_name(step):
    rule = step.inference_rule
    if rule is None:
        return "<none>"
    return rule.name


def reference_title(step):
    rule = step.inference_rule
    if rule is None or rule.literature_reference is None:
        return "-"
    ref = rule.literature_reference
    return ref.locator or ref.label


def conclusion_text(step):
    return str(step.conclusion).replace("\n", " ")


def block_step_ids(block, step_index_by_id):
    return tuple(step_index_by_id[id(step)] for step in block.steps)


def main():
    print("=" * 78)
    print("Phase 150 RC4-7B Argument-Flow Audit")
    print("Production changes: none")
    print("Existing test changes: none")
    print("=" * 78)

    any_unowned = False
    any_flow_gap = False

    for n, k, label in TARGETS:
        report = build_standard_toda_report(n=n, k=k)
        group_result = report.candidates[0].source_candidate.group_result
        replay = build_complete_toda_group_result_proof_replay(group_result)
        presentation = build_toda_group_proof_presentation(replay)
        semantic = build_toda_group_proof_narrative_semantic_sidecar(presentation)
        blocks = build_toda_group_proof_narrative_blocks(
            presentation,
            semantic_sidecar=semantic,
        )
        arguments = build_toda_group_proof_narrative_arguments(
            presentation,
            blocks,
            semantic_sidecar=semantic,
        )
        references = build_toda_group_proof_narrative_reference_entries(presentation)
        rendered = render_toda_group_proof_narrative_markdown(presentation)

        step_index_by_id = {
            id(node.proof_step): index
            for index, node in enumerate(presentation.nodes)
        }
        block_index_by_id = {id(block): index for index, block in enumerate(blocks)}

        owner_indices_by_block_id = {}
        local_indices_by_argument = {}
        for argument_index, argument in enumerate(arguments):
            local_blocks = extract_toda_group_proof_narrative_argument_local_body_blocks(
                presentation,
                blocks,
                semantic,
                arguments,
                argument_index,
            )
            local_indices_by_argument[argument_index] = tuple(
                block_index_by_id[id(block)] for block in local_blocks
            )
            for block in local_blocks:
                owner_indices_by_block_id.setdefault(id(block), []).append(argument_index)

        print()
        print("-" * 78)
        print(f"TARGET {label}")
        print(f"presentation_nodes={len(presentation.nodes)} blocks={len(blocks)} "
              f"arguments={len(arguments)} references={len(references)}")
        print()

        print("ARGUMENTS")
        for argument_index, argument in enumerate(arguments):
            conclusion_index = block_index_by_id[id(argument.conclusion_block)]
            conclusion_step = extract_toda_group_proof_narrative_argument_conclusion_step(argument)
            purpose = extract_toda_group_proof_narrative_argument_purpose_subject(argument)
            print(
                f"  A{argument_index:02d} role={argument.role.name} "
                f"purpose={purpose!s} conclusion_block=B{conclusion_index:02d} "
                f"child_arguments={argument.child_argument_indices}"
            )
            print(
                "      direct_support_blocks="
                + repr(tuple(block_index_by_id[id(block)] for block in argument.supporting_blocks))
            )
            print("      local_body_blocks=" + repr(local_indices_by_argument[argument_index]))
            print(
                "      conclusion_step="
                + (
                    f"S{step_index_by_id[id(conclusion_step)]:02d} {conclusion_text(conclusion_step)}"
                    if conclusion_step is not None
                    else "<ambiguous-or-missing>"
                )
            )

        print()
        print("BLOCK / OWNERSHIP FLOW")
        unowned_visible = []
        for block_index, block in enumerate(blocks):
            owners = tuple(owner_indices_by_block_id.get(id(block), ()))
            if not owners:
                unowned_visible.append(block_index)
            print(
                f"  B{block_index:02d} role={block.role.name:<15} "
                f"steps={block_step_ids(block, step_index_by_id)!r} owners={owners!r}"
            )
            for step in block.steps:
                step_index = step_index_by_id[id(step)]
                print(
                    f"      S{step_index:02d} ref={reference_title(step)!r} "
                    f"rule={rule_name(step)!r}"
                )
                print(f"          conclusion={conclusion_text(step)}")

        if unowned_visible:
            any_unowned = True
        print()
        print("UNOWNED_VISIBLE_BLOCKS=", tuple(unowned_visible))

        root_block_index = next(
            index
            for index, block in enumerate(blocks)
            if any(step is presentation.root_step for step in block.steps)
        )
        root_argument_indices = tuple(
            index
            for index, argument in enumerate(arguments)
            if argument.conclusion_block is blocks[root_block_index]
        )
        print("ROOT_BLOCK=", root_block_index)
        print("ROOT_ARGUMENTS=", root_argument_indices)

        if root_argument_indices:
            root_local = set(local_indices_by_argument[root_argument_indices[0]])
            non_root_argument_blocks = {
                block_index_by_id[id(argument.conclusion_block)]
                for index, argument in enumerate(arguments)
                if index != root_argument_indices[0]
            }
            detached_argument_boundaries = tuple(
                sorted(non_root_argument_blocks - root_local)
            )
        else:
            detached_argument_boundaries = ()
        print("DETACHED_ARGUMENT_BOUNDARIES_FROM_ROOT_LOCAL_BODY=", detached_argument_boundaries)

        suspicious_raw = tuple(
            token
            for token in (
                "Toda Proposition",
                "Toda Lemma",
                "Toda (",
                " is exact",
                " is injective",
                " is surjective",
            )
            if token in rendered
        )
        print("RAW_OR_SOURCE_STYLE_BODY_TOKENS=", suspicious_raw)

        if unowned_visible or detached_argument_boundaries or suspicious_raw:
            any_flow_gap = True

        print()
        print("RENDERED_BEGIN")
        print(rendered)
        print("RENDERED_END")

    print()
    print("=" * 78)
    print("ANY_UNOWNED_VISIBLE_BLOCKS=", any_unowned)
    print("ARGUMENT_FLOW_GAP_DETECTED=", any_flow_gap)
    print("AUDIT_DECISION=CLASSIFY_GAPS_BEFORE_RC4_7B_PRODUCTION_CHANGE")
    print("=" * 78)


if __name__ == "__main__":
    main()
