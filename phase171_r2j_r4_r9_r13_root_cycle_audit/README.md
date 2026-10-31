# Phase 171 R2J-R4-R9-R13: Public Root Search Recursion Audit

This is a read-only audit of equality-symmetry dependencies in the real public proof search for `pi_6^3`.

The R12 audit established that both orientations of the first unresolved equality are individually reconstructible, while the complete public root search is still partial. R13 observes the canonical recursive searcher's *active* and *solved* goals at the moment the equality goals are expanded. It distinguishes an active forward-goal cycle from missing routes, ambiguity, and unrelated root failures.

The package uses the R12 audit's reviewed baseline check and must be unpacked alongside the existing R12 package. The real `shared_expansion_provider` function is temporarily wrapped in-process during one ordinary public search. The wrapper returns every proposal without reordering or mutation and is restored even if the search raises an error.

**No repository source file is modified. No new GIVEN or inference rule is added. No completed proof tree is reused.** The audit JSON alone is written under this package's `output` directory.

## Windows PowerShell

From the repository root, after extracting the ZIP there:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r13_root_cycle_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r13_root_cycle_audit\run.ps1"
```

The targeted pytest uses `-p no:cacheprovider` to avoid updating `.pytest_cache/v/cache/nodeids`. Existing changes to that tracked file from earlier runs are not touched.

## Result classification

`REVERSE_SYMMETRY_CYCLE_WITH_ACTIVE_FORWARD` means the forward equality is already active in the canonical resolver when it is requested as the only premise of the inverse equality. `MULTIPLE_REVERSE_ROUTES_REQUIRE_AMBIGUITY_AUDIT` means competing inverse proposals were observed. Other classifications are recorded literally; no classification alone establishes a complete proof.

The next change, if any, must be justified by the JSON trace and a separate minimal patch. Do not treat a `partial` result as a completed Web proof.
