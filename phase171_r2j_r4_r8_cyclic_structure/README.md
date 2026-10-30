# EHP Proof Tracer — Phase 171 R2J-R4-R8

This is a read-only typed proof replay for the registered group presentation
`pi_6^3 = Z/4{nu-prime}`. It uses a cardinality-four proof and the separately
inferred order-four element of R4-R7. The general theorem is that an element
whose order equals the cardinality of a finite group generates that group.

The requested database group is a **goal**, never a GIVEN or an independently
proved source. Distinct typed spellings of nu-prime must match through the
existing HyoujiGen identity resolver. A matching identifier alone never
proves the order of a generator.

No production files, existing tests, existing project documents, registered
proof sources or public providers are modified. This package reports a local
inference tree only; public proof-search and web rendering integration are
explicitly deferred. No full-suite pytest is executed.

From the repository root, extract the archive to `.` and execute:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r8_cyclic_structure\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r8_cyclic_structure\run.ps1"
git status -sb
git diff --stat
```

The focused pytest suite covers 12 new tests and 12 R4-R7 tests. Success
requires a real inference root with two inferred parent proofs, all cited
GIVEN leaves screened before the pi_6^3 goal, and zero newly created GIVENs.
The output report is `output/audit.json` inside this package.
