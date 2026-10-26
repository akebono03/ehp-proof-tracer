# Phase 169 R3D — EHP Isomorphism Dependency Audit

This is an **AUDIT_ONLY** package for the current EHP Proof Tracer `develop` branch.
It does not modify production Python files, existing tests, or the five project documents.

It observes the live `pi_4^2` and `pi_5^3` searches with their real screened citation context, compares the **existing shared expansion provider** with the historical Phase 161 EHP goal-expansion contracts, and records the type and provenance obligations at both literature-terminal goals.

The report is written to `output/ehp_iso_dependency.json`. A candidate expansion **is not a proof**, and neither a published group assertion nor a hypothetical historical branch is automatically a certified EHP isomorphism. It is intentional that R3D does not complete `pi_5^3`.

The current HEAD is recorded, not guessed; unexpected statuses are included in the report rather than papered over with fabricated GIVEN proof steps.

## Windows PowerShell

From the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r3d_ehp_iso_dependencies.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3d_ehp_iso_dependencies\run.ps1"
```

The focused tests do not invoke the complete test suite. The next implementation step must preserve publication order and substantiate each leaf before connecting or generalizing an EHP rule.
