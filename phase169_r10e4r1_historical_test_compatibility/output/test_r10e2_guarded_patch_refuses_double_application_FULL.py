def test_r10e2_guarded_patch_refuses_double_application():
    from phase169_r10e2_unpositioned_citation.patch import transform
    target = 'phase169_r10e1_general_group_transport/transport.py'
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    before = root / "phase169_r10e2_unpositioned_citation" / "output" / (
        target.replace("/", "__") + ".before"
    )
    original = before.read_bytes()
    updated, functions = transform(target, original)
    assert 'uniquely_screened_prior_sources' in functions[
        'expand_prior_general_group_transport'
    ]
    # Later phases may append new transport policy to the same function.
    # Verify the R10E2 source-first guard survives without requiring the
    # entire production file to equal the old R10E2 snapshot.
    current = (root / target).read_bytes()
    assert b"uniquely_screened_prior_sources" in updated
    assert b"uniquely_screened_prior_sources" in current
    assert b"exact_prior_database_result" in current
    with pytest.raises(RuntimeError, match='expected changed source'):
        transform(target, updated)
