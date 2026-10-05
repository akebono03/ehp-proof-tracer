Phase157-R20 repair9 Reference pipeline audit

Purpose
-------
Do not make another speculative production change.

The previous repairs established:
- target-specific pi_6^3 Narrative helpers are absent;
- Proposition 2.2 -> Equation 5.7 proof dependency works;
- eta canonicalization executes;
- Proposition 5.3 still disappears from the public Reference section.

This audit prints exactly where Proposition 5.3, Proposition 5.1 and
Proposition 2.2 appear or disappear in the current cumulative local tree.

Stages
------
1. presentation nodes / consumer edges
2. raw Reference entries
3. fixed-statement boundary filter
4. Reference statement-line construction
5. root-reference exclusion

No production code changes.
No test changes.
No documentation changes.
No pytest.
