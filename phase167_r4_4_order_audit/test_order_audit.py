from audit import audit_one


def test_pi43_visible_dependency_order():
    result = audit_one(3, 1)
    assert not result["not_observed"], result
    assert not result["violations"], result


def test_representative_groups_render():
    for n, k in ((2, 1), (4, 1), (5, 1), (6, 1)):
        result = audit_one(n, k)
        assert result["line_count"] > 0, result
