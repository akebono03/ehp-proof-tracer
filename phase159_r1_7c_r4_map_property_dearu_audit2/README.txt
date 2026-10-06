Phase 159 R1-7c R4 map-property "である" source-route audit2

Purpose
-------
Classify the source route of the eight confirmed public Narrative occurrences
of:

- は単射である.
- は全射である.

Affected current audit-sample outputs:
- pi_11^6
- pi_12^6
- pi_13^7
- pi_16^9

The audit compares each public occurrence with generic rendering of every
ProofStep in the corresponding presentation.

For matching generic source steps it prints:
- node index;
- conclusion statement type;
- rule name;
- generic rendered text.

If no generic ProofStep renders the phrase, the occurrence is marked as
requiring investigation of a later prose-composition route.

Production code changes: none.
Test code changes: none.
No full pytest.
