# Phase 165 R27-R23-R2 terminal-branch installer fix

This installer changes only `main.py` to migrate the default CLI group query and the CLI `group-proof` command to the common registered Backward Search. It preserves unrelated CLI subcommands and makes no changes to the original theorem registry. It removes an overly strict AST statement-type check in the previous installer; the unique `build_argument_parser()` call remains the guarded boundary for the terminal default branch.

Run `run.ps1` in this extracted directory from the repository root. The script runs the targeted CLI tests and installer tests, not the full suite. A backup of the existing `main.py` is written to this directory before modification.
