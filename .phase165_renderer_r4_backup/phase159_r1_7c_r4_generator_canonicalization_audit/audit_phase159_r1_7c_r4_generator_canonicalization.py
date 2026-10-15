from pathlib import Path
import sys


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


ROOT = _repo_root()
TESTS = ROOT / "tests"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if str(TESTS) not in sys.path:
    sys.path.insert(0, str(TESTS))


from expression import Composition
from test_phase59_prop53_integration import build_phase59_8_data
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_generic_narrative_renderer import (
    _render_generic_narrative_expression_latex,
)
from toda_group_proof_narrative_renderer import (
    render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
    build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
    build_toda_group_result_proof_replay,
)
from toda_human_readable_renderer import (
    render_toda_expression_latex,
)
from toda_proof_narrative_renderer import (
    render_toda_raw_group_structure_latex,
)


def _section(title: str) -> None:
    print("")
    print("=" * 78)
    print(title)
    print("=" * 78)


def _print_matching_lines(
    label: str,
    text: str,
    needles: tuple[str, ...],
) -> None:
    print(label)
    matched = False

    for line_number, line in enumerate(
        text.splitlines(),
        start=1,
    ):
        if any(
            needle in line
            for needle in needles
        ):
            matched = True
            print(
                f"{line_number:04d}: {line}"
            )

    if not matched:
        print("  <no matching lines>")


def main() -> int:
    _section(
        "Phase 159 R1-7c R4 generator canonicalization audit"
    )

    data = build_phase59_8_data()
    higher_step = data[
        "higher_step"
    ]
    higher_relation = higher_step.conclusion
    finite_group = higher_relation.rhs
    generator = finite_group.generator

    _section(
        "A. Proposition 5.3 semantic data"
    )
    print(
        "group_dimension =",
        higher_relation.lhs.group_dimension,
    )
    print(
        "sphere_dimension =",
        higher_relation.lhs.sphere_dimension,
    )
    print(
        "finite_group_type =",
        type(finite_group).__name__,
    )
    print(
        "order =",
        finite_group.order,
    )
    print(
        "generator_type =",
        type(generator).__name__,
    )
    print(
        "generator_repr =",
        repr(generator),
    )

    if isinstance(
        generator,
        Composition,
    ):
        print(
            "left_type =",
            type(generator.left).__name__,
        )
        print(
            "left_repr =",
            repr(generator.left),
        )
        print(
            "right_type =",
            type(generator.right).__name__,
        )
        print(
            "right_repr =",
            repr(generator.right),
        )

    _section(
        "B. Expression rendering comparison"
    )
    raw_expression = (
        render_toda_expression_latex(
            generator
        )
    )
    generic_expression = (
        _render_generic_narrative_expression_latex(
            generator
        )
    )

    print(
        "render_toda_expression_latex =",
        raw_expression,
    )
    print(
        "_render_generic_narrative_expression_latex =",
        generic_expression,
    )

    _section(
        "C. Group-structure rendering comparison"
    )
    raw_group = (
        render_toda_raw_group_structure_latex(
            finite_group
        )
    )
    print(
        "render_toda_raw_group_structure_latex =",
        raw_group,
    )

    _section(
        "D. Public pi_6^3 Narrative"
    )
    report = build_standard_toda_report(
        n=3,
        k=3,
    )
    group_result = (
        report
        .candidates[0]
        .source_candidate
        .group_result
    )
    replay = (
        build_toda_group_result_proof_replay(
            group_result,
            max_depth=2,
        )
    )
    presentation = (
        build_toda_group_proof_presentation(
            replay
        )
    )
    rendered = (
        render_toda_group_proof_narrative_markdown(
            presentation
        )
    )

    _print_matching_lines(
        "eta-related public lines:",
        rendered,
        (
            r"\eta_{5}\eta_{6}",
            r"\eta_{5}^{2}",
            r"\pi_{7}^{5}",
            "Proposition 5.3",
        ),
    )

    _section(
        "E. Classification"
    )

    raw_is_composite = (
        r"\eta_{5}\eta_{6}"
        in raw_expression
    )
    generic_is_canonical = (
        generic_expression
        == r"\eta_{5}^{2}"
    )
    raw_group_is_composite = (
        r"\eta_{5}\eta_{6}"
        in raw_group
    )
    public_has_composite_group = (
        (
            r"\pi_{7}^{5}"
            in rendered
        )
        and (
            r"\eta_{5}\eta_{6}"
            in rendered
        )
    )
    public_has_canonical = (
        r"\eta_{5}^{2}"
        in rendered
    )

    print(
        "raw_expression_is_eta5_eta6 =",
        raw_is_composite,
    )
    print(
        "generic_expression_is_eta5_squared =",
        generic_is_canonical,
    )
    print(
        "raw_group_structure_is_composite =",
        raw_group_is_composite,
    )
    print(
        "public_has_eta5_eta6 =",
        public_has_composite_group,
    )
    print(
        "public_has_eta5_squared =",
        public_has_canonical,
    )

    print("")
    if (
        raw_is_composite
        and generic_is_canonical
        and raw_group_is_composite
    ):
        print(
            "AUDIT RESULT: renderer-route mismatch."
        )
        print(
            "The semantic generator is intentionally stored as "
            "Composition(eta_5, eta_6), while the generic Narrative "
            "renderer already canonicalizes it to eta_5^2."
        )
        print(
            "Therefore the next repair should normalize the "
            "group-structure/public rendering route, not rewrite "
            "the semantic Proposition 5.3 data and not globally "
            "replace eta_5 eta_6 in calculations."
        )
        return 0

    print(
        "AUDIT RESULT: observed state differs from the expected "
        "renderer-route mismatch. Inspect the printed layers before "
        "choosing a repair."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
