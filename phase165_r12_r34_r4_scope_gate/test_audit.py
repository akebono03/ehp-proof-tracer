from phase165_r12_r34_r4_scope_gate.audit import audit


def test_foundational_reference_retained():
    result = audit()
    assert result["foundational_reference"] == "foundational:suspension-identity"


def test_shared_renderer_has_reference_suppression():
    result = audit()
    assert result["existing_reference_internal_suppression"]


def test_shared_renderer_has_short_exact_ordering():
    result = audit()
    assert result["existing_exact_support_orderer"]


def test_scope_gate_does_not_claim_runtime_ancestry():
    result = audit()
    assert result["pi43_actual_tree_inspected"] is False
    assert result["pi32_boundary_certified"] is False
    assert result["renderer_modified"] is False
    assert result["full_pytest_run"] is False
