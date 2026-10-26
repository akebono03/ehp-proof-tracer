"""Installer regression: R3K has two matching import substrings."""
from __future__ import annotations

import ast

import pytest

from phase169_r3k2_eta_transport.apply import patch_renderer


R3K_SHAPED_FUNCTION = '''def render_model_backed_narrative_markdown(result, model):
    from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
    if should_check:
        from homotopy_groups import TodaPrimaryGroupZeroStatement
    for citation in model.citations:
        locator = citation.reference.locator or citation.reference.label
    if not incomplete:
        def unique_step_index(premise):
            return 0
        def only_consumed_by(candidate, consumer):
            return True
    from homotopy_groups import TodaPrimaryGroupZeroStatement
    if should_project:
        eta_numbers = (
                            cited_general_ancestor_numbers(step, TodaEtaFamilyGeneralDefinition)
                            if (isinstance(statement, GeneratorSuspension)
                                and _eta_pair(statement) is not None)
                            else ()
                        )
    displayed_cyclic_math = set()
    for index in order:
        pass
'''


def test_r3k2a_uses_body_loop_instead_of_repeated_import_substring():
    assert R3K_SHAPED_FUNCTION.count(
        "    from homotopy_groups import TodaPrimaryGroupZeroStatement\n"
    ) == 2
    result = patch_renderer(R3K_SHAPED_FUNCTION)
    ast.parse(result)
    assert result.count("    for index in order:\n") == 1
    assert result.count("for image_index in order:") == 1
    assert result.index("for image_index in order:") < result.index("for index in order:")
    assert "η 系列の定義（Chapter V, i）" in result
    assert "from phase165_r14_r6_generic_iso import GeneratorImage" in result


def test_r3k2a_rejects_missing_body_loop_without_file_write():
    source = R3K_SHAPED_FUNCTION.replace("    for index in order:\n", "    for item in order:\n")
    with pytest.raises(RuntimeError, match="body-loop anchor changed"):
        patch_renderer(source)
