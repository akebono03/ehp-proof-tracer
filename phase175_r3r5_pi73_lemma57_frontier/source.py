"""Read-only verification of the printed Toda Lemma 5.7, before Proposition 5.8.

The TeX text is evidence for a source statement, not a verified ProofStep.
"""
from __future__ import annotations

from hashlib import sha1
from pathlib import Path
import subprocess

SOURCE_PATH = "sources/toda/Toda_05_2.tex"
SOURCE_BLOB = "579661138928499ba04a51327f686d9b971b5314"
LEMMA_START = r"\begin{lemma}\label{lemma:5.7}"
LEMMA_END = r"\end{lemma}"
PROPOSITION_START = r"\begin{proposition}\label{prop:5.8}"


def source_clause_positions(source: str) -> dict[str, int]:
    """Require the exact Lemma 5.7 hypotheses and particular consequence."""
    if not isinstance(source, str):
        raise TypeError("source must be a str")
    if source.count(LEMMA_START) != 1 or source.count(PROPOSITION_START) != 1:
        raise ValueError("Toda Lemma 5.7 / Proposition 5.8 source anchor is not unique")
    start = source.index(LEMMA_START)
    if source.count(LEMMA_END, start, source.index(PROPOSITION_START)) != 1:
        raise ValueError("Toda Lemma 5.7 not closed before Proposition 5.8")
    end = source.index(LEMMA_END, start) + len(LEMMA_END)
    proposition = source.index(PROPOSITION_START)
    if not start < end < proposition:
        raise ValueError("Toda Lemma 5.7 must precede Proposition 5.8")
    lemma = source[start:end]
    for clause in (
        r"\alpha\in\pi_i(S^3)",
        r"E^2\alpha\in2\iota_5\circ\pi_{i+2}(S^5)",
        r"E(\eta_2\circ\alpha)=0",
        r"E(\eta_2\circ\nu')=0",
    ):
        if lemma.count(clause) != 1:
            raise ValueError("Missing or duplicated Lemma 5.7 clause: " + clause)
    between = source[end:proposition]
    for fragment in (
        r"E^2\nu'=2\nu_5",
        r"\pi^{2}_{6}=\Delta(\pi^{5}_{8})",
        r"E\pi_6^2=\gen{E(\eta_2\circ\nu')}=0",
    ):
        if fragment not in between:
            raise ValueError("Missing prerequisite argument following Lemma 5.7: " + fragment)
    return {
        "lemma_start": start,
        "lemma_end": end,
        "proposition_58_start": proposition,
        "general_conditional_count": 1,
        "particular_consequence_count": 1,
    }


def verify_reviewed_toda_source(root: Path) -> dict[str, object]:
    """Pin the committed blob; reject semantic changes in the checked-out file."""
    root = Path(root)
    path = root / SOURCE_PATH
    if not path.is_file():
        raise RuntimeError("R3R5_TODA_SOURCE_MISSING")
    actual = subprocess.run(
        ["git", "rev-parse", "HEAD:" + SOURCE_PATH],
        cwd=root, capture_output=True, text=True, check=True,
    ).stdout.strip()
    if actual != SOURCE_BLOB:
        raise RuntimeError("R3R5_TODA_SOURCE_PIN_CHANGED")
    raw = path.read_bytes()
    normalized = raw.replace(b"\r\n", b"\n")
    candidates = (raw, normalized, normalized.replace(b"\n", b"\r\n"))
    def blob(data: bytes) -> str:
        return sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
    if not any(blob(data) == SOURCE_BLOB for data in candidates):
        raise RuntimeError("R3R5_TODA_WORKTREE_SOURCE_CHANGED")
    source = normalized.decode("utf-8-sig")
    clauses = source_clause_positions(source)
    return {
        "source_path": SOURCE_PATH,
        "source_blob": actual,
        "locator": "Lemma 5.7",
        "original_print_independently_verified": False,
        "direct_given_added": False,
        **clauses,
    }
