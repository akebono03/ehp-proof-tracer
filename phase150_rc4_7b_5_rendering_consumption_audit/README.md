# Phase 150 RC4-7B-5 Rendering Consumption Audit

## Purpose

This is an audit-only package. It does not modify production code, existing tests, or project documentation.

RC4-7B-4 found 22 `VISIBLE_LOCAL_DERIVATION` transitions across `pi_10^4`, `pi_12^5`, and `pi_16^9`. This audit traces those same visible local derivations through the current rendering pipeline.

## Current-code scope inspected before this audit

The current GitHub `develop` code was inspected at commit `47670ba70b0365489820109dd4f1b9db5324b5d9`, especially:

- `toda_group_proof_narrative_renderer.py`
- `toda_group_proof_narrative_argument_multi_renderer.py`
- `toda_group_proof_narrative_contribution_renderer.py`
- `toda_group_proof_narrative_transition_renderer.py`
- related narrative transition and argument tests

## What is measured

For each RC4-7B-4 visible local derivation, the audit compares:

1. the transition connector selected by the multi-Argument renderer;
2. whether source blocks are present in base multi-Argument Markdown;
3. whether the conclusion is present in base multi-Argument Markdown;
4. whether contribution insertion adds missing source/conclusion material;
5. whether the public Narrative still contains the conclusion.

The audit classifies each derivation as:

- `FULLY_CONSUMED_GENERIC_CONNECTOR`
- `FULLY_CONSUMED_SPECIFIC_CONNECTOR`
- `CONTRIBUTION_COMPLETES_DERIVATION`
- `PARTIALLY_CONSUMED`
- `NOT_CONSUMED`

The key distinction is whether the current pipeline already consumes the mathematical material but expresses the inference only with a generic connector such as `これらから`, versus actually failing to consume required material.

## Boundary

This package does not change Argument ownership, ProofChain structure, semantic closure, contribution placement, or renderer behavior. It does not introduce RC5 EHP naming or RC6 equation/prose formatting work.

Repository-wide pytest is intentionally not run because Phase 150 is not yet complete.
