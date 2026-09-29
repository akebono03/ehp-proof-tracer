Phase 144-6-R5-43-11-R2
Visibility-aware R5-43 completion cross-group Narrative audit

Production code changes: none.

R2 repair:
The first audit assumed every selected ordered contribution could be located
with connected.index(rendered_line). That assumption was too strong for an
audit and caused ValueError before the audit could report what was missing.

R2 follows the actual renderer pipeline:
selected contribution
-> insertion index available
-> rendered line present exactly once
-> topological display order
-> before owning Argument conclusion

Missing rendered contributions are not ignored. They are counted explicitly
as missing_rendered_count and the completion test fails unless the count is 0.

Completion criteria:
- 6 representative groups
- 190 selected contributions
- 190 insertable contributions
- 16 transport connectors
- 0 missing rendered contributions
- 0 duplicate violations
- 0 order violations
- 0 conclusion-placement violations

No public route change.
No full test suite.
