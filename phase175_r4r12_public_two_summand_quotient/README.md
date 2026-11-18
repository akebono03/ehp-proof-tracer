# Phase 175 R4R12 — Public Generic EHP Two-Summand Quotient Candidate

This package connects the existing, independently audited R4R3 EHP rank-two quotient inference to the common backward proof search. It does not introduce any new mathematics or literature GIVEN, and it does not complete the proof of `π_9^5`.

The provider reads two exact, earlier database **goal candidates**, not proof certificates, and proposes both possible images of the Delta generator. The existing inference rule requires six independently proved premises: the two source-group presentations, Delta generator image, EHP exactness, E surjectivity, and E generator image. The ordinary proof resolver must authenticate and prove these before producing any conclusion.

## Installation

Unzip this archive into the root of `akebono03/ehp-proof-tracer` on branch `develop`. The reviewed baseline Git HEAD is `abf619040d52aa9fd61c5bca60db81e28912e24d`, with the R4R11R2 patch installed but uncommitted. A successful R4R11 full audit report is required.

From PowerShell, run `phase175_r4r12_public_two_summand_quotient/run.ps1 -DryRun -R4R11Report <path>`, inspect the report and the generated full replacement, and run again without `-DryRun`. The installer modifies only `shared_expansion_provider()` in `phase165_r52_r9_shared_math.py`.

Only focused tests are run. Run the entire test suite only when Phase 175 closes.

Expected final gate: `PASS_R4R12_TWO_SUMMAND_QUOTIENT_ROOT_CANDIDATE_PI95_PENDING`.
