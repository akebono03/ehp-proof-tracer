"""Targeted tests; no production registry or proof permissions are modified."""
from pathlib import Path

from expression import Composition, Multiple
from proof import RelationType
from phase166_r2_typed53.audit import ROOT, inspect, typed_witness


def test_typed_witness_has_matching_ambient_group():
    relation, typing = typed_witness()
    assert relation.relation_type is RelationType.EQUALITY
    assert isinstance(relation.lhs, Composition)
    assert isinstance(relation.rhs, Multiple)
    assert (typing["lhs_source"], typing["lhs_target"]) == (6, 3)
    assert (typing["rhs_source"], typing["rhs_target"]) == (6, 3)
    assert typing["inner_composition_compatible"]
    assert typing["outer_composition_compatible_by_boundary"]


def test_typed_witness_does_not_claim_truth_or_citation():
    _, typing = typed_witness()
    assert not typing["mathematical_identity_confirmed"]
    assert not typing["proof_permission_granted"]
    assert not typing["registry_content_equal_to_relation"]


def test_actual_equation53_rows_remain_uncertified():
    from phase165_r4_production_connection import discover_production_registry
    registry = discover_production_registry().bridge.registry
    path = ROOT / "sphere_relation2.csv"
    if not path.exists():
        path = ROOT / "phase166_r1_source_registry_audit" / "sphere_relation2.csv"
    report = inspect(path, registry)
    assert report["equation53_rows"] == 4
    assert report["display_match_rows"] == 2
    assert report["mathematical_identity_confirmed"] == 0
    assert report["proof_permission_granted"] == 0
    assert all(not row["proof_permission_granted"] for row in report["rows"])
