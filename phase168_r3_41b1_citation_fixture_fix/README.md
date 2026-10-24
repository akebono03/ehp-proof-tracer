# Phase 168 R3-41B1 — Citation Test Fixture Repair

This is a self-contained replay of the Phase 168 R3-41B implementation with an independent fix for an existing citation-validation test fixture. It does **not** change the production citation validation logic or add mathematical inference rules.

The prior test changed the step citation number from 1 to 2 while retaining citation 1 in the model. The validator correctly rejected the reverse association first, yielding a message different from the test's expected missing-citation error. This package empties the citation list in that test only, preserving its original assertion and keeping a separate test for reverse-association validation.

The two production implementation replacements are byte-for-byte identical to R3-41B. A PowerShell runner backs up and repairs the existing test, captures four complete proof narratives, applies the R3-41B changes, runs focused pytest, and compares complete narratives byte-for-byte. Both the test fixture and the implementation files are restored on failure. Full pytest is not run.

Run `run.ps1` from PowerShell after extracting the package into the repository root. Outputs are in `output/`; complete modified files appear in `full_files/`.
