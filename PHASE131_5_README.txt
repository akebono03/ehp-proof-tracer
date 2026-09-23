Phase 131-5 package

Files:
- web_group_proof.py (new)
- tests/test_phase131_5_web_group_proof.py (new)
- apply_phase131_5.py (patches web_group_query.py, web_app.py, templates/index.html)

Run from repository root:
  python apply_phase131_5.py
  python -m pytest -q tests/test_phase117_web_group_query.py tests/test_phase117_web_app.py tests/test_phase131_3_group_result_proof_replay.py tests/test_phase131_4_group_result_proof_replay_cli.py tests/test_phase131_5_web_group_proof.py
