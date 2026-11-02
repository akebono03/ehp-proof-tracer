# Phase 173 R4-R4 — Typed Toda (5.6) Generator-Image Audit

This package is read-only. It does not change production code, the registered database, proof records, citations, or the Web renderer.

## Reviewed baseline

- Branch: `develop`
- HEAD: `cd93bac8a2e4c08742f7eabc0ba97fda294d20b6`
- Prerequisite folder: `phase173_r4_r3_premise_frontier_audit` (tracked in the reviewed `develop` tree).

## Scope

Inspect the precise typed presentation images for the Toda Proposition 4.4 map

`(alpha, beta) -> E(alpha) + nu_4 composed with beta`

at dimensions 7–10. The existing dimension-7 proof is a protected regression baseline; only 8–10 receive new symbolic shape checks. Explicit source/target type checks and exact generator expressions are required. Generic textual aliases, abstract group matches, and stored database results are not accepted as proof.

The audit also checks whether the separately source-verified Toda Lemma 5.4 can be placed before each citing goal. A positive symbolic match is **not** a verified generator image, a new inference rule, or a completed proof.

## Run

From the repository root after extracting the ZIP:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r4_typed_generator_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r4_typed_generator_audit\run.ps1"
```

Find `audit.json` and `audit.md` under the printed `PHASE173_R4_R4_OUTPUT` directory. Send the PowerShell output and `audit.json` back for the next minimal implementation phase. Only focused pytest tests and the existing pi_7^4 public-proof regression verifier run; full-suite pytest is deferred to Phase 173 closeout.
