"""Focused live contract checks; no source mutations or fabricated proof trees."""
from __future__ import annotations

from phase171_r2j_r4_r9_r20r1_post_patch_route_audit.audit import preflight
from phase171_r2j_r4_r9_r20_eta_route_precedence.install import REPLACEMENT


def test_r20_guarded_installation_is_exactly_present():
    from pathlib import Path
    import phase165_r52_r9_shared_math as shared

    ready = preflight()
    assert ready["branch"] == "develop"
    text = Path(shared.__file__).read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    assert text.count(REPLACEMENT) == 1


def test_original_dedup_already_recognizes_both_scalar_rule_names():
    from phase165_r6_2_r4_r8_dedup import SCALAR_SPECIALIZATION_ROUTES
    assert SCALAR_SPECIALIZATION_ROUTES == frozenset({
        "Toda Proposition 5.1 generic higher-eta specialization",
        "generic cited typed scalar specialization",
    })
