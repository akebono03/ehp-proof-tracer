Phase 159 R1-7c R4 map-property "である" audit1

Purpose
-------
Audit the next unresolved public-display defect candidate after confirming that:
- proof-target "を示す." has no current public occurrences;
- display-math period handling has no true missing-period blocks.

The user previously preferred concise map-property prose such as:

  H は単射。(1)
  H は全射。(2)
  (1), (2) より H は同型。

rather than:

  H は単射である。
  H は全射である。
  H は同型である。

Scope
-----
Audit only.

The script searches current public Narrative output for:
- は単射である.
- は全射である.
- は同型である.

Range:
  n=2..15
  k=0..7
  max_depth=2

This range is a reproducible audit sample and not a permanent group-count
contract.

For each occurrence the audit prints:
- group label;
- line number;
- exact public line.

Production code changes: none.
Test code changes: none.
No full pytest.
