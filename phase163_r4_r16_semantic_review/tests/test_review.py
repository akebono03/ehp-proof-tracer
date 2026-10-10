from phase163_r4_r16_semantic_review.review import classify_context, inventory, locator_for, nested_items


def test_locator_named():
    assert locator_for('prop:1-3') == 'Proposition 1.3'
    assert locator_for('lem:double-coset') == 'Lemma 1.1 (provisional)'


def test_unknown_locator_remains_blank():
    assert locator_for('other') == ''


def test_mathematical_identity_not_inferred_by_locator():
    tex = r'''\section*{CHAPTER I\ Example}
\begin{proposition}\label{prop:1-3} A=B \end{proposition}
\end{document}'''
    entries = inventory(tex, 'reference_locator="Proposition 1.3"')
    assert entries[0]['legacy_locator_state'] == 'LOCATOR_ONLY_NOT_EQUIVALENCE'
    assert entries[0]['semantic_identity'] == 'UNREVIEWED'
    assert entries[0]['statement_id'] == ''


def test_clause_marker_is_not_promoted_to_statement():
    tex = r'''\section*{CHAPTER I\ Example}
\begin{proposition}\label{prop:1-2}
\begin{enumerate}
\item first
\item second
\end{enumerate}
\end{proposition}
\end{document}'''
    assert len(nested_items(tex)) == 2
    assert len(inventory(tex)) == 1


def test_context_is_only_provisional():
    kind, priority, reason = classify_context('と定める', 'numbered_math')
    assert kind == 'POSSIBLE_DEFINITION'
    assert priority == 'HIGH'
    assert reason == 'definition_marker'
