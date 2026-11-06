# Phase 174 R3-R7-R10 — Cited Family Image Gap Audit

A read-only source-first audit of the two factor `GeneratorImage` obligations created by an already existing composition suspension rule. The audit checks the registered nu-family identity, canonical family naming and citation availability independently. It does not create mathematical evidence, attach a source as a direct goal GIVEN, register a production inference rule, or change the public provider.

## Usage

Unpack `R10.zip` directly into the root of the `akebono03/ehp-proof-tracer` develop checkout. It requires the completed R9 JSON audit record under `%LOCALAPPDATA%/EHPProofTracerAudit/phase174_r3_r7_r9/composition_associativity.json`.

Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase174_r3_r7_r10_cited_family_gap_audit\run.ps1 -DryRun`, then run without `-DryRun`. The script uses focused, separate pytest processes and intentionally does **not** execute the full test suite.

A successful full audit writes `cited_family_gap.json` under `%LOCALAPPDATA%/EHPProofTracerAudit/phase174_r3_r7_r10/`. The reported proposal counts are **unverified backward candidates**, not completed proof trees.

GitHub develop HEAD is pinned to `23979feec6685446a48d392fce3f2f1a55e85fe8` and the reviewed source blob hashes. Any unexpected tracked change or HEAD mismatch fails closed.
