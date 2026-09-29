# Phase 144-6 R25-9A-R1-R2 — Test API Repair

## Production changes

None in this package.

R25-9A and R25-9A-R1 production changes were already applied before the
previous test collection error.

## Test correction

The previous test incorrectly imported a nonexistent
`TodaGroupProofPresentationNode`.

The current API exposes presentation nodes through
`TodaGroupResultProofReplayStep` objects owned by the source replay.

Rather than constructing an unnecessary synthetic replay/presentation fixture,
R2 uses the existing real pi_6^3 method-evidence fixture.

The corrected regression verifies both sides of the contract:

1. the internal pi_5^3 support step is classified into the Argument hidden set;
2. the final multi-Argument Narrative does not reintroduce that hidden step
   through relocated direct-premise rendering.

## Scope

No nu-prime depth-2 definition repair is attempted.
The full suite is intentionally deferred until the Phase 144-6 completion
boundary.
