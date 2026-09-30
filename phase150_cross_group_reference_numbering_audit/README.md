# Phase 150 Cross-Group Reference Numbering Audit

Audit-only package. It changes no production code and no existing tests.

The audit separates three questions:

1. Does each visible proof step carry a `LiteratureReference`?
2. Does the generic reference-entry builder collect and number those references?
3. Does the Narrative body use numbered references, or does it still render
   theorem/lemma names directly?

Representative targets:

- `pi_6^3`
- `pi_8^5`
- `pi_10^4`
- `pi_12^5`
- `pi_15^8`
- `pi_16^9`

For `pi_10^4`, the audit prints each inference rule together with its actual
`LiteratureReference` metadata and prints the rendered Narrative. This
distinguishes missing metadata from missing body-to-reference binding.

No repository-wide test suite is run. That remains reserved for the end of
Phase 150.
