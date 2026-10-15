"""R22 read-only source contract checks; no proof production changes."""
from pathlib import Path

from audit import FILES, static_audit

ROOT = Path(__file__).resolve().parent.parent


def test_r22_required_sources_present():
    assert all((ROOT / name).is_file() for name in FILES)


def test_r22_shared_search_has_forward_validation():
    checks = static_audit(ROOT)['checks']
    assert checks['search_recurses_over_provider_subgoals']
    assert checks['search_forward_checks_inference']


def test_r22_adapter_still_registered_in_shared_provider():
    checks = static_audit(ROOT)['checks']
    assert checks['shared_provider_calls_pi43_adapter']
    assert checks['pi43_adapter_contains_target_specific_goals']


def test_r22_general_components_exist_without_claiming_full_unification():
    checks = static_audit(ROOT)['checks']
    assert checks['inference_rule_has_conclusion_pattern']
    assert checks['generic_scalar_specialization_exists']
    assert checks['delta_image_reverse_exists']
    assert checks['finite_cyclic_substitution_exists']
