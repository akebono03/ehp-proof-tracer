# Phase 166 R3-F — Proposition 5.1 claim-order repair

This package patches only `restrict_registered_ordered_claims` to recognize concrete specializations of the registered fifth claim. It does not introduce new rules, citation gates, renderers, or new mathematical assertions.

Run `run.ps1` from a PowerShell session after extracting in the project root. The installer backs up the existing source and refuses to run if its expected source block does not match. Full pytest is deliberately not executed.

Note: This is a narrowly scoped repair for the observed self-citation. A complete unified statement-registry ordering migration is outside R3-F.
