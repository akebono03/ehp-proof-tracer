"""Phase 165 R6: current Phase 163/164 boundary guards, not legacy replay."""
import inspect
from pathlib import Path

import pytest

from phase163_r4_r11_literature_registration import (
    LiteratureAssertionInput,
    register_prop56_literature_statements,
)
from phase163_r4_r12_literature_registration import (
    LiteratureComponentInput,
    existing_prop51_prop53_candidates,
    register_prop51_prop53_literature_statements,
)
import web_app


def test_prop56_registry_requires_explicit_typed_inputs():
    parameters = inspect.signature(register_prop56_literature_statements).parameters
    assert "base" in parameters
    assert "inputs" in parameters
    assert LiteratureAssertionInput.__name__ == "LiteratureAssertionInput"


def test_prop51_prop53_registry_requires_explicit_typed_inputs():
    parameters = inspect.signature(register_prop51_prop53_literature_statements).parameters
    assert "base" in parameters
    assert "inputs" in parameters
    assert LiteratureComponentInput.__name__ == "LiteratureComponentInput"
    with pytest.raises(RuntimeError, match="retired"):
        existing_prop51_prop53_candidates()


def test_web_proof_uses_common_progress_entry_without_legacy_builder():
    source = inspect.getsource(web_app.create_app)
    assert source.count("group_proof_view = build_group_proof_progress_view(") >= 2
    assert "build_standard_web_group_proof_view" not in source


def test_web_proof_entry_has_no_legacy_import():
    source = Path(web_app.__file__).read_text(encoding="utf-8")
    assert "from web_group_proof import (\n  WebGroupProofView,\n)" in source
    assert "build_standard_web_group_proof_view(" not in source
