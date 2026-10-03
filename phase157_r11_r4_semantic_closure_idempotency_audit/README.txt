Phase157 R11-R4 — semantic closure idempotency/origin audit

R11-R3 repair2 established:
- E: pi_4^2 -> pi_5^3 is absent through reason prose and appears only in final output.
- pi_6^5 = Z/2{eta_5} exists from base markdown onward.

The public renderer rebuilds semantic closure at entry.
R11-R4 checks whether applying semantic closure to an already closed
presentation changes:
- node count;
- edge count;
- generic narrative;
- target statement visibility.

It compares:
1. generic output after one closure;
2. generic output after two closures;
3. public renderer from raw presentation;
4. public renderer from already-closed presentation.

Production code changes: none.
Test code changes: none.
pytest: not run.
