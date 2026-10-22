# Phase 168 R2-8(9): Live Renderer Reference Trace

Read-only instrumentation of the existing shared narrative Renderer for the `pi_4^2` proof. Uses `sys.setprofile` to observe returns from selected reference-selection functions and the actual local values of `generic_used_step_ids` where available. No project source file or test is patched.

From the project repository root, extract the ZIP into the current directory and run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase168_r2_8_9_renderer_runtime_trace\run.ps1"
```

The focused pytest runs before the live trace. Open `phase168_r2_8_9_renderer_runtime_trace/output/renderer_runtime_trace.json` to inspect the chronological events. If a selected function did not execute, no event is reported for it. The JSON records process-local Python object IDs, which should only be compared within one run.
