# Phase 173 R4-R1: Source-Bound Toda (5.6) Proof Candidate

This package provides a bounded, typed backward proof proposal for the
pi_7(S^4) direct-sum presentation. It does **not** mutate the production
provider or any existing tracked source file.

The rule requires an independently screened Toda Proposition 4.4 universal
reference, a publication-eligible prior pi_6(S^3) presentation, a proven
pi_7(S^7) diagonal presentation, and an independently derived Hopf-invariant
relation H(nu_4) = iota_7. In particular, a database goal or a literal
source string never counts as a proof step.

Run `run.ps1 -DryRun` before `run.ps1`. The standard shared backward search
is run with the new provider injected for this isolated process only. A new
root proposal does not constitute a completed proof. Inspect the reported
search status and open goals before considering production integration.

Only focused tests are run. No whole-suite pytest is executed.
