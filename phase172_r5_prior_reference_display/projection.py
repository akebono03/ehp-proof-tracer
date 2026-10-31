"""Present authentic adopted prior DB citations without changing provenance.

The internal locator remains unchanged for proof verification, citation identity,
and historical consumers. Only the public Reference heading is projected.
"""
from __future__ import annotations

import re

from homotopy_groups import TodaPrimaryGroup
from phase168_r3_3_proof_narrative_model import (
    NarrativeCitation,
    ProofNarrativeModel,
    root_ancestor_step_indices,
)
from phase165_r52_partial_proof import ProofSearchStatus
from phase169_r10e4_ordered_db_prior.db_prior import (
    DB_LOCATOR_PREFIX,
    group_coordinates,
    precedes_db_goal,
)
from proof import ProofRule


_DB_LOCATOR = re.compile(
    re.escape(DB_LOCATOR_PREFIX)
    + r" \(n=([0-9]+), k=([0-9]+)\)(?: \[参考: ([^\]\r\n]+)\])?"
)
_DB_NOTE = "ADOPTED_DATABASE_PRIOR; independent reference not asserted"


def display_prior_reference_locator(
    citation: object, model: object,
) -> str | None:
    """Return a Japanese heading only for an actual verified DB prior leaf.

    A locator alone cannot authorize presentation as a DB assumption. Require
    exactly one cited GIVEN leaf in the completed root ancestry, the canonical
    adopted-prior marker, an unmodified inference-rule locator, and matching
    typed group coordinates. Never rewrite literature/registry citations.
    """
    if (not isinstance(citation, NarrativeCitation)
            or not isinstance(model, ProofNarrativeModel)
            or model.status is not ProofSearchStatus.COMPLETE
            or model.open_goals
            or not isinstance(model.target, TodaPrimaryGroup)):
        return None
    locator = citation.reference.locator or citation.reference.label
    if not isinstance(locator, str):
        return None
    match = _DB_LOCATOR.fullmatch(locator)
    if match is None:
        return None
    if (citation.assertion_ids or citation.reference_ids
            or citation.statement_bodies
            or len(citation.step_indices) != 1):
        return None
    if (not isinstance(model.steps, tuple)
            or not isinstance(model.step_citation_numbers, tuple)
            or len(model.step_citation_numbers) != len(model.steps)):
        return None
    index = citation.step_indices[0]
    if type(index) is not int or not 0 <= index < len(model.steps):
        return None
    if type(model.root_index) is not int:
        return None
    try:
        ancestry = root_ancestor_step_indices(model.steps, model.root_index)
    except ValueError:
        return None
    if index not in ancestry:
        return None
    step = model.steps[index]
    reference = getattr(getattr(step, "inference_rule", None), "literature_reference", None)
    step_locator = getattr(reference, "locator", None)
    if (step.rule is not ProofRule.GIVEN
            or step.premises
            or step.note != _DB_NOTE
            or step_locator != locator
            or citation.number not in model.step_citation_numbers[index]):
        return None
    coordinates = group_coordinates(step.conclusion)
    if coordinates is None:
        return None
    n, k = coordinates
    if (str(n) != match.group(1) or str(k) != match.group(2)
            or type(model.target.sphere_dimension) is not int
            or type(model.target.group_dimension) is not int):
        return None
    target_n = model.target.sphere_dimension
    target_k = model.target.group_dimension - target_n
    if not precedes_db_goal(n, k, target_n, target_k):
        return None
    heading = (
        rf"先行データベース結果 $\pi_{{{n + k}}}^{{{n}}}$"
        f"（sphere.csv, n={n}, k={k}）"
    )
    if match.group(3) is not None:
        heading += f"［参考: {match.group(3)}］"
    return heading
