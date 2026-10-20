# Phase 166 R3-Q Web Publication Order Connection

This package connects the ordinary registered-group Web proof search to the publication-order boundary already stored in the Unified Statement Registry.

It changes only `search_group_from_registered_goal()` in `phase165_r55_nk_only_goal.py`. The selected registered target assertion is passed to the existing shared search as `citing_assertion_id`, so the existing `typed_reference_publication` lookup and `precedes_citing_assertion()` comparison are used.

No completed proof is imported. No pi5^4-specific proof path is added. No renderer is changed. Existing source IDs, mathematical statements, and ProofStep links are preserved.

Run from the repository root after extracting the ZIP:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase166_r3q_web_publication_order.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase166_r3q_web_publication_order\run.ps1"
```

The runner executes only the R3-Q targeted tests and the existing pi3^2 Web regression tests. Full pytest is intentionally not run; it remains the Phase 166 closing gate.
