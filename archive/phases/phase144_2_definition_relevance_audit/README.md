# Phase 144-2 Definition Relevance Audit

Audit only. No production code or tests are modified.

The pi_12^5 post-implementation audit shows:

- sigma triple-prime Definition is now a direct child of the target Argument;
- nu_n Definition remains a standalone main-discourse Definition.

It is not safe to detach every standalone Definition, because the pi_6^3 nu-prime Definition was historically standalone but mathematically relevant.

This audit compares the full block dependency closure of Arguments for:

- pi_6^3
- pi_12^5
- pi_16^9

It reports which Definition blocks occur in each Argument dependency closure. The goal is to find a generic relevance rule that keeps mathematically required standalone definitions while detaching unrelated definitions such as nu_n in pi_12^5.
