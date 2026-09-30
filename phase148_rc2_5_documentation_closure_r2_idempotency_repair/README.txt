Phase 148 RC2-5 Documentation Closure R2

Fixes the idempotency-marker bug in the documentation updater.

R1 incorrectly used the first line of each append block as its marker.
For four Japanese documents that first line was `---`, so existing horizontal
rules caused false `Already updated` results. README.md was updated correctly.

R2 uses one exact unique Phase 148 heading per document.
- README.md is detected as already updated and is not duplicated.
- design.md, development_log.md, roadmap.md, and proof_records.md receive
  their missing Phase 148 closure sections.
- Each exact heading must occur exactly once.

Production changes: none.
Test changes: none.
Repository-wide pytest: NOT rerun.
