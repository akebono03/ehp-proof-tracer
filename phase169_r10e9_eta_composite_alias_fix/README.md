# Phase 169 R10E9 — Typed Eta Alias in Composite Suspension Images

## Scope

This narrow patch makes the existing eta-family suspension inference accept the two already-validated names of one typed generator: Unicode-subscript notation from `HyoujiGen.csv` and the original underscore notation used by the cited Toda-family construction.

No mathematical source equation, inference rule, general group transport, direct-sum assumption, generator database record, renderer, or existing test is altered.

## Prerequisites

The local branch is `develop`, descendant from reviewed GitHub commit `940d1d1cc2e9943e9d2955c7204a4392984d65e9`, and R10E8 Chapter VI wiring has been successfully applied. The patch checks the Git blob hashes of its reviewed source and dependencies. It refuses an already modified eta module.

## Execute in PowerShell

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r10e9_eta_composite_alias_fix.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r10e9_eta_composite_alias_fix\run.ps1"
```

The script patches the complete `_eta_pair()` function in `phase165_r12_r21_eta_generator_chain.py` while retaining the original LF or CRLF style. It then runs focused tests only, followed by searches for the two previously partial 9-stem cases and one completed 8-stem control. The proof-search report is observational: an unresolved proof stays partial.

The entire updated module and function are exported under `output/`. Any failure restores the original bytes and previous output files. The full pytest suite is intentionally not run before Phase 169 closeout.
