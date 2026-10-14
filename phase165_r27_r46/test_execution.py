"""Targeted actual inference, plus CLI state tests."""
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def test_equality_symmetry_creates_real_proofstep():
    from proof import ProofRule, Relation, RelationType, relation_proof_step
    from relation_rules import equality_symmetry_inference_rule
    from toda_typed_execution import TypedExecutionOutcome, execute_typed_applicable_rules

    original = Relation(lhs=2, rhs=3, relation_type=RelationType.EQUALITY)
    premise = relation_proof_step(original)
    result = execute_typed_applicable_rules(
        (premise,), rules=(equality_symmetry_inference_rule(),), candidate_number=1,
    )
    assert result.status is TypedExecutionOutcome.EXECUTED
    assert result.proof_step.rule is ProofRule.INFERENCE
    assert result.proof_step.premises == (premise,)
    assert result.proof_step.conclusion == Relation(
        lhs=3, rhs=2, relation_type=RelationType.EQUALITY,
    )


def test_zero_premises_without_applicable_rules():
    from toda_typed_execution import TypedExecutionOutcome, execute_typed_applicable_rules
    result = execute_typed_applicable_rules((), rules=())
    assert result.status is TypedExecutionOutcome.NONE
    assert result.proof_step is None


def test_multiple_candidates_not_automatically_executed():
    from proof import Relation, RelationType, relation_proof_step
    from relation_rules import equality_symmetry_inference_rule
    from toda_typed_execution import TypedExecutionOutcome, execute_typed_applicable_rules
    step = relation_proof_step(Relation(lhs=2, rhs=3, relation_type=RelationType.EQUALITY))
    result = execute_typed_applicable_rules((step,), rules=(equality_symmetry_inference_rule(), equality_symmetry_inference_rule()))
    assert result.status is TypedExecutionOutcome.AMBIGUOUS
    assert result.proof_step is None


def test_cli_execute_uses_shared_typed_engine(monkeypatch, capsys):
    import main
    import phase165_r27_r34_typed_lookup as lookup
    from toda_typed_execution import TypedExecutionOutcome, TypedExecutionResult
    import toda_typed_execution as execution
    monkeypatch.setattr(lookup, 'search_typed_generator_statements', lambda value: SimpleNamespace(proven_steps=(), diagnostics=()))
    monkeypatch.setattr(execution, 'execute_typed_applicable_rules', lambda steps, candidate_number=None: TypedExecutionResult(TypedExecutionOutcome.NONE, ()))
    assert main._run_execute_command('eta_2') == 1
    assert 'No typed inference candidate' in capsys.readouterr().out
