# EHP Proof Tracer — Phase 174 R3-R7-R43R2

This package repairs the overly broad clean-worktree check in the **R43R1 installer**. It does not relax evidence requirements or modify a production module.

The new check accepts either a clean tracked working tree or **exactly** the already-reviewed R43 provider insertion into `phase165_r52_r9_shared_math.py`. Every staged change, unrelated tracked edit, or altered provider insertion remains a hard failure. It prints unreviewed tracked paths and performs no reset, checkout, or clean operation.

`run.ps1 -DryRun` validates without changing any files. `run.ps1` updates only the prior R43R1 `install.py`, runs its focused tests, and invokes the original R43R1 runner, which executes R43's guarded installation, public audit and focused pytest.

The original R43 source SHA correction remains exactly as authored. No group-specific proof, source GIVEN, mathematical rule, or renderer is added. An R43 provider-wiring PASS is not a completed proof of the root zero group.

Use PowerShell from the repository root after extracting this archive at that root. Do not run full pytest until the phase closes.
