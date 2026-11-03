# EHP Proof Tracer — Phase 173 R4-R15R5

This package performs a **read-only source-definition frontier audit** of the remaining named suspension images for $\pi_{35}^{4}$. It does not install a theorem, create a new `GIVEN` premise, modify production source files, alter the Web search, or certify a group proof.

## Prerequisites

- The `develop` checkout of `akebono03/ehp-proof-tracer`, based on reviewed commit `0fc543a0d12e5fac0b2a3d842a2cf9187fd6d49c`.
- The previously installed Phase 173 R4-R15R1 through R4-R15R4 packages.
- Python and pytest available as `python -m pytest`.
- The checked-out `develop` branch and `origin/develop` must match. A subsequent commit containing only the previous R15R4 package is accepted if the pinned source files remain unchanged.

## Files

- `source_scan.py`: scans the adopted Toda `.tex` files for possible explicit family suspension formulas. Text matches are **not mathematical proof**.
- `audit.py`: correlates missing source families with the actual R15R4 generator-image proof frontier.
- `preflight.py`: verifies repository lineage, Git blobs, and the exact previous audit implementation.
- `run.ps1`: performs DryRun or read-only focused verification and writes the JSON audit result.
- `tests/test_static.py`, `tests/test_scan.py`, `tests/test_integration.py`: independent and repository-backed tests.
- `SOURCE_CODE.md`: full source code and complete new tests.
- `design.md`: complete design notes in Japanese.

## Windows PowerShell

Download `EHP_Phase173_R4_R15R5_FAMILY_SOURCE_FRONTIER.zip` and extract it in the repository root:

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\EHP_Phase173_R4_R15R5_FAMILY_SOURCE_FRONTIER.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r5_family_source_frontier\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw "R15R5 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r5_family_source_frontier\run.ps1"
if ($LASTEXITCODE -ne 0) { throw "R15R5 failed" }
git status -sb
git diff --stat
```

## Output and pass criteria

The regular run creates `family_source_frontier_report.json` in this package directory. It must retain four candidate left-side named images, one independently replayed image, three unresolved candidate images, and missing cited family IDs 56 and 88. It captures source files, content hashes, and possible source text hits without treating hits as verified citations. The public proof remains incomplete.

Only focused tests are run. The full pytest suite belongs to the end of Phase 173.
