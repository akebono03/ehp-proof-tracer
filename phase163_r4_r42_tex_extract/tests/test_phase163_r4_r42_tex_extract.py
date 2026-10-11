from pathlib import Path

from phase163_r4_r42_tex_extract import clean_source, extract_chapter, locate, make_report


def test_comments_not_registered(tmp_path: Path):
    text = '%\\begin{lemma}\\label{lem:1.9}\\end{lemma}\n\\begin{lemma}\\label{lem:1.1}A\\end{lemma}\n'
    path = tmp_path / 'x.tex'
    path.write_text(text, encoding='utf-8')
    items = extract_chapter(path, 1)['items']
    assert len(items) == 1
    assert items[0]['locator_candidate'] == 'Lemma 1.1'


def test_locator_does_not_invent_missing_number():
    assert locate('lemma', [], [], 2) is None
    assert locate('equation', [], ['2.7'], 2) == '(2.7)'
    assert locate('proposition', ['prop:5.3'], [], 5) == 'Proposition 5.3'


def test_read_only_and_existing_id_matching(tmp_path: Path):
    (tmp_path / 'Toda_01_corrected.tex').write_text(
        '\\begin{proposition}\\label{prop:1.2}式\\end{proposition}', encoding='utf-8'
    )
    report = make_report(tmp_path, existing_ids=['toda:Proposition 1.2'])
    assert report['matched_existing_reference_count'] == 1
    assert report['registration_applied'] is False
    assert report['missing_sources'] == [
        'Toda_02_2(2).tex', 'Toda_03_2(2).tex',
        'Toda_04_2(2).tex', 'Toda_05_2(6).tex',
    ]


def test_escaped_percent_and_comment_handling():
    assert clean_source('A \\% B % comment\n') == 'A \\% B \n'
