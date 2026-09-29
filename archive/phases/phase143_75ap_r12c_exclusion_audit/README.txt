Phase 143-75AP R12C read-only exclusion audit

R12B shows excluded_non_exact_block_ids is checked before generic rendering.
This audit confirms whether the transported-decomposition block is both:
- excluded as already seen; and
- preserved as an argument-level DERIVATION source.

No production code is modified.
No pytest is run.
