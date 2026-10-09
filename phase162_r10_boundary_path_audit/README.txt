Phase 162 R10 - (5.3) reference boundary ancestry audit

Scope: read-only. No production file edits. No full pytest.

From repo root:
Expand-Archive -Path "$HOME\Downloads\phase162_r10_boundary_path_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase162_r10_boundary_path_audit\run.ps1"

Output: phase162_r10_boundary_path_audit.json

This checks the active group-root tree, the Phase 58 H(nu-prime)=eta5
witness, candidate Lemma 5.2 nodes, and the existence of R9 files at
repository root or tests directory. It does NOT claim reference boundary
is already implemented. The JSON contains concrete steps and premise links.

Interpretation:
- same_conclusion_in_final_tree proves matching repr only, not identity.
- hopf_witness_lemma52_nodes identifies rule names in the source ancestry.
- If R9 files are located in a nested package, report them separately.
- Validate R9's graph and text after these concrete paths are identified.
