from pathlib import Path
import inspect
from dataclasses import dataclass
from types import SimpleNamespace

from proof import ProofRule, ProofStep, InferenceRule, PremisePattern
from unified_statement_registry import AssertionOrigin

@dataclass(frozen=True)
class Statement:
    number: int

def test_r2_module_available():
    from phase165_r6_2_r2_verified_inverse import reverse_rules_from_witnesses
    rule=InferenceRule("sum of statements",premise_patterns=(PremisePattern(statement_type=Statement),),
                       conclusion_builder=lambda steps: Statement(steps[0].conclusion.number+1))
    step=ProofStep(Statement(2),(),ProofRule.GIVEN)
    proposals=reverse_rules_from_witnesses(Statement(3),(rule,),(step,))
    assert len(proposals)==1
    assert proposals[0].subgoals==(Statement(2),)

def test_shared_provider_contains_verified_witness_connection():
    from phase165_r52_r9_shared_math import shared_expansion_provider
    code=inspect.getsource(shared_expansion_provider)
    assert "reverse_rules_from_witnesses" in code
    assert "AssertionOrigin.FIXED_STATEMENT" in code
    assert "link.step.rule is ProofRule.GIVEN" in code
    assert "merge_backward_expansions" in code

def test_existing_adapter_not_removed_early():
    from phase165_r52_r9_shared_math import shared_expansion_provider
    assert "expand_existing_pi43_rules" in inspect.getsource(shared_expansion_provider)
