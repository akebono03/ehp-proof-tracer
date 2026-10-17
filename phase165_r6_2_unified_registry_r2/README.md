# Phase 165 R6-2 Unified Registry R2

Read-only inventory of factories requiring one or more arguments in the nine R8 default rule modules. This package makes no production code changes and does not call factories or synthesize mathematical evidence.

From the repository root run:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase165_r6_2_unified_registry_r2\run.ps1
```

Output: `phase165_r6_2_unified_registry_r2/reports/required_argument_rules.json` and `required_argument_rules.md`.

## Scope and status

Every identified parameter is classified by name, syntactic kind, and source annotation. Trusted value sources and applicability remain unverified until explicit review. The existing R1 `extra_rules` mechanism is the supported manual registration entry point; R2 does not populate it automatically. No full pytest run is performed.
