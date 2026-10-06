Phase 159 R1-7c R4 proof-target show-phrase audit1

Purpose
-------
Audit the next unresolved public-display defect after exact-sequence duplicate
suppression:

  を示す.

The user has already specified that the proof target should not be followed by
this redundant phrase.

Scope
-----
This is an audit only.

The script renders the current public Narrative over:
  n=2..15
  k=0..7
  max_depth=2

This range is only a reproducible audit sample. It is not a permanent contract
about how many groups the project supports.

For every public occurrence of:
  を示す.

the audit prints:
- group label;
- line number;
- surrounding context.

It also reports:
- rendered output count;
- failed render count;
- affected output count;
- total occurrence count.

Production code changes: none.
Test code changes: none.
No full pytest.
