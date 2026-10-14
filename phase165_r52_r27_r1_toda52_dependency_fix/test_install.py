"""Targeted static guard tests; repository integration tests run via run.ps1."""
from __future__ import annotations

import ast
from pathlib import Path

from install import MARKER, REPLACEMENT, _function


def test_transform_fragment_is_valid_python():
    source = ('def build_toda_52_composition_isomorphism_step():\n'
              '  phase49 = {}\n' + MARKER + '      1,\n    )\n  )\n  return premise_steps\n')
    ast.parse(source)
    transformed = source.replace(MARKER, REPLACEMENT)
    ast.parse(transformed)
    assert len(_function(transformed).body) > len(_function(source).body)


def test_uses_only_existing_phase50_premise_steps():
    assert 'phase50["premise_steps"]' in REPLACEMENT
    assert 'TodaPi32Eta2DefinitionStatement' in REPLACEMENT
    assert 'ProofRule.GIVEN' not in REPLACEMENT
    assert 'create_legacy_given_proof_step' not in REPLACEMENT


def test_no_specialized_rule_recreated():
    installer = Path(__file__).with_name('install.py').read_text(encoding='utf-8')
    assert 'def toda_pi3_2_define_eta2_inference_rule(' not in installer
    assert 'def toda_pi3_2_eta2_hopf_relation_inference_rule(' not in installer
