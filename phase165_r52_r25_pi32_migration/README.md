# Phase 165 R52-R25: Legacy rule retirement compatibility gate

This is a read-only, targeted compatibility check. It examines the active legacy `pi3^2` inference rule, the generic free-cyclic transport rule, and the legacy consumers in the bootstrap and probe. It does not delete a rule, rewrite old APIs, certify mathematical equivalence, or run the full test suite.

Run `run.ps1` from the extracted package directory. Outputs are stored in `audit_output`.
