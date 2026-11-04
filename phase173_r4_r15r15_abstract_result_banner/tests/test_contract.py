"""Source-independent contract for one evidence-driven Web result banner."""
from __future__ import annotations

import pytest

from phase173_r4_r15r15_abstract_result_banner.patches import (
    COMMON_FIELD,
    COMMON_GUARD,
    ADAPTER_ANCHOR,
    TEMPLATE_ANCHOR,
    patch_common,
    patch_adapter,
    patch_template,
)


def test_common_view_flag_is_optional_and_checked() -> None:
    source = (
        "@dataclass(frozen=True)\nclass WebGroupProofView:\n"
        + COMMON_FIELD + "  def __post_init__(self):\n" + COMMON_GUARD
    )
    patched = patch_common(source)
    assert patched.count("  abstract_structure_certified: bool = False\n") == 1
    assert patched.count("if not isinstance(self.abstract_structure_certified, bool)") == 1
    assert "if self.abstract_structure_certified and not self.partial_result" in patched
    assert source.count("abstract_structure_certified") == 0


def test_adapter_passes_only_existing_verified_certificate() -> None:
    source = "return WebGroupProofView(\n" + ADAPTER_ANCHOR + ")\n"
    patched = patch_adapter(source)
    assert "abstract_structure_certified=(result.abstract_structure is not None)" in patched
    assert patched.count("partial_result=(result.status is not ProofSearchStatus.COMPLETE)") == 1


def test_template_distinguishes_three_statuses() -> None:
    patched = patch_template(TEMPLATE_ANCHOR)
    assert patched.index("not group_proof_view.partial_result") < patched.index(
        "group_proof_view.abstract_structure_certified"
    ) < patched.index("No proof-backed result found")
    assert "named-generator proof is incomplete" in patched
    assert patched.count("No proof-backed result found") == 1


@pytest.mark.parametrize("transformer,source", (
    (patch_common, COMMON_FIELD + COMMON_GUARD),
    (patch_adapter, ADAPTER_ANCHOR),
    (patch_template, TEMPLATE_ANCHOR),
))
def test_duplicate_or_missing_anchors_fail_closed(transformer, source) -> None:
    with pytest.raises(ValueError, match="anchor mismatch"):
        transformer(source + source)
    with pytest.raises(ValueError, match="anchor mismatch"):
        transformer("unreviewed source")


def test_patch_rejects_invalid_input_types() -> None:
    with pytest.raises(TypeError):
        patch_template(None)
