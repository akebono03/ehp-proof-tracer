# Phase 144-6 R25-6 — Upstream Ownership Audit

This package performs an audit only. It does not modify production code.

The audit traces the `pi_6^3` proof from the unbounded recursive provenance graph through replay selection, presentation, Narrative blocks, and Argument local bodies.

It answers two remaining questions:

1. Where does the `nu'` definition `ProofStep` first exist, what is its shortest provenance depth, and at which replay depth does it enter the presentation?
2. Why is the `pi_5^3` supporting `ProofStep` included in both the order and group-structure Argument local bodies?

The audit prints:

- all unbounded provenance definition nodes;
- shortest root-to-definition paths with premise indices;
- the `pi_5^3` provenance path;
- replay inclusion for `max_depth=0..6`;
- Argument roles and local-body block identities at relevant depths;
- proof edges and semantic dependency edges involving the `pi_5^3` step.

The runner first verifies that the two files previously modified by R24 still match Git HEAD exactly, then runs only related focused tests.

The full test suite is intentionally not run.
No production repair is attempted.
