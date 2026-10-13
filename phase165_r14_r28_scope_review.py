"""R14-R28: inspect real local Toda TeX for Proposition 4.2 scope.

Source observation and mathematical certification are deliberately separate.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import re

from phase165_r5_manifest_bridge import build_phase165_r5_manifest_bridge
from phase165_r14_r26_prop42_typed import bind_proposition42


@dataclass(frozen=True)
class PropositionContext:
    path: str | None
    found: bool
    excerpt: str
    n_ge_2_text_detected: bool
    n_ge_1_text_detected: bool
    n1_applicability_certified: bool = False


def _normalized_backslashes(text: str) -> str:
    """Accept both normal TeX and doubly escaped diagnostic fixtures."""
    return text.replace("\\\\", "\\")


def find_toda_tex(root: Path) -> Path | None:
    """Look only at likely known local source locations; never search the network."""
    candidates = (
        root / "Toda_01.tex",
        root / "Toda" / "Toda_01.tex",
        root / "tex" / "Toda_01.tex",
        root / "toda" / "Toda_01.tex",
    )
    return next((p for p in candidates if p.is_file()), None)


def proposition_context(path: Path | None) -> PropositionContext:
    if path is None:
        return PropositionContext(None, False, "", False, False)
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    source = _normalized_backslashes(path.read_text(encoding="utf-8-sig"))
    marker = re.search(
        r"\\begin\{proposition\}(?:\[[^\]]*\])?\s*\\label\{prop:4\.2\}",
        source,
        flags=re.S,
    )
    if marker is None:
        return PropositionContext(str(path), False, "", False, False)
    # Include preceding text, not only the numbered proposition environment.
    preceding = source[max(0, marker.start() - 5000):marker.start()]
    end = source.find(r"\end{proposition}", marker.end())
    if end < 0:
        raise ValueError("Proposition 4.2 closing environment missing")
    excerpt = source[max(0, marker.start() - 5000):end + len(r"\end{proposition}")]
    # Observations only. A match never automatically certifies applicability.
    n2 = bool(re.search(r"\bn\s*(?:>=|\\geq?\s*\{?\s*)\s*2|\bn\s*>\s*1", preceding))
    n1 = bool(re.search(r"\bn\s*(?:>=|\\geq?\s*\{?\s*)\s*1", preceding))
    return PropositionContext(str(path), True, excerpt, n2, n1)


def audit_r28(root: Path) -> dict:
    bridge, summary = build_phase165_r5_manifest_bridge()
    binding = bind_proposition42(bridge)
    ctx = proposition_context(find_toda_tex(Path(root)))
    return {
        "phase": "165 R14-R28",
        "prop42_source": binding.assertion_id,
        "typed_exactness_goal": repr(binding.typed_statement),
        "source_tex_path": ctx.path,
        "prop42_found_in_local_tex": ctx.found,
        "n_ge_2_text_detected": ctx.n_ge_2_text_detected,
        "n_ge_1_text_detected": ctx.n_ge_1_text_detected,
        "n1_applicability_certified": ctx.n1_applicability_certified,
        "n1_scope_evidence_excerpt": ctx.excerpt,
        "source_archive_count": summary.source_assertion_count,
        "r23_iso_step_assumed_verified": False,
        "production_delta_zero_proved": False,
        "production_pi32_proved": False,
        "status": "PROP42_LOCAL_CONTEXT_OBSERVED_SCOPE_REVIEW_NEEDED" if ctx.found else "PROP42_LOCAL_TEX_NOT_FOUND",
        "full_pytest_run": False,
    }
