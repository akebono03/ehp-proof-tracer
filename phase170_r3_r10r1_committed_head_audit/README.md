# EHP Proof Tracer — Phase 170 R3-R10R1 (committed-HEAD fresh 33-stem audit)

This is an **audit-only** package. It does not modify production modules, mathematical proof rules, registries, source TeX, or existing tests. It does not run the full pytest suite.

## Why this revision exists

R3-R10 originally required Git `develop` at `fdf60522b6d477209e9d8d67720a63f9863e419c` with two tracked local modifications. The successful R3-R9 implementation was subsequently committed and merged. The current reviewed `develop` is `08382968b5359d6c956b48acec333f127014d4c8`, with **no tracked modifications**. The previous audit correctly refused an unreviewed state; it never started the 33-stem search.

R3-R10R1 changes only the audit's Git preflight expectations and adds corresponding focused negative tests. Both the prior verified source files and the newly committed Toda (5.2)/(7.12) files must have the exact reviewed Git blob IDs. The printed Toda (7.12) equality must match its unique literal `CLAUSE` in the committed Python module. The remote `origin/develop` must match the expected HEAD.

## Scope

The existing `phase170_r3_r8_n2_exhaustive_audit/audit.py --worker --k K` is executed separately for every `K=1,...,33`, with UTF-8 output. Its proof search and public Web trust boundary are unchanged. Every worker result must satisfy the typed goal, source order, completed search, zero open goals, proof steps, Web completion, and absence of Web errors.

## Run

Extract this ZIP to the repository root and run in PowerShell:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r10r1_committed_head_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r3_r10r1_committed_head_audit\run.ps1"
git status -sb
```

The launcher runs only focused contract tests, using `-p no:cacheprovider`. The full audit may execute 33 independent workers; each worker has a default 240-second timeout. Results and worker logs are written outside the repository to `%LOCALAPPDATA%\EHPProofTracerRecovery\phase170_r3_r10_n2_33_*`.

## Acceptance

The target result is:

```text
PHASE170_R3R10_DOMAIN_CHECKED=33
PHASE170_R3R10_DOMAIN_COMPLETE=33
PHASE170_R3R10_DOMAIN_GAPS=0
PHASE170_R3R10_TRACKED_UNCHANGED=True
PHASE170_R3R10_RESULT=DOMAIN_ALL_VERIFIED
```

Never infer completion from this document or from the previous successful `k=12` test: it must be observed from the new independent 33-stem run.
