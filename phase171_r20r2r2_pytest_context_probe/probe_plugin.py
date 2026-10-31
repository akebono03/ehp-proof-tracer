"""Inspect ordered-citation test fixtures inside the actual pytest process.

No production function is patched. This hook only reads isolated fixtures and
records citation decisions at the same collection/execution boundary as tests.
"""
from __future__ import annotations

import json
import os
import sys
import traceback
from pathlib import Path

import pytest


def _module_info(value: object) -> dict[str, object]:
    module_name = getattr(value, "__module__", None)
    module = sys.modules.get(module_name)
    return {
        "module_name": module_name,
        "module_path": str(getattr(module, "__file__", None)),
        "module_object_present": module is not None,
    }


def _snapshot(item: pytest.Item) -> dict[str, object]:
    import phase163_r3_registry_validation as validation
    import phase165_r52_r15_ordered_citation as ordered
    import unified_statement_registry as registry
    from proof import ProofRule, ProofStep

    test_module = item.module
    bridge, expected = test_module._fixture()
    assertion = bridge.registry.assertion("cited")
    citing = bridge.registry.assertion("citing")
    source = bridge.registry.reference(assertion.reference_id)
    destination = bridge.registry.reference(citing.reference_id)
    decision = validation.assess_citation(bridge.registry, "cited", "citing")
    ordered_fn = test_module.ordered_typed_reference_steps
    direct = ordered_fn(bridge, "fact", "citing")
    ordered_actual = ordered.ordered_typed_reference_steps(bridge, "fact", "citing")
    links = tuple(link for link in bridge.proof_links if link.assertion_id == assertion.assertion_id)
    test_globals = ordered_fn.__globals__
    backend_globals = ordered.ordered_typed_reference_steps.__globals__
    eligibility = {
        "origin_fixed_in_backend": assertion.origin is backend_globals["AssertionOrigin"].FIXED_STATEMENT,
        "origin_fixed_in_registry": assertion.origin is registry.AssertionOrigin.FIXED_STATEMENT,
        "goal_type_exact": type(assertion.content) is str,
        "goal_exact": assertion.content == "fact",
        "dependency_not_back_reference": "citing" not in assertion.dependencies,
        "decision_allowed_in_backend": decision.decision is backend_globals["CitationDecision"].ALLOWED,
        "decision_allowed_in_validation": decision.decision is validation.CitationDecision.ALLOWED,
        "source_id_equal": source.source_id == destination.source_id,
        "availability_prior": (assertion.available_after_position is not None
                               and destination.publication_position is not None
                               and assertion.available_after_position < destination.publication_position),
        "link_count_one": len(links) == 1,
        "link_step_given": len(links) == 1 and isinstance(links[0].step, ProofStep)
                           and links[0].step.rule is ProofRule.GIVEN,
        "link_conclusion_exact": len(links) == 1 and isinstance(links[0].step, ProofStep)
                                 and type(links[0].step.conclusion) is str
                                 and links[0].step.conclusion == "fact",
    }
    if not eligibility["origin_fixed_in_backend"]:
        classification = "ASSERTION_ORIGIN_IDENTITY_MISMATCH"
    elif not eligibility["decision_allowed_in_backend"]:
        classification = "CITATION_DECISION_OR_IDENTITY_REJECTED"
    elif not eligibility["link_count_one"] or not eligibility["link_step_given"]:
        classification = "PROOF_LINK_NOT_ELIGIBLE"
    elif not eligibility["link_conclusion_exact"]:
        classification = "PROOF_CONCLUSION_MISMATCH"
    elif not direct:
        classification = "LOOKUP_EMPTY_DESPITE_ELIGIBILITY"
    else:
        classification = "DIRECT_LOOKUP_SUCCESS_IN_PYTEST_HOOK"
    return {
        "test": item.nodeid,
        "classification": classification,
        "test_module": str(getattr(test_module, "__file__", None)),
        "test_function_module": _module_info(ordered_fn),
        "backend_function_module": _module_info(ordered.ordered_typed_reference_steps),
        "test_and_backend_function_identical": ordered_fn is ordered.ordered_typed_reference_steps,
        "test_fixture_module": _module_info(test_module._fixture),
        "backend_and_validation_assess_identical": backend_globals["assess_citation"] is validation.assess_citation,
        "backend_origin_enum_is_registry": backend_globals["AssertionOrigin"] is registry.AssertionOrigin,
        "backend_decision_enum_is_validation": backend_globals["CitationDecision"] is validation.CitationDecision,
        "test_proof_rule_is_backend": test_globals.get("ProofRule") is ProofRule,
        "decision_value": decision.decision.value,
        "decision_reason": decision.reason,
        "origin_value": assertion.origin.value,
        "source_id": source.source_id,
        "destination_source_id": destination.source_id,
        "cited_available_after": assertion.available_after_position,
        "citing_publication_position": destination.publication_position,
        "eligibility": eligibility,
        "test_direct_count": len(direct),
        "backend_direct_count": len(ordered_actual),
        "step_identity_expected": len(direct) == 1 and direct[0] is expected,
        "sys_path_first": sys.path[:8],
        "loaded_module_paths": {
            "ordered": str(getattr(ordered, "__file__", None)),
            "validation": str(getattr(validation, "__file__", None)),
            "registry": str(getattr(registry, "__file__", None)),
        },
    }


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_call(item: pytest.Item) -> None:
    if item.name not in (
        "test_ordered_reference_requires_only_prior_order",
        "test_ordered_reference_integrates_with_backward_search",
    ):
        return
    dest = os.environ.get("EHP_R20R2R2_PROBE_REPORT")
    if not dest:
        return
    try:
        result = _snapshot(item)
    except Exception as exc:
        result = {
            "test": item.nodeid,
            "probe_error": f"{type(exc).__name__}: {exc}",
            "traceback": traceback.format_exc(),
        }
    report = Path(dest)
    report.parent.mkdir(parents=True, exist_ok=True)
    with report.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, sort_keys=True) + "\n")
    print("R20R2R2_IN_PYTEST=" + json.dumps(result, ensure_ascii=False, sort_keys=True), flush=True)
