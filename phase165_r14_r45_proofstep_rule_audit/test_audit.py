from audit import audit_proofstep_rules


def test_proofstep_ancestry_has_nine_reference_leaves():
    report = audit_proofstep_rules()
    assert report['reference_leaf_count'] == 9


def test_proofstep_has_real_exactness_dependencies():
    report = audit_proofstep_rules()
    assert any('Exactness' in premise for row in report['map_and_delta_steps'] for premise in row['premise_types'])


def test_inference_rule_names_not_lost():
    report = audit_proofstep_rules()
    for row in report['map_and_delta_steps']:
        assert row['rule_kind']
        if row['premise_types']:
            assert row['rule_name'] is not None
