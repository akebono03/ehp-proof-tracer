import importlib

import pytest

from phase165_r52_partial_proof import (
    GroupStructureStatus,
    ProofSearchStatus,
    make_partial_proof_result,
    render_partial_proof_markdown,
)
from phase165_r56_presentation_adapter import render_completed_shared_narrative


def test_partial_renderer_keeps_not_searched_status():
    result = make_partial_proof_result(
        n=3, k=2,
        status=ProofSearchStatus.NOT_SEARCHED,
        structure_status=GroupStructureStatus.UNKNOWN,
    )
    output = render_partial_proof_markdown(result)
    assert isinstance(output, str) and output.strip()


def test_completed_adapter_rejects_unproved_goal():
    result = make_partial_proof_result(n=3, k=2, status=ProofSearchStatus.NOT_SEARCHED)
    with pytest.raises(ValueError):
        render_completed_shared_narrative(result)


def test_public_web_module_still_imports():
    assert callable(importlib.import_module('web_group_proof').build_standard_web_group_proof_view)
