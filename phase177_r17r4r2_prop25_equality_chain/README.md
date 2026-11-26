# Phase 177 R17R4R2 — Prop 2.5 equality chain compression

Presentation only. Preserve the actual typed inference graph, all citations and the existing R17R4R1 suspension elision. Compress a cited unsigned Proposition 2.5 equality followed by a verified, uncited composition-associativity equality and transitivity. Do not compress shared intermediate steps or protected projections. No generator names or dimensions are hardcoded in the projection.

Reviewed develop HEAD: `954e28b2aba788d7b1e66c8ce1d709458ab3fe3e`.

The installer updates the common renderer and adapts one R17R4R1 display assertion (the underlying suspension test is retained). Dry-run checks the exact baseline and exports the full proposed renderer and full proposed regression-test module to `%LOCALAPPDATA%/EHPProofTracerAudit/phase177_r17r4r2_prop25_equality_chain/`. It does not edit tracked files. Run the focused suite after installation; no full pytest or Git commits are performed.

Expected public proof: 43 typed steps, 8 references, one cited final Delta equation instead of three displayed equations. The package is syntax-checked, but repository-dependent tests must run in the user's checkout.
