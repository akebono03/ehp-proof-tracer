"""Focused insertion behavior without running or changing a real Git tree."""
from __future__ import annotations

import pytest

from phase174_r3_r6_r4_common_reference.patch import (
    candidate_source,
    _normalized,
)


MOCK = '''def project_reference_bodies(registry, assertion_ids):
    from proof import Relation

    result = []
    for statement in assertion_ids:
        if sentence is None:
            sentence = typed_sentence(statement, None)
    return result
'''


def test_two_unique_inserts_only_and_no_function_api_change() -> None:
    original = MOCK.replace("        if sentence is None:", "            if sentence is None:").replace(
        "            sentence = typed_sentence", "                sentence = typed_sentence",
    )
    patched = candidate_source(original)
    assert "project_cited_universal_toda_reference_body(" in patched
    assert patched.count("project_cited_universal_toda_reference_body") == 2
    assert patched.startswith("def project_reference_bodies(")
    assert "return result" in patched


def test_crlf_and_unrelated_text_preserved() -> None:
    original = MOCK.replace("        if sentence is None:", "            if sentence is None:").replace(
        "            sentence = typed_sentence", "                sentence = typed_sentence",
    )
    windows = "# unrelated\r\n" + original.replace("\n", "\r\n")
    patched = candidate_source(windows)
    assert patched.startswith("# unrelated\r\n")
    assert _normalized(patched).count("project_cited_universal_toda_reference_body") == 2
    assert "\r\n" in patched


def test_missing_or_duplicate_import_anchor_rejected() -> None:
    original = MOCK.replace("        if sentence is None:", "            if sentence is None:").replace(
        "            sentence = typed_sentence", "                sentence = typed_sentence",
    )
    with pytest.raises(ValueError, match="anchor"):
        candidate_source(original.replace("from proof import Relation", "from proof import ProofStep"))
    with pytest.raises(ValueError, match="anchor"):
        candidate_source(original.replace("    from proof import Relation\n\n    result = []\n",
                                          "    from proof import Relation\n\n    result = []\n    from proof import Relation\n\n    result = []\n"))
