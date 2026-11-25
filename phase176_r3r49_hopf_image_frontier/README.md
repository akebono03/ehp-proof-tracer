# Phase 176 R3R49 — Hopf Image Proof Frontier Audit

Read-only audit after R3R48. No existing production file, source registration,
mathematical rule, database row, or renderer is modified. Requires the R3R48
patch installed on develop, with reviewed dependencies matching the GitHub
baseline 58a40dc8ca53fdd8b7b7f73139fe111627997056.

The real Web group query (n=3,k=5) is observed without altering provider results.
The actual DB generator is taken from its root. Compare the exact Hopf goal
with a control obtained from the screened (5.3) source, keeping the right
composition and target fixed. The strict nu-prime alias predicate is only an
audit probe. Each control uses a fresh ordinary shared provider and the real
citation context; no injected proof, alias, or extra provider is used.
Standalone subgoal replay is not evidence that the Web root is complete.

`run.ps1 -DryRun` checks the R3R48 installation and dependency pins; ordinary
`run.ps1` runs four focused test files and writes the detailed audit to
`%LOCALAPPDATA%/EHPProofTracerAudit/phase176_r3r49_hopf_image_frontier/report.json`.
The report records both success and unresolved standalone goals, provider
calls, plan lengths and screened source availability. PASS means the audit
ran and the R3R48 kernel/injectivity were preserved, not that the Hopf goal or
root was proved. No full pytest is run.
