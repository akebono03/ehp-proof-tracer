Phase 161 R7 — Premise Provenance Validation

Install by running run_phase161_r7_premise_provenance_validation.ps1 from repository root.
R5 remains unchanged; the R7 entry point validates input ancestry and final ancestry.
Trusted GIVEN roots are provided explicitly as a tuple of the same ProofStep objects.
The tests use GIVEN roots collected from the existing Phase 59 fixture. This proves
consistency relative to the chosen trust boundary, NOT external mathematical truth.
R6's intentionally permissive diagnostic remains intact as a regression baseline.
Full test suite is NOT run at this intermediate phase stage.
