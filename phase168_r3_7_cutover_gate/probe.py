"""Run against the current shared Search and unchanged Web presentation."""
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
from phase168_r3_7_cutover_gate import inspect_narrative_cutover


def main():
    for n, k in ((2, 2), (2, 1), (3, 1), (4, 1)):
        bridge = build_shared_typed_bridge()
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        model = build_linked_proof_narrative_model(result, bridge)
        view = build_partial_web_group_proof_view(result)
        report = inspect_narrative_cutover(model, view.rendered_lines)
        print(f"PI_{n+k}^{n} model={report.model_references!r} shown={report.displayed_references!r} safe={report.safe_to_reuse_legacy_body} issues={report.issues!r}")
    print("AUDIT_ONLY: no existing Search, Renderer, or Web files modified")


if __name__ == "__main__":
    main()
