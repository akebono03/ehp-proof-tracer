from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent

def test_historical_entrypoints_removed():
    for file in ("phase165_r14_r37_closure.py", "phase165_r14_r40_replay.py",
                 "phase165_r14_r41_proof_transfer.py"):
        assert not (ROOT/file).exists()

def test_active_source_registry_preserved():
    from phase165_r14_r38_direct_registry import build_adopted_typed_reference_registry
    assert callable(build_adopted_typed_reference_registry)

def test_active_common_search_preserved():
    from phase165_r52_r9_shared_math import search_shared_group_goal
    assert callable(search_shared_group_goal)
