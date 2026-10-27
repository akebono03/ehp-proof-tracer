# EHP Proof Tracer — Phase 169 R10E4

## Purpose

Adopt explicitly stored earlier `sphere.csv` group structures as typed database premises, without requiring proposition-registration entries. Earlier means lexicographically smaller `(stem, sphere dimension)`: `source_k < target_k`, or `source_k == target_k and source_n < target_n`.

The database premise is independently distinguished from a fixed Toda theorem. The whole theorem bibliography and publication-order policy are unchanged. Matching registered proposition locators, when available, are *display annotations only*.

## Install and run

From the repository root on Windows:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r10e4_ordered_db_prior.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r10e4_ordered_db_prior\run.ps1"
```

Preconditions: `develop` with Phase 169 R10E2 applied, Python and pytest available, and the original `data/sphere.csv` and `data/HyoujiGen.csv` present. Phase R10E3 is optional.

Only three existing files are changed. The installer first saves exact byte-for-byte backups, writes whole replacement files and whole replacement functions into `output`, executes focused tests, and audits selected actual proof queries. On any failure it restores only those three files, preserving preexisting user edits to them. No Git reset, checkout, or commit is performed. It never invokes the full pytest suite.

## Trust and limitations

A database row is an *adopted prior datum*, not independently proved mathematics. The `GIVEN`-like assumption must be re-read from an **explicit** database row, match the requested typed statement exactly, and strictly precede the original proof target in `(k,n)`. Generated stable-range fallback rows are not accepted as independent premises. Such a premise is labeled `DB prior: sphere.csv (n=..., k=...)`, optionally with a separately matched reference locator.

The existing complete-proof verifier independently repeats the database-content and ordering checks; arbitrary forged `GIVEN` steps are still rejected. This makes the result a database-relative proof. To remove dependence on the adopted datum, prove or replace the base result with an independently sourced proposition. The general Toda (4.5) theorem, composition and generator-image premises still require their existing proofs.

## Artifacts

`output/audit.json` and `output/audit.md` show stable-base presence, selected DB premise and actual proof status. A change to this policy does not automatically complete an unsupported generator family, an uncited unstable base group, or a group missing from the database.
