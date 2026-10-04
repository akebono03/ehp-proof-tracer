Phase157-R20 repair2

Purpose
-------
Fix the remaining Equation 5.7 premise-guard mismatch after R20 repair1.

Cause
-----
`toda_eta_family_definition_statement(5)` preserves its constructor-facing
element name (`eta_5` internally), while the concrete Toda calculation uses
canonical notation `η₅`.

The Equation 5.7 guard already validates eta-family definitions structurally:
index, dimension, source, target, generator identity, and iterated-suspension
ancestry.

R20 accidentally reused `eta5_definition.element` inside the exact
Proposition 2.2 Relation equality check. Because HomotopyElement dataclass
equality includes the `name` field, the otherwise-correct Proposition 2.2
ProofStep was rejected.

Repair
------
Use `canonical_eta_5` in the expected Proposition 2.2 Relation.

This is not a pi_6^3 Narrative specialization. It restores the existing
constructor-name/canonical-notation boundary already enforced structurally by
the Equation 5.7 rule.

Changed file
------------
- toda_rules.py
  - toda_57_nu_prime_eta6_hopf_inference_rule()

Import changes: none.
Test-file changes: none.
Documentation changes: none.
Repository-wide pytest: intentionally not run.
