# Historical Phase Artifacts

This directory stores historical implementation, audit, repair, diagnostic, and
verification artifacts that were previously kept at the repository root.

## Purpose

The archive preserves the development history of EHP Proof Tracer while keeping
the repository root focused on the current implementation, canonical tests, and
active project documentation.

The archived files are historical snapshots. Their contents are preserved as
they existed before archival.

## Layout

Historical artifact directories retain their original names directly under
`archive/phases/`.

Historical standalone files that previously lived at the repository root are
stored under:

`archive/phases/_root_files/`

No additional regrouping by Phase number is performed. This keeps historical
names stable and makes old references easier to trace.

## Execution Policy

Archived runners, installers, repair scripts, payloads, audit scripts, and
diagnostic tools are preserved for historical inspection.

Execution from the archived location is not guaranteed. Some historical
artifacts assumed that their package directory was located directly under the
repository root, referred to another historical Phase artifact by its old root
path, or depended on a temporary or subsequently removed historical artifact.

Phase 145-2 intentionally does not rewrite those historical scripts. Updating
them would alter historical snapshots and would expand the scope from archival
cleanup into maintenance of obsolete execution environments.

Current production code and canonical tests must not depend on archived Phase
artifacts.

## Phase 145-2 Archival Boundary

Phase 145-2 moves the audited historical Phase-artifact population into this
archive without changing production semantics.

The archival operation does not:

- modify production implementation behavior;
- modify canonical test behavior;
- restore removed historical dependencies;
- guarantee archived runner executability; or
- introduce functionality planned for later phases.

The repository-wide test suite is run after the move as the final regression
gate for Phase 145-2.
