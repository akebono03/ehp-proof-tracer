Phase 159 R1-7c R4 map-property "である" exact source-route audit3

Purpose
-------
Audit2 confirmed eight public occurrences of:
- は単射である.
- は全射である.

However audit2 matched any generic step containing the same phrase, so it did
not prove source identity.

Audit3 performs exact source-route classification.

Method
------
For each affected output:
- build the raw presentation;
- build the semantic-closure presentation;
- render the current public Narrative;
- strip only an optional "[R#] より, " prefix from each affected public line;
- compare that exact line against:
  - generic rendering of every raw ProofStep;
  - generic rendering of every semantic-closure ProofStep;
  - aggregate statement prose of those ProofSteps.

Classification:
- exact raw match -> raw-step renderer route;
- exact closure-only match -> semantic-closure step renderer route;
- no exact match -> later contribution/dependency/prose-composition route.

Affected current audit-sample outputs:
- pi_11^6
- pi_12^6
- pi_13^7
- pi_16^9

Production code changes: none.
Test code changes: none.
No full pytest.
