"""Phase 169 R10E4: admitted prior DB results, ordered by (stem, dimension).

A DB result is an explicitly adopted hypothesis, not a cited mathematical
proposition.  It is re-read from a concrete sphere.csv row on every admission
and on the Web proof-tree trust boundary.  Publication metadata is never
invented; real proposition locators are optional display-only annotations.
"""
from __future__ import annotations

import csv
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep, Relation, RelationType

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = ROOT / "data" / "sphere.csv"
DEFAULT_GENERATORS = ROOT / "data" / "HyoujiGen.csv"
DB_LOCATOR_PREFIX = "DB prior: sphere.csv"


def precedes_db_goal(source_n: int, source_k: int, target_n: int, target_k: int) -> bool:
    """Project-authorized dependency order, not Toda publication order."""
    if not all(type(v) is int for v in (source_n, source_k, target_n, target_k)):
        return False
    if min(source_n, target_n) < 2 or min(source_k, target_k) < 0:
        return False
    return (source_k, source_n) < (target_k, target_n)


def group_coordinates(statement: object) -> tuple[int, int] | None:
    group = None
    if isinstance(statement, TodaPrimaryGroupZeroStatement):
        group = statement.group
    elif (isinstance(statement, Relation)
          and statement.relation_type is RelationType.EQUALITY
          and isinstance(statement.lhs, TodaPrimaryGroup)):
        group = statement.lhs
    if not isinstance(group, TodaPrimaryGroup):
        return None
    if type(group.group_dimension) is not int or type(group.sphere_dimension) is not int:
        return None
    n = group.sphere_dimension
    k = group.group_dimension - n
    return (n, k) if n >= 2 and k >= 0 else None


def _has_explicit_row(n: int, k: int, path: Path) -> bool:
    """Detect a real group row without accepting malformed nonempty dimensions.

    Separator rows may omit n; every nonempty n/k field is validated before
    returning a match, including fields after a matching row. The scanner
    never uses SphereRepository's stable-range fallback.
    """
    if not path.is_file():
        return False
    try:
        found = False
        with path.open(encoding="utf-8-sig", newline="") as stream:
            rows = csv.DictReader(stream)
            if rows.fieldnames is None or not {"n", "k", "id"}.issubset(rows.fieldnames):
                return False
            for row in rows:
                if not isinstance(row, dict):
                    return False
                raw_n = row.get("n")
                raw_k = row.get("k")
                if raw_n is None or raw_k is None:
                    return False
                raw_n = raw_n.strip()
                raw_k = raw_k.strip()
                if not raw_k:
                    if raw_n:
                        return False
                    continue
                parsed_k = int(raw_k)
                if not raw_n:
                    continue
                parsed_n = int(raw_n)
                if parsed_n == n and parsed_k == k:
                    found = True
        return found
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, csv.Error):
        return False


def exact_prior_database_result(
    n: int, k: int, *, csv_path: str | Path | None = None,
    generator_csv: str | Path | None = None,
) -> object | None:
    """Return exactly one typed DB group, without fabricating a proof or citation."""
    if not all(type(x) is int for x in (n, k)) or n < 2 or k < 0:
        return None
    path = Path(csv_path) if csv_path is not None else DEFAULT_CSV
    gens = Path(generator_csv) if generator_csv is not None else DEFAULT_GENERATORS
    if not _has_explicit_row(n, k, path):
        return None
    from phase169_r3m_prior_result_catalog.prior_results import _database_result_candidates
    from phase166_r3af_goal_adapter import database_zero_group_goal_candidates
    candidates = _database_result_candidates(
        source_n=n, source_k=k, csv_path=path, generator_csv=gens,
    )
    zeros = database_zero_group_goal_candidates(n=n, k=k, csv_path=path)
    unique = tuple(candidates) + tuple(zeros)
    if len(unique) != 1 or group_coordinates(unique[0]) != (n, k):
        return None
    return unique[0]


def _optional_registered_locator(statement: object, bridge: object | None) -> str | None:
    """Annotate matching registered propositions, without authorizing the DB."""
    if bridge is None:
        return None
    from unified_statement_registry import AssertionOrigin
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    if not isinstance(statement, Relation):
        return None
    citation_id = resolve_specialized_goal_citing_id(bridge, statement)
    if citation_id is None:
        return None
    assertion = bridge.registry.assertion(citation_id)
    if assertion.origin is not AssertionOrigin.FIXED_STATEMENT:
        return None
    locator = bridge.registry.reference(assertion.reference_id).locator
    return locator if isinstance(locator, str) and locator.strip() else None


def admitted_db_step(
    statement: object, *, proof_target: object,
    bridge: object | None = None,
    csv_path: str | Path | None = None,
    generator_csv: str | Path | None = None,
) -> ProofStep | None:
    """Adopt only a genuinely earlier, explicit, uniquely typed database row."""
    source = group_coordinates(statement)
    target = group_coordinates(proof_target)
    if source is None or target is None:
        return None
    n, k = source
    target_n, target_k = target
    if not precedes_db_goal(n, k, target_n, target_k):
        return None
    original = exact_prior_database_result(
        n, k, csv_path=csv_path, generator_csv=generator_csv,
    )
    if original is None or type(original) is not type(statement) or original != statement:
        return None
    locator = f"{DB_LOCATOR_PREFIX} (n={n}, k={k})"
    registered = _optional_registered_locator(statement, bridge)
    if registered is not None:
        locator += f" [参考: {registered}]"
    return ProofStep(
        conclusion=statement, premises=(), rule=ProofRule.GIVEN,
        note="ADOPTED_DATABASE_PRIOR; independent reference not asserted",
        inference_rule=InferenceRule(
            name="adopted prior database result (not a literature theorem)",
            literature_reference=LiteratureReference(label=locator, locator=locator),
        ),
    )


def verified_db_step(
    step: ProofStep, *, proof_target: object, bridge: object | None = None,
) -> bool:
    """Do not accept a note or caller-supplied provenance without fresh DB checks."""
    if not isinstance(step, ProofStep) or step.rule is not ProofRule.GIVEN or step.premises:
        return False
    if step.note != "ADOPTED_DATABASE_PRIOR; independent reference not asserted":
        return False
    expected = admitted_db_step(step.conclusion, proof_target=proof_target, bridge=bridge)
    return expected is not None and expected == step
