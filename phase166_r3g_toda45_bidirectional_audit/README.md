# Phase 166 R3-G — Toda (4.5) forward/backward audit

Read-only production-path audit. No production files are modified. Run from the repository root with `powershell -ExecutionPolicy Bypass -File .\phase166_r3g_toda45_bidirectional_audit\run.ps1`.

The audit distinguishes literature catalog registration, GIVEN proof links, exact `Toda45IsomorphismStatement` instances, and registered shared backward-expansion candidates for representative `(n,k)`. Standalone forward rule and backward rule tests in the repository are distinct from end-to-end registry connectivity.

This is not a claim that any code can test all infinitely many inputs. Full pytest is not run.
