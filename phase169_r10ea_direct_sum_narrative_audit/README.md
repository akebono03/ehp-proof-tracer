# Phase 169 R10EA — Direct-Sum Narrative Audit

This is an audit-only package: it **does not change production source, existing tests, proof rules, citations, or the renderer**.

It repeats the canonical screened search and Trust Boundary replay for four concrete queries: `(n,k)=(13,9), (15,8), (15,9), (30,9)`. It then renders the same verified Proof Narrative Model and measures duplicated one-step suspension equations, typed image steps unsupported by the current element TeX projector, output length, proof-step counts, and actual citation locators. It stores the original verified text without abbreviating it.

## Windows PowerShell

From the root of the working checkout:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive `
  -Path "$HOME\Downloads\phase169_r10ea_direct_sum_narrative_audit.zip" `
  -DestinationPath "." `
  -Force
powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase169_r10ea_direct_sum_narrative_audit\run.ps1"
```

The runner checks a reviewed develop ancestor and exact unchanged Git blobs of the renderer, model, and verifier. It requires the already-installed R10E8 and R10E9 production fixes. Only the four named focused test files and this audit execute; **no full pytest** runs.

Outputs: `output/audit.json`, `output/audit.md`, and one `output/pi_<degree>_<n>.rendered.md` file for each successfully verified goal. A complete result that fails the Trust Boundary is never presented as a verified narrative; the audit reports the rejection and exits unsuccessfully.

This package is not a presentation patch. A later change may compress only rendered text after the audit establishes exactly which certified steps and source references it represents.
