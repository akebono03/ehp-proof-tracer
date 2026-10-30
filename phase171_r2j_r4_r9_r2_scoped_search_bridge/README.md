# EHP Proof Tracer — Phase 171 R2J-R4-R9-R2

This audit-only package tests whether the verified R4-R8 proof **rules and typed subgoals** can be independently reconstructed by the existing canonical backward-search engine and accepted by its public proof-trust boundary.

## Scope

- No existing production modules, shared providers, tests, or historical documentation are changed.
- No existing complete `ProofStep` is inserted into the search. The R4-R8 tree is only inspected to obtain a finite catalog of `GoalExpansion` obligations; canonical search must rebuild each inference and find each genuine earlier registered `GIVEN` leaf.
- The scoped provider is limited to this audit; the public Web route remains unchanged, even if the scoped search succeeds.
- Conflicting inference routes for the same typed conclusion are refused.
- This is not a general-purpose automatic discovery mechanism for other groups. A future implementation must expose the general inference rules through the ordinary shared provider without relying on a completed prior tree.

## Prerequisites

A `develop` checkout of `akebono03/ehp-proof-tracer` with the successful R4-R8 proof and its R4-R7 dependencies. The audit is reviewed against GitHub `develop` at `a19d5e0fac33a55689dcb62228b4fffbfb036b92`.

## Windows PowerShell

Unpack the ZIP in the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r2_scoped_search_bridge\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r2_scoped_search_bridge\run.ps1"
git status -sb
git diff --stat
```

The run executes only eight focused tests and writes `output/audit.json` in the new untracked package. A full repository pytest is deferred until phase closeout. The package never edits tracked files.

## Interpretation

- `SCOPED_SEARCH=complete` means the existing recursive search reconstructed the target under the temporary scoped expansion provider.
- `TRUST_VERIFIED=True` means the resulting complete tree also passed the existing narrative trust boundary.
- `PUBLIC_WEB_VERIFIED=False` is intentional. This package does **not** connect the public provider or certify Web completion.
- A partial or failed scoped search is a valid audit observation. Consult `scoped_open_goals` and `scoped_diagnostics` in `output/audit.json`; do not promote it to completion.
