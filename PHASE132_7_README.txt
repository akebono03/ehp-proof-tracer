Phase 132-7 package

Purpose
-------
Connect Trace / Outline / Narrative to the existing group-proof CLI.

Modified source
---------------
main.py

Changed units
-------------
- import section
- build_group_proof_argument_parser()
- _run_group_proof_command()
- group-proof dispatch inside main()

New test
--------
tests/test_phase132_7_group_proof_cli_modes.py

CLI
---
Existing behavior remains the default:

python main.py group-proof 9 7

Equivalent explicit Trace:

python main.py group-proof 9 7 --mode trace

Outline:

python main.py group-proof 9 7 --mode outline

Narrative:

python main.py group-proof 9 7 --mode narrative

Depth is shared across all modes:

python main.py group-proof 9 7 --depth 2 --mode narrative

Apply
-----
python apply_phase132_7.py

Focused test
------------
python -m pytest tests/test_phase132_7_group_proof_cli_modes.py -q

Related regression
------------------
python -m pytest `
  tests/test_phase131_3_group_result_proof_replay.py `
  tests/test_phase131_4_group_result_proof_replay_cli.py `
  tests/test_phase131_5_web_group_proof.py `
  tests/test_phase132_4_group_proof_presentation.py `
  tests/test_phase132_5_group_proof_outline_renderer.py `
  tests/test_phase132_6_group_proof_narrative_renderer.py `
  tests/test_phase132_7_group_proof_cli_modes.py `
  -q

Do not run the repository-wide test suite until the end of Phase 132.
