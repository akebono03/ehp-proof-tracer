Phase 144-6-R5-42-R2 provider-key semantics repair

Observed after R1:
- production selected population: 175
- R5-40 selected population: 190
- at_provider_anchor: matched
- before_argument_conclusion: matched
- before_dependent_contribution: production 31, R5-40 46

Root cause:
The R5-38/R5-40 audit defines a provider key when the step belongs to that
single provider's anchored chain. The first production implementation added an
extra requirement that the step must also be graph-necessary for that provider
in isolation. That changed contribution grouping and ownership before placement.

Minimal repair:
- _provider_keys_for_step now adds the provider key on chain membership alone,
  exactly matching the audited R5-38/R5-40 rule.
- R1 occurrence-based bridge selection is retained.
- A regression test locks the provider-key rule.
- Renderer/public output remains unchanged.
- No full suite is run in this subphase.
