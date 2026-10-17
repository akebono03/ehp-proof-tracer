"""Targeted connection tests; never run retired catalog."""
from pathlib import Path

from phase165_rule_registry_r11_runtime_fix.audit import ROOT, function_calls, main, resolved_rule_discovery_calls


def test_r11_registry_and_discovery_share_order_and_ids():
    result = main()
    assert result["status"] == "CONNECTED"
    assert result["registry_entries"] == result["discovered_rules"]
    assert result["rule_ids_unique"] is True
    assert result["ordering_matches"] is True


def test_r11_shared_backward_provider_is_connected():
    search = function_calls(ROOT / "phase165_r57_r26_generic_search_connection.py", "build_generic_backward_expansion_provider")
    assert "discover_inference_rules" in search
    result = main()
    assert result["generic_provider_executed"] is True
    assert result["removed_adapter_absent"] is True
    assert result["removed_pi43_rule_definitions"] == []


def test_r11_retired_catalog_is_not_used_by_audit():
    source = (Path(__file__).parent / "audit.py").read_text(encoding="utf-8")
    assert "build_standard_production_applicability_catalog(" not in source
    assert "from standard_production_applicability_catalog import" not in source


def test_r11_discovery_alias_resolution(tmp_path):
    source = tmp_path / "example.py"
    source.write_text(
        "def shared_expansion_provider():\n"
        "    from phase165_r8_rule_provider import discover_inference_rules as seeded\n"
        "    seeded()\n",
        encoding="utf-8",
    )
    assert resolved_rule_discovery_calls(source, "shared_expansion_provider") == ("seeded",)


def test_r11_shared_provider_may_not_call_discovery_directly(tmp_path):
    """Indirect R8 access through the generic provider is valid."""
    source = tmp_path / "example.py"
    source.write_text(
        "def shared_expansion_provider():\n"
        "    return build_generic_backward_expansion_provider()\n",
        encoding="utf-8",
    )
    assert resolved_rule_discovery_calls(source, "shared_expansion_provider") == ()
    assert "build_generic_backward_expansion_provider" in function_calls(
        source, "shared_expansion_provider"
    )
