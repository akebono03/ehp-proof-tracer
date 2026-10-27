# EHP Proof Tracer — Phase 169 R10E8-R1 HEAD Guard Refresh

This package corrects **only the Windows execution guard** of Phase 169 R10E8. The original R10E8 implementation, production patch, and focused tests are bundled unchanged under `phase169_r10e8_hyoujigen_generic_suspension/`.

The original runner rejected the user's `develop` commit `2ccc356113f0322511c37b37929ecd8952498646` because its expected HEAD was `c3573d29e21688f54e73cf4d51ad53a5591d7959`. GitHub comparison confirms that this intervening commit added only the R10E7 audit artifacts. A subsequent reviewed commit `940d1d1cc2e9943e9d2955c7204a4392984d65e9` added only the unchanged R10E8 package. Neither commit modified the two R10E8 production patch targets.

The new, separate `phase169_r10e8r1_head_guard_refresh/run.ps1` accepts **only those three reviewed HEADs** on `develop`. It independently checks both exact Git blob IDs, rejects locally modified patch targets, runs the unchanged R10E8 guarded patch, executes focused tests only, and audits the two target groups. It restores the original production-file bytes after failure. It does **not** modify the existing R10E8 runner and does not remove its source review guard.

## Run from the repository root (PowerShell)

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r10e8r1_head_guard_refresh.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r10e8r1_head_guard_refresh\run.ps1"
```

## Scope and acceptance

- Patch targets: `phase169_r10d2_general_family_definition/family_citation.py` and `phase165_r52_r9_shared_math.py`.
- Unchanged R10E8 reusable components: `source_records.py`, `chapter_vi_reference.py`, `patch.py`, `audit.py`, focused tests.
- Focused tests: R10E8, R10D2, R10E5, and R10E4.
- All-source pytest is deliberately **not** run until Phase 169 closeout.
- Completion means the source guard, limited tests, and audit run without errors. The audit may report `partial` without treating it as a proven result.
- If the checkout has a HEAD outside the approved list, the runner fails closed. Review that commit and its relevant blobs before authorizing another HEAD.
