# Phase 169 R3H — Source-backed Toda (5.3) Hopf identity

This package registers **only** the exact statement `H(nu-prime)=eta_5` as a cited source leaf from Toda equation (5.3), which precedes Proposition 5.3 in the reviewed source-text manifest. It does not assert a newly inferred result, change an EHP rule, or complete the group proof of pi_5^3.

The implementation verifies the unique source archive record and its SHA-256 content hash, retains the reviewed literature-reference ID `toda:(5.3)`, and adds a typed `Relation` source with a **GIVEN** proof witness. The existing eight shared source inputs retain their positions. The updated complete `build_shared_typed_bridge` function is stored in `full_functions/`.

Extract this archive into the Git working directory so that the package directory is located directly below the repository root. Run `powershell -ExecutionPolicy Bypass -File .\phase169_r3h_toda53_hopf_source\run.ps1` from the root. The script verifies required paths, applies a guarded full-function patch against the reviewed `a9594064` Git baseline, runs focused pytest, audits the real citation-screened pi_5^3 context, and rolls back on failures. It does not run the full suite.

A successful audit proves only that the cited source was registered and made available before the Proposition 5.3 target. It does not bridge historical rules requiring INFERENCE-only premises. That remains for the next phase task.
