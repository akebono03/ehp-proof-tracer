# EHP Proof Tracer — Phase 175 R3R11R4 (Preserve Prior Hopf Narratives)

R3R11R3 passed read-only DryRun, but its focused tests reported **34 passed, 1 failed**. The failure was in the existing Phase 172 regression test for the complete $\pi_6^3$ proof. Its previously verified suspension equation disappeared because the R3R11 single-equation presentation was applied to a Hopf chain already condensed by the Phase 172 projector.

## Reviewed baseline and scope

Before preparing this package, the current `akebono03/ehp-proof-tracer` `develop` files and relevant tests were inspected. The shared formatter `phase171_r20r13_eta_sentence_layout/projection.py` has the R3R11R1 hook committed at Git blob `5deaa8886f36ec967d52b9fcd603d135ae290b39`; no modification to that tracked file is needed. This ZIP replaces the R3R11 package directory from R3R11R3 and retains the single-equation feature.

The only behavior change is within `phase175_r3r11_cited_hopf_narrative/projection.py::_verified_hopf_chain_lines()`. It now requires an actual source-cited `TodaLemma57ExplicitNuPrimeZero` GIVEN and its directly derived, uniquely verified zero `GeneratorImage` within the completed root before applying this **second-stage** Hopf compression. This is a typed source/proof guard, not a target-coordinate or textual equation match. All previously approved Phase 172 Hopf narratives remain handled by their own projector.

Other package changes are two focused regression tests in `tests/test_projection.py`, revision labels in `audit.py` and `run.ps1`, and complete updated documentation. No math inference rules, database GIVENs, references, search policy, or core renderer are modified. The old `phase174_r3_r7_r70_verified_narrative_projection` source-pin test is still excluded because it expects the intentionally pre-R3R10 version of another file; its functional tests continue to run.

## PowerShell execution

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\R3R11R4.zip" -DestinationPath "." -Force
$script = ".\phase175_r3r11_cited_hopf_narrative\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
if ($LASTEXITCODE -ne 0) { throw "R3R11R4 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File $script
if ($LASTEXITCODE -ne 0) { throw "R3R11R4 audit failed" }
git diff --check
git diff --stat
git status -sb
```

## Acceptance

DryRun must report `PATCH_STATUS=ALREADY_APPLIED` and gate `PASS_R3R11R4_READ_ONLY_DRYRUN`. The real run requires all focused tests, including the unchanged Phase 172 regression and the new pi63 non-interference test, to pass. The pi73 public narrative must remain complete, trusted, source-cited with seven references, free of Lemma 5.4 reliance, and display the single four-equality Hopf calculation. Final gate: `PASS_R3R11R4_SINGLE_EQUATION_AND_PRIOR_NARRATIVE`.

The full pytest suite is intentionally deferred until the end of Phase 175.
