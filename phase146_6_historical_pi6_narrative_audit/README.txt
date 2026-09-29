Phase 146-6 Historical pi_6^3 Narrative vs Current Generic Audit

Historical baseline
-------------------
Commit:
908e24db89669750949fa9ad149f5e306ac05546

This is the Phase 136-2 state. It includes the Phase 136-1 prose improvements
and the Phase 136-2 structural contract for pi_6^3.

Why this baseline
-----------------
The current develop versions of the old Phase 134/136 tests were rewritten by
Phase 144-6 to assert the new generic route. They no longer preserve the old
text contract.

Git history shows the Phase 136-2 commit still contains explicit tests for:
- 2 eta_3 = 0 before the Toda bracket definition of nu'
- nu' membership in pi_6^3
- H(nu') = eta_5
- 2 nu' = eta_3^3
- an EHP-sequence introduction stating its purpose
- the short exact sequence around pi_6^3
- the final pi_6^3 = Z/4{nu'} conclusion

Method
------
1. Create a temporary detached git worktree at the historical commit.
2. Render the historical CLI Narrative there.
3. Render the current CLI Narrative in the current repository.
4. Compare exact text, line similarity, formula-line differences, and selected
   historical semantic contracts.
5. Write a unified diff to:
   phase146_6_historical_vs_current.diff
6. Remove the temporary worktree.

Production changes
------------------
None.

Existing test changes
---------------------
None.
