# Phase 171 Closeout R2R3 — byte-preserving documentation correction

This package fixes a documentation writer that rejected existing `CRCRLF` (`\r\r\n`) line endings in `docs/design.md`. It does not change the mathematical proof search, source registry, citation rules, or Web renderer.

The reviewed `develop` repository contains mixed historical line endings. The correction normalizes repeated CR followed by LF **only for content comparison** and builds complete revised documents by preserving the original bytes and inserting/appending the reviewed Phase 171 section. Bare CR without LF remains rejected.

Run `run.ps1 -DryRun` before `run.ps1` from the repository root after extracting the ZIP. Both review the actual R2 source and test bytes, the five documents' committed Git blob IDs, the reviewed appendices, the branch, and the worktree changes. The real run backs up files under `%LOCALAPPDATA%\EHPProofTracerRecovery`, applies two reviewed Python-file replacements, executes focused pytest, and runs the original five-document writer. It restores prior source and document bytes on failure.

The full Phase-end pytest is **not** executed by this package. The five full revised Markdown files are saved under the recovery report directory after successful execution.
