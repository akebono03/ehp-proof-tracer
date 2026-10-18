# Renderer Restore R1 Test Fix

Only update the targeted test invocation to use the current shared-components module. The previously restored completed adapter is retained. No search logic or renderer implementation is changed. The retired `toda_group_proof_generic_narrative_renderer` import in historical R56 tests is not revived. Run `run.ps1`; this executes only four targeted tests.
