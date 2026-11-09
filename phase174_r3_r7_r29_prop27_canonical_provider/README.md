# Phase 174 R3-R7-R29: Canonical Proposition 2.7 Provider

This package connects the reviewed Toda Proposition 2.7 universal literature statement to the **existing canonical backward search API** through a newly registered, opt-in expansion provider. The source is independently checked in R28. The only GIVEN is the *universal literature theorem*, not an instance at n=6.

The integration produces `GoalExpansion` candidates for the general schema and each correctly typed, even-dimensional specialization, then delegates proof verification to `reconstruct_registered_goal`. It does **not** modify the default Web path or register global rules. The objective `pi_12^7=0` remains incomplete.

## Usage

Extract the archive at the EHP Proof Tracer repository root and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r29_prop27_canonical_provider\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r29_prop27_canonical_provider\run.ps1'
```

Only the named focused pytest files are executed. The full test suite is deferred until Phase closeout.
