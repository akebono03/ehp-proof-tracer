from pathlib import Path


def test_reference_precedes_internal_reuse():
    source = (Path(__file__).resolve().parent.parent / "phase165_r3_recursive_search.py").read_text(encoding="utf-8")
    start = source.index("    def resolve(target: object)")
    end = source.index("    return resolve(goal)", start)
    body = source[start:end]
    reference_lookup = body.index('if lookup_mode == "typed_reference_ordered":')
    reference_stop = body.index('if lookup_mode in ("typed_reference", "typed_reference_ordered") and len(options) == 1:')
    internal_reuse = body.index("if completed_internal_proofs:")
    assert reference_lookup < reference_stop < internal_reuse


def test_citation_scope_remains_external():
    source = (Path(__file__).resolve().parent.parent / "phase165_r3_recursive_search.py").read_text(encoding="utf-8")
    assert "_typed_reference_steps(bridge, target)" in source
    assert "ordered_typed_reference_steps(" in source
    assert "find_eligible_goal_candidates(" in source
