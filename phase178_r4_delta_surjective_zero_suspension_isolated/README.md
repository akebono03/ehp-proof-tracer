# Phase 178 R4 — Isolated Delta surjectivity

The conditional typed EHP rule derives surjectivity of $\Delta$ from a proved $\Delta$–$E$ exactness window and a proved zero image of the following suspension. Both premises must be INFERENCE steps. No new GIVEN, public hook, group-specific path, or saved proof is added. The rule checks dimensions and uses the existing `MapSurjective`, `ImageZeroStatement`, and Proposition 4.2 specialization vocabulary.

Extract at the repository root and run `run.ps1 -DryRun` and then `run.ps1`. The runner requires clean tracked files, develop synchronized with origin/develop, ancestry from the reviewed base and unchanged dependency blobs. It runs only the new isolated tests and two existing focused regression tests. No public search or full pytest is performed. Tests use explicitly hypothetical premises only; success is not a proof of the actual target group.
