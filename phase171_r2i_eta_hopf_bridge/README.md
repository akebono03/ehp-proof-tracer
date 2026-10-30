# EHP Proof Tracer — Phase 171 R2I

This installation introduces a **typed, source-dependent Hopf-image proof chain** from the already reviewed Proposition 2.2 and Toda (5.3) to the consecutive eta Definition. It does not prove the group structure of `pi_6^3`.

The shared backward provider gets one small additive hook. The new module uses the existing general equality symmetry, left-composition congruence, EHP H congruence, and transitivity rules, and introduces one general adapter from a **proved** `GeneratorSuspension` to an element equality. Two consecutive concrete eta Definition instances are derived from the cited universal Definition rather than asserted as new source facts. The renderer's existing typed composition-power display interprets `eta_5 o eta_6` as `eta_5^2`; the display cannot generate a proof step.

Unzip the archive at the existing repository root on the `develop` branch. Run `run.ps1 -DryRun`, then `run.ps1`. No git checkout, reset, pull, or update occurs. The installer preserves newline style, checks the existing R2H hook, backs up the exact bytes before applying the minimal hook, and writes the complete changed shared function and all new source/test code to `output/CHANGED_CODE_FULL_JA.md`.

Focused tests only: the new R2I tests plus the original R2H citation/formula tests. Full-suite pytest is intentionally deferred to Phase closeout. The independent audit verifies three fixed-citation GIVEN leaves, the derived eta definitions and suspension, the Hopf-image result, and rejection of a completed-group claim.

This package requires the repository's existing Python dependencies and prior Phase 171 R2H installation. It does not change repository documentation, search goals, database entries, trust boundary, narrative, or renderer.
