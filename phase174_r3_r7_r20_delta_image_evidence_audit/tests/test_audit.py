"""R20 focused source-audit contracts."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r20_delta_image_evidence_audit.audit import (
    END,
    MARKERS,
    START,
    inspect_source,
)


def example_source() -> str:
    return START + "\n" + "\n".join(MARKERS.values()) + "\n" + END


def test_preserves_source_chain_without_claiming_proof() -> None:
    result = inspect_source(example_source())
    assert result["delta_iso_is_present_in_proof_text"] is True
    assert result["delta_iso_is_independently_proven_in_public_search"] is False
    assert result["signed_generator_identity_is_typed_proof"] is False
    assert result["original_print_edition_checked"] is False


@pytest.mark.parametrize("missing", tuple(MARKERS))
def test_missing_mathematical_clause_is_rejected(missing: str) -> None:
    with pytest.raises(RuntimeError):
        inspect_source(example_source().replace(MARKERS[missing], "[MISSING]"))


def test_wrong_dependency_order_is_rejected() -> None:
    items = list(MARKERS.values())
    items[1], items[2] = items[2], items[1]
    with pytest.raises(RuntimeError, match="order"):
        inspect_source(START + "\n" + "\n".join(items) + "\n" + END)
