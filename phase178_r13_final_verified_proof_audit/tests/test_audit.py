from __future__ import annotations

import pytest

from phase178_r13_final_verified_proof_audit.audit import (
    BASE_LINE, FIRST, SECOND, check_narrative, digest,
)


def fixture():
    return '\n'.join([
        '使用する結果', '', '**[R1] Proposition 5.8.**', '',
        '**[R2] DB.**', '', '**[R3] Proposition 4.2 (4.4).**', '',
        '**[R4] Lemma 5.7.**', r"$E(\eta_{2}\nu')=0$.", '',
        '**[R5] DB.**', '', '証明', '', FIRST, '', SECOND, '', '□', '',
    ])


def test_final_narrative_contract():
    assert check_narrative(fixture()) == {
        'reference_headers': [1, 2, 3, 4, 5],
        'zero_image_body_count': 2, 'base_in_reference_only': True,
    }


@pytest.mark.parametrize('edit', [
    lambda s: s.replace(FIRST, FIRST + '\n' + FIRST),
    lambda s: s.replace(FIRST, BASE_LINE + '\n' + FIRST),
    lambda s: s.replace(SECOND, ''),
    lambda s: s.replace(FIRST, 'SWAP').replace(SECOND, FIRST).replace('SWAP', SECOND),
    lambda s: s.replace(r"$E(\eta_{2}\nu')=0$.", 'missing formula'),
    lambda s: s.replace('**[R4] Lemma 5.7.**', '**[R4] other source.**'),
    lambda s: s.replace('**[R5] DB.**', '**[R6] DB.**'),
    lambda s: s.replace('□', 'not completed'),
])
def test_reject_changed_display(edit):
    with pytest.raises(RuntimeError):
        check_narrative(edit(fixture()))


def test_normalized_hash_matches_windows_line_endings():
    assert digest(b'a\r\nb\r\n') == digest(b'a\nb\n')
    assert digest(b'\xef\xbb\xbfa\nb\n') == digest(b'a\nb\n')
    assert digest(b'a\nb\n') != digest(b'a\nc\n')
