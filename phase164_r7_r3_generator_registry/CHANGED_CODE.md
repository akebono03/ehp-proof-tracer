# R7-R3 Full changed code

## Existing module: complete new import section
```python
from expression import GeneratorSymbol
from generator_facts import (
  GENERATOR_FACT_REPOSITORY,
  GeneratorFactRepository,
)
from generator_input import (
  resolve_generator_input,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  Relation,
  RelationType,
)
from proof_repository import (
  ProofRepository,
)
from phase164_r7_r3_generator_registry import (
  validate_generator_repository_registry_links,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
  RepositoryProofScopeResult,
  build_repository_proof_scope,
)
from repository_symbolic_sigma_specialization import (
  is_toda_prop515_generic_sigma_specialization_generator,
  specialize_repository_proof_scope_for_generator,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)
from structural_containment import (
  contains_generator_symbol,
)
from toda_group_lookup import (
  is_toda_group_result_for_target,
)
```

## Existing module: complete replaced function
```python
def find_standard_repository_generator_known_group_identity_nodes(
  generator: GeneratorSymbol,
) -> tuple[
  RepositoryProofScopeNode,
  ...,
]:
  if not isinstance(
    generator,
    GeneratorSymbol,
  ):
    raise TypeError(
      "generator must be a GeneratorSymbol"
    )

  repository = (
    build_standard_production_proof_repository()
  )

  validate_generator_repository_registry_links(
    repository
  )

  return (
    find_repository_generator_known_group_identity_nodes(
      repository,
      generator,
    )
  )
```

## New file: phase164_r7_r3_generator_registry.py (complete)
```python
"""Phase 164 R7-R3: resolve generator repository roots through the R7 registry API.

The bridge records existing internal proof roots, not verified literature.
This module neither constructs nor authorizes mathematical ProofSteps.
"""
from types import SimpleNamespace

from phase163_r4_registry_bridge import build_registry_bridge
from phase164_r7_statement_resolution import resolve_registered_statement
from proof_repository import ProofRepository
from unified_statement_registry import AssertionOrigin


def validate_generator_repository_registry_links(
    repository: ProofRepository,
) -> ProofRepository:
    """Fail closed on inconsistent registered root steps, preserving identity."""
    if not isinstance(repository, ProofRepository):
        raise TypeError("repository must be a ProofRepository")

    bridge = build_registry_bridge(
        components_by_reference={},
        theorem_facts=SimpleNamespace(entries=()),
        proof_repository=repository,
    )
    for entry in repository.entries():
        resolved = resolve_registered_statement(
            bridge,
            f"repository:{entry.key}:conclusion",
            proof_repository=repository,
            expected_conclusion=entry.step.conclusion,
        )
        if resolved.assertion.origin is not AssertionOrigin.PROOF_INTERNAL:
            raise ValueError("generator root must remain proof-internal")
        if resolved.proof_link is None or resolved.proof_link.step is not entry.step:
            raise ValueError("generator root ProofStep identity mismatch")
    return repository

```

## New file: tests/test_phase164_r7_r3_generator_registry.py (complete)
```python
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

```
