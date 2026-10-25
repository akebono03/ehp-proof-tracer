# R3-X launch repair

Replace only `phase166_r3x_trace/run.ps1` in the existing project. Run from the project root. Uses `python -m` to resolve root-level imports. Does not change production code or the diagnostic logic.


<!-- PHASE166_HANDOFF_20261021 -->
## Phase 166 handoff (2026-10-21)

Phase 166 implementation work is stopped and handed over with an unresolved test-collection boundary. This is **not** a full-suite PASS certification.

The database-backed typed group goal and the public Web adapter were checked in targeted audits. For $\pi_5^3$, the public Web view rendered the intended goal but returned `generic-partial-proof`, `partial_result=true`, and zero proven steps (R3-AU-12: three targeted tests passed). A displayed goal is not a proof.

Repository-wide pytest attempts were interrupted by historical patch/install modules collected as tests, retired test-helper imports, and Windows command-line length limits. The Phase 165 active test baseline (`python -m pytest tests -q --tb=short`, 3525 passed on 2026-10-19) must not be confused with a Phase 166 whole-repository result.

Phase 167 will first audit and repair the proof narrative for $\pi_4^3$, then investigate why $\pi_5^3$ remains partial. See `docs/roadmap.md`, `docs/design.md`, `docs/development_log.md`, and `docs/proof_records.md`.
