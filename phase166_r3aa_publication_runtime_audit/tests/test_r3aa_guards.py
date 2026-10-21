from phase166_r3aa_publication_runtime_audit.audit import assert_legacy_gates_absent
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase166_r3c_publication_order import precedes_citing_assertion


def test_r3aa_old_order_gates_not_called_in_common_search():
    assert assert_legacy_gates_absent()["legacy_gates_absent"] is True


def test_r3aa_publication_comparison_retained():
    bridge = build_shared_typed_bridge()
    target = "shared:2:toda:adopted:prop5.1:higher_eta_group_relation"
    base = "shared:2:toda:adopted:prop5.1:pi4_3"
    assert precedes_citing_assertion(bridge, base, target)
    assert not precedes_citing_assertion(bridge, target, base)
