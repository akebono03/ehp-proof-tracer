# Phase 174 R3-R7-R16 — Public generic EHP zero-root connection

This narrowly scoped package connects the **existing** typed EHP zero-group backward rule to the shared public expansion provider. It does not introduce a new theorem, target-group GIVEN, special-case proof, or narrative renderer.

## Scope

- Modified production file: `phase165_r52_r9_shared_math.py`.
- Modified function: `shared_expansion_provider` (its nested `expand` function).
- New package: `phase174_r3_r7_r16_public_ehp_zero_root/`, containing a guarded patch, read-only source and proof audits, focused tests, and a PowerShell entry point.
- Original API and first-success proof search remain unchanged.

The single generic expansion has **four unproved child goals**: Delta surjectivity, Delta–E exactness, E–H exactness, and the terminal zero group. The proposal is *not* a verified ProofStep or a completed proof of `pi_12^7=0`.

## Windows execution

Unpack the ZIP directly into the existing repository root. Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r16_public_ehp_zero_root\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r16_public_ehp_zero_root\run.ps1"
```

The script fetches the remote branch without pulling, resetting, checking out, or stashing. It accepts only the two reviewed local HEAD layouts (`380a5b1741...` or `e7bcd34a52...`), pins the R15 merged remote HEAD, checks exact Git blobs, and rejects unrelated tracked edits or staged changes. It requires the completed R15 audit JSON in `%LOCALAPPDATA%/EHPProofTracerAudit/phase174_r3_r7_r15/`.

The DryRun emits `MODIFIED_FUNCTION_FULL_JA.md` with the **entire resulting `shared_expansion_provider` function**, including its nested `expand`. It does not write to tracked production files. The normal run makes the single guarded source change, tests the public provider and standard search, and writes an audit report to `%LOCALAPPDATA%/EHPProofTracerAudit/phase174_r3_r7_r16/`. On failure after patching, the script restores the exact backed-up source.

Focused pytest only; the full suite is deliberately not run until phase closeout.

## Expected gate

`PASS_PUBLIC_GENERIC_EHP_ROOT_PREMISES_OPEN`

This gate asserts that the root has exactly one new typed **candidate** with four independent premises, while the final target remains unresolved. It does not assert that all four premises are solvable, or that the browser renderer displays all proposed branches.
