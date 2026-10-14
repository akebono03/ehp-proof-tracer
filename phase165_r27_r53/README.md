# Phase 165 R27-R53 — Delay Legacy Group Imports

This installer changes only `toda_calculation_facade.py`, preserving its existing public functions. It moves imports needed solely by the legacy report API into those functions, so importing the facade for a typed partial-proof call does not eagerly import the legacy calculation stack. The two independent typed functions added in R50/R52 are preserved.

Run `run.ps1` in PowerShell after extracting the ZIP into the project root. The installer backs up the original facade and executes only installer-targeted pytest tests. No full test suite is run.

The four legacy `repository_*` modules are **not** deleted. Legacy report functions still call legacy calculation when explicitly invoked. Migrating and removing those APIs belongs to a subsequent R27 step.
