"""Real Group query POST; strict zero-root, citation and duplicate regression."""
from __future__ import annotations

from phase174_r3_r7_r55_common_exactness_intro.audit import inspect_common_intro


def test_r55_both_public_http_routes_keep_one_intro_and_cited_root()->None:
    report=inspect_common_intro()
    assert report['both_http_200'] is True
    assert report['both_complete_proof'] is True
    assert report['public_verified_steps']==28
    assert report['public_open_goals']==0
    assert report['repeated_intro_counts']==[1,1]
    assert report['common_intro_once'] is True
    assert report['later_chain_continuation'] is True
    assert report['proof_tree_mutated'] is False
    assert report['new_given']==0
    assert report['new_mathematical_rules']==0
    assert report['browser_katex_checked'] is False
