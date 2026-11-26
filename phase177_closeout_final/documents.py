"""Full document rendering from measured evidence; preserve dated history."""
from __future__ import annotations

MARKER = 'PHASE177_FINAL_CLOSEOUT_20261126'
HEADINGS = {
    'README.md': ('## Current development status — Phase 176 formally closed (active scope)',
                  '## Historical status — Phase 176 formally closed (active scope)'),
    'docs/design.md': ('## Phase 176 の現行設計境界（終了監査）',
                       '## Phase 176 の設計境界（終了時の履歴）'),
    'docs/roadmap.md': ('## Phase 176 正式終了後の現在地と次 Phase の境界',
                        '## Phase 176 正式終了時の計画（履歴）'),
}
DOCUMENTS = ('README.md', 'docs/design.md', 'docs/development_log.md', 'docs/roadmap.md', 'docs/proof_records.md')


def render_full(name, raw, section):
    if name not in DOCUMENTS or MARKER.encode() in raw or section.count(MARKER) != 1:
        raise ValueError('INVALID_DOCUMENT_BASELINE_OR_SECTION:' + name)
    raw.decode('utf-8-sig')
    if name != 'README.md':
        raw = raw.replace('不安定'.encode('utf-8'), '非安定'.encode('utf-8'))
        section = section.replace('不安定', '非安定')
    eol = b'\r\n' if raw.count(b'\r\n') > raw.count(b'\n') // 2 else b'\n'
    addition = section.rstrip().replace('\n', eol.decode('ascii')).encode('utf-8') + eol
    if name in HEADINGS:
        old, new = (s.encode('utf-8') for s in HEADINGS[name])
        if raw.count(old) != 1:
            raise ValueError('HISTORICAL_HEADING_NOT_UNIQUE:' + name)
        updated = raw.replace(old, new, 1)
        end = updated.index(b'\n') + 1
        return updated[:end] + eol + addition + eol + updated[end:]
    return raw + (eol if raw.endswith(b'\n') else eol + eol) + addition


def sections(report, r1_hash):
    head = report['head']
    summary = report['summary']
    stdout = report['stdout_sha256']
    stderr = report['stderr_sha256']
    marker = '<!-- ' + MARKER + ' -->\n\n'
    en_evidence = (f'The active `tests/` suite ran once on `{head}`: **{summary}**. '
                   f'Stdout SHA-256: `{stdout}`; stderr SHA-256: `{stderr}`. '
                   f'The scoped R1 report SHA-256 is `{r1_hash}`. '
                   'The original measurement was interrupted during the overly broad group scan, after pytest had passed. '
                   'R1 reused eight active group observations and ran only the seven missing searches; it did not rerun pytest. '
                   'The final document gate reuses those results without new proof searches. Four known historical Phase 174 '
                   'Source Guard failures remain outside the active suite; they were not rerun, resolved or counted as passing.\n')
    ja_evidence = (f'現行アクティブ `tests/` の全体 pytest は HEAD `{head}` で1回実行し、'
                   f'**{summary}**（終了コード0）。stdout SHA-256：`{stdout}`、stderr SHA-256：`{stderr}`。'
                   f'範囲修正 R1 report SHA-256：`{r1_hash}`。初回は全体 pytest 成功後、過大な登録群探索中の '
                   'KeyboardInterrupt により終了 Gate が FAIL となった。R1 は非安定群8件の既存観測を再利用し、'
                   '不足7件のみ探索した。全体 pytest は再実行していない。最終文書 Gate でも再探索・再テストしない。'
                   '歴史的な Phase 174 Source Guard 4件は現行範囲外の既知失敗として残し、再実行・解決・PASS 計上していない。\n')
    scope_ja = ('CSV の重複除去後の831座標（$n\\ge2, k\\ge0$）のうち、現行安定判定 '
                '`is_in_toda_stable_range`（$n\\ge k+2$）に従い、$k\\le5$ の非安定登録群15件を監査し、'
                '15件すべて complete、Open Goals 0、未完成・未測定0件。k=1,2,3,4,5 の非安定群は各1,2,3,4,5件。'
                'k=5 の登録6群（安定範囲1群を含む）も初回実測ですべて complete。'
                '安定群313件は既存完成方針に従い R1 の個別探索対象外、将来の非安定群503件も対象外。'
                '初回は75座標まで探索したが、全831群の完成を認定しない。安定群313件すべてを今回再検証したとは主張しない。\n')
    math = r'''選定目標 $(n,k)=(5,5)$：

$$
\pi_{10}^{5}=\mathbb Z/2\{\nu_5\eta_8^2\}.
$$

`generic-complete-proof`、証明木43段階（INFERENCE 35、GIVEN 8）、出典8件、先行 DB 結果4件、Open Goals 0、対象結論の直接 GIVEN 0。R18 限定 pytest 101件 PASS。公開の型付き参照探索、Trust Boundary（信頼境界）、Narrative（証明表示）を確認した。
'''
    rules = ('Proposition 2.5 の条件付き符号なし Δ 合成、一般懸垂等式、合成結合律と等式推移律、直和成分の位数、'
             '有限巡回群の生成元像の位数による単射性、Δ 単射と連続する EHP 完全性から E 全射、'
             '既存の rank-two elementary 2-group quotient（階数2の基本2群の商）および懸垂合成規則を接続した。'
             '対象群専用証明・専用 Narrative・結論直接 GIVEN は追加しない。Source-first、First Successful Proof Search、唯一性検査なしを維持する。\n')
    proof = r'''使用する結果：R1 `sphere.csv` (4,5)、R2 同 (9,2)（参考 Proposition 5.3）、R3 Proposition 2.5、R4 (5.11)、R5 Proposition 4.2 (4.4)、R6 `sphere.csv` (9,1)（参考 Proposition 5.1）、R7 同 (4,4)、R8 Chapter V, iii) $\nu$-family definition。

R5 の完全列：

$$
\pi_{11}^{9}\xrightarrow{\Delta}\pi_9^4\xrightarrow{E}\pi_{10}^5\xrightarrow{H}\pi_{10}^9\xrightarrow{\Delta}\pi_8^4.
$$

R1, R2 より $\pi_9^4=\mathbb Z/2\{\nu_4\eta_7^2\}\oplus\mathbb Z/2\{E\nu'\eta_7^2\}$、$\pi_{11}^9=\mathbb Z/2\{\eta_9^2\}$。R4 の $\Delta(\eta_9)=E\nu'\eta_7$ と R3 の条件付き合成公式から $\Delta(\eta_9^2)=E\nu'\eta_7^2$。

R6, R7 より $\pi_{10}^9=\mathbb Z/2\{\eta_9\}$、$\pi_8^4=\mathbb Z/2\{\nu_4\eta_7\}\oplus\mathbb Z/2\{E\nu'\eta_7\}$。生成元の像の位数が2なので後側の Δ は単射、完全性から E は全射。さらに

$$
\ker E=\operatorname{Im}\Delta=\mathbb Z/2\{E\nu'\eta_7^2\}.
$$

R8 と懸垂合成から $E(\nu_4\eta_7^2)=\nu_5\eta_8^2$。準同型定理と商群の生成元により

$$
\pi_{10}^5\cong\pi_9^4/\ker E,
\qquad \pi_{10}^5=\mathbb Z/2\{\nu_5\eta_8^2\}.
$$

これは共通 Renderer による検証済み証明の記録であり、新しい GIVEN ではない。補助等式の表示省略は内部43段階・出典8件を変更しない。
'''
    display = ('R17R1〜R17R6R1 は共通 Renderer で有限巡回群の単射理由、商群、補助懸垂等式、'
               '対称律・結合律・推移律の等式連鎖、重複等式、懸垂合成の補助等式と出典引き継ぎを整理した。'
               '表示圧縮は実際の型付き依存関係に基づき、Verified Proof Tree → `ProofNarrativeModel` → 共通 Renderer → Web '
               'の経路を維持する。内部証明木・出典・未解決状態を書き換えない。\n')
    next_ja = ('次の Phase 178 は $k=6$ の非安定登録群の Source-first 監査を開始候補とする。'
               '現行コード・出典・未完成 Goal の確認後に対象を確定し、今回新規規則や将来 Phase の機能を追加しない。'
               '以後の Closeout は開発済み stem までの非安定登録群を対象とし、安定群は個別再探索せず、'
               '将来の非安定群も対象外とする。取得済み実測を再利用し、全体 pytest は Phase 末尾にのみ実行する。\n')
    return {
        'README.md': marker + r'''## Current development status — Phase 177 formally closed (active scope)

Phase 177 completes $(n,k)=(5,5)$:

$$
\pi_{10}^5=\mathbb Z/2\{\nu_5\eta_8^2\}.
$$

The source-first public search returns `generic-complete-proof`: 43 linked ProofSteps (35 INFERENCE, 8 GIVEN), eight references, four verified prior database results, zero open goals, and no direct target GIVEN. R18 passed 101 focused tests. The proof combines the conditional unsigned Delta composition formula, typed suspension and reassociation, order of a direct-summand generator, finite cyclic injectivity, EHP exactness and suspension surjectivity, and the existing rank-two quotient rule. The common renderer compresses auxiliary equalities without removing internal proof nodes or citations. The first successful proof is accepted; no uniqueness search or target-specific proof/narrative is introduced.

The scoped closeout measured all 15 registered unstable groups with $k\le5$ as complete (zero incomplete or unmeasured); all six registered 5-stem groups also completed in the original measurement, including one stable-range group. Of the 831 distinct CSV coordinates with $n\ge2,k\ge0$, the 313 stable-range coordinates ($n\ge k+2$) and 503 future unstable coordinates were excluded from R1's individual searches. The initial scan observed 75 coordinates before interruption; this is not an audit of every stable or registered group. The established stable-group completion policy is retained without new individual stable searches in R1.

''' + en_evidence + '\nNext: audit registered unstable 6-stem groups before selecting a Phase 178 target. This closeout certifies only the measured active scope, not every CSV group or independent verification of all printed literature.\n',
        'docs/design.md': marker + '## Phase 177 の現行設計と終了監査の境界\n\n' + math + '\n' + rules + '\n' + display + '\n' + scope_ja + '\n' + ja_evidence,
        'docs/development_log.md': marker + '## 2026-11-26 — Phase 177 正式終了（現行範囲）\n\n' + math + '\n' + rules + '\n' + display + '\n' + ja_evidence + '\n' + scope_ja + '\n' + next_ja,
        'docs/roadmap.md': marker + '## Phase 177 正式終了後の現在地と Phase 178 の境界\n\n' + math + '\n' + scope_ja + '\n' + ja_evidence + '\n' + next_ja,
        'docs/proof_records.md': marker + '## 2026-11-26 — Phase 177：5-stem の完成証明\n\n' + math + '\n' + proof + '\n' + scope_ja + '\n' + ja_evidence,
    }
