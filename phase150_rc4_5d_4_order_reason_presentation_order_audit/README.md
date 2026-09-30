# Phase 150 / RC4-5D-4

Read-only audit of the presentation order around
`MULTIPLE_RELATION_TO_ORDER`.

The audit checks whether the direct equality premise used to establish an
order-four conclusion is:

1. present in the typed proof graph;
2. already visible in the base Narrative;
3. selected by RC3 ordered-contribution relocation;
4. positioned before or after the conclusion in the final Narrative.

The expected diagnosis is that an already-visible direct premise is outside
the hidden-contribution relocation mechanism, which explains why the reason
renderer can place explanatory prose before the conclusion while the numbered
derived equality remains later in the Narrative.

No production files or existing tests are changed. Expression normalization is
observed only; it is not modified. Repository-wide tests remain deferred until
the end of Phase 150.
