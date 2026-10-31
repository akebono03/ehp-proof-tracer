# Phase 171 Closeout R2 — Guarded full-document record update

This package creates five complete Markdown files from the reviewed existing
Git worktree files, preserving historical text. The complete files are exported
to a standalone ZIP and retained in the local recovery directory.

The only repository changes are the five canonical documents; this package
requires the already reviewed Phase 169 R3Z test correction from R1R1. No
production source, inference rule, proof tree, citation data or search behavior
is changed. No full pytest is run at R2.

The historical documents are not embedded in this package. They are recovered
from the checked-out Git worktree, compared to the pinned GitHub blob IDs, and
written in full to the `FULL_DOCUMENTS` recovery folder and its ZIP. This avoids
shippping partial replacement documents and preserves the original newline form.

Execute `run.ps1 -DryRun` and, after reviewing the output, `run.ps1`. The
installer refuses a different commit, unexpected tracked modifications, or a
missing R1R1 semantic fix. On focused test failure it restores document bytes.

**Formal Phase 171 closeout is pending:** Phase-end active-suite full pytest
will run only at the final gate, after this reviewed document update.
