# EHP Proof Tracer — Phase 174 R3-R4 Public Delta-Zero Connection

This package connects the already reviewed, source-grounded general
Delta-zero inference to the **existing** common `shared_expansion_provider()`.
It adds one local import and one `options.extend()` in the nested `expand()`
function; no new source premises, group-specific cases, narrative renderers,
or citation policy are introduced.

The patcher guards the exact committed Git blob of the full production file,
refuses to overwrite user edits or staged changes, and preserves CRLF/LF.
It outputs the **complete modified function** (not a shortened diff) to
`%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r4\shared_expansion_provider_FULL.py`.

It then reconstructs `Delta : pi_7^7 -> pi_5^3 = 0` through the *ordinary*
source-screened common provider. The two independent premises must be inferred
from Proposition 4.4 and Proposition 4.2 respectively. No statement is added
as a direct GIVEN. This does not complete the named group proof for `pi_8^5`.

The focused tests do not run the full pytest suite. Run `run.ps1 -DryRun`
first and then `run.ps1` from the repo root after unzipping.
