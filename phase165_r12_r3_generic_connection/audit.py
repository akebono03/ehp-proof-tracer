"""Read-only R12-R3 local code / registry diagnostic."""
import json
from phase165_r8_rule_provider import DEFAULT_RULE_MODULES, discover_inference_rules
from phase165_r10_rule_registry import build_rule_registry


def main():
    registry = build_rule_registry(DEFAULT_RULE_MODULES)
    rules, report = discover_inference_rules()
    r12 = tuple(entry for entry in registry.entries
                if entry.factory_module == "phase165_r12_r2_quotient_rules")
    result = {
        "phase": "165 R12-R3",
        "mode": "GENERIC_CHAIN_INTEGRATION_TEST_NOT_PI43_COMPLETION",
        "registered_rules": len(registry.entries),
        "production_provider_rules": len(rules),
        "r12_r2_auto_registered_ids": [entry.rule_id for entry in r12],
        "backward_pattern_candidates": sum(entry.backward_pattern_candidate for entry in registry.entries),
        "required_input_factories": len([s for s in report.skipped_factories if "requires-input" in s]),
        "target_pi43_proof_certified": False,
        "full_pytest_run": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if len(r12) != 2 or len(registry.entries) != len(rules):
        raise SystemExit("R12-R2 auto-registration precondition failed")


if __name__ == "__main__":
    main()
