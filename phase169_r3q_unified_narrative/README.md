# Phase 169 R3Q — Unified Reasoned Narrative

This patch removes the parallel prose path in the common Model renderer. Every proof step first uses the existing typed sentence projector; generic LaTeX fallback is used only when there is no typed sentence. The same rule projects Toda-specific and generic map-property statements from verified typed premises. No proof search, source assertions, references, or mathematical rules are changed.

Run `run.ps1` from the extracted package. Installation is guarded, idempotent, and writes full replacement files and functions into `output/`. Only focused pytest suites run.
