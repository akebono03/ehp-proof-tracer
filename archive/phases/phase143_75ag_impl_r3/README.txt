Phase 143-75AG implementation R3

R3 changes only the already-added semantic renderer branch:
- remove the undefined render_toda_scalar_latex call
- render integer modulus with str(statement.modulus)
- correct doubled LaTeX backslashes for \in and \pmod

No new import.
No inference/API/docs changes.
Focused tests only.
No full pytest.
