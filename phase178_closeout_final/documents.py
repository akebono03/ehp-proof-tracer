"""Build complete Phase 178 Markdown files from verified local evidence."""
from __future__ import annotations

MARKER = 'PHASE178_FINAL_CLOSEOUT_20261127'
DOCUMENTS = ('README.md', 'docs/design.md', 'docs/development_log.md',
             'docs/roadmap.md', 'docs/proof_records.md')
HEADINGS = {
    'README.md': ('## Current development status — Phase 177 formally closed (active scope)',
                  '## Historical status — Phase 177 formally closed (active scope)'),
    'docs/design.md': ('## Phase 177 の現行設計と終了監査の境界',
                       '## Phase 177 の設計と終了監査の境界（履歴）'),
    'docs/roadmap.md': ('## Phase 177 正式終了後の現在地と Phase 178 の境界',
                        '## Phase 177 正式終了時の計画（履歴）'),
}
MATH = r'''$$
\begin{aligned}
\pi_8^2 &= \mathbb Z/2\{\eta_2\nu'\eta_6^2\},\\
\pi_9^3 &= 0,\\
\pi_{10}^4 &= \mathbb Z/8\{\nu_4^2\},\\
\pi_{11}^5 &= \mathbb Z/2\{\nu_5^2\},\\
\pi_{12}^6 &= \mathbb Z/2\{\nu_6^2\},\\
\pi_{13}^7 &= \mathbb Z/2\{\nu_7^2\}.
\end{aligned}
$$
'''
BOUNDARY = r'$\pi_{14}^8=\mathbb Z/2\{\nu_8^2\}$'


def render_full(name, raw, section):
    """Preserve all prior content except explicit heading and terminology corrections."""
    if name not in DOCUMENTS or MARKER.encode() in raw or section.count(MARKER) != 1:
        raise ValueError('INVALID_DOCUMENT_BASELINE_OR_SECTION:' + name)
    raw.decode('utf-8-sig')
    if name != 'README.md':
        raw = raw.replace('不安定'.encode(), '非安定'.encode())
        section = section.replace('不安定', '非安定')
    eol = b'\r\n' if raw.count(b'\r\n') > raw.count(b'\n') // 2 else b'\n'
    section = section.replace('\r\n', '\n').replace('\r', '\n')
    addition = section.rstrip().replace('\n', eol.decode('ascii')).encode('utf-8') + eol
    if name in HEADINGS:
        old, new = (s.encode('utf-8') for s in HEADINGS[name])
        if raw.count(old) != 1:
            raise ValueError('HISTORICAL_HEADING_NOT_UNIQUE:' + name)
        updated = raw.replace(old, new, 1)
        end = updated.index(b'\n') + 1
        return updated[:end] + eol + addition + eol + updated[end:]
    return raw + (eol if raw.endswith(b'\n') else eol + eol) + addition


def stats_lines(report, language):
    lines = []
    for row in report['k6_groups']:
        n = row['n']
        s, i, g, c = (row[key] for key in ('proven_step_count', 'inference_count', 'given_count', 'model_citation_count'))
        if language == 'en':
            lines.append(f'- n={n}, k=6: {s} steps (INFERENCE {i}, GIVEN {g}), {c} model citations.')
        else:
            lines.append(f'- n={n}, k=6：{s} 段階（INFERENCE {i}、GIVEN {g}）、モデル出典 {c} 件。')
    return '\n'.join(lines) + '\n'


def sections(report, evidence_hash, narratives):
    """Write the current design, history, roadmap and actual saved narratives."""
    head = report['head']
    full = report['summary']
    focused = report['focused']['passed']
    stdout = report['stdout_sha256']
    stderr = report['stderr_sha256']
    xml = report['full_pytest_evidence']['xml_sha256']
    marker = '<!-- ' + MARKER + ' -->\n\n'
    stats_en = stats_lines(report, 'en')
    stats_ja = stats_lines(report, 'ja')
    scope_en = ('The 831 distinct registered CSV coordinates (n >= 2, k >= 0) are partitioned by the existing '
                'stable-range predicate `is_in_toda_stable_range` into 21 active unstable groups through the 6-stem, '
                '313 stable-range groups, and 497 future unstable groups. All 21 active groups are complete with '
                'zero open goals, incomplete groups or unmeasured groups. No bulk stable-range or future-stem search '
                'was performed. The stable boundary ' + BOUNDARY + ' alone was separately observed as '
                '`generic-partial-proof` with 8 open goals and zero target GIVENs; it is deferred to Phase 179. '
                'This is not a certification of all 831 coordinates or every literature assertion.\n')
    scope_ja = ('CSV の重複除去後の831座標（$n\\ge2,k\\ge0$）について、現行安定判定 '
                '`is_in_toda_stable_range`（$n\\ge k+2$）に従い、$k\\le6$ の非安定群21件を測定した。'
                '各 stem の件数は1、2、3、4、5、6。全21件 complete、Open Goals 0、未完成・未測定0件。'
                '安定群313件および将来の非安定群497件は一括探索対象外。安定境界 '
                + BOUNDARY + ' は別枠の観測で `generic-partial-proof`、Open Goals 8、対象 GIVEN 0。'
                'Phase 179 に持ち越す。全831座標または文献全命題の独立検証を認定しない。\n')
    en_evidence = (f'The end-of-phase active `tests/` suite ran once on `{head}`: **{full}** (exit 0). '
                   f'The separate focused suite passed {focused} tests, including all six historical R4C tests. '
                   f'Full stdout SHA-256: `{stdout}`; stderr SHA-256: `{stderr}`; JUnit XML SHA-256: `{xml}`. '
                   f'Measurement report SHA-256: `{evidence_hash}`. The document gate reuses the measurement '
                   'without running pytest or new proof searches. The R4C source contract now requires the independent '
                   'pre-Proposition 4.4 Hopf splitting, Proposition 4.2, (5.1), source chronology and proof replay. '
                   'Four distinct Phase 174 historical source-guard failures remain outside the active suite; '
                   'they were not rerun or counted as passing.\n')
    ja_evidence = (f'測定時 HEAD `{head}` にて現行アクティブ `tests/` の全体 pytest を Phase 末尾に1回実行し、'
                   f'**{full}**（終了コード0）。別枠の限定 pytest は {focused} 件 PASS（訂正済み R4C 全6件を含む）。'
                   f'全体 stdout SHA-256：`{stdout}`、stderr SHA-256：`{stderr}`、JUnit XML SHA-256：`{xml}`。'
                   f'測定 report SHA-256：`{evidence_hash}`。最終文書 Gate は実測記録を再利用し、pytest・再探索を行わない。'
                   '旧 R4C の出典条件を独立した Proposition 4.4 直前の Hopf 分解、Proposition 4.2、(5.1)、'
                   '文献順序と証明木再検証に訂正し、全6テスト PASS を確認した。'
                   'これとは別の Phase 174 履歴専用 Source Guard 4件は現行範囲外の既知失敗として維持し、'
                   '再実行・解決・PASS 計上していない。\n')
    rule_ja = ('Source-first（出典優先）、First Successful Proof Search（最初の成功で終了）、唯一性検査なしを維持する。'
               '先行 DB 結果は検証済みの順序条件を満たす場合に採用し、対象群の直接 GIVEN は追加しない。'
               'Δ 全射から懸垂零写像、有限群の位数一致と全射から単射、有限巡回群の生成元零像から零写像、'
               '有限巡回商群と懸垂同型による生成元輸送、一般の写像同型から型付き懸垂同型への接続を用いた。'
               'Toda (5.12) の適用範囲は n=4,5,6 に限定する。(5.13) の型付き関係を出典順序に従い使用し、'
               'η の表記を既存の型付き DB 表記と整合させた。群専用証明・専用 Narrative は追加しない。\n')
    renderer_ja = ('共通経路 Verified Proof Tree（検証済み証明木）→ `ProofNarrativeModel` → 共通 Renderer（表示器）→ Web '
                   'を維持する。R12R2、R17R3/R17R4、R23 の表示整理は実際の根祖先・出典・型付き前提を確認したうえで、'
                   '零合成の冗長な記述、有限巡回商群と部分群の表記、因子の懸垂等式および重複同型表示を整理する。'
                   '内部 ProofStep、出典対応、完成・未完成状態は変更しない。旧 R4C はテストの出典契約だけを訂正し、'
                   '数学的規則、Provider、Renderer は R30R1 で変更していない。\n')
    next_ja = (r'Phase 179 は $k=7$ の非安定登録群の Source-first 監査から開始する。'
               'Lemma 5.14 による $\\sigma_8$ の存在と (5.15) の分解を型付きの独立した出典・前提として監査し、'
               + BOUNDARY + ' の証明への接続を検討する。後続の出典を先行目標に循環使用しない。'
               'R27 では (5.15) と Lemma 5.14 が archive に存在するが必要な型付き GIVEN が未接続であり、'
               '既存の Proposition 4.4 直前の分解の単射規則は n=4 に限定されていることを確認した。'
               '今回の Closeout では新規の数学規則や将来 Phase の機能を先取りしない。\n')
    totals_ja = ('非安定6-stem の6群はすべて `generic-complete-proof`。根祖先83段階（INFERENCE 56、GIVEN 27）、'
                 'モデル出典延べ27件、Open Goals 0、対象群の直接 GIVEN 0。出典数は群間の重複を含む。\n')
    proof_sections = []
    for row in report['k6_groups']:
        n = row['n']
        proof_sections.append(f'### n={n}, k=6：保存済み共通 Narrative\n\n'
                              + narratives[n].strip() + '\n')
    return {
        'README.md': marker + '## Current development status — Phase 178 formally closed (active scope)\n\n'
            + 'Phase 178 completes all six registered unstable 6-stem groups (free part and 2-primary component):\n\n'
            + MATH + '\nAll six results are `generic-complete-proof`: 83 root-ancestry steps, 56 INFERENCE steps, '
            '27 GIVEN leaves, 27 model citations counted across proofs, zero open goals and zero direct target-group GIVENs.\n\n'
            + stats_en + '\nSource-first typed backward search, first successful proof, no uniqueness search and the common '
            'Verified Proof Tree → ProofNarrativeModel → Renderer → Web path remain the policy. '
            'Finite-group cardinality, zero-map, cyclic quotient and suspension-isomorphism transport rules and '
            'source-scoped (5.12), (5.13) connections support the 6-stem proofs. Display compression preserves the proof tree.\n\n'
            + scope_en + '\n' + en_evidence + '\nNext: Phase 179 audits the 7-stem, including Lemma 5.14, the sigma family '
            'and (5.15), before connecting the deferred stable 6-stem boundary. No future-phase rules are added by this closeout.\n',
        'docs/design.md': marker + '## Phase 178 の現行設計と終了監査の境界\n\n'
            + MATH + '\n' + totals_ja + '\n' + rule_ja + '\n' + renderer_ja + '\n' + scope_ja + '\n' + ja_evidence,
        'docs/development_log.md': marker + '## 2026-11-27 — Phase 178 正式終了（現行範囲）\n\n'
            + MATH + '\n' + totals_ja + '\n' + stats_ja + '\n'
            + 'R1〜R13：非安定6-stem の出典優先監査、有限群の全射・単射・零写像、零群証明と表示整理。\n\n'
            + 'R14〜R17： (5.12)、(5.13) と有限巡回商群の接続、共通表示の整理。R19〜R26：懸垂同型による有限巡回群輸送、'
            '生成元零像、n=6,7 の証明完成、表記整合、根祖先・出典・表示監査。\n\n'
            + 'R27：安定境界を別枠で監査し、R28 の接続を Phase 179 に延期。R29：非安定6群の最終監査（106件 PASS）。'
            'R30：旧 R4C の失敗原因を出典条件の不一致と判定（41件 PASS、旧テスト1件の既知失敗を別枠確認）。'
            'R30R1：出典条件を訂正し47件 PASS、旧 R4C は全6件 PASS。\n\n'
            + scope_ja + '\n' + ja_evidence + '\n' + next_ja,
        'docs/roadmap.md': marker + '## Phase 178 正式終了後の現在地と Phase 179 の境界\n\n'
            + MATH + '\n' + totals_ja + '\n' + scope_ja + '\n' + ja_evidence + '\n' + next_ja
            + '\n今後の終了測定も開発済み stem までの非安定登録群を対象とし、安定群の一括再探索と将来の非安定群の探索を行わない。'
            '必要な安定境界の個別監査は別枠に記録する。全体 pytest は Phase 末尾に実施する。\n',
        'docs/proof_records.md': marker + '## 2026-11-27 — Phase 178：非安定6-stem の完成証明\n\n'
            + MATH + '\n' + totals_ja + '\n' + stats_ja + '\n'
            + '以下は Closeout Measurement の各公開探索で保存した共通 Narrative の記録である。'
            '新たな GIVEN や専用証明として登録するものではない。\n\n'
            + '\n'.join(proof_sections) + '\n' + scope_ja + '\n' + ja_evidence,
    }
