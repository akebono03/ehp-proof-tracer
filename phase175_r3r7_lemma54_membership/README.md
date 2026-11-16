# EHP Proof Tracer — Phase 175 R3R7

## Purpose

This **isolated, source-first** package derives the missing hypothesis for the already cited universal Toda Lemma 5.7. Its source is the reviewed Toda Lemma 5.4 clause `2 E(nu_4) = E^2(nu-prime)`. The formal group identity on `S^5` converts this independently proved equation into `E^2(nu-prime) in 2 iota_5 o pi_8(S^5)`.

There is no new goal-specific GIVEN, no database proof fabrication, no modification to the shared production search provider or renderer, and no whole-repository test run. The original printed Toda edition has **not** been independently authenticated; the pinned evidence is the project's adopted Chapter V transcription.

## Scope and proof discipline

- `source.py` validates the existing Chapter V Git blob, the exact text of Lemma 5.4, the reviewed manifest hashes, and the citation sequence Lemma 5.4 (8300), Lemma 5.7 (9100), Proposition 5.8 (9200).
- `rule.py` extracts the **specific source clause** from the existing `TodaLemma54TypedSource` only when a unique screened GIVEN proof leaf is available. It then offers an independently checked, **degree-generic** mathematical inference from any proved equality `E^2(alpha) = 2 beta`, where `alpha` is in `pi_i(S^3)` and `beta` is in `pi_(i+2)(S^5)`.
- `audit.py` independently reconstructs the cited equality, double-suspension membership, Lemma 5.7 zero image of the generator, zero suspension image, Hopf injectivity, and the isolated cyclic structure for `pi_7^3`, in that order. Every inference requires actual parents and the canonical typed proof search. It reports `UNRESOLVED` when necessary.
- `run.ps1` performs only focused pytest and a read-only source audit, writing JSON, Markdown, and worker logs under `%LOCALAPPDATA%\EHPProofTracerAudit\phase175_r3r7_lemma54_membership\<UTC>\`.

Mathematically, the middle identity `E^2(nu-prime)=2nu_5` is **not needed** to establish the membership criterion: Toda Lemma 5.4 already gives `E^2(nu-prime)=2E(nu_4)`. This avoids an unnecessary new rule or a direct assertion of the target conclusion.

## Windows PowerShell

Unzip the supplied `R3R7.zip` into the root of the `develop` checkout *after* the successful normal R3R6R2 run. From the checkout root:

```powershell
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\R3R7.zip" -DestinationPath '.' -Force
$script = '.\phase175_r3r7_lemma54_membership\run.ps1'
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
if ($LASTEXITCODE -ne 0) { throw 'R3R7 DryRun failed' }
powershell -NoProfile -ExecutionPolicy Bypass -File $script
if ($LASTEXITCODE -ne 0) { throw 'R3R7 audit failed: inspect report.json for unresolved obligations' }
git status -sb
```

`-TimeoutSeconds` is available for the isolated recursive proof search; its default is 300 seconds. The runner enables UTF-8 for Windows Python. It neither stages nor commits nor resets Git files.

## Gate meanings

- `PASS_R3R7_READ_ONLY_DRYRUN`: source checks and previous audit evidence passed; no mathematical search was performed.
- `PASS_R3R7_MEMBERSHIP_INFERRED_PI73_PENDING`: the missing Lemma 5.7 hypothesis was independently inferred, but at least one later proof obligation is unresolved.
- `PASS_R3R7_ISOLATED_PI73_CYCLIC_INFERRED`: the isolated typed search completed the cyclic-structure obligation; this is **not** a production or Web proof until a later explicit public integration phase.
- `R3R7_MEMBERSHIP_UNRESOLVED`: source-first searches did not establish the central membership claim. This is a nonzero audit exit, not mathematical success.
- `R3R7_REFUSED_OR_WORKER_ERROR`: preflight/source guard/worker failure. No completion claim.

The full pytest suite is deferred until the Phase 175 final gate. This package does not modify `README.md`, `design.md`, `development_log.md`, `roadmap.md`, or `proof_records.md` in the repository root.
