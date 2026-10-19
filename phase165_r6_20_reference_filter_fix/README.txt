Phase 165 R6-20 reference filter installer fix

The previous installer expected one exact whitespace-matching source block and aborted.
This version uses Python AST to find the unique 'boundary.component_key is None'
branch inside filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary.
It checks the branch still contains aggregate retention, then changes only that branch.
If the local implementation is different, it aborts without modifying files.
A timestamped backup is made before changes. Only targeted pytest runs.
The complete changed function is saved beside report.json as changed_function.py.
Do not run the full pytest until Phase 165 final closure.
