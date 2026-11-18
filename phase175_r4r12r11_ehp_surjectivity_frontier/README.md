# Phase 175 R4R12R11 — Read-only EHP surjectivity frontier audit

This package inspects shared, typed, backward-search candidates for the rank-two EHP quotient rule. It is explicitly **not** a proof of the target group and does not register new source statements or modify production Python code.

The published equation (5.11) is reused as registered by R10R1. The audit identifies the six prerequisite goals for each orientation and highlights the invalid `pi_9(S^9)=0` subgoal that may be proposed by the existing zero-codomain surjectivity shortcut. That shortcut remains mathematically valid when its premise is true; the audit never asserts the premise for the diagonal sphere group.

Unzip into the repository root on the `develop` branch and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r11_ehp_surjectivity_frontier\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r11_ehp_surjectivity_frontier\run.ps1
```

Focused tests only. Reports are saved under this package's `output` directory. No full pytest is run. The `production_dirty` field is reported but changes are never applied. The accepted Git HEAD is not pinned, since this audit makes no modification; branch and root are checked.
