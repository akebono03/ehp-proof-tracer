"""Static checks before the user's real renderer/Flask regression tests."""
from __future__ import annotations

import ast

import pytest

from phase174_r3_r7_r55_common_exactness_intro.patch import (
    BEFORE_CHAIN, BEFORE_INTRO, AFTER_CHAIN, AFTER_INTRO,
    replace_lines_preserving_eol, extract_full_function,
)


def minimal_source(eol:str='\n')->str:
    original='\n'.join((
        'def render_model_backed_narrative_markdown(result, model):',
        BEFORE_CHAIN,
        '        exactness_numbers = (3,)',
        *BEFORE_INTRO,
        '        lines.append("")',
        '    return lines',
        '',
    ))
    return original.replace('\n',eol)


def test_one_intro_with_multiple_chains_without_changing_proof_obligations()->None:
    patched=replace_lines_preserving_eol(minimal_source())
    assert AFTER_CHAIN in patched
    assert 'if chain_index == 0 else "さらに, "' in patched
    assert patched.count('の群構造を決定するために')==1
    assert 'exactness_numbers' in patched
    assert 'for number in exactness_numbers' in patched
    assert 'lines.append("")' in patched
    ast.parse(patched)


def test_idempotence_and_full_function_is_extractable()->None:
    patched=replace_lines_preserving_eol(minimal_source())
    assert replace_lines_preserving_eol(patched)==patched
    assert 'def render_model_backed_narrative_markdown' in extract_full_function(patched)
    assert 'return lines' in extract_full_function(patched)


def test_original_eol_preserved_and_unrelated_code_unchanged()->None:
    baseline=minimal_source('\r\n')
    patched=replace_lines_preserving_eol(baseline)
    assert '\n' not in patched.replace('\r\n','')
    assert patched.endswith('    return lines\r\n')


def test_reject_drift_and_partial_installation()->None:
    with pytest.raises(RuntimeError):
        replace_lines_preserving_eol(minimal_source().replace(BEFORE_CHAIN,'    for other in chains:'))
    with pytest.raises(RuntimeError):
        replace_lines_preserving_eol(minimal_source().replace(BEFORE_INTRO[2],'            lines.append("unexpected")'))
    with pytest.raises(RuntimeError):
        replace_lines_preserving_eol(minimal_source().replace(BEFORE_CHAIN,AFTER_CHAIN))
