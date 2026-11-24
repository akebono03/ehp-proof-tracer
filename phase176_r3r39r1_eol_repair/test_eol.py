import pytest

from phase176_r3r39_public_equality_transport.apply import (
    INSERT_AFTER_AVAILABLE, INSERT_AFTER_HOPF, normalized_source,
    patched_bytes, updated_source,
)


def baseline_text():
    return (
        "def f(prior_conclusions, goal, available):\n"
        + INSERT_AFTER_AVAILABLE + "        pass\n"
        + "    if True:\n"
        + "        options.extend(expand_composite_suspension_equality(goal))\n"
        + INSERT_AFTER_HOPF
    )


@pytest.mark.parametrize("eol", ["\n", "\r\n"])
@pytest.mark.parametrize("bom", [b"", b"\xef\xbb\xbf"])
def test_exact_patch_and_repair_preserve_baseline_bytes(eol, bom):
    original = baseline_text()
    expected_text = updated_source(original)
    baseline = bom + original.replace("\n", eol).encode("utf-8")
    expected = bom + expected_text.replace("\n", eol).encode("utf-8")
    wrong = expected_text.replace("\n", "\r\n" if eol == "\n" else "\n").encode("utf-8")
    assert patched_bytes(baseline, baseline) == expected
    assert patched_bytes(baseline, wrong) == expected
    assert patched_bytes(baseline, expected) == expected
    assert normalized_source(expected) == expected_text


def test_unrelated_change_is_refused():
    original = baseline_text().encode("utf-8")
    with pytest.raises(ValueError, match="UNRELATED_WORKTREE_CHANGE_REFUSED"):
        patched_bytes(original, original + b"# unrelated\n")


def test_mixed_baseline_is_refused():
    original = baseline_text().encode("utf-8")
    mixed = original.replace(b"\n", b"\r\n", 1)
    with pytest.raises(ValueError, match="MIXED_OR_UNSUPPORTED_BASELINE_EOL"):
        patched_bytes(mixed, original)
