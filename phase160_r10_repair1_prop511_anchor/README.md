# Phase 160-R10 Repair 1

This package continues Phase 160-R10 after the initial apply stopped at the `toda_prop511_zero_bootstrap.py` stable-import insertion.

## Cause

The initial apply script used `from toda_rules import (` as a replacement anchor and required exactly one match. `toda_prop511_zero_bootstrap.py` contains more than one such import form, so the script stopped safely before changing that file.

## Repair

The repair:

1. verifies that the R10 changes before the failure point are already present;
2. uses the complete top-level `toda_prop58_zero_bootstrap` import followed by the top-level `toda_rules` import as the unique anchor;
3. adds `run_inference_until_stable_with_history` to the top-level `proof` import because the new six-stem aggregate uses it;
4. connects five-stem production to the generic zero-group transport;
5. connects six-stem production to generic finite-cyclic transport followed by nu-squared normalization;
6. installs the R10 public Narrative helper and focused tests.

No new Phase 160 semantics beyond the original R10 package are added.

Only focused tests are run. The full test suite is reserved for Phase 160 closure.
