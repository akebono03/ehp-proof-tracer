import pytest
from standard_production_applicability_catalog import build_standard_production_applicability_catalog


def test_legacy_production_catalog_remains_retired():
    with pytest.raises(RuntimeError, match="Legacy production applicability catalog is retired"):
        build_standard_production_applicability_catalog()


def test_unified_registry_remains_available():
    from phase163_r4_registry_bridge import build_registry_bridge
    result = build_registry_bridge()
    assert result.registry is not None
    assert result.records
