from audit import classify, markdown, same


def test_same_type_and_value():
    assert same(3, 3)
    assert not same(3, '3')


def test_canonical_complete():
    assert classify(None, 1, True) == 'CANONICAL_COMPLETE'


def test_ambiguity_classification():
    assert classify('expected one registered derivation for X, found 2', 0, False) == 'UNRESOLVED_OR_AMBIGUOUS'


def test_cycle_classification():
    assert classify('cyclic proof dependency', 0, False) == 'CYCLE'


def test_exception_classification():
    assert classify('RuntimeError: sample', 0, False) == 'EXCEPTION'


def test_markdown_contains_result():
    document = markdown({'root_candidate_count': 1, 'results': [{'path': 'ROOT_1', 'root_rule': 'rule', 'status': 'CYCLE', 'proved_observations': 0, 'unresolved_observations': 1, 'error': 'cyclic proof dependency'}]})
    assert 'ROOT_1' in document and 'CYCLE' in document
