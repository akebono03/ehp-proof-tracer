# Phase 178 R7 — Finite Group Cardinality Public Connection

Expose the unchanged R6 rule through the existing screened presentation discovery function. Only `shared_expansion_provider` is modified; the new provider emits conditional goals, not proof steps. No new GIVEN, root-specific rule, or injectivity rule is added.

DryRun exports the complete proposed shared function/imports and file, without editing tracked files. The normal run installs the hook, captures the ordinary (3,6) root search, probes the two cardinality goals, and separately replays the rule with each verified earlier DB premise. Replay is not acceptance in the root search. The root can remain incomplete. Focused pytest: R6 tests and R7 installer/provider tests; cacheprovider disabled. The full suite is not run.

The reviewed R6 rule and tests are pinned by normalized SHA-256, including when untracked. The shared source and dependencies are pinned at the reviewed develop baseline. Only the expected shared file may change. Reports and full code are exported under LOCALAPPDATA/EHPProofTracerAudit.
