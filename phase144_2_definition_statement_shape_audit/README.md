# Phase 144-2 Definition Statement Shape Audit

Audit only. No production code or tests are modified.

This audit compares the concrete data shape of:

- `TodaNuFamilyDefinitionStatement`
- `TodaSigmaFamilyDefinitionStatement`
- `TodaLemma513Statement`

The current Narrative argument subject extractor expects a definition statement to expose an `element` attribute. Before classifying `TodaLemma513Statement` as a generic Definition block, this audit checks whether it satisfies that existing contract or needs a small generic subject-extraction extension.

Targets:

- pi_8^5
- pi_12^5
- pi_16^9

For each matching statement it prints:

- statement type
- inference-rule name
- current semantic roles
- whether `element` exists
- element type/name when present
- dataclass field names, types, and compact values

No production implementation belongs to this audit package.
