# Phase 169 R10ET-R6 — Residual Definition Dependency Audit

This **audit-only** package checks whether the production R10ET-R5 search really eliminated eligible family-specific Definition dependencies from trusted Proof Trees. It never edits production code, tests, existing documents, or the Git index.

## Preconditions

- Windows PowerShell and Python/pytest available in the EHP Proof Tracer repository.
- Branch `develop`, descending from the inspected R4 commit `3a8014efb91ddf76060c4d07d73153e55ea52c75`.
- The exact R4 projection/renderer changes and the exact R5 provider/test changes must already be present (committed or uncommitted). All seven files are checked against inspected Git baselines and deterministic R5 transforms.
- Prior R10ET-R1 and R10ET-R2 audit packages and their reviewed baseline files are present. The R5D package with `patch.py` must be present.
- Existing staged audit packages are preserved exactly; no reset, checkout, add, or restore is executed.

## Run

From the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r10et_r6_residual_definition_dependency_audit.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10et_r6_residual_definition_dependency_audit\run.ps1"
git status -sb
```

Pass `-Probes off` to check only the required 16 cases. `-SkipTests` skips focused pytest, not the audit.

## What is checked

The 16 previously verified cases are evaluated by the **real production provider**, without monkeypatching. All must be complete, replay-trusted, and have no noncanonical `GeneratorImage` when the universal Definition applies. Each Proof Tree is compared with the independently reviewed R2 shadow baseline, including its actual citation locators, Definition image count, and root source/isomorphism citation ancestry. The ten stable-transport cases must use exactly the DB prior and Toda (4.5), with independent root support.

Three further completed-case probes (2-stem, 9-stem) are checked independently, without claiming that any finite audit proves all stems. Optional probes failing cause a review-required exit, not an assertion of a changed theorem.

A full Proof Tree trace and narrative Markdown are saved for each completed case. The script also verifies its exact source inputs and captures both staged and unstaged Git snapshots before and after the audit.

## Outputs

- `output/<timestamp>/audit.json`: machine-readable assessment, independent citation support and exact repository checks.
- `output/<timestamp>/audit.md`: Japanese summary and caveats.
- `output/<timestamp>/pi<q>_<n>/proof_steps.json`: indexed typed Proof Tree, its premises and citations.
- `output/<timestamp>/pi<q>_<n>/narrative.md`: the rendered certified proof.

The PowerShell runner executes focused pytest for the new pure helpers, R5 production proof tests, R10EQ universal Definition tests and R4 projection tests. **It does not run the complete suite.**

## Phase boundary

R6 is read-only. It neither deletes legacy source statements nor changes family registries. Any remaining dependency or newly discovered unsupported case must be reviewed in a separate, explicitly scoped implementation phase.
