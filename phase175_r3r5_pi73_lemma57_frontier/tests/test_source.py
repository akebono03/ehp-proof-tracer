"""Source-first safeguards for the printed general Toda Lemma 5.7."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase175_r3r5_pi73_lemma57_frontier import source


def sample_source() -> str:
    return "\n".join((
        r"\pi^{2}_{6}=\mathbb Z_4\gen{\eta_2\circ\nu'}",
        r"\begin{lemma}\label{lemma:5.7}",
        r"\alpha\in\pi_i(S^3)",
        r"E^2\alpha\in2\iota_5\circ\pi_{i+2}(S^5)",
        r"E(\eta_2\circ\alpha)=0",
        r"E(\eta_2\circ\nu')=0",
        r"\end{lemma}",
        r"E^2\nu'=2\nu_5",
        r"\pi^{2}_{6}=\Delta(\pi^{5}_{8})",
        r"E\pi_6^2=\gen{E(\eta_2\circ\nu')}=0",
        r"\begin{proposition}\label{prop:5.8}",
    ))


def test_lemma57_precedes_prop58_and_has_real_conditional() -> None:
    positions = source.source_clause_positions(sample_source())
    assert positions["lemma_start"] < positions["lemma_end"]
    assert positions["lemma_end"] < positions["proposition_58_start"]
    assert positions["general_conditional_count"] == 1
    assert positions["particular_consequence_count"] == 1


@pytest.mark.parametrize("old,new", [
    (r"E(\eta_2\circ\alpha)=0", r"E(\eta_2\circ\alpha)\ne0"),
    (r"E(\eta_2\circ\nu')=0", r"E(\eta_2\circ\nu')\ne0"),
    (r"E^2\nu'=2\nu_5", r"E^2\nu'=3\nu_5"),
    (r"\pi^{2}_{6}=\Delta(\pi^{5}_{8})", r"\pi^{2}_{6}=0"),
    (r"E\pi_6^2=\gen{E(\eta_2\circ\nu')}=0", "Unproved statement"),
])
def test_missing_or_changed_source_refused(old: str, new: str) -> None:
    with pytest.raises(ValueError):
        source.source_clause_positions(sample_source().replace(old, new))


def test_duplicate_lemma_source_refused() -> None:
    with pytest.raises(ValueError):
        source.source_clause_positions(sample_source().replace(
            source.LEMMA_START, source.LEMMA_START + "\n" + source.LEMMA_START,
        ))


def test_prop58_before_lemma_is_refused() -> None:
    text = sample_source().replace(source.PROPOSITION_START, "")
    text = source.PROPOSITION_START + "\n" + text
    with pytest.raises(ValueError):
        source.source_clause_positions(text)


def test_text_is_not_registered_as_given_or_group_proof() -> None:
    assert "from proof import" not in Path(source.__file__).read_text(encoding="utf-8")
    assert source.SOURCE_PATH == "sources/toda/Toda_05_2.tex"
    assert len(source.SOURCE_BLOB) == 40


def test_reject_non_string_source() -> None:
    with pytest.raises(TypeError):
        source.source_clause_positions(b"not TeX")
