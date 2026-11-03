# EHP Proof Tracer — Phase 173 R4-R15R6

## Purpose

This package adds a **separate, source-first, typed abstract group consequence** of Toda Proposition 4.4 for the registered $n=4$ family. It is intentionally independent of the names of individual generators. It does **not** change the existing strict generator certification, public Group query, renderer, or registered database.

The uniform specialization is

$$
\pi_{k+4}^{4}\cong\pi_{k+3}^{3}\oplus\pi_{k+4}^{7}
$$

where the source proposition, its Hopf condition, and two genuinely earlier database priors must be justified. At $k=31$, the abstract statement has eight cyclic factors of order 2. This is **not** certification of any of the eight named target generators.

## Scope and changed files

Only new files are added under `phase173_r4_r15r6_abstract_toda44_rule/`:

- `abstract_rule.py`: immutable abstract statement, canonical structural condition, guarded inference rule, screened backward expansion.
- `audit.py`: deterministic read-only summary for $k=3,4,7,8,31$.
- `preflight.py`: current `develop` lineage, Git blob checks, reviewed previous package checks.
- `run.ps1`: DryRun, focused tests, and JSON audit.
- `tests/test_static.py`: isolated package safety tests.
- `tests/test_integration.py`: typed real-repository inference replay and negative contracts.
- `SOURCE_CODE.md`: all added Python functions/classes/imports and complete test contents.
- `design.md`: full Japanese design and Phase boundary.

## Preconditions

Use the checked-out `develop` branch of `akebono03/ehp-proof-tracer`, with `origin/develop` in sync. Baseline reviewed HEAD: `1f46799f0673df0de880830b37bea7071cba64b8`. Only an additional commit that contains the previous R15R5 audit package (and the pytest cache node list) may follow this baseline. All mathematical dependencies are pinned to their reviewed Git blob IDs.

R15R1 through R15R5 must already be installed. The R15R5 source modules are independently pinned by normalized SHA-256, so a modified or mismatched audit cannot be silently accepted.

## PowerShell

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\EHP_Phase173_R4_R15R6_ABSTRACT_TODA44_RULE.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r6_abstract_toda44_rule\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw "R15R6 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r6_abstract_toda44_rule\run.ps1"
if ($LASTEXITCODE -ne 0) { throw "R15R6 failed" }
git status -sb
git diff --stat
```

## Proof security and expected output

The inference rule has **four genuine proof obligations**: source-screened Proposition 4.4, two admitted earlier DB relations, and a typed Hopf identity derived from source-screened Lemma 5.4. The package does not produce a GIVEN statement, attach unaudited citations, or install a public proof provider. The focused tests construct test-only leaves to exercise the inference rule's contract; that replay is not itself a live, source-screened public proof.

On a successful regular run the report `abstract_toda44_report.json` must contain a $k=31$ abstract tuple of eight `("finite", 2)` entries; the strict named generator guard remains false. Expect:

```text
PHASE173_R4_R15R6_SOURCE_GUARD=PASS
PHASE173_R4_R15R6_FOCUSED_PYTEST=PASS
PHASE173_R4_R15R6_K31_ABSTRACT_RULE=PASS
PHASE173_R4_R15R6_AUDIT=PASS
PHASE173_R4_R15R6_PUBLIC_COMPLETION=False
```

The full pytest suite is reserved for Phase 173 closeout.
