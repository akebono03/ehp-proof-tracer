Phase 144-6-R5-23-R1 audit import repair.

Observed failure:
the active checkout was under C:\Users\oomae\..., while Python resolved
package-style tests.* imports through another checkout under C:\Users\user\....

This repair changes audit files only. It replaces:
  from tests.test_phase144_6_r5_18_production_generic_proof_chain_foundation import (
with:
  from test_phase144_6_r5_18_production_generic_proof_chain_foundation import (

The runner places the current repository root and its tests directory on
PYTHONPATH. Production code, Narrative behavior, ProofChain behavior, tests,
and the Phase 23 audit logic are unchanged.
