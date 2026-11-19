# Phase 175 R4R12R13R8R5R2 — Web Regression Audit Guard Correction

This patch corrects the read-only general reference binding audit. The previous audit incorrectly treated Python object equality between a literature source and its derived proof statement as a mandatory Web display condition. The proof may use a verified notation conversion, so such equality is diagnostic only.

The audit still checks the actual Web reference body and proof-body citation prefix for both Toda (5.11) and (5.8), plus the unchanged `generic-complete-proof` key. It retains diagnostic flags for typed equality. If there is an actual Web regression, the JSON report now records the completed target audits and the precise failing visible flags before exiting nonzero.

This package changes only audit.py and its focused tests, not any production code, mathematical rule, cited GIVEN, proof tree or renderer. Run from the repository root using run.ps1, first -DryRun and then normally. A report is stored in the Windows TEMP directory as EHP_Phase175_R13R8R5_general_binding_audit.json. Full-suite pytest is deferred until Phase closeout.
