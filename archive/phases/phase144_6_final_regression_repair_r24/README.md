# Phase 144-6 Final Regression Repair R24

## Target files

- `toda_group_proof_narrative_argument_multi_renderer.py`
  - `_toda_group_proof_narrative_argument_frontier_hidden_step_ids`
- `main.py`
  - `_run_group_proof_command`

## Production changes

R24 removes the obsolete blanket protection of second-level premises from the
Narrative frontier. Direct premises, transition steps and the Argument
conclusion remain protected.

The runner also verifies the actual local depth=2 boundary before touching the
CLI path. It proceeds only when depth=2 omits the `establish_definition`
Argument. In that state the renderer cannot reconstruct the missing definition
chain, so Narrative mode builds its presentation from the complete replay.
Trace and Outline retain the requested replay depth.

## Tests

No test files are changed.

The runner first executes exactly the two failed final-completion tests and
then the directly related generic-route, frontier-filtering, direct-premise,
semantic-suppression and Phase144-5 equation-reference tests.

No full suite is run.
