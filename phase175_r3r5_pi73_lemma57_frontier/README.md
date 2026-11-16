# EHP Proof Tracer — Phase 175 R3R5, Lemma 5.7 Frontier

This is a **read-only** source-first audit of the last unresolved obligation in the isolated proof of `pi_7^3 = Z/2{nu-prime eta_6}`. The preceding R3R4 audit independently reconstructed the Hopf generator image and the cyclic Hopf codomain, but not Hopf injectivity.

Toda **Lemma 5.7**, in the adopted Chapter V transcription `sources/toda/Toda_05_2.tex`, states a general conditional vanishing of `E(eta_2 o alpha)` and explicitly establishes `E(eta_2 o nu-prime)=0`. This source is earlier than the target Proposition 5.8. **The text check does not register either statement as GIVEN**; it solely verifies the reference and its position. The original printed edition is not independently checked.

The audit uses the existing typed EHP rules, the existing finite-cyclic zero-image rule, and the canonical recursive search to examine five separate obligations: EHP exactness, the prior cyclic domain, the zero suspension of its generator, zero image of its whole suspension homomorphism, and Hopf injectivity. No new mathematical rule or source assertion is installed. No previously completed ProofStep is injected into search. The ordinary public proof search and Web renderer are unchanged.

## Changes and files

Add only `phase175_r3r5_pi73_lemma57_frontier/` at the project root:

- `source.py`: Git-pinned Toda Lemma 5.7 text and source-order verification.
- `frontier.py`: strictly typed, independent canonical proof-search probes.
- `audit.py`: reuses the successful R3R4 and R2 source/lineage guards; bounded read-only worker and structured report.
- `tests/test_source.py`, `tests/test_audit.py`, `tests/test_frontier.py`: focused regressions.
- `run.ps1`, `AUDIT_PLAN_JA.md`, `CODE_FULL_JA.md`, `TEST_RESULTS_JA.md`, and this `README.md`.

No existing file is changed. Existing public APIs, provider priorities, mathematical sources, or documentation in the repository root are unaffected. Extracting the ZIP creates only the new folder. Reports are saved outside the repository under `%LOCALAPPDATA%\EHPProofTracerAudit\phase175_r3r5_pi73_lemma57_frontier\`.

## PowerShell (repository root)

```powershell
Expand-Archive -Path "$HOME\Downloads\R3R5.zip" -DestinationPath "." -Force
$script = ".\phase175_r3r5_pi73_lemma57_frontier\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
if ($LASTEXITCODE -ne 0) { throw "R3R5 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File $script
if ($LASTEXITCODE -ne 0) { throw "R3R5 audit failed" }
git status -sb
```

## Acceptance and boundary

A successful DryRun confirms the source pins, R2 lineage, and a preceding successful R3R4 normal-run report. A successful normal run records five independently observed statuses with the real typed search and zero new GIVEN. Neither result claims that the group is proved or the public UI has changed.

The next increment, only if indicated by this evidence, should connect the **general, source-cited Lemma 5.7** to a typed inference for the suspension of the lower generator and then prove the whole zero-image and Hopf injectivity obligations. It must not insert the target group or the concrete zero suspension as a gratuitous GIVEN.

Full-suite pytest remains reserved for the end of Phase 175.
