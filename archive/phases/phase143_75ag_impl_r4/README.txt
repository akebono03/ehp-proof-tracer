Phase 143-75AG implementation R4

R3 result:
- 32 existing related tests passed
- the four renderer tests reached ambient-group rendering
- all four failed because the real field is HomotopyGroup while
  render_toda_primary_group_latex accepts only TodaPrimaryGroup

R4 changes only the ambient-group portion of the already-added
TodaLemma510BracketModuloStatement renderer branch.

Instead of converting the type, it renders:
pi_{group_dimension}^{sphere_dimension}

directly from statement.ambient_group first-class fields.

No import changes.
No inference/API/docs changes.
Focused tests only.
No full pytest.
