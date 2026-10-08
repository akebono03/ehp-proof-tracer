"""Read-only audit: explain why E^2 eta_3 = eta_5 is still rendered."""

from phase162_validated_proof_presentation import (
    _fixed_statement_reuse_visible_ids,
    _render_validated_backward_step,
    _render_validated_reference_section,
    _validated_main_proof_steps,
    _validated_proof_body_step_lines,
    build_validated_backward_proof_presentation,
)
from tests.test_phase162_r2_validated_proof_presentation import _validated_fixture


def main():
    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    _, reference_ids = _render_validated_reference_section(presentation)
    visible = _fixed_statement_reuse_visible_ids(presentation, reference_ids)
    core = _validated_main_proof_steps(presentation)
    records = _validated_proof_body_step_lines(presentation, reference_ids)
    children = {}
    for step in presentation.nodes:
        for premise in step.premises:
            children.setdefault(id(premise), []).append(step)

    matches = [
        (step, prose) for step, prose in records
        if r"E^{2}" in _render_validated_backward_step(step)
        and r"\eta_{3}" in _render_validated_backward_step(step)
        and r"\eta_{5}" in _render_validated_backward_step(step)
    ]
    print("TARGET: E^2 eta_3 = eta_5")
    print("matches:", len(matches))
    print("total nodes:", len(presentation.nodes))
    for index, (step, prose) in enumerate(matches, 1):
        print("\nMATCH", index)
        print("conclusion:", _render_validated_backward_step(step))
        print("rule:", step.rule, "inference rule:", getattr(step.inference_rule, "name", None))
        print("visible:", id(step) in visible, "core:", id(step) in core, "fixed:", id(step) in reference_ids)
        print("direct premises:", len(step.premises))
        for premise in step.premises:
            print("  FROM:", _render_validated_backward_step(premise))
        direct = children.get(id(step), [])
        print("direct consumers:", len(direct))
        for consumer in direct:
            print("  TO:", _render_validated_backward_step(consumer), "visible:", id(consumer) in visible, "fixed:", id(consumer) in reference_ids)
        paths = []
        def trace(current, chain, seen):
            if id(current) in seen:
                return
            if current is presentation.root_step:
                paths.append(chain)
                return
            for consumer in children.get(id(current), []):
                trace(consumer, chain + [consumer], seen | {id(current)})
        trace(step, [step], set())
        print("paths to final goal:", len(paths))
        for path in paths[:8]:
            print("  PATH:", " => ".join(type(part.conclusion).__name__ for part in path))
            print("  crosses fixed boundary:", any(id(item) in reference_ids for item in path[1:]))
    if not matches:
        print("E2 equality is not in emitted proof-body records.")
    print("\nDECISION DATA ONLY: this script does not suppress a proof step.")


if __name__ == "__main__":
    main()
