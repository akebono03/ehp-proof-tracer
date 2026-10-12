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
