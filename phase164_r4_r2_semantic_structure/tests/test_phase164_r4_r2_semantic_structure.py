"""Targeted R4-R2 tests. These do not certify mathematical equivalence."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path

import pytest

from phase164_r4_r1_source_crosswalk import source_crosswalk
from phase164_r4_r2_semantic_structure import compare_structured_leaves
from proof import ProofRule, Relation
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from toda_rules import TodaProp42ExactnessStatement


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "phase163_r4_r94_output" / "manifest.json"


@pytest.fixture(scope="module")
def inputs():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    steps = tuple(step for step in build_phase59_3_data()["premise_steps"]
                  if step.rule is ProofRule.INFERENCE
                  and not isinstance(step.conclusion, TodaProp42ExactnessStatement))
    return source_crosswalk(manifest, steps), steps


def test_four_prop51_components_structurally_present(inputs):
    report = compare_structured_leaves(*inputs)
    assert [item["name"] for item in report["prop51"]["components"]] == [
        "pi3_2_group_relation", "eta2_hopf_relation",
        "delta_iota5_relation", "higher_eta_group_relation",
    ]
    assert report["prop51"]["all_four_components_structurally_present"]
    assert report["prop51"]["additional_stable_clause_in_source"]


def test_hopf_relation_shape_and_source_clause(inputs):
    report = compare_structured_leaves(*inputs)
    hopf = report["nu_prime_hopf"]
    assert hopf["relation_type"] == "EQUALITY"
    assert hopf["map_is_ehp_h"]
    assert hopf["source_tokens_all_present"]
    assert hopf["lhs_type"] == "MapApplication"


def test_no_citation_or_registry_promotion(inputs):
    report = compare_structured_leaves(*inputs)
    assert report["source_archive_proof_eligible_count"] == 0
    assert report["citation_eligible"] is False
    assert report["typed_registry_binding_written"] is False
    assert report["proof_search_connected"] is False
    assert report["independent_mathematical_verification"] is False
    assert not report["original_edition_verified"]
    assert all(not item["semantic_equivalence_verified"]
               for item in report["prop51"]["components"])


def test_wrong_source_token_rejected(inputs):
    crosswalk, steps = inputs
    altered = deepcopy(crosswalk)
    altered["leaves"][1]["source_text"] = altered["leaves"][1]["source_text"].replace(
        r"H(\nu')=\eta_5", r"H(\nu')=\eta_4"
    )
    with pytest.raises(ValueError, match="source clauses"):
        compare_structured_leaves(altered, steps)


def test_wrong_hopf_relation_rejected(inputs):
    crosswalk, steps = inputs
    from expression import HomotopyElement
    changed = replace(steps[1], conclusion=replace(
        steps[1].conclusion, rhs=HomotopyElement(name="η₄", dimension=4, source=5, target=4)
    ))
    with pytest.raises(ValueError, match="element typing"):
        compare_structured_leaves(crosswalk, (steps[0], changed))


def test_source_identity_mismatch_rejected(inputs):
    crosswalk, steps = inputs
    altered = deepcopy(crosswalk)
    altered["leaves"][0]["source_statement_id"] = "wrong"
    with pytest.raises(ValueError, match="source IDs"):
        compare_structured_leaves(altered, steps)
