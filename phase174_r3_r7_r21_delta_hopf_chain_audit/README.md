# EHP Proof Tracer — Phase 174 R3-R7-R21

This is a read-only audit of the Hopf/Delta dependency chain in the
adopted Toda Proposition 5.9 text. It does not create proof steps,
register GIVEN statements, change proof rules, or claim root completion.

The package must be extracted at the root of the `develop` checkout of
`akebono03/ehp-proof-tracer`. The checkout must be at the reviewed
commit `654d46f6f225fc6b641a1760ce0e3f08598419c3`, with no tracked
changes. The R20 audit package must already be extracted there.

Run `run.ps1 -DryRun`, then `run.ps1`. Both use focused pytest only;
the full test suite is reserved for the phase closeout. The reports
are written to `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r21`.

The acceptance gate confirms source evidence and an incomplete public
proof frontier. A signed, typed Delta image witness remains a later task.
