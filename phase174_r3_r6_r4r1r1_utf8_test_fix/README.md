# Phase 174 R3-R6-R4R1R1 UTF-8 Test Fix

This package corrects two implicit-encoding `.read_text()` calls in one already-reviewed test function. The correction makes UTF-8 explicit on Windows CP932 environments. It does not modify production code, the proof search, GIVEN assertions, or Renderer behavior.

Run `run.ps1 -DryRun` first, then `run.ps1` using PowerShell. The script refuses any unreviewed HEAD or prior production changes, preserves LF/CRLF and optional BOM, and runs only the previously selected focused tests plus its own five guards. The full test suite remains deferred until Phase 174 closeout.
