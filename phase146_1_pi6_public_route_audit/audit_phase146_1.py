from __future__ import annotations

import inspect

import toda_group_proof_narrative_renderer as renderer


def main() -> int:
    source = inspect.getsource(
        renderer.render_toda_group_proof_narrative_markdown
    )
    helper_source = inspect.getsource(
        renderer._is_phase134_3_pi6_3_presentation
    )

    required_route_fragments = (
        "_is_phase134_3_pi6_3_presentation",
        "build_toda_group_proof_narrative_semantic_sidecar",
        "build_toda_group_proof_narrative_blocks",
        "build_toda_group_proof_narrative_arguments",
        "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown",
    )

    missing = tuple(
        fragment
        for fragment in required_route_fragments
        if fragment not in source
    )

    target_specific_fragments = (
        "target.group_dimension == 6",
        "target.sphere_dimension == 3",
        '"Toda Proposition 5.6"',
    )

    missing_target_specific = tuple(
        fragment
        for fragment in target_specific_fragments
        if fragment not in helper_source
    )

    print("=" * 78)
    print("Phase 146-1: pi_6^3 public Narrative route audit")
    print("=" * 78)
    print()
    print("A. Public Narrative route")
    print("-" * 78)

    if missing:
        print("Expected route fragments missing:")
        for fragment in missing:
            print(f"  - {fragment}")
        return 1

    print("PASS: pi_6^3 enters the semantic/block/argument multi-renderer path.")
    print()
    print("B. Remaining pi_6^3-specific route gate")
    print("-" * 78)

    if missing_target_specific:
        print("Expected target-specific gate fragments missing:")
        for fragment in missing_target_specific:
            print(f"  - {fragment}")
        return 1

    print("CONFIRMED:")
    print("  _is_phase134_3_pi6_3_presentation() still selects the route by")
    print("  target.group_dimension == 6, target.sphere_dimension == 3, and")
    print('  source theorem == "Toda Proposition 5.6".')
    print()
    print("C. Phase 146 concrete issue")
    print("-" * 78)
    print(
        "Replace only this public-route target identity gate with a general "
        "capability-based decision, while preserving the current pi_6^3 "
        "Narrative output and existing APIs."
    )
    print()
    print("Production changes in Phase 146-1: none")
    print("Existing test changes in Phase 146-1: none")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
