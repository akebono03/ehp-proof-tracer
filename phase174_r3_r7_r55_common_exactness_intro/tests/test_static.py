"""Check the reviewed rendering change, not another mathematical rule."""
from __future__ import annotations

import ast
from pathlib import Path

from phase174_r3_r7_r55_common_exactness_intro.source_guard import ROOT, TARGET
from phase174_r3_r7_r55_common_exactness_intro.patch import AFTER_CHAIN, AFTER_INTRO


def test_shared_renderer_has_single_first_chain_intro_contract()->None:
    source=(ROOT/TARGET).read_text(encoding='utf-8-sig')
    ast.parse(source)
    assert source.count(AFTER_CHAIN)==1
    assert source.count('if chain_index == 0 else "さらに, "')==1
    assert source.count('lines.append(f"{prefix}{tags}を用いて次の完全列を考える.")')==1
    assert 'def render_model_backed_narrative_markdown(' in source


def test_r55_has_no_new_specific_group_match_or_premise_installer()->None:
    folder=Path(__file__).resolve().parents[1]
    source=(folder/'patch.py').read_text(encoding='utf-8')
    assert 'TodaPrimaryGroupZeroStatement(' not in source
    assert 'ProofStep(' not in source
    assert 'ProofRule.GIVEN' not in source
    assert 'n == 7' not in source and 'k == 5' not in source
