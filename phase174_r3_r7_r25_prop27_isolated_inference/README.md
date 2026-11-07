# Phase 174 R3-R7-R25 — Isolated Proposition 2.7 inference

This package defines an independently testable, source-cited, conditional inference rule for even dimensions. It **does not** register the rule in production or create a certified source premise. The synthetic cited premise used in a unit test is **not** mathematical evidence. A genuine, independently validated general-theorem premise must be connected before any public Verified ProofStep can be claimed.

Run `run.ps1 -DryRun` for a Git/source preflight, followed by `run.ps1` for focused tests. The full test suite is intentionally excluded. No tracked project files are modified by this package.

## R25R1 lineage correction

The guard accepts a reviewed-HEAD descendant only when intervening committed files are confined to R24/R25, the remote is either the reviewed HEAD or matches local HEAD, and reviewed source bytes remain unchanged. Unrelated commits and diverging remote history fail closed. The mathematical rule is unchanged.

## R25R2 committed pytest cache exception

This revision permits only the exact `.pytest_cache/v/cache/nodeids` path in reviewed descendant commits, after the R24-only lineage was confirmed. It does not generally ignore pytest cache paths or relax the tracked source integrity guard. Two files change: `audit.py` and `tests/test_lineage.py`; the full code and audit plan are refreshed.
