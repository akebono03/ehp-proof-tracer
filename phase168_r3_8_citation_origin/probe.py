"""Report why public narrative model citations are not the expected two sources."""
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_8_citation_origin import inspect_citation_origins


def main():
    for n, k in ((2, 1), (3, 1)):
        bridge = build_shared_typed_bridge()
        result = search_group_from_registered_goal(n=n, k=k, bridge=bridge)
        model = build_linked_proof_narrative_model(result, bridge)
        report = inspect_citation_origins(model)
        print(f"GROUP pi_{n+k}^{n}: status={result.status} proven_steps={len(result.proven_steps)}")
        print("EXPECTED:", report.expected_locators)
        print("DISTINCT:", report.distinct_locators)
        print("REPEATED_LOCATORS:", report.repeated_locators)
        print("UNEXPECTED:", report.unexpected_locators)
        print("MISSING:", report.missing_locators)
        for origin in report.origins:
            print(
                f"  R{origin.number} locator={origin.locator!r} "
                f"steps={origin.step_indices} assertion_ids={origin.assertion_ids} "
                f"kind={origin.source_kind} duplicate_of={origin.duplicate_locator_of} "
                f"rules={origin.rule_names}"
            )
            for i in origin.step_indices:
                step = model.steps[i]
                print(f"    STEP {i}: {step.rule.value}: {type(step.conclusion).__name__}")
        print("MATCHES_EXPECTED_LOCATORS:", report.matches_expected_sources)
    print("AUDIT_ONLY: Search, model, Renderer, and Web production files unchanged")


if __name__ == "__main__":
    main()
