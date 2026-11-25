from phase176_r3r56r1_historical_source_audit.audit import namespace_pair


def test_same_namespace_pair_only():
    assert namespace_pair(('shared:21:a',), ('shared:21:r',), 'a', 'r')
    assert not namespace_pair(('shared:21:a',), ('shared:22:r',), 'a', 'r')
    assert not namespace_pair(('shared:21:a',), (), 'a', 'r')
    assert not namespace_pair(('shared:x:a',), ('shared:x:r',), 'a', 'r')
    assert not namespace_pair(('shared:21:a:other',), ('shared:21:r',), 'a', 'r')
    assert not namespace_pair(('shared:21:a','shared:22:a'), ('shared:21:r','shared:22:r'), 'a', 'r')
