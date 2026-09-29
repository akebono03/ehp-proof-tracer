Phase 144-6-R5-39 R2

Audit-only repair. Production changes: none.

R1 failure:
Phase 39 tried to recover an owner occurrence only from the owner Argument
index/role stored in the Phase-38 contribution group. That recovery assumption
was too weak and raised StopIteration before the Phase-39 audit could run.

R2:
Re-select the owner occurrence from each contribution's occurrence rows using
the exact Phase-38 ordering rule:
1. direct provider anchor first;
2. shorter distance to the Argument conclusion;
3. earlier Argument index.

R2 then asserts that the reconstructed owner Argument index/role agrees with
the Phase-38 contribution group. This changes audit plumbing only.

Boundary:
- no production visibility rule;
- no production ownership rule;
- no renderer change;
- no ProofChain change;
- no production deduplication change;
- no expression-to-membership rule;
- no parity matcher change;
- no public route change;
- no dedicated pi_6^3 renderer removal.
