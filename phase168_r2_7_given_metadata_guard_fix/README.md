# Phase 168 R2-7: Metadata GIVEN Guard (Windows Patch Fix)

This package applies the narrow Phase 168 R2-7 guard in `phase165_r52_r16_web_citation_gate.py`.

The original package searched for a fixed multi-line string and could reject Windows CRLF source files with `GUARD_MISMATCH`. This replacement locates the intended AST condition and preserves source line endings. It never applies a patch when the expected AST condition is missing or altered. A backup is saved before modifications.

The change prevents `TodaFixedStatementComponent` metadata from becoming a `GIVEN` proof leaf. It preserves automatic `ProofStepLink` generation, publication ordering, typed mathematical statements, and earlier components of the same proposition.

From the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase168_r2_7_given_metadata_guard_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r2_7_given_metadata_guard_fix\run.ps1"
```

Tests are scoped to the patch application, new R2-7 regression cases, and the existing Phase 167 duplicate-GIVEN tests. The full test suite is reserved for the end of Phase 168.
