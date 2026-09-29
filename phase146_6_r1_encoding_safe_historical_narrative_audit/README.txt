Phase 146-6-R1 Encoding-Safe Historical Narrative Audit

Baseline:
  Phase 136-2 commit 908e24db89669750949fa9ad149f5e306ac05546

Purpose:
  Re-run the historical-vs-current pi_6^3 Narrative comparison without the
  PowerShell text-pipeline encoding ambiguity seen in Phase 146-6.

Method:
  - Create a temporary detached worktree at the historical commit.
  - Capture historical and current CLI output using .NET Process redirection
    configured explicitly for UTF-8.
  - Write UTF-8 without BOM.
  - Decode both files in Python with errors='strict'.
  - Compare semantic contracts after whitespace normalization.
  - Write a UTF-8 unified diff.

Semantic contracts checked:
  - 2 eta_3 = 0
  - Toda bracket definition of nu'
  - ordering: 2 eta_3 = 0 before the bracket
  - nu' membership in pi_6^3
  - H(nu') = eta_5
  - 2 nu' = eta_3^3
  - EHP purpose prose
  - five-term EHP sequence
  - short exact sequence
  - final pi_6^3 = Z/4{nu'}

Production changes: none.
Existing test changes: none.
