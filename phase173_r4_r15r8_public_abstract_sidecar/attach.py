"""Attach a cited abstract certificate without promoting named group completion."""
from __future__ import annotations

from dataclasses import replace

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_partial_proof import (
    CertifiedAbstractStructure,
    GroupStructureStatus,
    PartialProofResult,
    ProofSearchStatus,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r7_source_first_abstract_certificate.search import (
    search_source_first_abstract,
)
from phase173_r4_r10_general_toda56_core.core import checked_abstract_inputs
from proof import ProofRule


def attach_certified_abstract_structure(
    result: PartialProofResult, *, n: int, k: int,
    goal: object, bridge: RegistryBridgeResult,
) -> PartialProofResult:
    """Attach *only* a separately replayed abstract proof to a named partial.

    No result status, named conclusion, open goal, named structure status, or
    registered source context is modified. The certificate's source context is
    internal to its proof construction. Missing evidence always returns the
    original result without granting any new proof claim.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("Expected a canonical partial proof result")
    if (type(n) is not int or type(k) is not int or n != 4 or k < 3
            or result.status not in (
                ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED,
            )
            or result.abstract_structure is not None
            or result.target.group_dimension != n + k
            or result.target.sphere_dimension != n
            or result.structure_status is GroupStructureStatus.KNOWN
            or not isinstance(bridge, RegistryBridgeResult)):
        return result
    target = exact_prior_database_result(n, k)
    if (target is None or type(target) is not type(goal) or target != goal
            or checked_abstract_inputs(target) is None):
        return result
    try:
        certificate = search_source_first_abstract(k=k, bridge=bridge)
    except (ValueError, LookupError):
        # An optional abstract sidecar must not break existing named queries
        # when an independently screened source is absent from a caller bridge.
        return result
    if certificate is None or certificate.proof_target != target:
        return result
    root = certificate.root_step
    if (certificate.public_group_complete is not False
            or root.rule is not ProofRule.INFERENCE
            or root.conclusion != certificate.conclusion
            or root.inference_rule is None
            or not root.inference_rule.match_guard(root.premises, ())):
        return result
    structural = CertifiedAbstractStructure(
        group=certificate.conclusion.group,
        invariant_summands=certificate.conclusion.invariant_summands,
        proof_step=root,
    )
    return replace(result, abstract_structure=structural)
