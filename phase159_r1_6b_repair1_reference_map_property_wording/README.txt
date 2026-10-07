Phase 159-R1-6b repair1

Problem
-------
Toda (5.1) attribution is correct, but the Reference section still renders
the low-dimensional suspension isomorphism as:

  $E: ...$ は同型写像である.

The Phase 159 public formula-style contract requires:

  $E: ...$ は同型.

Cause
-----
The proof-body map-property normalizer intentionally operates only on the
proof body. Reference statements are rendered by the existing literature
Reference pipeline and retain low-level generic prose.

Fix
---
Add a public Reference-only normalizer. It changes only standalone
formula-style map-property lines between `## 使用する結果` and `---`.

Mappings:
- 単射である. -> 単射.
- 全射である. -> 全射.
- 同型写像である. -> 同型.
- 零写像である. -> 零写像.

Production:
- toda_group_proof_narrative_renderer.py

Tests:
- no changes

Full pytest:
- not run
