from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_semantics import (
    build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
    build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
    build_toda_group_result_proof_replay,
)


TARGETS = (
    (5, 3, "nu_5"),
    (5, 7, "sigma triple-prime"),
    (9, 7, "sigma_9"),
)

TARGET_TYPE_NAMES = {
    "TodaNuFamilyDefinitionStatement",
    "TodaSigmaFamilyDefinitionStatement",
    "TodaLemma513Statement",
}


def _rule_name(proof_step):
    inference_rule = proof_step.inference_rule
    if inference_rule is None:
        return None
    return inference_rule.name


def _safe_value(value):
    if value is None:
        return "None"
    if isinstance(value, (str, int, float, bool)):
        return repr(value)

    name = getattr(value, "name", None)
    if isinstance(name, str):
        return f"{type(value).__name__}(name={name!r})"

    return type(value).__name__


def _field_inventory(statement):
    fields = getattr(
        statement,
        "__dataclass_fields__",
        None,
    )
    if fields is None:
        return ()

    return tuple(
        (
            field_name,
            type(
                getattr(
                    statement,
                    field_name,
                )
            ).__name__,
            _safe_value(
                getattr(
                    statement,
                    field_name,
                )
            ),
        )
        for field_name in fields
    )


def audit_target(n, k, label):
    report = build_standard_toda_report(
        n=n,
        k=k,
    )
    group_result = (
        report.candidates[
            0
        ].source_candidate.group_result
    )
    replay = build_toda_group_result_proof_replay(
        group_result,
        max_depth=3,
    )
    presentation = build_toda_group_proof_presentation(
        replay
    )
    sidecar = (
        build_toda_group_proof_narrative_semantic_sidecar(
            presentation
        )
    )

    print("=" * 100)
    print(
        f"n={n}, k={k}, "
        f"target=pi_{n + k}^{n}, "
        f"label={label}"
    )

    matches = tuple(
        (
            index,
            node.proof_step,
        )
        for index, node in enumerate(
            presentation.nodes
        )
        if (
            type(
                node.proof_step.conclusion
            ).__name__
            in TARGET_TYPE_NAMES
        )
    )

    print(f"matching_steps={len(matches)}")

    for node_index, proof_step in matches:
        statement = proof_step.conclusion
        semantic_roles = tuple(
            semantic.role.value
            for semantic in sidecar.step_semantics
            if semantic.proof_step is proof_step
        )

        print("-" * 100)
        print(f"node={node_index}")
        print(
            "statement_type="
            f"{type(statement).__name__}"
        )
        print(
            f"own_rule={_rule_name(proof_step)!r}"
        )
        print(
            f"semantic_roles={semantic_roles}"
        )
        print(
            "has_element="
            f"{hasattr(statement, 'element')}"
        )

        if hasattr(statement, "element"):
            element = statement.element
            print(
                "element_type="
                f"{type(element).__name__}"
            )
            print(
                "element_name="
                f"{getattr(element, 'name', None)!r}"
            )

        print("fields:")
        inventory = _field_inventory(
            statement
        )
        if not inventory:
            print("  <NONE>")
        for field_name, field_type, value in inventory:
            print(
                f"  {field_name}: "
                f"type={field_type}, "
                f"value={value}"
            )

    print()


def main():
    for n, k, label in TARGETS:
        audit_target(
            n,
            k,
            label,
        )


if __name__ == "__main__":
    main()
