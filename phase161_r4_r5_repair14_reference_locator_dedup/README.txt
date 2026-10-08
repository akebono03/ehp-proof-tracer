Phase 161-R4-R5 repair14
Reference locator deduplication

Root cause
==========
References are created at the beginning of the Narrative pipeline, but:

  build_toda_group_proof_narrative_reference_entries()

currently groups them using exact LiteratureReference object equality:

  references.index(reference)

The module already defines:

  _same_toda_group_proof_literature_reference()

which treats references with the same non-null locator as the same literature
reference.

Because the builder does not use that helper, two references such as:

  Proposition 5.1 higher-eta component
  Proposition 5.1 finite-dimensional aggregate

can become separate Reference entries if their LiteratureReference metadata is
not exactly equal even though both locators are "Proposition 5.1".

This was observed directly in the earlier audit as separate R3 and R5 entries.

Repair
======
Change only:

  build_toda_group_proof_narrative_reference_entries()

Use the existing semantic literature identity helper when locating an existing
entry.

No new Reference identity rule is introduced.
No dataclass field is added.
No renderer-specific pi_4^2 or Proposition 5.1 condition is added.

Expected effect
===============
At initial Reference construction there is exactly one Proposition 5.1 entry,
and its proof_steps contain both the fixed higher-eta component and aggregate
provenance steps.

Downstream statement selection can then select the fixed higher-eta component
while keeping one stable Reference identity.

Files
=====
Modified:
- toda_group_proof_narrative_references.py
  - build_toda_group_proof_narrative_reference_entries()

New:
- tests/test_phase161_r4_r5_repair14_reference_locator_dedup.py

Imports
=======
No production import changes.

No full pytest is run until Phase161 ends.
