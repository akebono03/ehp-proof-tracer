from __future__ import annotations

import difflib
import re

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
    build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
    build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_contribution_renderer import (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_renderer import (
    render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
    build_toda_group_proof_narrative_semantic_closure_presentation,
    build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import (
    build_complete_toda_group_result_proof_replay,
)


TARGETS = (
    (3, 3),
    (5, 3),
    (4, 6),
    (5, 7),
    (8, 7),
    (9, 7),
)

MATH_LINE_RE = re.compile(r"\$")


def _context(n: int, k: int):
    report = build_standard_toda_report(n=n, k=k)
    group_result = report.candidates[0].source_candidate.group_result
    replay = build_complete_toda_group_result_proof_replay(group_result)
    presentation = build_toda_group_proof_presentation(replay)
    presentation = (
        build_toda_group_proof_narrative_semantic_closure_presentation(
            presentation
        )
    )
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
        semantic_sidecar=sidecar,
    )
    return presentation, sidecar, blocks, arguments


def _nonempty_lines(markdown: str) -> tuple[str, ...]:
    return tuple(
        line.strip()
        for line in markdown.splitlines()
        if line.strip()
    )


def _math_lines(markdown: str) -> tuple[str, ...]:
    return tuple(
        line
        for line in _nonempty_lines(markdown)
        if MATH_LINE_RE.search(line)
    )


def _ordered_unique(lines) -> tuple[str, ...]:
    seen = set()
    result = []
    for line in lines:
        if line in seen:
            continue
        seen.add(line)
        result.append(line)
    return tuple(result)


def _print_sample(label: str, lines: tuple[str, ...], limit: int = 5) -> None:
    print(f"  {label}: {len(lines)}")
    for line in lines[:limit]:
        print(f"    {line}")
    if len(lines) > limit:
        print(f"    ... ({len(lines) - limit} more)")


def main() -> int:
    print("=" * 78)
    print("Phase 146-5 Public-vs-Generic Parity Audit")
    print("Production changes: none")
    print("Existing test changes: none")
    print("=" * 78)

    for n, k in TARGETS:
        presentation, sidecar, blocks, arguments = _context(n, k)

        public = render_toda_group_proof_narrative_markdown(
            presentation
        )
        generic = (
            render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
                presentation,
                blocks,
                sidecar,
                arguments,
            )
        )

        public_lines = _nonempty_lines(public)
        generic_lines = _nonempty_lines(generic)
        public_math = _ordered_unique(_math_lines(public))
        generic_math = _ordered_unique(_math_lines(generic))

        public_only_math = tuple(
            line for line in public_math
            if line not in set(generic_math)
        )
        generic_only_math = tuple(
            line for line in generic_math
            if line not in set(public_math)
        )

        matcher = difflib.SequenceMatcher(
            a=public_lines,
            b=generic_lines,
            autojunk=False,
        )
        opcodes = matcher.get_opcodes()
        changed_hunks = sum(
            tag != "equal"
            for tag, _, _, _, _ in opcodes
        )

        print()
        print(f"pi_{n + k}^{n}")
        print(f"  exact parity: {public == generic}")
        print(f"  public chars: {len(public)}")
        print(f"  generic chars: {len(generic)}")
        print(f"  public nonempty lines: {len(public_lines)}")
        print(f"  generic nonempty lines: {len(generic_lines)}")
        print(f"  line similarity ratio: {matcher.ratio():.4f}")
        print(f"  changed hunks: {changed_hunks}")
        _print_sample("public-only math lines", public_only_math)
        _print_sample("generic-only math lines", generic_only_math)

    print()
    print("=" * 78)
    print("Audit complete.")
    print(
        "Use exact parity and semantic line differences to identify why "
        "historical public routes still differ from the generic renderer."
    )
    print(
        "No route changes should be made from character counts or similarity "
        "ratios alone."
    )
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
