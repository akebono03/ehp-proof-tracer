# Phase 149 RC3-4 Cross-group Ordering Audit

This package audits the RC3-3 general Narrative ordering rule across six representative groups.

## Audit targets

- `pi_6^3`
- `pi_8^5`
- `pi_10^4`
- `pi_12^5`
- `pi_15^8`
- `pi_16^9`

## Scope

Production changes: none.

The audit checks each Narrative Argument independently so that repeated formulas in references or other Arguments do not create false ordering results.

For every Argument, it records:

- Argument role
- conclusion block index
- visible `OWNED_PRIMARY` exactness contributions
- evidence positions in the rendered Argument body
- conclusion position
- whether every visible owned-primary exactness contribution precedes the owner conclusion

It also saves the final Narrative for every target group for manual prose-order inspection.

## Expected result

`AUDIT_RESULT=PASS`

and all focused tests pass.

Repository-wide tests are intentionally deferred to RC3-5.
