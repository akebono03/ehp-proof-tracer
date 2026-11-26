# Phase 177 R17R4R1 — Proposition 2.5 suspension-elision display

Presentation only. The complete narrative renderer may omit a verified, uncited
branch of definitional suspension and equality transport if its only external
consumer is the actual typed unsigned Proposition 2.5 application. All proof
nodes, citations, root status and search order are retained. Shared, cited,
protected, incomplete or unrecognized branches stay visible. No regrouping of
the final Delta calculation is done in this stage (R17R4R2).

The reviewed baseline is develop `7d6b35deb2a5c3d8f6740844460a5bae41a206ce`.
Run `run.ps1 -DryRun` first, then `run.ps1`. The installer exports the complete
proposed renderer to the reported review file, preserves line endings, and
refuses unrelated tracked changes. It does not commit. The focused tests check
several valid dimensions, incomplete/cited/shared/protected branches and the
actual 43-step, 8-reference proof. Full pytest is intentionally not run here.
