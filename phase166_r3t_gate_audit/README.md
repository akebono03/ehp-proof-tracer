# Phase 166 R3-T Gate Audit

Read-only diagnosis of the existing Toda (4.5) finite-cyclic transport path for pi_5^4.

## Scope
This package adds audit.py and three focused tests. It does not modify production modules or theorem registrations. It inspects the literal target, source, order, and generator conditions already used by the production backward rule. A compatible base conclusion must be a screened, proven premise before a production fix can rely on it.

## Run
From the project root, execute `powershell -ExecutionPolicy Bypass -File .\phase166_r3t_gate_audit\run.ps1`.

## Success criteria
Three focused tests pass and a JSON report is generated. The package does not claim to complete the pi_5^4 proof; the report is required to decide the minimal production correction.

## Next phase boundary
Only after identifying the failed gate, repair a shared inference/expansion connection. Do not add a pi_5^4-specific rule or new renderer. Do not run the full test suite until phase closure.
