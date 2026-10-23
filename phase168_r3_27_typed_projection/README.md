# Phase 168 R3-27 — Typed Statement Projection

Extracts generic typed-statement formatting helpers from the model-backed renderer into `phase168_r3_27_typed_statement_projection.py`. The renderer retains the same public function signature.

Adds shared formatting support for `MapInjective`, `MapSurjective`, `MapIsomorphism`, `TodaSuspensionIsomorphismStatement`, and `GeneratorImage`. No new proof fact is inferred: only statements present in the Proof Tree are formatted. Other typed statements are unchanged.

The still-missing zero-Delta prose and proof-order projection are explicitly deferred, rather than introducing unverified behavior. No group-specific fixed narrative is added. Existing EHP chain projection and reference numbering are unchanged.

Prerequisite: R3-26a. The patch checks the existing renderer and creates a backup. Limited tests are run; the full suite is deferred to the end of Phase 168.
