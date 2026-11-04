# Phase 173 R4-R15R13: Unified Proof Presentation

One status-independent presentation contract for complete and incomplete group proofs.

The canonical ProofNarrativeModel and its Markdown API are unchanged. The single common Web parser applies a source-independent layout policy: one Reference heading, one section boundary, the existing Web-owned Proof heading, and no duplicated target heading. It never changes proof steps, citations, search status, or mathematical inference.

Run `run.ps1 -DryRun` before `run.ps1`. Both enforce an exact `develop` HEAD and a source blob guard. The installer modifies one production function with a reversible byte-level backup. Focused pytest is run only after installation. Full pytest is deferred until phase closeout.

The audit intentionally does not modify math rendering of unresolved goals or Python diagnostic strings; those remain separate work.
