# Phase 165 — Explicit Typed Goal Connection (R2)

This package adds an optional typed `goal` argument to the existing common group search and Web proof entry. It does not register group-specific facts or treat a requested goal as GIVEN evidence. The legacy `n,k`-only path remains available and fails closed when it cannot select a group structure.

Run `run.ps1` from an extracted copy inside the project root. The installer backs up each original file and executes focused pytest tests. The full test suite is not run.

The current Web UI still presents only `n,k`; that UI must supply a previously specified typed Goal to take advantage of the new argument. This patch does not guess a group structure or automatically discover one.
