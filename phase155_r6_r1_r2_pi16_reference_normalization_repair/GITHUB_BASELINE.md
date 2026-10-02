# GitHub baseline — Phase 155-R6-R1-R2

Repository: `akebono03/ehp-proof-tracer`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Re-inspected after the R6-R1 local failure:
- current/archived Reference rendering outputs,
- `使用する結果を先にまとめる.` usage,
- the Phase150 pi16_9 normalization test,
- renderer/wrapper history around `## 使用する結果`.

The user's local current output proves the remaining failure occurs at the old
section-heading assertion, before the exact Reference-name assertions.

R2 therefore narrows the old Phase150 test back to its stable contract:
normalized Reference presentation, not a frozen Reference selection.

No production code is changed.
No Phase156 functionality is implemented.
