# Unified Rule Registry R3-2

Read-only static mapping of non-R8 expansion provider functions and their directly referenced inference-rule factories. This package depends on the R3 inventory package already installed at the project root. Run `run.ps1` from the repository root on Windows.

Reports are written to `reports/provider_rule_mapping.json` and `.md`. Direct AST references are not proofs of mathematical correctness, recursive reachability, or equivalence of inference rules. No production modules are changed. Only targeted tests are run.
