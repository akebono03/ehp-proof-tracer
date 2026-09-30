# Phase 150 / RC4-5B-1 — Reference / beta-to-nu-prime binding audit

## Purpose

Audit whether the current typed Narrative semantics can support prose of the form:

> この前提条件を満たすので、Lemma 5.2 を適用できる.
> Lemma 5.2 の beta を nu-prime と定めると、...

## Production changes

None.

## Existing test changes

None.

## Current architecture found before the local audit

The current `TodaGroupProofNarrativeDependencySemantic` stores:

- `prerequisite_step`
- `dependent_step`
- `role`

The current `TodaGroupProofNarrativeReason` stores:

- `kind`
- `premise_steps`
- `conclusion_step`
- `owner_argument_index`

Neither object currently has first-class fields for:

- reference identity;
- reference variable;
- instantiated concrete element;
- a variable-to-element binding.

The generic Lemma 5.2 capability does represent `beta` as a `HomotopyElement`
in its general representative. The concrete nu-prime specialization represents
the concrete element inside a `TodaBracketMembershipStatement`, but the current
Narrative semantic layer does not preserve an explicit `beta -> nu-prime`
instantiation relation.

## Expected classification

- precondition -> definition: `SAFE_NOW`
- reference-aware prose: `NEEDS_TYPED_SEMANTICS`
- beta -> nu-prime prose: `NEEDS_TYPED_SEMANTICS`

This audit intentionally does not add the missing semantic structure.
