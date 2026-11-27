import pytest

from phase178_r25_typed_generator_notation_alignment.installer import (
    OLD, NEW, TARGET, R24_PINS, SELF_FILES, proposed_source, normalized, encode_like, validate_scope,
)


def test_exact_replacement():
    before = 'def canonical_513():\n' + OLD + '    return eta13\n'
    after = proposed_source(before)
    assert after == before.replace(OLD,NEW)
    assert after.endswith('    return eta13\n') and not after.endswith('\n\n')


@pytest.mark.parametrize('text', ['', OLD+OLD, NEW])
def test_reject_missing_duplicate_or_already_modified_anchor(text):
    with pytest.raises(RuntimeError,match='MISSING_OR_AMBIGUOUS_ETA13_ANCHOR'):
        proposed_source(text)


@pytest.mark.parametrize('raw',[b'a\n',b'a\r\n',b'\xef\xbb\xbfa\r\n'])
def test_preserve_encoding(raw):
    assert encode_like(normalized(raw),raw)==raw


def test_change_scope_allows_own_and_r24_commits_only():
    validate_scope(set(R24_PINS)|SELF_FILES|{TARGET},[TARGET])
    with pytest.raises(RuntimeError,match='UNREVIEWED_COMMITTED_PATHS'):
        validate_scope(['expression.py'],[])
    with pytest.raises(RuntimeError,match='UNREVIEWED_WORKTREE_PATHS'):
        validate_scope([],['expression.py'])
