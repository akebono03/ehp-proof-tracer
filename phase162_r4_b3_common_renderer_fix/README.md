# Phase 162 R4-B3 common renderer fix

This patch adds a narrowly scoped ProofStep-based rendering path to the existing common baseline renderer, for the concrete eta-family stable transport derivation built in Phase 162 R4-B2. It uses the actual derived root, finite-cyclic transport, Toda (4.5) isomorphism and generator definition premises. It does not append text to an existing narrative. All other roots retain their existing code path.

Run the PowerShell script from the repository root after extracting the zip. The script creates a backup and runs focused tests only.

Known boundary: This does not change the public stable-specific renderer, clean up all historical baseline prose paths, or generalize generator normalization beyond eta-family 1-stem. Do not run the full suite before the end of Phase 162.
