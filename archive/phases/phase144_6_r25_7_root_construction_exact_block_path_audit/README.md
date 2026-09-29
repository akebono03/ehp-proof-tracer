# Phase 144-6 R25-7 — Root Proof Construction and Exact Block-Path Audit

This package performs an audit only. It does not modify production code.

## Scope

The audit follows the two unresolved `pi_6^3` Narrative issues upstream.

First, it inspects the actual `nu'` construction route used by
`build_toda_53_nu_prime_steps()` and the Proposition 5.6 upstream core. It
checks whether any returned `nu'` proof step has a
`TodaNuFamilyDefinitionStatement` premise and then scans the complete recursive
provenance graph for all `nu'`-related nodes and all nu-family definition nodes.

Second, it reconstructs the depth-2 Narrative block graph using the production
`_argument_direct_dependency_indices()` function. It verifies exact one-block
membership for every selected `ProofStep` and enumerates every dependency path
from each Argument conclusion block to the `pi_5^3` group-structure block.

## Expected diagnostic boundary

The audit is intended to determine:

- whether a `nu'` definition step is ever constructed on the root proof path;
- whether such a step is connected as a premise to the returned membership,
  Hopf, or double-relation steps;
- the exact block containing `pi_5^3`;
- every production block-dependency path that makes `pi_5^3` part of the
  group-structure and order Argument local bodies;
- the proof or semantic edge that introduces that dependency.

The runner verifies the relevant production files against Git HEAD and runs only
focused related tests.

The full test suite is intentionally not run.
Stop after the audit. No production repair is attempted.
