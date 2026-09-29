# Phase 144-6 R25-23 Narrative Evidence Selection / Dependency Ordering Audit

## Purpose

Diagnose two presentation defects exposed by the real Web `pi_6^3` depth-2
Narrative after R25-22:

1. too many exactness/EHP-sequence facts are rendered;
2. equation dependency references can appear before the referenced numbered
   equation is displayed.

## Scope

This package makes no production changes.

It audits the six representative groups:

- `pi_6^3`
- `pi_8^5`
- `pi_10^4`
- `pi_12^5`
- `pi_15^8`
- `pi_16^9`

For every NarrativeArgument it prints:

- conclusion statement type;
- direct derivation premise types;
- local-body block count;
- local exactness block count;
- method-evidence block count and exactness statement types.

It also reports:

- numbered equations;
- forward equation references;
- duplicated exactness prose.

## Current code hypothesis

`extract_toda_group_proof_narrative_argument_local_body_blocks()` and
`extract_toda_group_proof_narrative_argument_method_evidence()` recursively
traverse block dependencies. With complete replay this can expose a much larger
exactness ancestry than should be narrated.

`number_toda_group_proof_narrative_equations()` assigns numbers from proof-step
transitions and applies them to already rendered Markdown. The audit checks
whether this produces references before the corresponding numbered equation is
actually displayed.

## Phase boundary

R25-23 is diagnostic only. Do not add suppression or reorder equations until the
audit identifies which selection boundary and which ordering layer are
responsible.

Repository-wide pytest is intentionally not run.
