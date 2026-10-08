Phase 161-R4-R5 repair17
Stale repair13 expectation

Status after repair16
=====================
Repair16 production behavior passed its new focused tests.

The only remaining focused failure is an old repair13 internal expectation:

  "Toda Proposition 5.1 finite-dimensional integration"
  not in rule_names

That expectation predates repair14.

Current contract
================
After repair14, same-locator literature facts are represented by one
Proposition 5.1 Reference entry.

Its proof_steps intentionally retain both:
- the fixed higher-eta component step
- the finite-dimensional aggregate provenance step

Public rendering and Reference/body linkage use the higher-eta component for
the displayed statement and concrete pi_4^3 application.

Therefore the aggregate step being present in the internal Reference entry is
not a defect.

Repair
======
Update only the stale repair13 test function.

New expectation:
- exactly one Proposition 5.1 entry
- higher-eta component step is present
- aggregate provenance step is also present
- selected statement lines contain the general higher-eta relation

Production changes: NONE.
Imports changed: NONE.

No full pytest is run until Phase161 ends.
