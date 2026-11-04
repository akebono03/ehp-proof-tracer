# Phase 173 R15R17 documentation checkpoint

This package creates **complete, reviewable copies** of all five canonical Markdown documents from the original tracked files, preserving historical content. `-DryRun` only writes full preview documents into `full_documents/`. Normal execution writes the same reviewed full documents back to the repository, and saves exact byte-for-byte backups in `original_backups/`. It does not run the project-wide pytest suite, stage changes, commit, clean, reset, or edit production Python modules.

The inputs are guarded by the actual 2026-11-04 GitHub `develop` document Blob SHA values, the reviewed branch ancestry, and local document cleanliness. A Git HEAD change that leaves the canonical document Blobs unchanged is accepted. A changed document, conflicting local edit, or staged edit is rejected.

The checkpoint explicitly records that browser MathJax/layout review and phase-end full pytest have **not** completed. It does not declare Phase 173 closed. Historical content is preserved. Once installed, the complete files can be reviewed under `full_documents/` and in the modified repository.
