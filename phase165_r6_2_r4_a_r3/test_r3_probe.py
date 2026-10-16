from __future__ import annotations

from pathlib import Path
from types import ModuleType

import sys
from dataclasses import dataclass

@dataclass
class InferenceRule:
    name: str
    premise_patterns: tuple = ()
    conclusion_pattern: object = None

@dataclass
class PremisePattern:
    statement_pattern: object = None

proof_module = ModuleType('proof')
proof_module.InferenceRule = InferenceRule
proof_module.PremisePattern = PremisePattern
sys.modules.setdefault('proof', proof_module)
from r3_probe import inspect_factory_module, markdown


def test_factory_identity_and_pattern() -> None:
    mod = ModuleType('fake_rules')
    exec('from proof import InferenceRule, PremisePattern\n'
         'def alpha_inference_rule():\n'
         '    return InferenceRule("alpha", premise_patterns=(PremisePattern(statement_pattern=1),), conclusion_pattern=2)\n', mod.__dict__)
    rows = inspect_factory_module('fake_rules', loader=lambda _: mod)
    assert len(rows) == 1
    assert rows[0]['rule_id'] == 'fake_rules.alpha_inference_rule'
    assert rows[0]['pattern_backward_candidate'] is True
    assert rows[0]['goal_probe_status'] == 'NOT_TESTED'


def test_required_input_is_not_executed() -> None:
    mod = ModuleType('fake_rules')
    exec('def unsafe_inference_rule(witness):\n'
         '    raise AssertionError("must not run")\n', mod.__dict__)
    rows = inspect_factory_module('fake_rules', loader=lambda _: mod)
    assert rows[0]['status'] == 'REQUIRES_INPUT'


def test_factory_error_is_reported() -> None:
    mod = ModuleType('fake_rules')
    exec('def broken_inference_rule():\n'
         '    raise ValueError("cannot build")\n', mod.__dict__)
    assert inspect_factory_module('fake_rules', loader=lambda _: mod)[0]['status'] == 'FACTORY_ERROR'


def test_non_rule_is_excluded() -> None:
    mod = ModuleType('fake_rules')
    exec('def fake_inference_rule():\n'
         '    return object()\n', mod.__dict__)
    assert inspect_factory_module('fake_rules', loader=lambda _: mod)[0]['status'] == 'NOT_INFERENCE_RULE'


def test_markdown_has_unverified_goals() -> None:
    sample = {'status': 'OK', 'source_root': '/sample',
              'counts': {'factories': 1, 'goal_verified': 0},
              'rules': [{'rule_id': 'a.b', 'status': 'INSTANTIATED', 'name': 'x|y',
                         'pattern_backward_candidate': True, 'goal_probe_status': 'NOT_TESTED'}],
              'r8_comparison': {}, 'limitations': []}
    report = markdown(sample)
    assert 'x/y' in report
    assert 'NOT_TESTED' in report
