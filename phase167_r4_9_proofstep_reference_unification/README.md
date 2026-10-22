# Phase 167 R4-9 — ProofStep Reference Connection

This package modifies only `link_toda_group_proof_narrative_reference_body_consumers` in `toda_group_proof_narrative_contribution_renderer.py`. It preserves the existing reference catalog, reference text, and downstream formatting.

The previous renderer-level mathematical re-specialization check (`specialize_typed_statement`) is removed. A visible inference with exactly one actual cited GIVEN premise can receive that premise's reference marker. No statement-type special cases or rule-name string checks are introduced. If the proof lacks an actual edge or the visible line is ambiguous, no reference is invented.

The script backs up the original file before writing, and saves the complete replacement function to `modified_function_full.py`. It runs focused tests only; the full test suite remains out of scope until phase completion.

This is a narrowly scoped replacement of the direct-consumer branch. It intentionally preserves legacy handling for exactness, multiple-premise reasoning, and later rendering stages; their consolidation is not part of this patch.

## Apply on Windows PowerShell

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase167_r4_9_proofstep_reference_unification.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase167_r4_9_proofstep_reference_unification\run.ps1"
```
