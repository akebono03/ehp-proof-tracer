import pytest

from phase176_r3r39_public_equality_transport.apply import (
    INSERT_AFTER_AVAILABLE, INSERT_AFTER_HOPF, updated_source,
)
from phase176_r3r39r2_git_state_guard.guard import classify


def inputs():
    original = (
        "def f(prior_conclusions, goal, available):\n"
        + INSERT_AFTER_AVAILABLE + "        pass\n"
        + "    if True:\n"
        + "        options.extend(expand_composite_suspension_equality(goal))\n"
        + INSERT_AFTER_HOPF
    )
    return original.encode(), updated_source(original).encode()


@pytest.mark.parametrize("state", ["UNSTAGED", "STAGED", "COMMITTED"])
def test_exact_change_in_each_git_state(state):
    original, expected = inputs()
    head = expected if state == "COMMITTED" else original
    index = original if state == "UNSTAGED" else expected
    assert classify(original, head, index, expected) == state


def test_missing_patch_rejected():
    original, _ = inputs()
    with pytest.raises(ValueError, match="WORKTREE_BYTES_NOT_REPAIRED"):
        classify(original, original, original, original)


def test_unrelated_index_rejected():
    original, expected = inputs()
    with pytest.raises(ValueError, match="UNEXPECTED_HEAD_OR_INDEX_BYTES"):
        classify(original, original, expected + b"# unrelated\n", expected)


def test_wrong_eol_rejected():
    original, expected = inputs()
    with pytest.raises(ValueError, match="WORKTREE_BYTES_NOT_REPAIRED"):
        classify(original, original, original, expected.replace(b"\n", b"\r\n"))
