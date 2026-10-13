"""Phase 165 R14-R21: complete the six-clause source representation of Toda (5.1)."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import re

from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r15_typed_diagonal import match_diagonal_toda51_claims
from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge

CLAUSE_KEYS = (
    "pi1_zero", "below_diagonal_zero", "negative_stem_zero",
    "diagonal_cyclic", "stable_zero_stem_cyclic", "stable_identity",
)
CLAUSE_TEX = (
    r"\pi^{1}_{i}=0\ (i>1)",
    r"\pi^{n}_{i}=0\ (i<n)",
    r"G_k=(G_k;2)=0\ (k<0)",
    r"\pi^{n}_{n}=\gen{\iota_n}\cong \mathbb Z",
    r"G_0=\gen{\iota}\cong \mathbb Z",
    r"\iota=E^{\infty}\iota_n",
)

@dataclass(frozen=True)
class Toda51Clause:
    key: str
    source_tex: str
    reference_locator: str = "(5.1)"

@dataclass(frozen=True)
class Toda51CompletedSource:
    reference_locator: str
    clauses: tuple[Toda51Clause, ...]
    source_sha256: str
    numbered_equation_found: bool
    adjacent_display_found: bool

def normalize_tex(value: str) -> str:
    """Whitespace-insensitive equality only, not a semantic equivalence checker."""
    return re.sub(r"\s+", "", value)

def complete_toda51_source(tex: str) -> Toda51CompletedSource:
    """Check original equation AND immediately following unnumbered display."""
    if not isinstance(tex, str) or not tex.strip():
        raise ValueError("Toda (5.1) TeX source is required")
    match = re.search(
        r"\\begin\{equation\}\\label\{5\.1\}(.*?)\\end\{equation\}"
        r"\s*\\\[(.*?)\\\]",
        tex, flags=re.DOTALL,
    )
    if match is None:
        raise ValueError("(5.1) equation and adjacent display not both present")
    equation, display = (normalize_tex(x) for x in match.groups())
    for clause in CLAUSE_TEX[:3]:
        if normalize_tex(clause) not in equation:
            raise ValueError(f"numbered (5.1) is missing {clause}")
    for clause in CLAUSE_TEX[3:]:
        if normalize_tex(clause) not in display:
            raise ValueError(f"adjacent display is missing {clause}")
    if len(set(CLAUSE_KEYS)) != 6:
        raise ValueError("invalid clause IDs")
    return Toda51CompletedSource(
        "(5.1)",
        tuple(Toda51Clause(key, source) for key, source in zip(CLAUSE_KEYS, CLAUSE_TEX)),
        sha256(tex.encode("utf-8")).hexdigest(),
        True, True,
    )

def diagonal_specializations(source: Toda51CompletedSource) -> tuple[object, object]:
    """Reuse existing typed schemas. No new mathematical proof claim."""
    if len(source.clauses) != 6 or source.clauses[3].key != "diagonal_cyclic":
        raise ValueError("completed source is required")
    suspension = TodaSuspensionMap(TodaPrimaryGroup(1, 1), TodaPrimaryGroup(2, 2))
    rows = match_diagonal_toda51_claims(suspension)
    if len(rows) != 3 or any(row.verified for row in rows[:2]):
        raise ValueError("R15 typed source contract changed")
    return rows[0].goal, rows[1].goal

def audit_r21(tex_path: Path) -> dict:
    source = complete_toda51_source(Path(tex_path).read_text(encoding="utf-8"))
    bridge, _ = build_phase165_r5_manifest_bridge()
    before = (len(bridge.registry._assertions), len(bridge.proof_links))
    goals = diagonal_specializations(source)
    after = (len(bridge.registry._assertions), len(bridge.proof_links))
    if before != after:
        raise ValueError("read-only audit modified production registry")
    return {
        "phase": "165 R14-R21",
        "locator": source.reference_locator,
        "registered_source_clause_count": len(source.clauses),
        "clause_keys": [c.key for c in source.clauses],
        "adjacent_display_included": source.adjacent_display_found,
        "diagonal_typed_specializations": [repr(g) for g in goals],
        "adopted_tex_sha256": source.source_sha256,
        "toda51_production_proof_steps": 0,
        "pi32_proved": False,
        "status": "TODA51_SIX_CLAUSE_SOURCE_COMPLETED_TYPED_SPECIALIZATIONS_NOT_CERTIFIED",
        "full_pytest_run": False,
    }
