Phase 145-1 Repository Cleanup

Audited develop HEAD:
3bcb84fe687ace64f15859df1f9dcb5da7113266

Scope:
- Delete only clearly named tracked backup artifacts.
- Never delete tests/.
- Never delete docs/development_log/ or docs/proof_records/ archives.
- Never delete README.md, docs/design.md, docs/development_log.md,
  docs/proof_records.md, or docs/roadmap.md.
- Do not change production code or existing tests.

The PowerShell runner first performs a dry run and requires the literal answer YES
before applying deletions.
