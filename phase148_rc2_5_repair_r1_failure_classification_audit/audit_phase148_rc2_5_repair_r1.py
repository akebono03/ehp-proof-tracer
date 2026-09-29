from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_closure_presentation
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown

CASES = (
    ("pi16_9_depth0", 9, 7, 0),
    ("pi6_3_depth2", 3, 3, 2),
    ("pi8_5_depth3", 5, 3, 3),
    ("pi16_9_depth3", 9, 7, 3),
)

def build_case(n, k, depth):
    report = build_standard_toda_report(n=n, k=k)
    result = report.candidates[0].source_candidate.group_result
    replay = build_toda_group_result_proof_replay(result, max_depth=depth)
    presentation = build_toda_group_proof_presentation(replay)
    closure = build_toda_group_proof_narrative_semantic_closure_presentation(presentation)
    original_ids = {id(node.proof_step) for node in presentation.nodes}
    added = tuple(node for node in closure.nodes if id(node.proof_step) not in original_ids)
    rendered = render_toda_group_proof_narrative_markdown(presentation)
    return presentation, closure, added, rendered

def main():
    print("=" * 96)
    print("Phase 148 RC2-5 Repair R1 failure classification audit")
    print("Production changes: none")
    print("=" * 96)
    for label, n, k, depth in CASES:
        presentation, closure, added, rendered = build_case(n, k, depth)
        print("\n" + "-" * 96)
        print(label)
        print("-" * 96)
        print(f"input_nodes={len(presentation.nodes)} closure_nodes={len(closure.nodes)} added={len(added)}")
        print(f"input_depth={presentation.max_depth} closure_depth={closure.max_depth}")
        for node in added:
            print(f"  added depth={node.depth} role={node.role.value} statement={node.proof_step.conclusion!r}")
        if label == "pi16_9_depth0":
            print(f"depth0_added_premises={bool(added)}")
            print("depth0_contains_pi12_5=" + str(r"\pi_{12}^{5}" in rendered))
        if label == "pi6_3_depth2":
            print("tag1=" + str(r"\tag{1}" in rendered))
            print("tag2=" + str(r"\tag{2}" in rendered))
            print("tag3=" + str(r"\tag{3}" in rendered))
            print("group_result=" + str(r"\pi_{6}^{3} = \mathbb{Z}/4" in rendered))
        if label in ("pi8_5_depth3", "pi16_9_depth3"):
            print("raw_text_is_exact=" + str(r"\text{ is exact}" in rendered))
    print("\n" + "=" * 96)
    print("CLASSIFICATION")
    print("A depth=0 additions -> production-scope regression candidate.")
    print("B Phase143 raw exactness expectations -> superseded only when RC2 intentionally suppresses them.")
    print("C Phase144-6 one-node closure expectation -> superseded when additions are R4.2 equality premises.")
    print("D public/direct parity -> stale construction if only public path applies semantic closure.")
    print("=" * 96)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
