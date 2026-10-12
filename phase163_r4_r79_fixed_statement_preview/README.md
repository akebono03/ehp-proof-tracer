# Phase 163 R4-R79: Fixed-statement and proof-internal separation

This package previews eight claims extracted from the numbered mathematical statements of four existing references and keeps ten previous proof-internal candidates separate. It validates the TeX SHA-256 hashes recorded in R76, checks numbered statement boundaries, and instantiates the existing `UnifiedStatementRegistry` **in memory**. It does not register authoritative statements, assign production IDs, connect proof search, or run the full suite.

Run `run.ps1` with PowerShell from the extracted package. Prerequisites: the Phase 163 R4-R78 output and Phase 163 R4-R42 source TeX files in the project root. Results are written to `phase163_r4_r79_output`.

The preview source intervals are inclusive and retain the Japanese/TeX wording verbatim. The first line of some assertion components may not contain all shared conditions from the containing theorem; consumers must consult the full numbered statement before interpreting a component as a standalone claim.
