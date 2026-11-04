# Phase 173 R4-R15R15 — Verified abstract result banner

This package fixes the public Web result banner for groups with a verified abstract structure but incomplete named-generator proof. It does **not** change proof search, proof status, generator identities, the abstract certificate, citations, or the group-query result API.

## Scope

Three production files are changed:

- `web_group_proof_common.py`: add a backward-compatible, evidence-backed Boolean field to `WebGroupProofView`.
- `phase165_r52_r3_web_adapter.py`: carry the already validated abstract certificate into the view.
- `templates/index.html`: show a distinct informative banner for abstract-only results.

The patch deliberately preserves **uncommitted R15R14 changes** to the shared Web renderer and R15R13 layout. It refuses unreviewed HEADs and tracked edits. Installation records local backups and supports rollback.

## Run on Windows

Extract the ZIP into the EHP Proof Tracer repository root. Run `run.ps1 -DryRun` from the extracted folder, then `run.ps1` to apply and execute focused pytest. The script does not commit anything or run the full test suite.

## Expected UI states

- Complete named-generator proof: `Typed proof search completed. See Group proof below.`
- Incomplete named-generator proof with verified abstract group structure: `A verified abstract group structure is available, but the named-generator proof is incomplete. See Group proof below.`
- No complete or verified abstract proof: `No proof-backed result found for this query.`

R15R14's real browser rendering still requires user verification. The R15R15 banner is driven only by the canonical `PartialProofResult.abstract_structure` certificate, not by Markdown text or mathematical heuristics.
