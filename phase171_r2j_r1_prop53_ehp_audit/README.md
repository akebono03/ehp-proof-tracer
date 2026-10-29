# Phase 171 R2J-R1 — Read-Only Proposition 5.3 / EHP Audit

This package audits the next proof obligations after the source-cited Phase 171 R2I derivation of `H(nu' o eta_6) = eta_5^2`.

It verifies the adopted Toda Chapter V Proposition 5.3 statement, inspects the present typed registry and publication-order screening for the `pi_6^3` goal, observes the *independent* `pi_7^5` group search, reconstructs an H-to-Delta EHP exactness window from the adopted Proposition 4.2, and identifies the direction of the already implemented Hopf-surjectivity rule.

**This is an audit, not a proof of Hopf surjectivity or of the `pi_6^3` group structure.** The inspected `pi_7^5` search result and any database row are never inserted as a new GIVEN statement. In particular, the existing EHP rule that derives H-surjectivity *from* `Delta=0` must not be used to derive `Delta=0` *from* H-surjectivity.

## Changed files and code units

Production files: **none**.

New package files:

- `audit.py`: `hopf_map`, `delta_map`, `h_delta_exactness_goal`, `_source_claim_audit`, `_registry_prop53`, `_r2i_report`, `_pi75_status`, `inspect`, `_markdown`, and `main`.
- `tests/test_audit.py`: five focused test functions, including negative type validation.
- `run.ps1`: branch/file preflight, `-DryRun`, focused pytest with cache disabled, live read-only audit, and tracked-change verification.
- `__init__.py`, `tests/__init__.py`: package markers.
- `監査仕様.md`: Japanese scope and stop conditions.
- `CODE_FULL_JA.md`: the complete new Python modules and all test functions, with full imports.

No existing classes, functions, imports, project documentation or tests are modified. No postponed Phase 171 feature is introduced.

## Requirements

Run from an existing checked-out `develop` working tree of `akebono03/ehp-proof-tracer`. The R2I provider hook and its dependencies must already be installed, whether tracked or uncommitted. The existing working tree, including the R2H/R2I modifications, is preserved.

## Windows PowerShell

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R2J_R1_AUDIT.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r1_prop53_ehp_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r1_prop53_ehp_audit\run.ps1"
git status -sb
git diff --stat
```

Reports are written to `phase171_r2j_r1_prop53_ehp_audit/output/audit.json` and `audit.md`.

Only five focused tests in this package are executed, with pytest cache disabled. **The full suite is not executed.** The audit may report missing proof obligations without presenting them as passed mathematical derivations.
