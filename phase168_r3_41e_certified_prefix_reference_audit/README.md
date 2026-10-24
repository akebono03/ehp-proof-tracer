# Phase 168 R3-41E — Certified-Prefix Reference Audit

This package performs a **read-only** audit of source citations in partially displayed proof steps. No mathematical assertions are inferred and no implementation files are changed.

The five genuinely incomplete searches tested in R3-41D1 had no retained proof steps, so they could not validate cited-step rendering. Instead, this audit takes an identity-preserving, premise-closed strict prefix of the actual completed π₄³ search, creates a clearly labeled **audit-only reconstructed partial state**, projects only its genuinely linked citations from the original screened bridge, and renders it through the shared Narrative pipeline. This is **not** a naturally produced PARTIAL search.

The audit separately checks Reference headings, full source bodies, Web rendering, and whether each source number appears on its own proof-step line. A citation number appearing elsewhere in the Reference section does not satisfy the step-level provenance requirement. Results and scope limitations are written to `output/audit.json`, `output/audit.md`, and `output/review_bundle.zip`.

Run `run.ps1` from PowerShell after extraction into the repository root. Only the six new focused tests and the existing R3-41D1 boundary tests run. The complete pytest suite is deferred to the end of Phase 168.
