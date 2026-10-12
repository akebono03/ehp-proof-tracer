"""R5-R3: shared Web math punctuation regression tests."""
import pytest

from web_group_proof import (
    _build_group_proof_inline_segments,
    _build_group_proof_rendered_lines,
)


@pytest.mark.parametrize("mark", [".", "。", ",", "、"])
def test_tagged_equation_keeps_trailing_punctuation_in_display_math(mark):
    segments = _build_group_proof_inline_segments(
        r"$2\nu'=\eta_3\eta_4\eta_5\tag{1}$" + mark
    )
    assert len(segments) == 1
    assert segments[0].kind == "display_math"
    expected = "." if mark in (".", "。") else ","
    assert segments[0].value.endswith(r"\text{" + expected + r"}\tag{1}")


def test_tagged_equation_punctuation_with_space_is_not_orphaned():
    segments = _build_group_proof_inline_segments(r"$x=y\tag{2}$ .")
    assert len(segments) == 1
    assert segments[0].value == r"x=y\text{.}\tag{2}"


def test_tagged_equation_without_punctuation_is_unchanged():
    segments = _build_group_proof_inline_segments(r"$x=y\tag{2}$")
    assert [(s.kind, s.value) for s in segments] == [
        ("display_math", r"x=y\tag{2}"),
    ]


def test_tagged_equation_followed_by_prose_is_not_modified():
    segments = _build_group_proof_inline_segments(r"$x=y\tag{2}$, therefore")
    assert [(s.kind, s.value) for s in segments] == [
        ("display_math", r"x=y\tag{2}"),
        ("text", ", therefore"),
    ]


def test_untagged_inline_equation_keeps_sentence_punctuation():
    segments = _build_group_proof_inline_segments(r"Therefore $x=y$.")
    assert [(s.kind, s.value) for s in segments] == [
        ("text", "Therefore "), ("inline_math", "x=y"), ("text", "."),
    ]


def test_markdown_line_parser_handles_tagged_equation_without_orphan():
    lines = _build_group_proof_rendered_lines(r"$x=y\tag{1}$.")
    assert len(lines) == 1
    assert [(s.kind, s.value) for s in lines[0].segments] == [
        ("display_math", r"x=y\text{.}\tag{1}"),
    ]


def test_third_level_markdown_heading_is_rendered_as_heading():
    lines = _build_group_proof_rendered_lines("### 単射性\n$x=y$.\n")
    assert lines[0].kind == "heading"
    assert lines[0].prefix == "単射性"
    assert lines[1].segments[-1].value == "."


def test_second_level_heading_and_separator_unchanged():
    lines = _build_group_proof_rendered_lines("## 証明\n---\n")
    assert [line.kind for line in lines] == ["heading", "separator"]


def test_unterminated_math_block_still_rejected():
    with pytest.raises(ValueError, match="unterminated display-math"):
        _build_group_proof_rendered_lines("\\[\n x=y")
