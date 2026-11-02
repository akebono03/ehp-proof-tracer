# Phase 173 R4-R1 Narrative Prose Layout Fix

This package makes presentation-only corrections to the completed, source-verified public proof of pi_7^4.

## Scope

- Split sentences at periods into separate rendered lines.
- Cite Proposition 4.4 and Lemma 5.4 without presenting equation (5.6) as an independently registered source.
- Retain the verified isomorphism, but remove redundant wording and explicit generator-image sentences.
- Preserve all seven proof steps, four verified references, and the existing search interface.

## Apply on Windows

Unzip the archive into the repository root and run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase173_r4_r1_prose_layout_fix\run.ps1 -DryRun`. If it succeeds, rerun without `-DryRun`.

The installer verifies Git blobs, exact reviewed file contents, and dependency states. It writes recovery backups outside the repository before editing. The package also contains complete reviewed replacements for all four edited files. Full-suite tests remain reserved for the end of Phase 173.
