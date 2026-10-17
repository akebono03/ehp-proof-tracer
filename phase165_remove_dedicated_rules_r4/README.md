# Phase 165 R4: Remove dedicated pi4^3 rules

Run `run.ps1` from the repository root. This removes only six named pi4^3-specific inference factories and their catalog entries. It also removes obsolete test functions that explicitly call those deleted factories, preserving unrelated tests in the same files.

The installer validates source syntax and live root references before writing. It preserves original modified files under `phase165_remove_dedicated_rules_r4/backups/` for recovery. The installer does not create generic replacements, does not prove pi4^3, and never runs the full test suite.

GitHub main may differ from the local working tree. A blocked status signals that live references or unexpected layouts require manual review. Historic archived code and probes are intentionally untouched.
