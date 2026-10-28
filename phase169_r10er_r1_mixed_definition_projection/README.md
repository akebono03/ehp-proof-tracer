# Phase 169 R10ER-R1 — Mixed Definition Image Projection

This package changes only the presentation of already verified direct-sum stable transport proofs. It neither introduces a proof rule nor modifies a mathematical statement.

It distinguishes individually cited generator-image derivations from direct zero-premise inferences under the pre-existing universal stable representative Definition. Each cited derivation must retain its own registered source; an image derived solely from the Definition does not acquire an invented literature citation.

## Execution

Extract the ZIP to the root of `akebono03/ehp-proof-tracer` on branch `develop` at one of the reviewed commits, then run `run.ps1` in Windows PowerShell. The script checks the exact source blob, performs a complete-function replacement, runs focused pytest with cache disabled, replays the trust gateway, checks live narrative output, and rejects unrelated tracked changes. On failure it restores only the modified projection file.

The package includes the complete replacement function in `full_functions/`, and the complete replacement file in `full_files/`. `patch.py` writes the same full output to a timestamped `output/` folder at execution. No full test suite is run.
