# GitHub baseline — Phase 155-R4-3

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Before R4-3, GitHub was re-inspected for current internal production ownership
and representative tests.

The repository contains many current non-public modules such as:
- Toda calculation/proof modules,
- proof repository modules,
- Toda rule modules,
- Narrative renderers,
- repository-generator infrastructure.

Older numbered Phase tests still directly import and exercise these current
modules. Therefore internal canonical classification must be based on current
production ownership rather than only public entry points or Phase age.

R4-3 performs this ownership classification conservatively and preserves
test-helper-only cases as lineage-support candidates instead of deleting them.

No production/test changes are made and repository-wide pytest remains
reserved for Phase 155 closure.
