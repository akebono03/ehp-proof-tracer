def test_r3r4_real_production_file_has_only_reviewed_wiring():
    from phase174_r3_r5_finite_cyclic_extension.patch import git, insert_shared
    from phase174_r3_r6_source_extension.patch import connect_shared
    from phase174_r3_r6_r2_prop44_lemma54.patch import normalize, patch_shared
    old = git('show', 'b5f5208a7e23397834e4a38ad307c660a4f26b59:phase165_r52_r9_shared_math.py')
    current = Path('phase165_r52_r9_shared_math.py').read_bytes()
    r3r4 = replace_provider_call(old)
    r3r5 = insert_shared(r3r4)
    r3r6 = connect_shared(r3r5)
    new_source = patch_shared(normalize(r3r6.decode('utf-8'))).encode('utf-8')
    assert normalize(current.decode('utf-8')) in tuple(
        normalize(candidate.decode('utf-8'))
        for candidate in (r3r4, r3r5, r3r6, new_source)
    )
    assert git_blob_sha(old) == 'f49b0b7699e29ec1b78d73578dc66a0e33d6e336'
    assert current.count(b'options.extend(expand_delta_zero_from_injection(goal))') == 1
