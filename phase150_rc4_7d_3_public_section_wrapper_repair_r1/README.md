# Phase 150 RC4-7D-3 Public Section Wrapper Repair R1

## Failure diagnosis

The RC4-7D-3 route integration passed its focused route tests and reason
tests. Three existing RC4-7A tests then showed that the public Narrative
section contract had been lost: the generic contribution renderer returns a
low-level fragment, while the public renderer is responsible for the
`## 使用する結果` and `## 証明` section headings.

## Changed target

- `toda_group_proof_narrative_renderer.py`

Import changes: none.

A new helper `_wrap_phase150_rc4_generic_public_narrative` is inserted
immediately before `_is_phase150_rc4_generic_route_target`.

The helper separates the normalized `[R1]`, `[R2]`, ... reference prefix from
the proof body and restores the public section wrapper.

The generic branch of `render_toda_group_proof_narrative_markdown` now stores
the generic fragment in `rendered`; only the three Phase 150 RC4 targets are
wrapped. The existing pi6 generic route remains unchanged.

## Tests

No existing test is weakened or modified.

The runner executes:

1. RC4-7A reference-section contract tests.
2. RC4-7D-3 route tests.
3. RC4-7D reason regressions.
4. related Web/Narrative regressions.
5. actual Web Narrative snapshots.

Repository-wide pytest remains reserved for the end of Phase 150.

## Completion criteria

The three RC4 targets must retain both:

- the public `## 使用する結果` / `## 証明` structure;
- the generic RC4-7D reason prose now exposed by the integrated route.

Reason selection/ownership, RC5 semantic naming, and RC6 formatting remain
outside this repair.
