# Phase 169 R10ET-R5: Production Common Definition Preference

This package makes the verified universal stable-element Definition the first backward-search option **only for an eligible, typed `GeneratorImage`**. An ineligible goal continues through the unchanged legacy expansion providers. It also updates four existing regression-test files whose expectations referred to the former, citation-heavy proof path.

## Requirements

- Windows PowerShell and Python with the existing project's pytest dependencies.
- `develop`, with the reviewed R10ET-R4 implementation present as the only two preexisting tracked modifications.
- An ancestor commit of `5a8ad4a56c5407c0fbe15ba14516a1c1a99f0562`. Any commits since that revision must modify only `phase169_r10et_*` paths. All five changed files must match their verified Git blob hashes.
- The reviewed R10ET-R2 shadow result must exist in the repository.

## Run

Extract the ZIP at the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase169_r10et_r5_common_definition_provider\run.ps1
git status -sb
```

The script validates the existing R4 byte-for-byte against its reviewed patch, validates the five R5 targets, exports the full replacement files and full changed functions, applies the changes, runs focused pytest only, and finally audits 16 completed trusted proofs with the real production provider (no shadow monkeypatch). It restores **only R5's five modifications** on failure and leaves the prior R4 changes intact.

The output folder contains `audit.json`, `audit.md`, `narratives`, and `full_sources/` with every replacement file and full changed function. It does not edit the main README or docs.

## Scope

Production: `phase165_r52_r9_shared_math.py::shared_expansion_provider` only. Existing regression tests: R10A, R10EC, R10EL, and R10ER. No new source statement, DB fact, theorem, trust bypass, or notation-family special case. The full pytest suite is deferred to Phase closeout.
