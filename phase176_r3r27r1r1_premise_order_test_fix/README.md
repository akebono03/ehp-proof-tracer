# Phase 176 R3R27R1R1 — Premise-order regression correction

This patch corrects one test expectation in the previously installed R3R27R1 isolated package. The proof matcher selects premises by their typed patterns, so supplying the same valid set in a different input order must still produce one match. The matched premises are returned in the rule's canonical pattern order.

The implementation changes **only** the test `test_only_independently_inferred_family_member_can_close` in `phase176_r3r27r1_toda55_quadruple_isolated/tests/test_source.py`. Production rules, source registrations, and the public proof provider are unchanged.

## Execute

Extract the archive at the repository root and run `phase176_r3r27r1r1_premise_order_test_fix/run.ps1` with `-DryRun` first, then without it. The installation checks the complete reviewed test file before replacing it. The focused pytest set is identical to R3R27R1. No full pytest run is performed.
