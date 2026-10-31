# Phase 171 R20R6 — Public Order-Four Backward Proposal

This package connects **one existing typed inference rule** to the canonical EHP shared expansion provider: a finite group of cardinality four plus a proved nonzero double implies an element of order four.

It does not add mathematical axioms, `GIVEN` leaves, group results, completed proof trees, or Web presentation features. It does not claim that the public pi(6,3) proof is complete. Three additional public proof connections remain outside this step.

## Installation

Extract the ZIP into the `ehp_proof` repository root on the `develop` branch. Run the dry-run first:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r6_order_four_connection\run.ps1" -DryRun
```

Then apply the content-guarded patch and run only the included focused tests and source-anchored audit:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r6_order_four_connection\run.ps1"
```

`-SkipTests` is available for inspection, but the normal run is the recommended completion check. No full pytest suite is run. The installer preserves a pre-patch backup, supports repeat execution, and rejects unexpected source content or partial installation.

## Complete replacement code

The entire edited source module and the entire edited `shared_expansion_provider` function are generated from the reviewed local inputs after installation:

- `output/SOURCE_FULL_AFTER.py`
- `output/SHARED_PROVIDER_FUNCTION_FULL_AFTER.py`

The ZIP also includes the entire new function and the complete installer, audit, and new tests. The output directory is not included in the production modification scope.

## R20R6R1 installer repair

The previous installer matched a line feed (`LF`) string against a reviewed
provider stored with Windows (`CRLF`) line endings. As a result, dry-run stopped
without modifying production sources. This replacement ZIP fixes **only** the
installer's anchor matching and adds CRLF regression tests. The original
production patch, proof rules, provenance checks and focused test runner remain
unchanged. Extract over the prior package, run `-DryRun`, then the normal run.
