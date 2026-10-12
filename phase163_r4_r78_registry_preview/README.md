# Phase 163 R4-R78: Transient Registry Validation

Run `run.ps1` from the extracted directory. Requires Python, pytest, existing project `unified_statement_registry.py`, and R75/R77 JSON outputs.

This stage constructs an in-memory `UnifiedStatementRegistry` with four **temporary** owner references and ten **temporary proof-internal** assertion records. The Proposition 1.5 paraphrase is kept out of the registry preview. Nothing is written to the production registry, no official IDs are allocated, and no mathematical or original-edition verification is claimed.

Focused pytest runs first. Full test suite runs only at phase completion.
