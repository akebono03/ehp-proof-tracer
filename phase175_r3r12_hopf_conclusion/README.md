# EHP Proof Tracer — Phase 175 R3R12R4

This is a presentation-only simplification of the certified finite-cyclic Hopf lift. The two prior paragraphs were customized for the displayed example, even though the underlying mathematical rule is general. They are now replaced with two concise, map-symbol-derived sentences:

- `よって, $H$ は全射.`
- `よって, $H$ は同型.`

The projector reads the map symbol from the existing, proved `MapInjective` premise, not from fixed sphere dimensions or citation labels. It continues to require the same typed Hopf-lift certificate, the actual cited codomain generator, the proved image, the already-rendered Hopf chain, and the original injectivity sentence before it changes any display. It does not add a surjectivity or isomorphism `ProofStep` or a new mathematical rule. Missing or ambiguous premises leave the original display unchanged.

## Changes

- `phase175_r3r12_hopf_conclusion/projection.py`: modify only `project_verified_hopf_lift_conclusion()` and add the `map_symbol_tex` import.
- `tests/test_projection.py`: update the concise-output assertions and add one source-bound map-symbol test.
- `audit.py`, `run.ps1`, and the package documents: update the focused public gate to R3R12R4.
- The already installed R3R12R3 hook in `phase175_r3r11_cited_hopf_narrative/projection.py` is unchanged. All mathematical source facts, proofs, tests outside this package, and database entries are unchanged.

## Run on Windows PowerShell

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\R3R12R4.zip" -DestinationPath "." -Force
$script = ".\phase175_r3r12_hopf_conclusion\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
if ($LASTEXITCODE -ne 0) { throw "R3R12R4 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File $script
if ($LASTEXITCODE -ne 0) { throw "R3R12R4 audit failed" }
git diff --check
git diff --stat
git status -sb
```

## Verification boundary

The patch installer accepts only the previously reviewed R3R11R4 production file and the exact R3R12 hook; its expected state on a successful R3R12R3 installation is `ALREADY_APPLIED`. Source-first, first successful proof search, and the seven references are unchanged. The focused tests cover the current pi_7^3 proof and the older pi_6^3 narrative. The full suite remains reserved for the end of Phase 175. The next proof-search phase is not implemented by this package.

Expected gate: `PASS_R3R12R4_CONCISE_VERIFIED_HOPF_CONSEQUENCES`.
