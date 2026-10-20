"""Publication order for explicitly identified typed citing assertions.

Only existing source positions and component positions are compared. This
module neither certifies source text nor invents a mathematical ProofStep.
"""
from phase163_r4_registry_bridge import RegistryBridgeResult
from unified_statement_registry import AssertionOrigin


def precedes_citing_assertion(bridge: RegistryBridgeResult, cited_id: str, citing_id: str) -> bool:
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    cited = bridge.registry.assertion(cited_id)
    citing = bridge.registry.assertion(citing_id)
    if cited.origin is not AssertionOrigin.FIXED_STATEMENT or cited_id == citing_id:
        return False
    if citing_id in cited.dependencies:
        return False
    if cited.reference_id == citing.reference_id:
        return (cited.component_position is not None
                and citing.component_position is not None
                and cited.component_position < citing.component_position)
    source = bridge.registry.reference(cited.reference_id)
    destination = bridge.registry.reference(citing.reference_id)
    return (source.publication_position is not None
            and destination.publication_position is not None
            and source.publication_position < destination.publication_position)
