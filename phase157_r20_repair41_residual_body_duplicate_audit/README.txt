Phase157-R20 repair41 runtime audit

Purpose
-------
Audit the remaining visible pi_6^3 Narrative defects after repair40.

Current focused/regression status
---------------------------------
- repair40 focused: 9 passed
- Phase157 Narrative regression: 43 passed
- Phase156 Reference regression: 12 passed

Visible residuals
-----------------
The final pi_6^3 body still contains:
- repeated H(nu') = eta_5 statements;
- repeated tagged equations;
- empty connector paragraphs;
- a late repeated Delta = 0 conclusion.

This audit does not change production code.

It reports:
1. final watched paragraphs;
2. duplicate normalized public-display keys;
3. whether re-running reference-body duplicate suppression changes the body;
4. whether re-running reference-body restatement suppression changes the body;
5. whether re-running connector normalization changes the body;
6. whether re-running reflexive suppression changes the body;
7. occurrence counts for the watched residuals.

The goal is to identify whether these paragraphs are:
- reintroduced after an existing suppression pass; or
- outside the current suppression contract and need a new generic rule.

No pytest is run.
