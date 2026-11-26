"""Regression: the shared complete-proof layout splits the R11 sentence."""
from phase178_r11_hopf_zero_reason_display.audit import hopf_reason_displayed

FIRST = r"完全性より, $\operatorname{Im}H=\ker\Delta=0$ なので, $H$ は零写像."
SECOND = (r"よって, $\operatorname{Im}E=\ker H=\pi_{9}^{3}$ となり, "
          r"$E: \pi_{8}^{2}\to \pi_{9}^{3}$ は全射.")
SENTENCE = FIRST + ' ' + SECOND


def body(*lines):
    return '\n'.join(('使用する結果', '', '証明', '', *lines, '', '□'))


def test_accept_exact_split_paragraphs():
    assert hopf_reason_displayed(body(FIRST, '', SECOND), SENTENCE)
    assert hopf_reason_displayed(body(FIRST, '', '', SECOND), SENTENCE)
    assert not hopf_reason_displayed(body(SENTENCE), SENTENCE)


def test_reject_missing_reordered_or_intervening_sentences():
    for lines in ((FIRST,), (SECOND,), (SECOND, FIRST),
                  (FIRST, '別の推論.', SECOND),
                  (FIRST, SECOND.replace('\\pi_{9}^{3}', '\\pi_{10}^{3}'))):
        assert not hopf_reason_displayed(body(*lines), SENTENCE)


def test_reject_duplicate_and_reference_only_matches():
    assert not hopf_reason_displayed(body(FIRST, SECOND, FIRST), SENTENCE)
    assert not hopf_reason_displayed(body(FIRST, SECOND, SECOND), SENTENCE)
    assert not hopf_reason_displayed('\n'.join((FIRST, SECOND, '証明', '□')), SENTENCE)
    assert not hopf_reason_displayed(body(FIRST, SECOND, '証明'), SENTENCE)
    assert not hopf_reason_displayed(body(FIRST, SECOND), None)


def test_real_common_sentence_layout():
    from phase171_r20r13_eta_sentence_layout.projection import split_completed_proof_sentences
    lines = ['使用する結果', '', '証明', '', SENTENCE, '', '□']
    formatted = split_completed_proof_sentences(lines)
    assert FIRST in formatted and SECOND in formatted
    assert hopf_reason_displayed('\n'.join(formatted), SENTENCE)
