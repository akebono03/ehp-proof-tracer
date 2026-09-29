Phase 147 RC1-4 Repair R1

Runner-only repair.

Cause:
The RC1-4 audit script is located in a subdirectory and was executed directly,
so Python used that subdirectory as sys.path[0] and could not import repository
root modules.

Repair:
Temporarily set PYTHONPATH to the repository root before running the existing
RC1-4 audit and focused tests, then restore the previous environment.

Production changes: none.
Audit logic changes: none.
Tests changes: none.
