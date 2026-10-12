"""R7-R4: common root validation and Operation facade identity tests."""
from unittest.mock import patch

import pytest

from phase164_r7_repository_root_resolution import validate_repository_internal_proof_roots
from phase164_r7_r3_generator_registry import validate_generator_repository_registry_links
from proof import ProofRule, ProofStep
from proof_repository import ProofRepository, ProofRepositoryEntry
from repository_operation_query_facade import (
    query_standard_repository_operation_input,
)
from repository_operation_query_lookup import RepositoryOperationQueryResult
from repository_operation_query import parse_repository_operation_query


def _repository():
    repository = ProofRepository()
    step = ProofStep(conclusion="operation fixture", premises=(), rule=ProofRule.GIVEN)
    entry = ProofRepositoryEntry(key="fixture.operation", step=step)
    repository.register(entry)
    return repository, entry


def test_r7_r4_common_validator_preserves_repository_and_step_identity():
    repository, entry = _repository()
    assert validate_repository_internal_proof_roots(repository) is repository
    assert repository.get(entry.key) is entry
    assert repository.get(entry.key).step is entry.step


def test_r7_r4_generator_compatibility_uses_same_validator():
    repository, _ = _repository()
    with patch(
        "phase164_r7_r3_generator_registry.validate_repository_internal_proof_roots",
        wraps=validate_repository_internal_proof_roots,
    ) as common:
        assert validate_generator_repository_registry_links(repository) is repository
    common.assert_called_once_with(repository)


def test_r7_r4_standard_operation_checks_before_search():
    repository, _ = _repository()
    expected = RepositoryOperationQueryResult(
        query=parse_repository_operation_query("H(nu_prime)"),
        matches=(),
    )
    with (
        patch(
            "repository_operation_query_facade.build_standard_production_proof_repository",
            return_value=repository,
        ),
        patch(
            "repository_operation_query_facade.validate_repository_internal_proof_roots",
            wraps=validate_repository_internal_proof_roots,
        ) as guard,
        patch(
            "repository_operation_query_facade.query_repository_operation_input",
            return_value=expected,
        ) as query,
    ):
        actual = query_standard_repository_operation_input("H(nu_prime)")
    assert actual is expected
    guard.assert_called_once_with(repository)
    query.assert_called_once_with(repository, "H(nu_prime)")


def test_r7_r4_guard_failure_prevents_operation_lookup():
    repository, _ = _repository()
    with (
        patch(
            "repository_operation_query_facade.build_standard_production_proof_repository",
            return_value=repository,
        ),
        patch(
            "repository_operation_query_facade.validate_repository_internal_proof_roots",
            side_effect=ValueError("registry link mismatch"),
        ),
        patch("repository_operation_query_facade.query_repository_operation_input") as query,
    ):
        with pytest.raises(ValueError, match="registry link mismatch"):
            query_standard_repository_operation_input("H(nu_prime)")
    query.assert_not_called()


def test_r7_r4_empty_repository_is_preserved():
    repository = ProofRepository()
    assert validate_repository_internal_proof_roots(repository) is repository
    assert repository.entries() == ()


def test_r7_r4_invalid_repository_fails_closed():
    with pytest.raises(TypeError, match="repository must be a ProofRepository"):
        validate_repository_internal_proof_roots(object())
