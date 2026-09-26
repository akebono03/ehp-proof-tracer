from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_blocks import (
    TodaGroupProofNarrativeMathematicalBlockRole,
    build_toda_group_proof_narrative_blocks,
    recognize_toda_group_proof_narrative_step_role,
)
from toda_group_proof_narrative_renderer import (
    _render_group_proof_narrative_latex,
)
from toda_group_proof_narrative_semantics import (
    build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_proof_narrative_renderer import (
    render_toda_proof_statement_latex,
)


TARGETS = (
    (4, 6),
    (5, 7),
    (8, 7),
)


def _rule_name(proof_step):
    inference_rule = proof_step.inference_rule
    if inference_rule is None:
        return None
    return inference_rule.name


def _semantic_roles_for_step(sidecar, proof_step):
    step_roles = tuple(
        semantic.role.value
        for semantic in sidecar.step_semantics
        if semantic.proof_step is proof_step
    )

    premise_roles = tuple(
        semantic.role.value
        for semantic in sidecar.premise_semantics
        if semantic.edge.premise_step is proof_step
    )

    return step_roles, premise_roles


def _safe_render(renderer, value):
    try:
        rendered = renderer(value)
    except Exception as exc:
        return f"<ERROR {type(exc).__name__}: {exc}>"

    if rendered is None:
        return "<NONE>"

    return rendered


def _safe_value_summary(value):
    if value is None:
        return "None"

    if isinstance(value, (str, int, float, bool)):
        return repr(value)

    if isinstance(value, tuple):
        return (
            "tuple["
            + ", ".join(type(item).__name__ for item in value)
            + "]"
        )

    if isinstance(value, list):
        return (
            "list["
            + ", ".join(type(item).__name__ for item in value)
            + "]"
        )

    if isinstance(value, dict):
        return (
            "dict["
            + ", ".join(
                f"{type(key).__name__}:{type(item).__name__}"
                for key, item in value.items()
            )
            + "]"
        )

    return type(value).__name__


def _field_inventory(statement):
    dataclass_fields = getattr(statement, "__dataclass_fields__", None)

    if dataclass_fields is None:
        return ()

    return tuple(
        (
            field_name,
            type(getattr(statement, field_name)).__name__,
            _safe_value_summary(getattr(statement, field_name)),
        )
        for field_name in dataclass_fields
    )


def audit_target(n, k):
    report = build_standard_toda_report(n=n, k=k)

    print("=" * 100)
    print(f"n={n}, k={k}, target=pi_{n + k}^{n}")
    print(f"candidate_count={len(report.candidates)}")

    if not report.candidates:
        print("NO CANDIDATE")
        return

    group_result = report.candidates[0].source_candidate.group_result
    replay = build_toda_group_result_proof_replay(
        group_result,
        max_depth=3,
    )
    presentation = build_toda_group_proof_presentation(replay)
    sidecar = build_toda_group_proof_narrative_semantic_sidecar(presentation)
    blocks = build_toda_group_proof_narrative_blocks(
        presentation,
        semantic_sidecar=sidecar,
    )

    other_blocks = tuple(
        block
        for block in blocks
        if block.role is TodaGroupProofNarrativeMathematicalBlockRole.OTHER
    )

    print(f"blocks={len(blocks)}")
    print(f"other_blocks={len(other_blocks)}")

    for block_index, block in enumerate(other_blocks):
        print("-" * 100)
        print(f"OTHER BLOCK {block_index}")
        print(f"steps={len(block.steps)}")

        for step_index, proof_step in enumerate(block.steps):
            statement = proof_step.conclusion
            step_roles, premise_roles = _semantic_roles_for_step(
                sidecar,
                proof_step,
            )
            recognized_role = recognize_toda_group_proof_narrative_step_role(
                presentation,
                proof_step,
                semantic_sidecar=sidecar,
            )

            print(f"  step={step_index}")
            print(f"    statement_type={type(statement).__name__}")
            print(f"    rule_name={_rule_name(proof_step)!r}")
            print(f"    recognized_role={recognized_role.value}")
            print(f"    semantic_step_roles={step_roles}")
            print(f"    semantic_premise_roles={premise_roles}")
            print(
                "    generic_statement_renderer="
                + _safe_render(
                    render_toda_proof_statement_latex,
                    statement,
                )
            )
            print(
                "    legacy_group_renderer="
                + _safe_render(
                    _render_group_proof_narrative_latex,
                    proof_step,
                )
            )

            inventory = _field_inventory(statement)

            if inventory:
                print("    fields:")
                for field_name, field_type, summary in inventory:
                    print(
                        f"      {field_name}: "
                        f"type={field_type}, "
                        f"value={summary}"
                    )
            else:
                print("    fields=<NONE>")

    print()


def main():
    for n, k in TARGETS:
        audit_target(n, k)


if __name__ == "__main__":
    main()
