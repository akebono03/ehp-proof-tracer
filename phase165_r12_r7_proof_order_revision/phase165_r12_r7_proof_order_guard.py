"""Generic citation eligibility for ordered clauses in a typed composite.

A statement's printed position is metadata, not permission to cite it.
A proof dependency must be explicitly reviewed. A parent GIVEN is never
allowed when the target is a clause of the same composite reference.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase163_r4_registry_bridge import RegistryBridgeResult
from proof import ProofRule


@dataclass(frozen=True)
class OrderedClaim:
    position: int
    component_name: str
    statement: object


def restrict_ordered_claim_context(
    bridge: RegistryBridgeResult,
    *,
    target: object,
    ordered_claims: tuple[OrderedClaim, ...],
    reference_id: str,
    allowed_dependencies: dict[str, tuple[str, ...]],
) -> RegistryBridgeResult:
    """Restrict same-reference sources using explicit reviewed dependencies.

    The parent composite and the target itself cannot become GIVEN steps.
    Claims not present in the dependency policy are not automatically allowed.
    All unrelated references retain upstream citation-screening decisions.
    """
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    if not isinstance(ordered_claims, tuple) or not ordered_claims:
        raise ValueError("ordered_claims must be a nonempty tuple")
    if any(not isinstance(c, OrderedClaim) or type(c.position) is not int or c.position < 1
           or not c.component_name for c in ordered_claims):
        raise TypeError("ordered_claims must contain valid positive-position entries")
    if len({c.position for c in ordered_claims}) != len(ordered_claims):
        raise ValueError("duplicate claim position")
    if len({c.component_name for c in ordered_claims}) != len(ordered_claims):
        raise ValueError("duplicate component name")
    if not isinstance(allowed_dependencies, dict):
        raise TypeError("allowed_dependencies must be a dict")
    matches = tuple(c for c in ordered_claims if type(c.statement) is type(target)
                    and c.statement == target)
    if len(matches) != 1:
        raise ValueError("target must match exactly one registered claim")
    current = matches[0]
    by_name = {c.component_name: c for c in ordered_claims}
    permitted_names = allowed_dependencies.get(current.component_name, ())
    if not isinstance(permitted_names, tuple):
        raise TypeError("dependency names must be a tuple")
    if any(name not in by_name or name == current.component_name for name in permitted_names):
        raise ValueError("invalid proof dependency")
    eligible = {name: by_name[name].statement for name in permitted_names}
    retained = []
    for link in bridge.proof_links:
        assertion = bridge.registry.assertion(link.assertion_id)
        if assertion.reference_id != reference_id:
            retained.append(link)
            continue
        # A complete compound GIVEN, including a later clause, bypasses the
        # dependency policy and is therefore rejected unconditionally.
        if ":component:" not in assertion.assertion_id:
            continue
        name = assertion.assertion_id.rsplit(":component:", 1)[-1]
        if name not in eligible or assertion.content != eligible[name]:
            continue
        step = link.step
        if step is None or step.rule is not ProofRule.GIVEN or step.premises:
            continue
        if type(step.conclusion) is not type(assertion.content) or step.conclusion != assertion.content:
            continue
        retained.append(link)
    return RegistryBridgeResult(bridge.registry, bridge.records, tuple(retained))


def restrict_registered_ordered_claims(
    bridge: RegistryBridgeResult, target: object,
) -> RegistryBridgeResult:
    """Apply proof-order prefix restrictions to registered Proposition 5.1 claims.

    Printed positions remain unchanged; proof order is Hopf, pi3, delta, pi4, higher.
    The source composite is never admitted as a proof leaf.
    """
    from phase165_prop51_claim_order import proof_ordered_prop51_items

    parents = tuple(
        a for a in bridge.registry._assertions.values()
        if a.assertion_id.endswith(":toda:adopted:prop5.1:finite_dimensional")
    )
    if not parents:
        return bridge
    if len(parents) != 1:
        raise ValueError("ambiguous registered Proposition 5.1 parent")
    parent = parents[0]
    proof_items = proof_ordered_prop51_items(parent.content)
    claims = tuple(OrderedClaim(index, item.component_key, item.statement)
                   for index, item in enumerate(proof_items, start=1))
    # Earlier proof-use positions, not original publication positions.
    reviewed = {item.component_key: tuple(earlier.component_key for earlier in proof_items[:index])
                for index, item in enumerate(proof_items)}
    identified = tuple(c for c in claims if c.component_name in reviewed
                       and type(c.statement) is type(target)
                       and c.statement == target)
    if not identified:
        # The target's canonical generator may not match the translated
        # literature notation. A unique typed group and group-structure
        # family match may identify the same proof target; no fact is proved.
        identified = tuple(c for c in claims if c.component_name in reviewed
                           and getattr(c.statement, "lhs", object()) == getattr(target, "lhs", None)
                           and type(getattr(c.statement, "rhs", None))
                           is type(getattr(target, "rhs", None)))
    if not identified:
        return bridge
    if len(identified) != 1:
        raise ValueError("ambiguous adopted Proposition 5.1 target")
    chosen = identified[0]
    concrete_claims = tuple(
        OrderedClaim(c.position, c.component_name,
                     target if c.component_name == chosen.component_name else c.statement)
        for c in claims
    )
    return restrict_ordered_claim_context(
        bridge, target=target, ordered_claims=concrete_claims,
        reference_id=parent.reference_id, allowed_dependencies=reviewed,
    )
