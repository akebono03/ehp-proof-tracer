"""R14-R26: bind Toda Proposition 4.2's (4.4) to typed EHP windows."""
from __future__ import annotations
from dataclasses import dataclass
import re
from homotopy_groups import TodaEHPExactnessWindow, TodaPrimaryGroup
from map_facts import EHP_E_MAP, EHP_DELTA_MAP
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from proof import ProofRule, ProofStep
from toda_rules import TodaProp42ExactnessStatement

SOURCE_ID = "phase163:archive:toda:tex:ch4:0005"
EXPECTED_LOCATOR = "Proposition 4.2"
TARGET_N, TARGET_I = 1, 2

@dataclass(frozen=True)
class Prop42TypedBinding:
    assertion_id: str
    typed_statement: TodaProp42ExactnessStatement
    adopted_tex_matched: bool
    original_edition_verified: bool
    index_scope_confirmed: bool
    proof_eligible_in_strict_search: bool

def _clean(tex: str) -> str:
    return re.sub(r"\s+", "", tex)

def validate_prop42_source(bridge) -> str:
    """Use the unique Proposition 4.2 record, never numbered equation (4.2)."""
    row = bridge.registry.assertion(SOURCE_ID)
    reference = bridge.registry.reference(row.reference_id)
    if reference.locator != EXPECTED_LOCATOR:
        raise ValueError("Proposition 4.2 locator mismatch")
    if not isinstance(row.content,dict):
        raise ValueError("archival content is not source text")
    raw = row.content.get("source_text")
    if not isinstance(raw,str):
        raise ValueError("Proposition 4.2 source is missing")
    compact = _clean(raw)
    tokens = (
        r"\begin{proposition}[]\label{prop:4.2}",
        "次の列は完全列である",
        r"\begin{equation}\label{4.4}",
        r"\pit{i}{n}",
        r"\pit{i+1}{n+1}",
        r"\pit{i+1}{2n+1}",
        r"\pit{i-1}{n}",
        r"\pit{i}{n+1}",
        r"\Delta",
        r"\Ex",
        r"\end{proposition}",
    )
    if any(_clean(t) not in compact for t in tokens):
        raise ValueError("Proposition 4.2 EHP equation tokens are incomplete")
    required_order = (
        r"\pit{i}{n}",r"\pit{i+1}{n+1}",
        r"\pit{i+1}{2n+1}",r"\pit{i-1}{n}",r"\pit{i}{n+1}",
    )
    positions = [compact.find(token) for token in required_order]
    if positions != sorted(positions):
        raise ValueError("EHP group terms are out of order")
    return raw

def typed_delta_e_window(n: int, i: int) -> TodaProp42ExactnessStatement:
    if type(n) is not int or n < 1 or type(i) is not int or i < 0:
        raise ValueError("invalid EHP indices")
    if i-1 < 0:
        raise ValueError("negative group dimension")
    window = TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(i+1,2*n+1),
        middle_term=TodaPrimaryGroup(i-1,n),
        target_term=TodaPrimaryGroup(i,n+1),
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
    )
    return TodaProp42ExactnessStatement(window=window)

def bind_proposition42(bridge,n: int=TARGET_N,i: int=TARGET_I,
                       *,index_scope_confirmed: bool=False) -> Prop42TypedBinding:
    validate_prop42_source(bridge)
    return Prop42TypedBinding(
        assertion_id=SOURCE_ID,
        typed_statement=typed_delta_e_window(n,i),
        adopted_tex_matched=True,
        original_edition_verified=False,
        index_scope_confirmed=index_scope_confirmed,
        proof_eligible_in_strict_search=False,
    )

def adopted_tex_proofstep(binding: Prop42TypedBinding) -> ProofStep:
    """Conditional demonstration ONLY; does not add a strict eligible registry leaf."""
    if not binding.adopted_tex_matched or not binding.index_scope_confirmed:
        raise ValueError("index scope review must be explicit")
    if binding.assertion_id != SOURCE_ID:
        raise ValueError("invalid source")
    return ProofStep(
        conclusion=binding.typed_statement,
        premises=(),
        rule=ProofRule.GIVEN,
    )

def audit_r26() -> dict:
    bridge, _ = build_phase165_r5_manifest_bridge()
    binding = bind_proposition42(bridge)
    return {
        "phase":"165 R14-R26",
        "source_assertion_id":binding.assertion_id,
        "source_locator":EXPECTED_LOCATOR,
        "wrong_candidate_excluded":"phase163:archive:toda:tex:ch4:0002",
        "adopted_tex_matched":binding.adopted_tex_matched,
        "typed_exactness_goal":repr(binding.typed_statement),
        "index_n":TARGET_N,
        "index_i":TARGET_I,
        "n1_scope_confirmed":binding.index_scope_confirmed,
        "strict_citation_eligible":binding.proof_eligible_in_strict_search,
        "production_exactness_proofsteps":0,
        "production_delta_zero_proved":False,
        "pi32_proved":False,
        "status":"PROP42_SOURCE_IDENTIFIED_TYPED_DELTA_E_SCOPE_REVIEW_REQUIRED",
        "full_pytest_run":False,
    }
