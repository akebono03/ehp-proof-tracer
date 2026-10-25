# Phase 169 R1 — Two-stem live baseline audit

Status: AUDIT ONLY; no production code, test, or documentation file is patched.

Purpose: inspect the live typed backward search for π₄² and π₅³ and compare
the resulting completion status with the standard Web route. Collect the
candidate typed goals, every observed ProofStep and its premises, open goals,
diagnostics, and a publication-order diagnostic for completed proofs.

Verified GitHub basis before packaging:
- `develop`: `d24d909c3c19ec731bdf4fca90aa682dfc1555ed`
- Phase 168 closure text is present in `README.md`, `docs/design.md`,
  and `docs/roadmap.md`.
- This audit does not assert that the Windows local checkout is synchronized.

Files added on extraction:
- `phase169_r1_two_stem_baseline_audit/audit.py`: audit functions
  `describe_step`, `audit_publication_order`, `audit_group`,
  `render_report`, and `main`. These belong only to this audit package.
- `phase169_r1_two_stem_baseline_audit/run.ps1`: Git state, audit,
  and focused pytest runner.
- this README.

No application classes, functions, imports, tests, or docs are modified.

Run in PowerShell at repository root:

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive `
  -Path "$HOME\Downloads\phase169_r1_two_stem_baseline_audit.zip" `
  -DestinationPath "." `
  -Force
powershell -ExecutionPolicy Bypass `
  -File ".\phase169_r1_two_stem_baseline_audit\run.ps1"
```

Reports:
- `output/git_state.txt`: local status, HEAD, fetched origin/develop,
  ahead/behind counts (the script runs `git fetch`, which updates refs
  but does not update checked-out working files).
- `output/two_stem_baseline.txt`: human-readable target-by-target account.
- `output/two_stem_baseline.json`: searchable detailed proof-step audit.
- `output/bridge_error.txt`, only if bridge construction fails.

Five relevant existing test modules are executed with focused pytest.
The whole test suite is NOT run.

Completion criterion for R1: actual search status, ProofStep provenance,
unresolved goals, and Web status have been recorded without modifying the
application. Phase 169 final completion is NOT implied. Subsequent R2
implementation is to be chosen only after reviewing the observed gaps.

Scope boundary: No old replay/adapter, no per-group Narrative, no
assumed completion, no trust-boundary redesign, no all-stem changes.
