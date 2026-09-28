from proof_repository import (
  ProofRepository,
)
from standard_repository import (
  build_standard_proof_repository,
)
from toda_prop515_upper_bootstrap import (
  build_toda_prop515_upper_bootstrap,
)


def build_standard_production_proof_repository(
) -> ProofRepository:
  upper_result = (
    build_toda_prop515_upper_bootstrap()
  )

  low_result = (
    upper_result
    .sigma_chain_result
    .low_result
  )

  return build_standard_proof_repository(
    low_result.prop56_step,
    low_result.prop58_step,
    low_result.prop511_step,
    upper_result.aggregate_step,
  )
