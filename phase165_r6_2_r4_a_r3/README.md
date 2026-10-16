# Phase 165 R6-2 R4-A-R3 — Source Factory Identity Audit

Run `run.ps1` from the repository root. The package creates `reports/rule_identity.json` and `reports/rule_identity.md`. It does not edit production files. The audit maps discovered rule factories to `module.function` identifiers and compares their instantiated rule-name multisets against R8 discovery.

**Limitations:** It does not execute goal applicability or reconstruct proofs. Python imports and factory calls may have import-time side effects. A factory identity is source-based, not a persistent identifier across renames.
