from types import SimpleNamespace

def test_r40_uses_common_entry(monkeypatch):
    import phase165_r14_r40_replay as old
    seen = []
    monkeypatch.setattr(old,"build_registered_common_replay",lambda **k: (seen.append(k),"ok")[1])
    assert old.build_phase165_r40_pi32_common_replay("group",2)=="ok"
    assert seen == [{"group_result":"group","max_depth":2,"mode":"trace"}]

def test_r41_uses_common_entry(monkeypatch):
    import phase165_r14_r41_proof_transfer as old
    seen=[]
    monkeypatch.setattr(old,"build_registered_common_replay",lambda **k: (seen.append(k),"ok")[1])
    assert old.build_phase165_r41_pi32_common_replay("group",2,"narrative")=="ok"
    assert seen == [{"group_result":"group","max_depth":2,"mode":"narrative"}]

def test_no_direct_pi32_reconstructor_in_r40_r41():
    from pathlib import Path
    root=Path(__file__).resolve().parent.parent
    for name in ("phase165_r14_r40_replay.py","phase165_r14_r41_proof_transfer.py"):
        assert "reconstruct_registered_pi32" not in (root/name).read_text(encoding="utf-8")
