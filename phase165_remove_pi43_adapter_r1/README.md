# Phase 165: Remove the pi4^3-specific reverse adapter

This package removes the active import and call of `expand_existing_pi43_rules` in `shared_expansion_provider`, then removes its unused top-level module after checking for other top-level module imports. The old module is preserved as a non-importable text backup. Generic discovery, witness inversion, seeded premise generation, and typed proof checking are unchanged. Removal does not imply generic derivation is complete.

Run `run.ps1` from an extracted directory under repository root. Targeted tests only. This package does not change Goal, Statement or Rule registries.
