# Phase 171 R2J-R4-R4 — R1 Namespace-Qualified Citation Lookup Repair

This package repairs a read-only audit failure in R2J-R4-R4. The original focused
pytest suite passed, but the actual proof replay stopped at `screened_source_link`
because the merged bridge prefixes an assertion ID with `shared:<index>:`.
The previously registered Toda (5.3) Hopf source uses the canonical suffix
`toda:adopted:eq5.3:nu_prime_hopf_relation`.

The repair allows either the exact canonical ID or a namespace-qualified ID
ending in `:` followed by that **entire** canonical ID. The existing checks
for a unique source, a linked `GIVEN` with no premises, exact typed statement
content, fixed statement origin, literature locator, and publication precedence
are unchanged. A real-context regression test now detects this integration failure.

## Mathematical target

Infer the surjectivity of `H: pi_6^3 -> pi_6^5` using the earlier cited
`H(nu') = eta_5` and the inferred specialization of Proposition 5.1,
`pi_6^5 = Z/2{eta_5}`. This audit does not establish the order or presentation
of `pi_6^3`, a short exact sequence, or any new `GIVEN`.

## Replacements in this archive

- `audit.py`: full `screened_source_link()` replacement; no import changes.
- `tests/test_audit.py`: full file replacement with two real-context regression
  tests and its complete import section; 12 focused tests total.
- `CODE_FULL_JA.md`, `README.md`, and `監査仕様.md`: complete refreshed documents.

The unchanged files `source.py`, `run.ps1`, and package initializers are included
for reproducible extraction. The production shared provider, existing production
tests, R4-R3 directory, and repository-level documents are untouched.

## Windows PowerShell

From the repository root, extract the ZIP to `.` with `Expand-Archive -Force`.
The replacement only overwrites files within the existing R4-R4 package.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r4_cited_hopf_surjectivity\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r4_cited_hopf_surjectivity\run.ps1"
```

The runner first executes the 12 focused tests, then replays the real typed
proof tree. The full pytest suite remains reserved for Phase 171 closeout.
The script cannot claim `INFERRED` unless the actual replay passes.
