# Phase 150 / RC4-5B-2 — Reference / variable-binding semantic design

## Status

Design only. No production changes. No existing test changes.

## Goal

Support generic Narrative prose such as:

> この前提条件を満たすので、Lemma 5.2 を適用できる.
> Lemma 5.2 の $\beta$ を $\nu'$ と定めると、
> $\nu'\in\{\eta_3,2\iota_4,\eta_4\}_1$.

without hard-coding `Lemma 5.2`, `beta`, `nu_prime`, `(n, k)`, or rendered prose in the renderer.

## Current facts confirmed by RC4-5B-1

The current typed semantic layer contains:

- `PRECONDITION_FOR_DEFINITION`;
- `DEFINITION_INTRODUCTION`.

It does not contain first-class:

- reference identity;
- formal reference variable;
- instantiated concrete expression;
- formal-variable-to-concrete-expression binding.

The generic Lemma 5.2 capability does contain a formal `HomotopyElement(name="β", ...)`.
The concrete nu-prime specialization contains the concrete element `ν′` in a
`TodaBracketMembershipStatement`.

## Design decision

Do not add reference strings or variable names directly to the renderer.

Do not overload `REFERENCE_STATEMENT_TYPES`: it classifies display/reference
statements, while the new information describes an application/instantiation
relationship.

Add a typed semantic object dedicated to reference application.

### Proposed types

Add to `toda_group_proof_narrative_semantics.py`:

```python
@dataclass(frozen=True)
class TodaGroupProofNarrativeReferenceIdentity:
  label: str
```

The first implementation may use a validated display label because the current
proof model has no repository-wide first-class theorem identifier. The label
must be produced by semantic construction, never inferred by the renderer.

```python
@dataclass(frozen=True)
class TodaGroupProofNarrativeVariableBinding:
  formal_variable: object
  instantiated_expression: object
```

`formal_variable` and `instantiated_expression` should hold mathematical
expression objects, not rendered strings.

```python
@dataclass(frozen=True)
class TodaGroupProofNarrativeReferenceApplicationSemantic:
  dependent_step: ProofStep
  reference: TodaGroupProofNarrativeReferenceIdentity
  bindings: tuple[TodaGroupProofNarrativeVariableBinding, ...]
```

The `dependent_step` is the concrete definition-introduction step to which the
reference application belongs.

### Sidecar extension

Extend `TodaGroupProofNarrativeSemanticSidecar` with:

```python
reference_application_semantics: tuple[
  TodaGroupProofNarrativeReferenceApplicationSemantic,
  ...,
] = ()
```

Validation requirements:

1. every dependent step belongs to the presentation;
2. reference label is non-empty;
3. bindings is non-empty for an instantiated reference application;
4. no duplicate formal variable inside one application;
5. no duplicate application for the same dependent step/reference pair;
6. formal/concrete values are mathematical objects, not renderer strings.

## How the nu-prime case should be represented

Conceptually:

```python
TodaGroupProofNarrativeReferenceApplicationSemantic(
  dependent_step=nu_prime_bracket_membership_step,
  reference=TodaGroupProofNarrativeReferenceIdentity(
    label="Lemma 5.2",
  ),
  bindings=(
    TodaGroupProofNarrativeVariableBinding(
      formal_variable=beta,
      instantiated_expression=nu_prime,
    ),
  ),
)
```

This is semantic data, not renderer logic.

## Reason-layer design

`TodaGroupProofNarrativeReason` should not duplicate all binding data.

For `DEFINITION_APPLICABILITY`, add an optional typed link:

```python
reference_application: (
  TodaGroupProofNarrativeReferenceApplicationSemantic | None
) = None
```

The reason builder may attach it only when exactly one compatible reference
application semantic exists for the conclusion step.

If none or multiple incompatible applications exist, leave it `None`.
The renderer must then retain the current conservative prose rather than guess.

## Renderer rule

When a `DEFINITION_APPLICABILITY` reason has no reference application:

```text
この前提条件を満たすので、次の定義を用いる.
```

When it has exactly one safe reference application with a binding:

```text
この前提条件を満たすので、{reference} を適用できる.
{reference} の {formal variable} を {instantiated expression} と定めると、
```

The following mathematical statement remains rendered by the existing generic
step renderer.

For the current pi_6^3 case this becomes:

```text
この前提条件を満たすので、Lemma 5.2 を適用できる.
Lemma 5.2 の $\beta$ を $\nu'$ と定めると、

$\nu'\in\{\eta_3,2\iota_4,\eta_4\}_1$
```

## Important semantic wording boundary

The phrase `beta を nu-prime と定める` is appropriate only if the stored
binding genuinely represents the formal Lemma variable instantiated by the
concrete element.

If the proof data only says that `nu_prime` belongs to the bracket but does not
establish that instantiation relation, the semantic builder must not create the
binding.

## Construction boundary

The current semantic builder still recognizes the nu-prime definition path via
rule-name/index tables. RC4-5B-2 does not redesign that existing mechanism.

RC4-5B-3 may minimally construct the new reference-application semantic at the
same already-recognized definition path, provided it derives the concrete
element from the typed `TodaBracketMembershipStatement` and obtains the formal
Lemma variable from typed Lemma-5.2 semantic data rather than from renderer
text.

A repository-wide theorem/reference identity system is explicitly out of scope.

## Tests required for RC4-5B-3

Focused tests should establish:

1. pi_6^3 gets exactly one reference application;
2. its reference is `Lemma 5.2`;
3. its formal variable is the mathematical beta object;
4. its instantiated expression is the mathematical nu-prime object;
5. the application points to the existing definition-introduction step;
6. the reason builder attaches the application;
7. the renderer produces reference-aware prose;
8. no application means conservative fallback prose;
9. ambiguous applications do not produce guessed prose;
10. no `(6, 3)`, `pi6`, `nu_prime`, `ν′`, or rendered-bracket matching is used
    as a renderer branch.

## Phase boundary

RC4-5B-2 ends with design only.

RC4-5B-3 may implement only the minimal typed reference-application path needed
for the already-recognized Lemma 5.2 definition application and its focused
tests.

It must not implement:
- other RC4 reason kinds;
- RC5 EHP semantic naming;
- RC6 equation numbering/formatting;
- a repository-wide theorem registry;
- unrelated refactoring.
