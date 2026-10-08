Phase 161-R4-R2 repair1

The original R4-R2 audit incorrectly accessed:

  proof_step.rule_name

ProofStep has no such attribute.

Current repository API uses:

  proof_step.inference_rule.name

when an inference rule exists, otherwise:

  proof_step.rule.value

This repair changes only the audit script.

Production changes:
- none

Test changes:
- none

Full pytest:
- not run
