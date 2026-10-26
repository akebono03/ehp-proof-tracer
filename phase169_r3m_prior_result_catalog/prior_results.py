"""Read prior group *results* independently of proof construction and status.

A group structure stored in sphere.csv is a result, not a ProofStep.  A
literature citation is usable only when the project's existing typed source
binding and publication/component ordering can identify an earlier statement.
This module deliberately never manufactures a GIVEN or claims the database row
itself has a publication position.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from phase163_r4_registry_bridge import RegistryBridgeResult
from proof import Relation, RelationType


@dataclass(frozen=True)
class PriorGroupResult:
    source_n: int
    source_k: int
    relation: Relation | None
    citing_assertion_id: str
    source_assertion_id: str | None
    eligible: bool
    reason: str


def _database_result_candidates(
    *, source_n: int, source_k: int,
    csv_path: str | Path | None = None,
    generator_csv: str | Path | None = None,
) -> tuple[Relation, ...]:
    """Match the existing DB-goal precedence, without searching for proofs."""
    from phase166_r3aj_structured_generator import (
        database_structured_group_goal_candidates,
    )
    from phase166_r3af_goal_adapter import database_group_goal_candidates

    if source_k >= 2:
        structured = database_structured_group_goal_candidates(
            n=source_n, k=source_k,
            csv_path=csv_path, generator_csv=generator_csv,
        )
        if structured:
            return structured
    return database_group_goal_candidates(
        n=source_n, k=source_k, csv_path=csv_path,
    )


def resolve_prior_group_result(
    bridge: RegistryBridgeResult,
    *,
    source_n: int,
    source_k: int,
    citing_assertion_id: str,
    csv_path: str | Path | None = None,
    generator_csv: str | Path | None = None,
) -> PriorGroupResult:
    """Locate a prior DB relation and assess its independent source position.

    The operation reads only DB result rows, typed reference metadata and
    the common publication-order checker. It never reads, computes or tests
    completion of any proof. Missing source positions fail closed; the DB
    result remains visible to callers even if not yet authorized as a premise.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if (type(source_n) is not int or source_n < 2
            or type(source_k) is not int or source_k < 0):
        raise ValueError("source_n and source_k must be valid group dimensions")
    if not isinstance(citing_assertion_id, str) or not citing_assertion_id:
        raise ValueError("citing_assertion_id must be a nonempty string")
    citing = bridge.registry.assertion(citing_assertion_id)
    candidates = _database_result_candidates(
        source_n=source_n, source_k=source_k,
        csv_path=csv_path, generator_csv=generator_csv,
    )
    if len(candidates) != 1:
        return PriorGroupResult(
            source_n, source_k, None, citing_assertion_id, None,
            False, "db_result_missing" if not candidates else "db_result_ambiguous",
        )
    relation = candidates[0]
    from homotopy_groups import TodaPrimaryGroup
    if (not isinstance(relation, Relation)
            or relation.relation_type is not RelationType.EQUALITY
            or relation.lhs != TodaPrimaryGroup(source_n + source_k, source_n)):
        raise ValueError("DB group result is not the requested typed relation")

    if (isinstance(citing.content, Relation)
            and citing.content.lhs == relation.lhs):
        return PriorGroupResult(
            source_n, source_k, relation, citing_assertion_id, None,
            False, "same_group_as_target",
        )

    from phase166_r3t_goal_source_binding.goal_source import (
        resolve_specialized_goal_citing_id,
    )
    source_id = resolve_specialized_goal_citing_id(bridge, relation)
    if source_id is None:
        return PriorGroupResult(
            source_n, source_k, relation, citing_assertion_id, None,
            False, "source_not_uniquely_positioned",
        )

    from phase166_r3c_publication_order import precedes_citing_assertion
    if not precedes_citing_assertion(bridge, source_id, citing_assertion_id):
        return PriorGroupResult(
            source_n, source_k, relation, citing_assertion_id, source_id,
            False, "source_not_prior",
        )
    return PriorGroupResult(
        source_n, source_k, relation, citing_assertion_id, source_id,
        True, "prior_fixed_source",
    )
