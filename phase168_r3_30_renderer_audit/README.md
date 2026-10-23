# Phase 168 R3-30: Renderer architecture audit

This is a **read-only audit**, not a patch. It inspects the installed working-tree sources, lists the narrative projection components, checks that the public renderer calls each projection, looks for direct legacy-renderer imports and documents scope limitations. It writes its output under `phase168_r3_30_renderer_audit/output/`.

Run in Windows PowerShell after unpacking into the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_30_renderer_audit\run.ps1"
```

The audit tests exercise only the audit itself; full pytest remains deferred until the end of Phase 168. Structural static analysis does not establish the runtime web route or proof correctness. These should be checked in a separate, targeted dynamic audit if needed.

No existing source, API, imports or tests are changed.
