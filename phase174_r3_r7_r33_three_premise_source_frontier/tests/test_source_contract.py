"""Pure R33 source contract regression tests (no repository required)."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r33_three_premise_source_frontier.source_contract import (
    CODOMAIN_CLAUSE, DERIVED_KERNEL, DIAGONAL_CLAUSE, END_EQUATION,
    END_PROPOSITION, EQ510, IMAGE_CLAUSE, PROP58, PROP59,
    classify_three_premises, inspect_prior_three_clauses,
)


def source_fixture() -> str:
    return "\n".join((
        DIAGONAL_CLAUSE, PROP58, CODOMAIN_CLAUSE, END_PROPOSITION,
        EQ510, IMAGE_CLAUSE, END_EQUATION, PROP59, DERIVED_KERNEL,
    ))


def test_source_evidence_is_prior_and_not_a_proof_step() -> None:
    evidence = inspect_prior_three_clauses(source_fixture())
    assert len(evidence) == 3
    assert tuple(x.name for x in evidence) == (
        "diagonal_domain", "finite_codomain", "delta_generator_image",
    )
    assert all(x.appears_before_prop59 for x in evidence)
    assert all(not x.statement_is_verified_proof_step for x in evidence)


@pytest.mark.parametrize("missing", (
    DIAGONAL_CLAUSE, CODOMAIN_CLAUSE, IMAGE_CLAUSE,
    PROP58, PROP59, EQ510, DERIVED_KERNEL,
))
def test_missing_required_text_rejected(missing: str) -> None:
    with pytest.raises(ValueError):
        inspect_prior_three_clauses(source_fixture().replace(missing, "DELETED"))


def test_duplicated_source_statement_rejected() -> None:
    with pytest.raises(ValueError):
        inspect_prior_three_clauses(source_fixture().replace(
            IMAGE_CLAUSE, IMAGE_CLAUSE + "\n" + IMAGE_CLAUSE,
        ))


def test_reversed_provenance_rejected() -> None:
    prior = source_fixture()
    prior = prior.replace(PROP58, "PLACEHOLDER").replace(PROP59, PROP58).replace("PLACEHOLDER", PROP59)
    with pytest.raises(ValueError):
        inspect_prior_three_clauses(prior)


def test_earlier_kernel_conclusion_rejected() -> None:
    prior = source_fixture().replace(PROP58, DERIVED_KERNEL + "\n" + PROP58)
    with pytest.raises(ValueError):
        inspect_prior_three_clauses(prior)


def test_three_independent_premises_are_required() -> None:
    full = classify_three_premises(domain=True, codomain=True, image=True)
    assert full["all_screened"] and full["missing"] == ()
    for key in ("domain", "codomain", "image"):
        flags = {"domain": True, "codomain": True, "image": True}
        flags[key] = False
        result = classify_three_premises(**flags)
        assert not result["all_screened"]
        assert len(result["missing"]) == 1


def test_unknown_proof_availability_is_rejected() -> None:
    with pytest.raises(TypeError):
        classify_three_premises(domain=1, codomain=True, image=True)
    with pytest.raises(TypeError):
        inspect_prior_three_clauses(None)
