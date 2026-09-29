Phase 144-6-R5-15D
====================

Audit only. No production code, tests, or project documents are modified.

R5-15C separated claim/provider depth selection from supporting-evidence
selection. R5-15D sweeps every depth from D_claim through full depth.

For each depth it records:
- required claim/provider preservation
- Narrative Argument role counts
- structured LiteratureReference count
- CALCULATION_CHAIN / SUPPORT / DERIVATION transition counts
- equation tag count
- Narrative character count

A semantic event is printed whenever that evidence signature changes.
Previews are printed at D_claim and the first Reference, calculation-chain,
derivation, and equation-tag depths.

Full-depth equation/reference counts are NOT completion criteria.
No n/k-specific depth rule is used.
No inference-rule-name parsing is used.
No pytest is run because production code is unchanged.
