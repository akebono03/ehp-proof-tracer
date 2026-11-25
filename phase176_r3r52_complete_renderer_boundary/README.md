# Phase 176 R3R52 — Complete proof and renderer boundary audit

Read-only audit of the R3R51 completed public proof. Requires the exact R3R51 patch applied on the develop branch, and reviewed renderer files from e008b994ee1750c080a1dcbdfa646d54fda83a1b.

- `run.ps1 -DryRun`: checks the local applied patch and reviewed renderer hashes.
- `run.ps1`: runs three focused suites in separate processes and observes the actual public search, trust boundary, linked model, typed sentence projection and Web view. No production source is edited. No proof or display value is substituted.
- The existing incorrect integer-brace rendering of the finite kernel is an expected finding, not a claim that the renderer is correct. A missing finding stops the baseline audit for review.
- Output: `%LOCALAPPDATA%/EHPProofTracerAudit/phase176_r3r52_complete_renderer_boundary/report.json` and `actual_narrative.md` and `partial_prefix_narrative.md`. The report includes the exact accepted proof ancestry, trust-gate counts, citation bodies, and display diagnostics. The partial narrative is a display-only projection of the accepted search prefix before the lift; it is not a second search result.
- No full pytest, new mathematical rule, source registration, or rendering fix in this phase. R3R53 will address the kernel projection.
