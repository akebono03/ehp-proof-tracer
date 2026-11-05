# EHP Proof Tracer — Phase 174 R1 Read-only Audit

This package examines the existing public typed proof search for
`pi_8^5`, `pi_12^4`, and `pi_13^4` against a reviewed GitHub `develop`
commit. It records complete, unmodified typed open goals, candidate sources,
observed proof steps, diagnostics, non-certifying source-screened root
rule proposals, and any separately certified abstract structure.

No production code, repository tests, mathematical relations, source
assertions, or documentation are modified. An audit result is never
considered a proof. Reports are saved outside the repository under
`%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r1\audit.json`.

The runner checks the live remote branch with `git ls-remote` and requires
the local `develop` HEAD to match the reviewed commit. It never performs a
fetch, pull, checkout, reset, clean, commit, or push.

## Run

From the repository root, extract the ZIP and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r1_goal_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r1_goal_audit\run.ps1"
```

Only targeted pytest files are executed; the complete suite is reserved for
the end of Phase 174.

If the remote or local HEAD differs from the reviewed commit, the script
stops without attempting to synchronize the repository. Reinspect GitHub
and local changes before creating a new reviewed audit.
