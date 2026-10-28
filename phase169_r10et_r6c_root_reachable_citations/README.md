# R10ET-R6C — Root-reachable citations in completed proofs

This focused patch suppresses **unused alternative proof evidence** from the
citations and displayed text of a **completed** proof. The original search
result, all `ProofStep` objects, trust verification, canonical Definition
provider, and partial-proof evidence remain unchanged.

The observed defect was `pi_10^8`: the search record contained nine steps,
including an unused DB prior. The final proof used eight reachable steps.
The unused DB prior was incorrectly displayed as `[R1]`, followed by the
actual prior and Toda (4.5). The corrected completed proof should cite only
the reachable prior and (4.5), numbered `[R1]` and `[R2]`.

## Execution

From the repository root on Windows:

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_R10ET_R6C.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10et_r6c_root_reachable_citations\run.ps1"
git -c core.longpaths=true status -sb
```

Only HEAD `232a92883b0cb009762b437cbb3cc550f00ab6bd` on `develop` is
approved. The script checks the exact prior production blobs and the five
uncommitted R5D files, backs up both changed files **outside the repository**, 
executes focused pytest and re-audits all R6's 19 cases. On failure the two
files are restored from their exact original bytes.

Changed files: `phase168_r3_3_proof_narrative_model.py` (add
`root_ancestor_step_indices`, replace `build_proof_narrative_model`) and
`phase168_r3_5_model_renderer.py` (replace
`render_model_backed_narrative_markdown`). The only import added is inside
the changed renderer function. Full replacement Python files and complete
functions are exported to `%LOCALAPPDATA%\EHPProofTracerRecovery\r10et_r6c_*`.

The package adds a test file without modifying preexisting tests. No full
pytest suite runs; no commits, staging or Git reset occur. The R6 original
record is unchanged and is superseded by a successful R6C re-audit.
