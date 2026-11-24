# Phase 176 R3R40 — Toda (5.5) connection audit

Baseline: `develop`, commit `e962074129ced65b00a0ee184d8ed0e6ae22e912`.
This package adds an audit-only caller-supplied expansion provider. It does not
modify existing production code, register GIVENs, or create mathematical rules.

The existing R3R28 quadruple relation uses the same right-associated typed
composition as the R3R39 Hopf transport. The audit requires exact expression
equality and reconstructs the two existing equality steps through the canonical
DFS using a screened context for the registered group goal. Both independent
premises must be proved by the existing shared providers. The audit also checks
whether the registered generator uses the exact same expression representation;
a mismatch is reported, never silently normalized.

Run from the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r40_toda55_connection_audit\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r40_toda55_connection_audit\run.ps1
```

The full test suite is not run. The final gate is
`PASS_R3R40_TODA55_CONNECTION_FOCUSED_TESTS`. The default shared provider and
registered group proof remain unchanged; a later phase may connect the audited
expansions publicly. See `CODE_FULL_JA.md` for complete new code.
