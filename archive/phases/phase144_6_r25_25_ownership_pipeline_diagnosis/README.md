# Phase 144-6 R25-25 Ownership Pipeline Diagnosis

## Purpose

R25-24 tested the hypothesis that recursive traversal beyond an EXACTNESS block
caused the excessive Narrative evidence population. The focused test showed no
strict evidence reduction across the six representative groups, so that
hypothesis is rejected.

This package first rolls back the R25-24 production experiment, then diagnoses
the actual ownership/rendering pipeline.

## Production state

After the rollback, production behavior is restored to the R25-23 baseline.

No new production behavior is introduced.

## Diagnostic pipeline

For each representative group the audit measures:

1. presentation node count;
2. total block and EXACTNESS-block count;
3. exactness display-contribution count;
4. per-argument local-body and method-evidence counts;
5. exactness method components;
6. selected primary component;
7. ordered proof-chain contributions;
8. base multi-argument Markdown size;
9. final contribution-rendered Markdown size;
10. insertion delta between base and final Markdown.

The six groups are:

- `pi_6^3`
- `pi_8^5`
- `pi_10^4`
- `pi_12^5`
- `pi_15^8`
- `pi_16^9`

## Phase boundary

Do not make another ownership/suppression change until this audit identifies
which stage actually expands the visible Narrative.

Repository-wide pytest remains deferred until the end of Phase 144-6.
