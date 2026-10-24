from phase168_r3_39g5_fulltext_review.review import citation_integrity, compact, compare_lines, literal_positions, sections


def test_compact_retains_mathematical_restrictions():
    assert compact(r'$\pi_i^1=0\quad(i>1)$') != compact(r'$\pi_i^1=0$')


def test_sections_rejects_missing_headings():
    try:
        sections('証明のみ')
    except ValueError:
        return
    raise AssertionError('Expected ValueError')


def test_citation_integrity_requires_existing_reference():
    result = citation_integrity('**[R1] (4.5).**\nsource', '[R2]を適用')
    assert result['all_proof_citations_resolve'] is False


def test_order_search_finds_clauses():
    rows = literal_positions('A text B', (('A', ('A',)), ('B', ('B',))))
    assert rows[0]['position'] < rows[1]['position']


def test_diff_preserves_content_differences():
    assert compare_lines(r'\pi_i^1=0\quad(i>1)', r'\pi_i^1=0')
