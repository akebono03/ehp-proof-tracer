"""Pure classification of independent derivation probes."""
from __future__ import annotations


def classify_routes(full_status: str, statuses: tuple[str, ...]) -> str:
    """Classify observed results without treating a proposal as evidence."""
    if full_status == "proved":
        return "RIGHT_ALREADY_PROVED"
    if full_status != "unresolved":
        return "UNEXPECTED_DIRECT_STATUS"
    successful = sum(status == "proved" for status in statuses)
    if successful >= 2:
        return "MULTIPLE_INDEPENDENT_PROVED_ROUTES"
    if successful == 1:
        return "SINGLE_ROUTE_PROVED_BUT_UNSCOPED_GOAL_UNRESOLVED"
    if not statuses:
        return "NO_PROVIDER_ROUTES"
    if all(status == "unresolved" for status in statuses):
        return "NO_INDIVIDUAL_ROUTE_PROVED"
    return "SOME_ROUTE_PROBES_INCONCLUSIVE"
