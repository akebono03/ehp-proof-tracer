"""Source-first R21 dependency guards; no production imports needed."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r21_delta_hopf_chain_audit.audit import (
    DIAGONAL,
    END,
    MARKERS,
    PROP27,
    PROP27_HOPF,
    START,
    inspect_source,
)


def sample_source() -> str:
    prefix = PROP27 + "\n" + PROP27_HOPF + "\n" + DIAGONAL + "\n"
    body = START + "\n" + "\n".join(MARKERS.values()) + "\n" + END
    return prefix + body


def test_independent_hopf_chain_source() -> None:
    result = inspect_source(sample_source())
    assert result["hopf_injection_via_exactness_stated"] is True
    assert result["hopf_image_2Z_via_kernel_stated"] is True
    assert result["typed_delta_witness_proof_present"] is False
    assert result["isomorphism_arrow_is_direct_given"] is False
    assert len(result["mathematical_dependency_order"]) == 7


@pytest.mark.parametrize("marker", tuple(MARKERS.values()))
def test_missing_proof_clause_rejected(marker: str) -> None:
    with pytest.raises(ValueError, match="missing or ambiguous"):
        inspect_source(sample_source().replace(marker, "REMOVED"))


def test_wrong_evidence_order_rejected() -> None:
    source = sample_source()
    a, b = MARKERS["hopf_delta_generator"], MARKERS["cyclic_codomain"]
    with pytest.raises(ValueError, match="order"):
        inspect_source(source.replace(a, "TEMP").replace(b, a).replace("TEMP", b))


@pytest.mark.parametrize("marker", (PROP27, PROP27_HOPF, DIAGONAL))
def test_missing_independent_source_rejected(marker: str) -> None:
    with pytest.raises(ValueError, match="Independent"):
        inspect_source(sample_source().replace(marker, "REMOVED"))


def test_duplicate_clause_rejected() -> None:
    with pytest.raises(ValueError, match="ambiguous"):
        inspect_source(sample_source().replace(MARKERS["root_zero"], MARKERS["root_zero"] * 2))
