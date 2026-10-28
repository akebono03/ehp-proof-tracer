# R10ET-R6D: R6C-Aware Reviewed Production Certification

This package changes **only** `certify_reviewed_production()` in the untracked
R6 audit script. No production source, proof rule, provider, regression test,
or Git index is modified.

## Context

The original R6 audit expected the Git R4 renderer byte-for-byte. R6C
legitimately changed the Model and Renderer to limit complete-proof citations
to the ancestry of the verified root. The original R6 certification therefore
refuses the reviewed and tested R6C renderer before running any proof case.

## Verification

R6D independently validates the exact original R6 audit source and the exact
R6C transformation source. Its replacement certification compares both the
Model and Renderer with the precise transformations of their Git R4 content.
The R10A projection must still equal the reviewed R4 bytes. The R5D provider
and its related tests must still match the reviewed R5D transformations.
Unexpected changes are rejected; this is not a relaxed renderer hash check.

## Execution

From the repository root, extract `EHP_R10ET_R6D.zip` with `Expand-Archive`
and run `phase169_r10et_r6d_r6c_aware_certification/run.ps1`.

The script saves the original R6 audit, its full updated source and the whole
changed function outside the Dropbox repository under
`%LOCALAPPDATA%\EHPProofTracerRecovery\r10et_r6d_<timestamp>`.
It then runs the original R6 19-case audit and its focused pytest suite.
If either fails, it restores the original R6 audit script, without changing
any production file. It also refuses to overwrite an unreviewed R6 script.

## Success criteria

- `R10ET_R6_REQUIRED_PASS=True`
- `R10ET_R6_PROBES_PASS=True`
- `R10ET_R6_AUDIT_ONLY_COMPLETE=PASS`
- `R10ET_R6D_TRACKED_INDEX_PRESERVED=True`
- `R10ET_R6D_COMPLETE=PASS`

Do not run the entire test suite before the end of Phase 169.

Complete pre/post-change audit files and the complete updated function are
bundled in `reviewed_sources/` for direct inspection and replacement.
