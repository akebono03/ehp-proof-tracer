from pathlib import Path
from phase163_r4_r15_chapter1.inventory import extract, run, strip_comments


def test_comment_does_not_introduce_false_label():
    text = '\\section*{CHAPTER I}\n% \\begin{lemma}\\label{fake}\n\\begin{lemma}\\label{real}\ntext\n\\end{lemma}'
    rows = extract(text)
    assert len(rows) == 1
    assert rows[0]['label'] == 'real'


def test_nested_enumeration_kept_in_proposition():
    text = '\\section*{CHAPTER I}\n\\begin{proposition}\\label{p}\n\\begin{enumerate}\n\\item x\n\\end{enumerate}\n\\end{proposition}'
    rows = extract(text)
    assert len(rows) == 1 and rows[0]['end_line'] == 6


def test_numbered_and_unnumbered_math_are_separate():
    text = '\\section*{CHAPTER I}\n\\begin{equation}x\\end{equation}\n\\[y\\]'
    rows = extract(text)
    assert [r['category'] for r in rows] == ['numbered_math', 'unnumbered_display']


def test_no_automatic_verification_or_id(tmp_path: Path):
    source = tmp_path / 'chapter.tex'
    source.write_text('\\section*{CHAPTER I}\n\\begin{lemma}\\label{a} x \\end{lemma}', encoding='utf-8')
    summary = run(source, tmp_path / 'out')
    assert summary['statement_ids_assigned'] == 0
    assert summary['source_verified'] == 0
    assert (tmp_path / 'out' / 'candidates.csv').exists()


def test_escaped_percent_is_not_comment():
    assert strip_comments(r'\\text{50\%} % comment') == r'\\text{50\%} '
