Phase 144-6-R5-32
visible contribution assembly / dedup audit

Production changes: none.

Purpose:
Compare current non-exact block-level assembly dedup with a hypothetical
visible ProofStep identity-level dedup, while preserving the existing
Argument frontier.

The audit:
- follows actual Argument ordering/discourse and skips DETACHED Arguments;
- computes currently visible non-exact steps per Argument;
- simulates current block-level suppression;
- simulates identity-level step suppression;
- reports occurrences released by step-level dedup;
- traces the two pi_6^3 Hopf facts;
- leaves EXACTNESS on its existing contribution-key path.

Boundary:
- no renderer change;
- no body-renderer API change;
- no exactness dedup change;
- no ProofChain change;
- no membership rule;
- no public route change;
- no dedicated pi_6^3 renderer removal.
