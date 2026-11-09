# Phase 174 R3-R7-R31: General Delta Surjectivity Audit

This package performs a read-only, source-first mathematical and typed audit of the missing hypotheses behind the general Delta-surjectivity inference. It does not install any proof rule, register a GIVEN, or claim that the root proof is complete.

## Requirements

- Windows PowerShell, Python 3.10 and pytest.
- The `akebono03/ehp-proof-tracer` repository, branch `develop`.
- The reviewed remote HEAD `25118e281445ca17b30c60c8fd02d00acaa25ea5`.
- Either the reviewed R30 handoff at local HEAD `42025c9fb7198f766d3e09531e35bfe04142ceb7` with its exact source changes present, or the merged R30 checkout at the reviewed remote HEAD.

Extract the ZIP at the repository root. The archive adds only `phase174_r3_r7_r31_delta_surjectivity_general_audit/`.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r31_delta_surjectivity_general_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r31_delta_surjectivity_general_audit\run.ps1"
```

The script does not run `git reset`, `git checkout`, `git pull`, or modify production source files. It verifies reviewed source blobs and runs selected pytest groups separately. The report is saved under `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r31\`.

A passing gate means **only that the conditional inference and missing premises were audited**. Neither Delta surjectivity nor the zero-group result is certified. No full pytest run is performed during R31.
