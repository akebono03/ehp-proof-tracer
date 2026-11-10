"""Static regression: no target-specific R55R3 proof prose survives."""
from __future__ import annotations

import ast
from pathlib import Path

from phase174_r3_r7_r55r3r2_narrative_removal.install import (
    PACKAGE, REFERENCE, RENDERER, TYPED, ROOT, LEGACY_A, LEGACY_B,
    REFERENCE_LEGACY, REFERENCE_SHARED, RENDERER_LEGACY, TYPED_SHARED,
    construct_sources,
)


def test_no_special_r55r3_modules_or_hooks() -> None:
    assert not (ROOT / LEGACY_A).exists()
    assert not (ROOT / LEGACY_B).exists()
    reference = (ROOT / REFERENCE).read_text(encoding='utf-8-sig')
    renderer = (ROOT / RENDERER).read_text(encoding='utf-8-sig')
    typed = (ROOT / TYPED).read_text(encoding='utf-8-sig')
    assert REFERENCE_LEGACY not in reference
    assert RENDERER_LEGACY not in renderer
    assert REFERENCE_SHARED in reference
    assert TYPED_SHARED in typed
    assert 'project_certified_proof_sentence' not in renderer
    assert '_typed_upper_delta_transition' not in renderer
    assert 'r55r3_common_proof_display' not in renderer
    for source in (reference, renderer, typed):
        ast.parse(source)


def test_shared_reference_helper_is_only_a_citation_formatter() -> None:
    source = (ROOT / REFERENCE).read_text(encoding='utf-8-sig')
    fragment = (PACKAGE / 'reference_body_helper.txt').read_text(encoding='utf-8')
    assert fragment in source
    helper = source[source.index('def _project_certified_general_reference_body('):]
    helper = helper[:helper.index('\ndef project_reference_bodies(')]
    for forbidden in ('project_certified_proof_sentence',
                      '_typed_upper_delta_transition', 'pi_12^7', '(n,k)'):
        assert forbidden not in helper


def test_installer_is_idempotent_after_removal() -> None:
    proposals = construct_sources()
    assert set(proposals) == {REFERENCE, RENDERER, TYPED}
    assert all(original == expected for _, original, expected in proposals.values())
