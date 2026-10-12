# Phase 164 R7-R4 変更コード全文

- `repository_operation_query_facade.py`: import 全体、変更関数全体
- `phase164_r7_r3_generator_registry.py`: 互換モジュール全体
- `phase164_r7_repository_root_resolution.py`: 新規モジュール全体
- `tests/test_phase164_r7_r4_operation_registry.py`: 新規テスト全体

## Operation の変更後 import 全文

```python
from proof_repository import ProofRepository
from phase164_r7_repository_root_resolution import (
  validate_repository_internal_proof_roots,
)
from repository_nu5_eta8_suspension_zero_specialization import (
  is_nu5_eta8_suspension_zero_operation_query,
  query_nu5_eta8_suspension_zero_handoff,
)
from repository_nu5_stable_bridge_specialization import (
  is_nu5_stable_bridge_operation_query,
  query_nu5_stable_bridge_handoff,
)
from repository_nu_prime_suspension_membership_specialization import (
  is_nu_prime_suspension_membership_operation_query,
  query_nu_prime_suspension_membership_handoff,
)
from repository_operation_query import (
  parse_repository_operation_query,
)
from repository_operation_query_lookup import (
  RepositoryOperationQueryResult,
  query_repository_operation,
)
from repository_sigma11_suspension_specialization import (
  is_sigma11_suspension_operation_query,
  query_sigma11_suspension_handoff,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)
```

## Operation 変更関数全文

```python
def query_standard_repository_operation_input(
  query_input: str,
) -> RepositoryOperationQueryResult:
  repository = (
    build_standard_production_proof_repository()
  )

  validate_repository_internal_proof_roots(
    repository
  )

  return query_repository_operation_input(
    repository,
    query_input,
  )
```

## `phase164_r7_r3_generator_registry.py` 全文

```python
"""R7-R3 compatibility shim for the shared R7 repository proof-root validator."""
from phase164_r7_repository_root_resolution import (
    validate_repository_internal_proof_roots,
)
from proof_repository import ProofRepository


def validate_generator_repository_registry_links(
    repository: ProofRepository,
) -> ProofRepository:
    """Keep the R7-R3 API while sharing the canonical root resolver."""
    return validate_repository_internal_proof_roots(repository)
```

## `phase164_r7_repository_root_resolution.py` 全文

```python
"""Phase 164 R7-R4: shared internal proof-root resolution for all repository queries.

The bridge records existing internal proof roots, not verified literature.
This module neither constructs nor authorizes mathematical ProofSteps.
"""
from types import SimpleNamespace

from phase163_r4_registry_bridge import build_registry_bridge
from phase164_r7_statement_resolution import resolve_registered_statement
from proof_repository import ProofRepository
from unified_statement_registry import AssertionOrigin


def validate_repository_internal_proof_roots(
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
            raise ValueError("repository root must remain proof-internal")
        if resolved.proof_link is None or resolved.proof_link.step is not entry.step:
            raise ValueError("repository root ProofStep identity mismatch")
    return repository
```

## `tests/test_phase164_r7_r4_operation_registry.py` 全文

```python
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
```
