# Phase 166 R3: Ordered Lookup Boundary

This package changes only the explicitly selected `typed_reference_ordered` lookup path. It removes independent-review eligibility checks from that path, while keeping strict prior-order checking and requiring an existing, type-correct linked GIVEN proof step. It does not modify the default Web search path, invent literature positions, write to `sphere.db`, or implement the future database-backed Goal Builder.

## Install on Windows

Extract this archive in the project root, then run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase166_r3_ordered_lookup\run.ps1"
```

This saves the original production module before replacing it and runs only focused pytest. Backups are stored outside the package in `phase166_r3_ordered_lookup_backups`. Full pytest belongs at the end of Phase 166. Existing Web pi_3^2 must be rechecked separately.
