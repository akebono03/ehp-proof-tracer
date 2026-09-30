# Phase 150 RC4-7C Reason-Prose Consumption Audit

Audit-only package. No production files or existing tests are changed.

## Purpose

Determine whether weak Narrative prose such as:

- `[R3]を用いる。`
- `これらから、`
- `このことから、`

is caused by:

1. missing generic reason semantics, or
2. an existing reason that is built but not consumed by the public renderer.

## Targets

Primary:

- `pi_10^4`
- `pi_12^5`
- `pi_16^9`

Control:

- `pi_15^8`

## Pipeline inspected

```text
ProofStep / semantic statement
  -> literature reference
  -> reason sidecar
  -> reason sentence
  -> generic rendered conclusion
  -> public Narrative
```

## Classifications

- `REASON_INSERTED`
- `REASON_BUILT_BUT_CONCLUSION_NOT_RENDERED`
- `REASON_BUILT_BUT_NOT_INSERTED`
- `REFERENCE_ONLY_WITHOUT_REASON`
- `SEMANTIC_LINE_WITHOUT_REASON`
- `NO_REASON_AND_NOT_RENDERED`

## Decision

If an existing reason is built but not consumed, repair consumption before
adding new reason kinds.

If existing reasons are consumed but important literature-backed or semantic
steps have no reason, extend the generic reason vocabulary in the next
production repair.

No group-specific renderer or group-specific reason branch is introduced by
this audit.

Repository-wide tests are intentionally not run.
