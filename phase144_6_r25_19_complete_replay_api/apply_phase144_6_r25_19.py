from pathlib import Path

REPLAY = Path("toda_group_result_proof_replay.py")
MAIN = Path("main.py")

REPLAY_ANCHOR = """def build_toda_group_result_proof_replay(
  group_result: TodaGroupResult,
  max_depth: int = 1,
) -> TodaGroupResultProofReplayResult:
"""

COMPLETE_FUNCTION = """def build_complete_toda_group_result_proof_replay(
  group_result: TodaGroupResult,
) -> TodaGroupResultProofReplayResult:
  if not isinstance(
    group_result,
    TodaGroupResult,
  ):
    raise TypeError(
      "group_result must be a TodaGroupResult"
    )

  provenance = (
    extract_toda_recursive_proof_provenance(
      group_result
    )
  )
  max_depth = max(
    node.shortest_depth
    for node in provenance.nodes
  )

  return build_toda_group_result_proof_replay(
    group_result,
    max_depth=max_depth,
  )


"""

IMPORT_OLD = """from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
"""

IMPORT_NEW = """from toda_group_result_proof_replay import (
  build_complete_toda_group_result_proof_replay,
  build_toda_group_result_proof_replay,
)
"""

R25_17_CALL = """      narrative_replay = (
        build_toda_group_result_proof_replay(
          group_result
        )
      )
"""

R25_19_CALL = """      narrative_replay = (
        build_complete_toda_group_result_proof_replay(
          group_result
        )
      )
"""

replay_text = REPLAY.read_text(encoding="utf-8-sig")
if COMPLETE_FUNCTION in replay_text:
    print("Complete replay API already present.")
elif REPLAY_ANCHOR in replay_text:
    replay_text = replay_text.replace(
        REPLAY_ANCHOR,
        COMPLETE_FUNCTION + REPLAY_ANCHOR,
        1,
    )
    REPLAY.write_text(replay_text, encoding="utf-8")
    print("Added build_complete_toda_group_result_proof_replay.")
else:
    raise SystemExit("Replay builder anchor not found.")

main_text = MAIN.read_text(encoding="utf-8-sig")
if IMPORT_NEW in main_text:
    print("main.py complete replay import already present.")
elif IMPORT_OLD in main_text:
    main_text = main_text.replace(
        IMPORT_OLD,
        IMPORT_NEW,
        1,
    )
else:
    raise SystemExit("main.py replay import anchor not found.")

if R25_19_CALL in main_text:
    print("main.py Narrative already uses complete replay.")
elif R25_17_CALL in main_text:
    main_text = main_text.replace(
        R25_17_CALL,
        R25_19_CALL,
        1,
    )
else:
    raise SystemExit("R25-17 Narrative replay call anchor not found.")

MAIN.write_text(main_text, encoding="utf-8")
print("R25-19 production repair applied.")
