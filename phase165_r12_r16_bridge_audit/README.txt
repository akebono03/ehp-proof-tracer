Phase 165 R12-R16: generic proof-premise bridge (partial integration)

This package adds two general typed inference bridges, not a pi43-specific adapter:
  certified MapSurjective -> SurjectiveMapStatement
  certified SuspensionKernelFreeCyclicStatement -> KernelMultipleStatement
No source proof or mathematical axiom is synthesized.

It then reconstructs both derivations from R12-R14 and R12-R15 proof steps.
The proof of pi43 remains OPEN unless the homomorphism presentation,
source group structure, generator image, quotient proof, and final relation
have all been independently established. The audit explicitly reports this.

Run run.ps1 from the project root. Only targeted pytest, no full pytest.
