# Phase 175 R4R3R2 — Isolated EHP Rank-Two Quotient Rule (Reviewed R4 Commit Lineage)

This package implements **one general typed inference rule** for an exact EHP
window. It does not add a source GIVEN, edit the existing proof engine, register
a public provider, replay a prior proof, or mark the target group complete.

## Scope

Consider a consecutive EHP exact window

$$
C \xrightarrow{\Delta} A \xrightarrow{E} B.
$$

The proposed rule consumes six separately proved statements:

1. $A=\mathbb{Z}/2\{a\}\oplus\mathbb{Z}/2\{b\}$.
2. $C=\mathbb{Z}/2\{z\}$.
3. The generator-image fact $\Delta(z)=b$, or the symmetric case
   $\Delta(z)=a$.
4. Proposition 4.2 exactness $\operatorname{im}\Delta=\ker E$.
5. $E:A\to B$ is surjective.
6. The surviving generator maps to $y$, i.e. $E(a)=y$ (or $E(b)=y$
   in the symmetric case).

These premises entail the **general** conclusion
$B=\mathbb{Z}/2\{y\}$, by the first isomorphism theorem. The existing
`finite_cyclic_structure_as_relation_inference_rule()` converts the resulting
`CyclicStructureStatement` into the canonical group `Relation`.

The rule validates exact EHP dimensions, Delta/E map types, all four generator
endpoints, both summand orders and independence, and the exact identity of the
killed versus surviving summand. The two group relations may be independently
admitted prior results; the four map and exactness statements must have
inferred `ProofStep` premises. Trust and provenance for any prior results
remain governed by the existing proof verifier.

## R4R3R2 maintenance fix

The preceding real R4 report was produced on `c77a26fdebe0eead67f1f7dad3a469aa446b134f`.
The current observed `develop` commit is `20622a303b8c4558fe297eed070b43ca2f322831`,
whose sole parent is the former commit. The intervening commit (`175-4`)
adds the R4 audit-only package and updates the already tracked pytest
`nodeids` cache. No mathematical source, proof engine or prior proof was
changed.

`audit.py` now verifies the Git object IDs, immediate parent and the **exact
nine path/status changes** before accepting the earlier real R4 report. Any
other commit or changed production source fails closed; this is not a generic
waiver of HEAD checks. The original report policy and mathematical result
checks are preserved.

## R4R3R1 maintenance fix

The only executable change from R4R3 is the pytest collection flag in
`run.ps1`. All rule code, source checks, assertion contracts and tests are
unchanged. No generated caches or test fixtures are bundled.

## Status

The confirmed Phase 175 R4 observation is:

- Target $\pi_9^5$: incomplete with three open goals and zero proved steps.
- Earlier $\pi_8^4$: complete and trust-verified.
- Toda Proposition 5.8 proof: supplies the planned $\Delta(\eta_9)$ and
  EHP quotient route; it is **not** registered as a direct target GIVEN.

**R4R3 does not prove $\pi_9^5$ in production.** It isolates the rank-two
quotient inference. Later work must connect independently proved source
relations, Delta image, EHP exactness, E surjectivity, and generator suspension
within the shared backward proof search.

## Files

- `rule.py` — the new typed general inference with a backward proposal API.
- `audit.py` — read-only source-pin and previous R4-report verification.
- `tests/test_rule.py` — six-premise math and fail-closed type contracts.
- `tests/test_audit.py` — previous R4 result and source-evidence contracts.
- `run.ps1` — focused pytest and isolated audit, DryRun or full audit.
- `AUDIT_PLAN_JA.md` — Japanese design and boundary record.
- `CODE_FULL_JA.md` — full replacement-ready code for all new modules/tests.
- `TEST_RESULTS_JA.md` — verification status and remaining obligations.

## Run on the local `develop` checkout

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\EHP_Phase175_R4R3R2_REVIEWED_R4_HEAD_LINEAGE_FIX.zip" -DestinationPath "." -Force
$runner = '.\phase175_r4r3_two_summand_quotient\run.ps1'
$r4 = 'C:\Users\oomae\AppData\Local\EHPProofTracerAudit\phase175_r4_pi95_audit\20261117T041315_004766Z\report.json'
powershell -NoProfile -ExecutionPolicy Bypass -File $runner -R4Report $r4 -DryRun
if ($LASTEXITCODE -ne 0) { throw 'R4R3 DryRun failed' }
powershell -NoProfile -ExecutionPolicy Bypass -File $runner -R4Report $r4
if ($LASTEXITCODE -ne 0) { throw 'R4R3 audit failed' }
git diff --check
git diff --stat
git status -sb
```

`run.ps1` sets `--import-mode=importlib` so tests with the same filename in
separate phase packages (such as two `tests/test_audit.py` files) are collected
under distinct import identities. The previous `prepend` mode caused an
`import file mismatch` before any mathematical tests were run.

`run.ps1` also disables pytest's cache provider and writes all audit reports under
`%LOCALAPPDATA%\EHPProofTracerAudit\phase175_r4r3_two_summand_quotient\`.
It never resets the user's working tree. It verifies the current R3-descended
`develop` HEAD and all 18 existing R4 Source PINs. The previous full R4 report must be from the same HEAD, or from the
one explicitly reviewed parent commit mentioned above. Ancestry, exact
committed diff, unchanged source pins and the original report contract are
all required.

Expected gates: `PASS_R4R3_ISOLATED_RULE_DRYRUN` and
`PASS_R4R3_ISOLATED_RULE_NOT_PUBLIC`. No full test suite is run in R4R3.
