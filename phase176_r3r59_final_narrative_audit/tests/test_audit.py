"""Text-only preview guards; these fixtures are not proof certificates."""
import json

from phase176_r3r59_final_narrative_audit import audit
from phase176_r3r59_final_narrative_audit.audit import (
    add_source_tag, preview, unique_body_line,
)


def test_source_tag_keeps_math_and_existing_citations():
    original = '[R6], [R7]を用いて, $H(a)=b$.'
    assert add_source_tag(original, 8) == '[R6], [R7], [R8]を用いて, $H(a)=b$.'
    assert add_source_tag(original, 7) == original
    assert add_source_tag('$H(a)=b$.', 8) is None
    assert add_source_tag('prefix ' + original, 8) is None


def test_preview_changes_exact_body_anchors_only():
    original = '使用する結果\n$E(a)=b$.\n証明\n\n$E(a)=b$.\n\n[R6]より, $H(b)=c$.\n\n□\n'
    expected = '使用する結果\n$E(a)=b$.\n証明\n\n[R6], [R8]を用いて, $H(b)=c$.\n\n□\n'
    assert preview(original, ['$E(a)=b$.'], {'[R6]より, $H(b)=c$.': '[R6], [R8]を用いて, $H(b)=c$.'}) == expected
    assert unique_body_line(original, '$E(a)=b$.') == 4


def test_preview_refuses_missing_ambiguous_and_overlapping_anchors():
    md = '証明\n$a=b$.\n$a=b$.\n□\n'
    assert preview(md, ['$a=b$.'], {}) is None
    assert preview(md, ['$x=y$.'], {}) is None
    assert preview('証明\n$a=b$.\n', ['$a=b$.'], {'$a=b$.': '$b=a$.'}) is None
    assert preview('使用する結果\n$a=b$.\n', ['$a=b$.'], {}) is None


def test_preflight_head_is_text_and_dry_run_prints_it(monkeypatch, capsys):
    """A git bytes result must be printable and JSON serializable."""
    head = '4a23549266f6f7d85306072aa3ab2544c0f70f0e'

    def git(*args):
        assert args == ('rev-parse', 'HEAD')
        return head.encode('ascii') + b'\r\n'

    # Only the external preflight inputs are isolated in this unit test.
    monkeypatch.setattr(audit.prior_apply, 'planned_changes', lambda: {'file': (b'same', b'same')})
    monkeypatch.setattr(audit, 'PINS', {})
    monkeypatch.setattr(audit.baseline.prior, 'git', git)
    assert audit.preflight() == head
    assert json.loads(json.dumps({'head': audit.preflight()})) == {'head': head}
    monkeypatch.setattr('sys.argv', ['audit', '--dry-run'])
    assert audit.main() == 0
    assert capsys.readouterr().out.splitlines() == [
        'PHASE176_R3R59_HEAD=' + head,
        'PHASE176_R3R59_GATE=PASS_R3R59_DRYRUN',
    ]
