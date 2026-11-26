# Phase 178 R12R2

Display-only removal of repeated verified right-zero suspension composition prose.
The renderer retains the first equivalent typed equation and the later extended
zero image, with their original citation tags. The common base is not repeated
in the proof body when its verified formula remains in the source block and
all actual uses are covered. No mathematical rule, proof step or source is removed.

Run `run.ps1 -DryRun`, then `run.ps1`. The installer requires the reviewed R12R1
Git tree (or a descendant with exactly the same tree), synchronized develop and
no unrelated tracked edits. Dry run exports complete modified source. Actual
execution compares against the R12R1 preview and rolls back the renderer on failure.
The audit runs focused tests only and writes a report, before/after narrative and
display elision plan under LOCALAPPDATA/EHPProofTracerAudit. Full pytest is not run.
