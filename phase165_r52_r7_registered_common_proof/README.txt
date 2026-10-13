Phase 165 R52-R7: typed registered proof dispatch (incremental commonization).

Changed production files:
- phase164_r5_r2_common_replay.py: full replacement function and imports.
- phase165_r52_r7_registered_common_proof.py: new provider dataclass,
  registration function and generic proof adapter.
- test_phase165_r52_r7_registered_common_proof.py: six targeted tests.

Existing pi3^2 typed-reference backward proof is regenerated at runtime.
The generic dispatch does not special-case n/k. Other target groups remain
unresolved until typed goal, leaf Reference and expansion provider are registered.
No legacy proof fallback. No changes to templates or mathematical rule definitions.
Only targeted pytest; full pytest deferred until end of Phase.
