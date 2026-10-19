from types import SimpleNamespace
import pytest
from phase166_r2_three_groups.audit import FOCUS, inspect


def _fixture():
    refs = {}
    assertions = {}
    for n, k, locator, key, _ in FOCUS:
        ref = "ref:" + locator
        refs[ref] = SimpleNamespace(locator=locator)
        assertions[f"boundary:{locator}:{key}"] = SimpleNamespace(
            reference_id=ref,
            content=SimpleNamespace(reference_locator=locator, component_key=key, statement_role=SimpleNamespace(value="group_structure")),
        )
    class Registry:
        def assertion(self, key):
            return assertions[key]
        def reference(self, key):
            return refs[key]
    sphere = [dict(n=str(n), k=str(k), id="0", orders="2", generator="eta", Element="2") for n,k,*_ in FOCUS]
    return sphere, [{"id": "2", "display": "η"}], SimpleNamespace(registry=Registry())


def test_three_candidates_without_grant():
    result = inspect(*_fixture())
    assert result["target_count"] == 3
    assert result["mathematical_identity_confirmed"] == 0
    assert result["proof_permission_granted"] == 0
    assert all(r["correspondence"] == "METADATA_COMPONENT_CANDIDATE_ONLY" for r in result["targets"])


def test_missing_group_fails_closed():
    sphere, generators, bridge = _fixture()
    with pytest.raises(ValueError, match="missing sphere rows"):
        inspect(sphere[:2], generators, bridge)


def test_unknown_generator_fails_closed():
    sphere, generators, bridge = _fixture()
    sphere[0]["Element"] = "999"
    with pytest.raises(ValueError, match="unknown generator ID"):
        inspect(sphere, generators, bridge)


def test_wrong_component_fails_closed():
    sphere, generators, bridge = _fixture()
    original = bridge.registry.assertion
    def altered(key):
        a = original(key)
        return SimpleNamespace(reference_id=a.reference_id, content=SimpleNamespace(component_key="WRONG", reference_locator="Proposition 5.1"))
    bridge.registry.assertion = altered
    with pytest.raises(ValueError, match="inconsistent registry"):
        inspect(sphere, generators, bridge)
