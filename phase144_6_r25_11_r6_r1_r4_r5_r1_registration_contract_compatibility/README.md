# Phase 144-6 R4-R5-R1 Registration Contract Compatibility

R4-R5 focused tests produced 53 passes and one failure.

The failure is an audit-contract compatibility issue rather than a semantic
cleanup failure. R4-R3's test explicitly requires the source-level
initialization `$isRegistered = $false`. R4-R5 moved registration detection
into `Get-RegisteredAuditWorktreeState`, so the explicit initialization
disappeared even though the new logic still returns a boolean state.

This repair makes the smallest possible change:

```powershell
$isRegistered = $false
$isRegistered = Get-RegisteredAuditWorktreeState
```

No cleanup semantics change.

Preserved:
- idempotent registration recheck after failed Git removal;
- stale audit-path cleanup guard;
- scalar `git worktree prune` handling;
- collector native stderr handling;
- restored `Read-PopulationCache`;
- exact historical baseline target 190.

Unchanged:
- production code;
- existing project tests;
- existing historical audit tests;
- collector Python;
- population cache contents.

After focused tests pass, the runner resumes localization using the existing
cache. No full project pytest is run.
