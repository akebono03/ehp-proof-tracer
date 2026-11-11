# Phase 175 R3R1 — registered generator identity fix for `pi_7^3`

This corrects the isolated R3 Hopf-lift candidate filter for the actual
Toda (5.3) nu-prime notation versus the typed HyoujiGen database notation.
It does not alter any existing tracked production source, introduce a GIVEN
fact, or publish a group proof.

## What was observed

The original Phase 175 R3 audit passed its provenance checks and its focused
pytest suite, but returned `PHASE175_R3_HOPF_LIFT_CANDIDATES=0` and
`search_failed`. Consequently, the public Group query still reports
`generic-partial-proof`. This is not evidence that the group is unknown.

The original isolated rule required exact Python dataclass equality between
the database generator `nu' o eta_6` and the source-backed Hopf chain's
`nu-prime o eta_6`. The adopted (5.3) registers nu-prime using a decorated
Unicode generator, while the database registers the corresponding TeX code.
The existing `same_registered_group_presentation` identity check already
recognizes the two presentations through unique HyoujiGen factor IDs.

## Scope of this repair

- `rule.py`: complete replacement of `hopf_lift_inputs` and
  `expand_cited_hopf_lift`; they use the existing strict ID-checked
  `_same_generator` helper instead of object identity to match the input
  generator. Map dimensions, source and codomain, cyclic order and all three
  independently INFERRED premises remain mandatory.
- `audit.py`: complete replacement of `inspect_pi73` and reporting functions
  to show cited Hopf chain count, exact spelling matches, registered ID
  matches, preceding cyclic codomain schemas, and matched candidate pairs.
- `tests/test_rule.py`, `tests/test_audit.py`: regression tests and negative
  tests for unregistered, wrong or look-alike generators.
- `AUDIT_PLAN_JA.md` and `CODE_FULL_JA.md`: complete revised documents.

No other tracked source, historical main documentation, or Phase 175 R2
record is modified. Existing API signatures and the ordinary shared
provider are preserved.

## Run in Windows PowerShell

Extract `EHP_Phase175_R3R1_PI73_GENERATOR_ID_FIX.zip` into the repository
root, overwriting the earlier `phase175_r3_pi73_hopf_lift/` directory.
Then run the same `run.ps1` as before.

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
$ErrorActionPreference = 'Stop'
Expand-Archive -Path "$HOME\Downloads\EHP_Phase175_R3R1_PI73_GENERATOR_ID_FIX.zip" -DestinationPath "." -Force
$script = ".\phase175_r3_pi73_hopf_lift\run.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
if ($LASTEXITCODE -ne 0) { throw "R3R1 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File $script
if ($LASTEXITCODE -ne 0) { throw "R3R1 audit failed" }
git status -sb
```

## Success boundary

The isolated worker now reports five separate source-discovery counters.
`HOPF_LIFT_CANDIDATES>0` only means that a backward inference path has been
proposed, not that its premises were proved. `PASS_R3_PI73_ISOLATED_VERIFIED`
requires an actual complete proof and an independently accepted Trust Boundary;
`PASS_R3_PI73_HOPF_FRONTIER_RECORDED` records a legitimate incomplete search.
The public Web result will remain unchanged until a separately reviewed
provider integration. Whole-suite pytest is postponed until Phase 175 closeout.

The downloaded local verification of this package is only for the audit
contracts: real source-screened search must be run on the user's checkout.
