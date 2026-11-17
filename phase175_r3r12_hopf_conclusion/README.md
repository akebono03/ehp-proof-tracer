# EHP Proof Tracer — Phase 175 R3R12R5

This patch gives the two concise, source-bound Hopf consequences the same map-domain and codomain display already used for the proven injectivity sentence.

A successful public $\pi_7^3$ proof now shows:

- `よって, $H: \pi_{7}^{3}\to \pi_{7}^{5}$ は全射.`
- `よって, $H: \pi_{7}^{3}\to \pi_{7}^{5}$ は同型.`

These dimensions are **test expectations**, not hard-coded into the projector. The function obtains the symbol with `map_symbol_tex(injective_step.conclusion.map)` and both group labels with `group_tex()` from the certified root and codomain premises. It keeps all previously verified finite-cyclic Hopf lift guards: citations, generator-image equation, Hopf chain, injectivity sentence, and final conclusion uniqueness. It changes display only; it does not create a `MapSurjective`, `MapIsomorphism`, mathematical rule, source fact, or `ProofStep`.

## Modified files

- `phase175_r3r12_hopf_conclusion/projection.py` — replace the complete `project_verified_hopf_lift_conclusion()` function. Existing imports already provide `group_tex` and `map_symbol_tex`; no import changes are necessary.
- `phase175_r3r12_hopf_conclusion/tests/test_projection.py` — update entire relevant tests so source, target and map arrow are asserted. Other regression tests remain.
- `phase175_r3r12_hopf_conclusion/audit.py` and `run.ps1` — update the focused gate and output assertions.
- `AUDIT_PLAN_JA.md`, `TEST_RESULTS_JA.md`, `CODE_FULL_JA.md` and this README — full-file documentation updates.

The existing `install.py`, R3R11 hook, mathematical rules, and databases are unmodified.

## Windows PowerShell

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\R3R12R5.zip" -DestinationPath "." -Force
$script = ".\phase175_r3r12_hopf_conclusion\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
if ($LASTEXITCODE -ne 0) { throw "R3R12R5 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File $script
if ($LASTEXITCODE -ne 0) { throw "R3R12R5 audit failed" }
git diff --check
git diff --stat
git status -sb
```

## Verification scope

R3R12R4 was confirmed by the user with 52 focused tests passing, a complete/trusted public proof, seven references, and one final conclusion. R3R12R5 changes only the subsequent display of the two map properties. This package runs the same focused integration tests, not the whole suite. The expected installer state on the verified R3R12R4 connection is `ALREADY_APPLIED`.

Expected gate: `PASS_R3R12R5_VERIFIED_HOPF_MAP_DOMAIN_CODOMAIN`.
