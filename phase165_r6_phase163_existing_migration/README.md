# Phase 165 R6 — Phase 163 test input migration

This package changes only the test input providers for Toda Propositions 5.1, 5.3, 5.6 and adds standalone explicitly typed candidate fixtures. No production code is modified. Old derived-assertion and negative-generator tests remain intact. Backups are created before rewriting. Execute `run.ps1` from Windows PowerShell after extracting into the repository root. No full pytest is run.
