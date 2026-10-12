"""R7-R3: synthetic registry resolution and unchanged standard Generator route."""
from unittest.mock import patch

import pytest

from expression import GeneratorSymbol
from phase164_r7_r3_generator_registry import validate_generator_repository_registry_links
from proof import ProofRule, ProofStep
from proof_repository import ProofRepository, ProofRepositoryEntry
from repository_generator_known_group_identity_lookup import (
    find_standard_repository_generator_known_group_identity_nodes,
)


def _repository():
    repository = ProofRepository()
    step = ProofStep(conclusion="fixture conclusion", premises=(), rule=ProofRule.GIVEN)
    entry = ProofRepositoryEntry(key="fixture.root", step=step)
    repository.register(entry)
    return repository, entry


def test_r7_r3_resolves_registered_proof_root_without_changing_identity():
    repository, entry = _repository()
    assert validate_generator_repository_registry_links(repository) is repository
    assert repository.get(entry.key) is entry
    assert repository.get(entry.key).step is entry.step


def test_r7_r3_empty_repository_is_preserved():
    repository = ProofRepository()
    assert validate_generator_repository_registry_links(repository) is repository
    assert repository.entries() == ()


def test_r7_r3_rejects_non_repository():
    with pytest.raises(TypeError, match="repository must be a ProofRepository"):
        validate_generator_repository_registry_links(object())


def test_r7_r3_standard_generator_path_uses_registry_guard():
    repository, _ = _repository()
    generator = GeneratorSymbol(family="η", index=3)
    with (
        patch(
            "repository_generator_known_group_identity_lookup.build_standard_production_proof_repository",
            return_value=repository,
        ),
        patch(
            "repository_generator_known_group_identity_lookup.validate_generator_repository_registry_links",
            wraps=validate_generator_repository_registry_links,
        ) as guard,
        patch(
            "repository_generator_known_group_identity_lookup.find_repository_generator_known_group_identity_nodes",
            return_value=(),
        ) as lookup,
    ):
        result = find_standard_repository_generator_known_group_identity_nodes(generator)
    assert result == ()
    guard.assert_called_once_with(repository)
    lookup.assert_called_once_with(repository, generator)


def test_r7_r3_guard_failure_prevents_generator_search():
    repository, _ = _repository()
    generator = GeneratorSymbol(family="η", index=3)
    with (
        patch(
            "repository_generator_known_group_identity_lookup.build_standard_production_proof_repository",
            return_value=repository,
        ),
        patch(
            "repository_generator_known_group_identity_lookup.validate_generator_repository_registry_links",
            side_effect=ValueError("registry link mismatch"),
        ),
        patch(
            "repository_generator_known_group_identity_lookup.find_repository_generator_known_group_identity_nodes",
        ) as lookup,
    ):
        with pytest.raises(ValueError, match="registry link mismatch"):
            find_standard_repository_generator_known_group_identity_nodes(generator)
    lookup.assert_not_called()
