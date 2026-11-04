"""Patch safety, reviewed AST scopes, and isolated Web inline-math behavior."""
from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

import pytest

from phase173_r4_r15r12_reference_correction.install import preflight
from phase173_r4_r15r12_reference_correction.patch import (
    CHANGED_PATHS,
    MODEL_PATH,
    REFERENCE_PATH,
    WEB_PATH,
    R4E_TEST_PATH,
    TEST_PATH,
    patch_source,
)


ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope='module')
def reviewed_sources():
    return preflight(ROOT)


def test_reviewed_patch_changes_five_files(reviewed_sources) -> None:
    assert tuple(reviewed_sources) == CHANGED_PATHS
    assert len(CHANGED_PATHS) == 5
    for path, (before, after) in reviewed_sources.items():
        assert before != after
        ast.parse(after.decode('utf-8-sig'))
        with pytest.raises(RuntimeError, match='Unreviewed|already-patched'):
            patch_source(path, after)


def test_prop44_typing_and_unnecessary_prelude_removed(reviewed_sources) -> None:
    before, after = reviewed_sources[REFERENCE_PATH]
    assert 'Proposition 4.4 直前の記述（Steenrod1951 を引用）' in before.decode('utf-8-sig')
    updated = after.decode('utf-8-sig')
    assert 'Steenrod1951' not in updated
    assert r'\alpha\circ\gamma' in updated
    assert r'\xrightarrow{\;\cong\;}' in updated
    assert 'project_cited_proof_step_reference_bodies' in updated


def test_model_uses_only_cited_proof_steps(reviewed_sources) -> None:
    _, after = reviewed_sources[MODEL_PATH]
    text = after.decode('utf-8-sig')
    assert 'project_cited_proof_step_reference_bodies(' in text
    assert 'tuple(steps[j] for j in associations[i])' in text
    assert 'project_reference_bodies(registry, tuple(assertion_ids[i]))' in text


def test_strong_reference_math_is_parsed_not_displayed_verbatim(reviewed_sources) -> None:
    _, after = reviewed_sources[WEB_PATH]
    tree = ast.parse(after.decode('utf-8-sig'))
    node = next(
        item for item in tree.body
        if isinstance(item, ast.FunctionDef)
        and item.name == '_build_group_proof_inline_segments'
    )

    @dataclass(frozen=True)
    class Segment:
        kind: str
        value: str

    namespace = {'WebGroupProofInlineSegmentView': Segment}
    module = ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[]))
    exec(compile(module, '<reviewed-web-inline>', 'exec'), namespace)
    render = namespace['_build_group_proof_inline_segments']
    sample = r'**[R2] 先行データベース結果 $\pi_{6}^{3}$（sphere.csv, n=3, k=3）.**'
    segments = render(sample)
    assert sum(segment.kind == 'inline_math' for segment in segments) == 1
    assert any(segment.kind == 'inline_math' and segment.value == r'\pi_{6}^{3}'
               for segment in segments)
    assert any(segment.kind == 'strong' and '先行データベース結果' in segment.value
               for segment in segments)
    assert render('**plain text**') == (Segment('strong', 'plain text'),)
    assert render('**unpaired $ dollar**') == (Segment('strong', 'unpaired $ dollar'),)


def test_mixed_newlines_fail_closed(reviewed_sources) -> None:
    original, _ = reviewed_sources[WEB_PATH]
    normalized = original.replace(b'\r\n', b'\n')
    mixed = normalized.replace(b'\n', b'\r\n', 1)
    if normalized.count(b'\n') > 1:
        with pytest.raises(RuntimeError, match='Mixed line endings'):
            patch_source(WEB_PATH, mixed)


def test_first_success_step_count_contract_in_both_historical_tests(reviewed_sources) -> None:
    """Retain the actual proof as the oracle, never fabricate an eighteenth step."""
    for path in (TEST_PATH, R4E_TEST_PATH):
        before, after = reviewed_sources[path]
        old = before.decode('utf-8-sig')
        new = after.decode('utf-8-sig')
        assert 'assert len(result.proven_steps) == 18' in old
        assert 'assert len(view.steps) == 18' in old
        assert 'assert len(result.proven_steps) == 18' not in new
        assert 'assert len(view.steps) == 18' not in new
        assert 'assert any(step.conclusion == result.conclusion for step in result.proven_steps)' in new
        assert 'assert len(view.steps) == len(pi64[0].proven_steps)' in new
        assert patch_source(path, before) == after
        with pytest.raises(RuntimeError, match='Unreviewed|already-patched'):
            patch_source(path, after)


def test_r4g_prior_result_does_not_assume_28_steps(reviewed_sources) -> None:
    """The prior completed proof remains valid regardless of search-path length."""
    before, after = reviewed_sources[TEST_PATH]
    original = before.decode('utf-8-sig')
    modified = after.decode('utf-8-sig')
    assert 'assert len(previous.proven_steps) == 28' in original
    assert 'assert len(previous.proven_steps) == 28' not in modified
    assert (
        'assert any(step.conclusion == previous.conclusion '
        'for step in previous.proven_steps)'
    ) in modified
    assert 'assert previous.status is ProofSearchStatus.COMPLETE' in modified
    assert patch_source(TEST_PATH, before) == after
    with pytest.raises(RuntimeError, match='Unreviewed|already-patched'):
        patch_source(TEST_PATH, after)
