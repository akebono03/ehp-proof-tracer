# Phase 155-R3-3A — removable duplicate graph and canonical survivor audit

## Input

- Git HEAD: `a0c16da9163df6a6f2be25e3de01fa7d88e191ae`
- Verified candidate pairs: 332
- Removable duplicate pairs: 164
- Retain-independent pairs: 125
- Historical-keep pairs: 43
- Needs-review pairs: 0

## Graph result

- Removable connected components: 64
- Unique tests in removable graph: 227
- Unique deletion candidates: 161
- Survivor/protected tests: 66
- Components containing directed cycles: 0
- Components needing manual review: 0

## Safety rule

An older-side test becomes a deletion candidate only when it can reach a protected or natural newer-side survivor through one or more R3-2F-r1 `deletion_authorized=true` edges.

Tests participating in `historical_keep` pairs are protected from deletion.

R3-3A performs no deletion. File-level helper/import dependencies must still be audited before R3-3B changes existing test files.

Repository-wide pytest remains deferred until Phase 155 closure.
