"""Phase 165 R14-R27: audit n=1 scope and conditionally connect existing proofs."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re

from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r14_r26_prop42_typed import bind_proposition42, adopted_tex_proofstep

@dataclass(frozen=True)
class ScopeEvidence:
    source_file: str | None
    context: str
    explicit_n1_permitted: bool
    explicit_n1_excluded: bool

def inspect_scope_context(tex_file: Path | None) -> ScopeEvidence:
    """Read vicinity of Proposition 4.2; absent context is unresolved."""
    if tex_file is None:
        return ScopeEvidence(None,"",False,False)
    path=Path(tex_file)
    if not path.is_file():
        raise FileNotFoundError(path)
    data=path.read_text(encoding="utf-8-sig")
    match=re.search(r"\\begin\{proposition\}(?:\[[^]]*\])?\\label\{prop:4\.2\}",data)
    if match is None:
        raise ValueError("Proposition 4.2 not present in TeX")
    excerpt=data[max(0,match.start()-2400):match.end()+1500]
    # Never certify n=1 from a heuristic excerpt or from a numerical match.
    # Review must distinguish global prerequisites and exception clauses.
    excluded=bool(re.search(r"n\s*(?:>=|\\geq?)\s*2|n\s*>\s*1",excerpt))
    return ScopeEvidence(str(path),excerpt,False,excluded)

def conditional_exactness_step(scope_confirmed: bool):
    bridge,_=build_phase165_r5_manifest_bridge()
    binding=bind_proposition42(bridge,index_scope_confirmed=scope_confirmed)
    if not scope_confirmed:
        return None
    return adopted_tex_proofstep(binding)

def audit_r27(tex_file: Path | None = None) -> dict:
    scope=inspect_scope_context(tex_file)
    exact=conditional_exactness_step(False)
    return {
        "phase":"165 R14-R27",
        "r24_iso_connected":None,  # R24 is not re-audited in this R27 scope check
        "exactness_source":"phase163:archive:toda:tex:ch4:0005",
        "scope_file":scope.source_file,
        "context_excerpt":scope.context,
        "n1_scope_confirmed":scope.explicit_n1_permitted,
        "n1_exclusion_detected":scope.explicit_n1_excluded,
        "conditional_exactness_step_possible":conditional_exactness_step(True) is not None,
        "production_exactness_step":exact is not None,
        "production_delta_zero_proved":False,
        "pi32_proved":False,
        "status":"PROP42_TYPED_SCOPE_NOT_ESTABLISHED_DELTA_BLOCKED",
        "full_pytest_run":False,
    }
