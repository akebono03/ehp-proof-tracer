# Phase 173 R4-R15R16: Verified Progress and Shared Punctuation

This patch adds source-backed intermediate progress to abstract-only partial proof narratives, using the existing certified four-premise inference tree. It also makes public prose use ASCII commas and periods, with line breaks at sentence-final periods while protecting mathematical expressions and numbered citation locators.

No proof search, registration, group status, named-generator inference, or citation ownership is changed. Markdown compatibility is preserved by keeping sentence normalization in the common Web presentation layer. The abstract progress section is shared by the model-backed and legacy paths.

## Run

From the repository root in Windows PowerShell, expand the ZIP and execute `phase173_r4_r15r16_verified_progress_punctuation/run.ps1 -DryRun`, then execute the same script without `-DryRun`. The installer checks current GitHub lineage and exact reviewed source blobs, and preserves local line endings.

Full-suite pytest is intentionally not run. Review `FULL_CHANGED_UNITS.md`, `SOURCE_CODE.md`, and `design.md` before applying.
