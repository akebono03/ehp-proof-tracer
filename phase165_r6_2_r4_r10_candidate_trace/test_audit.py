from audit import classify_root, summary

def test_prop51_classification():
    assert classify_root('Toda Proposition 5.1 generic higher-eta specialization') == 'PROP51_SPECIALIZATION'

def test_scalar_classification():
    assert classify_root('generic cited typed scalar specialization') == 'CITED_SCALAR_SPECIALIZATION'

def test_symmetry_classification():
    assert classify_root('equality symmetry') == 'SYMMETRY'

def test_unknown_classification():
    assert classify_root('another rule') == 'OTHER'

def test_summary_empty_traces():
    value = summary({'status': 'GOAL_SELECTION_BLOCKED', 'goal_count': 0, 'traces': {}})
    assert value['traces'] == {}
    assert value['production_modified'] is False
