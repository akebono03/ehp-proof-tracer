"""Build full documents from the exact reviewed checkout; preserve history."""
from __future__ import annotations

MARKER = 'PHASE176_FINAL_CLOSEOUT_20261125'
DOCUMENT_BLOBS = {
    'README.md': 'b80e23a0e9d917554e98c7d531b006eb593002fd',
    'docs/design.md': '7812ca7a9d560912e15d894773373801bf6eb303',
    'docs/development_log.md': '9b28c168199a188a8d6d6cab3845a9de42daee19',
    'docs/roadmap.md': 'c80f77c495f9008b1d3bade3a37ed23ec95a521b',
    'docs/proof_records.md': 'ad5029d979654a2efc48102917d41510091e8a50',
}
# These obsolete current-status headings become explicitly historical. The
# actual checkpoint text and later final records are retained byte-for-byte.
HISTORICAL_HEADINGS = {
    'README.md': (
        '## Current development status — Phase 175 closeout pending (2026-11-19)',
        '## Historical checkpoint — Phase 175 before closeout (2026-11-19)',
    ),
    'docs/design.md': (
        '## Phase 175 の現行設計境界（2026-11-19・終了文書準備）',
        '## 履歴：Phase 175 の終了文書準備時点の設計境界（2026-11-19）',
    ),
    'docs/roadmap.md': (
        '## Phase 175：R4R14R12 終了文書整備後の工程（2026-11-19）',
        '## 履歴：Phase 175 R4R14R12 時点の終了工程（2026-11-19）',
    ),
}


def sections(report):
    """Return the new sections only after the gate has passed its test checks."""
    if report['full_pytest_exit'] != 0 or report['passed'] <= 0 or not report['summary']:
        raise ValueError('UNVERIFIED_FULL_TEST_RESULT')
    evidence = (f"HEAD `{report['head']}`; pytest `{report['summary']}`; "
                f"stdout SHA-256 `{report['stdout_sha256']}`; "
                f"stderr SHA-256 `{report['stderr_sha256']}`.")
    ja_evidence = ('現行アクティブ `tests/` 全体 pytest を Phase 末尾に1回実施し、成功を確認した。'
                   + evidence + '\n\n'
                   '旧 Phase 174 の固定 HEAD・関数スナップショット依存 Source Guard 4件は、'
                   '現行アクティブ範囲外の既知失敗として残す。今回再実行・解決・PASS 計上していない。'
                   '任意の球面ホモトピー群、5-stem 全体、全文献命題の独立検証を認定しない。\n')
    marker = f'<!-- {MARKER} -->\n\n'
    readme = marker + r'''## Current development status — Phase 176 formally closed (active scope)

Phase 176 completes the selected 5-stem target $(n,k)=(3,5)$:

$$
\pi_8^3=\mathbb Z/2\{\nu'\eta_6^2\}.
$$

The shared source-first search returns `generic-complete-proof`, with 62 linked ProofSteps (51 INFERENCE, 11 GIVEN), 10 internal citations and no open goals. The proof uses prior group results, Toda Lemma 5.7, Proposition 4.2 (4.4), Proposition 2.2, (5.3), family definitions and (5.5). It derives the zero suspension image by typed right composition, the finite cyclic Delta kernel, and the finite cyclic lift along an injective Hopf map. The target is not directly registered as a GIVEN. The first successful proof is accepted; no uniqueness search is required.

The common renderer preserves the verified tree and the partial-proof state. R3R60R2 uses 18 nonblank proof-body rows (including the end marker) and nine displayed references; the auxiliary nu-family definition is omitted only in the presentation, and original citation 10 is displayed as 9. All ten internal citations remain available. The public adapter and the final narrative were verified; the R3R60R2 focused run passed 60 tests. These projections are conditional on actual typed proof dependencies, not on the target coordinates.

The end-of-phase active `tests/` suite was run once successfully. ''' + evidence + r'''

**Scope and remaining limitations:** four historical Phase 174 source-guard failures remain outside this active suite; they were not rerun, resolved or counted as passes. This closure is for the selected target and the active suite, not every registered 5-stem group or independent verification of the original printed Toda edition. Earlier status sections below are dated history. The next phase must first select its mathematical scope; no future proof rule is introduced by this closeout.
'''
    design = marker + r'''## Phase 176 の現行設計境界（終了監査）

対象は $(n,k)=(3,5)$ の $\pi_8^3=\mathbb Z/2\{\nu'\eta_6^2\}$。Source-first（出典優先）、First Successful Proof Search（最初の成功で終了）、唯一性検査なしを維持する。出典に基づく型付き GIVEN、一般規則の INFERENCE、先行 DB の検証を分離する。対象結論の直接 GIVEN 登録や群専用 Narrative は導入しない。

- `phase176_r3r10_right_zero_transport_isolated/rule.py`：型付き懸垂零像を合成の右因子へ移送する。実際の前提、写像、合成因子の型を検査する。
- `phase176_r3r27r1_toda55_quadruple_isolated/source.py`：Toda (5.5) の一般公式を出典付きで特殊化する。族定義は内部前提として維持する。
- `phase176_r3r48_cited_finite_delta_kernel/rule.py`：有限巡回群間の生成元の像が符号付き生成元となるとき、型・位数・出典を検査して核を導く。
- `phase176_r3r43r1_finite_cyclic_subgroup_lift_isolated/rule.py`：H の単射性、EHP 完全性、余域の有限巡回構造、Δ の核、生成元候補の像という5前提から有限巡回群構造を導く。位数は $m/\gcd(m,q)$。候補の一致だけを証明とみなさない。

公開経路は Verified Proof Tree（検証済み証明木）→ `ProofNarrativeModel` → 共通 Renderer → Web Adapter。R3R53〜R3R60R2 は共通表示で核を部分群として表し、冗長等式、Hopf 合成、有限巡回持ち上げ、定義的懸垂、既出零関係と出典を整理した。最後の `project_citation_premise_elision()` は確認済みの一般公式の特殊化と右合成の実依存関係を要求する。表示に限り補助定義出典を省略し、残る参照を同時に再採番する。内部の Citation（出典対応）10件、証明木62段階、状態、未解決 Goal は変更しない。適用条件が成立しない場合は元の表示を返す。表示用番号を内部証明の出典番号として再利用しない。

実測対象は complete、INFERENCE 51、GIVEN 11、Open Goals 0、本文18行、表示出典9件。未完成表示の不変性を確認。R3R60R2 限定 pytest 60 PASS。今回の Closeout は本番コード、数学規則、GIVEN、旧テストを変更しない。

''' + ja_evidence
    log = marker + r'''## Phase 176 — 5-stem 選定目標の完成と正式終了

- R1〜R3：登録目標の Source-first（出典優先）監査、n=3 の不足前提・一般規則の調査。
- R3R5〜R3R10：Lemma 5.7 の明示零関係を確認し、型付き右合成零像移送の一般規則を整備。
- R3R16〜R3R42：公開接続、Hopf 合成・等式移送・Toda (5.3)/(5.5) の出典付き特殊化を順次監査・接続。
- R3R43〜R3R51：有限巡回部分群の持ち上げと有限巡回 Δ 核、Hopf 像の型付き接続を整備。選定目標 $\pi_8^3=\mathbb Z/2\{\nu'\eta_6^2\}$ の実探索が完成。根は INFERENCE、Open Goals 0。
- R3R52〜R3R58R1：共通核表示、等式の冗長性、出典表示、Hopf 合成の集約、有限巡回持ち上げの説明を改善。証明木は62段階（INFERENCE 51、GIVEN 11）、内部出典10件。
- R3R59〜R3R59R4：実際の型付き懸垂・表記移送の依存関係を監査し、定義的懸垂関係2文を表示のみ省略。R3R59R3 限定25 PASS、R3R59R4 限定38 PASS、本文21→19行。
- R3R60〜R3R60R2：既出の Lemma 5.7 零関係と右合成の実依存関係、Toda (5.5) の直接引用を監査。R3R60 14 PASS、R3R60R1 19 PASS、R3R60R2 60 PASS。本文19→18行、表示出典10→9件。旧内部出典9（ν-family 定義）を表示のみ省略、旧内部10（(5.5)）を表示9に再採番。内部出典は10件維持し、未引用表示出典0、結論表示1回、未完成表示不変。ユーザー環境の実 Web 表示を確認。
- Closeout：R3R60R2 の実 Web・Trust Boundary（検証境界）監査を再実施し、5文書を履歴保持の全文として生成。全体テストは次の実測結果に限定する。

''' + ja_evidence
    roadmap = marker + r'''## Phase 176 正式終了後の現在地と次 Phase の境界

選定目標 $(n,k)=(3,5)$ は $\pi_8^3=\mathbb Z/2\{\nu'\eta_6^2\}$、`generic-complete-proof`、Open Goals 0。証明木62段階（INFERENCE 51、GIVEN 11）、内部出典10件、共通 Narrative 本文18行・表示出典9件を確認した。Phase 175 の k=4 登録6群の終了記録は履歴として維持する。

次 Phase は残る k=5 登録群の完成・未完成状態と出典・型付き前提の不足を監査してから選定する。この段階で特定の追加目標や将来機能の実装を確定しない。DB 上の群構造と証明の完成を区別する。既に証明済みの群を先行結果として利用する場合は出典と順序を検証し、不要な再証明をしない。Source-first、First Successful Proof Search、唯一性検査なし、一般規則と共通 Renderer の方針を維持する。

''' + ja_evidence
    proof = marker + r'''## Phase 176 — $\pi_8^3=\mathbb Z/2\{\nu'\eta_6^2\}$ の完成証明

対象 $(n,k)=(3,5)$。公開結果 `generic-complete-proof`、Open Goals 0。検証済み証明木62段階（INFERENCE 51、GIVEN 11）、内部出典10件、表示出典9件。以下は実 Web Narrative に基づく数学的記録である。

### 使用する結果（表示用番号）

- [R1] 先行 DB（sphere.csv, n=2, k=5）：$\pi_7^2=\mathbb Z/2\{\eta_2\nu'\eta_6\}$。
- [R2] Lemma 5.7：$\Delta(\nu_5)=\pm\eta_2\nu'$、$E(\eta_2\nu')=0$。
- [R3] Proposition 4.2 (4.4)：EHP 完全性。
- [R4] 先行 DB（sphere.csv, n=5, k=3）：$\pi_8^5=\mathbb Z/8\{\nu_5\}$（参考：Proposition 5.6）。
- [R5] 先行 DB（sphere.csv, n=2, k=4）：$\pi_6^2=\mathbb Z/4\{\eta_2\nu'\}$。
- [R6] Proposition 2.2：$H(\alpha E\beta)=H(\alpha)E\beta$。
- [R7] Toda (5.3)：$H(\nu')=\eta_5$。
- [R8] Chapter V, i)：$\eta_n=E^{n-2}\eta_2$（$n\ge2$）。
- [R9] Toda (5.5)：$4\nu_n=\eta_n^3$（$n\ge5$）。

### 証明

[R3] の完全列

$$
\pi_7^2\xrightarrow{E}\pi_8^3\xrightarrow{H}\pi_8^5\xrightarrow{\Delta}\pi_6^2
$$

を考える。[R1], [R2] より、右合成と懸垂の関手性によって

$$
E(\eta_2\nu'\eta_6)=E(\eta_2\nu')E\eta_6=0.
$$

生成元が零に写るので E は零写像。完全性より H は単射。[R4], [R5], [R2] より Δ は位数8の巡回群の生成元を位数4の巡回群の符号付き生成元に写す。したがって

$$
\ker\Delta=\langle4\nu_5\rangle.
$$

[R6], [R7], [R8] により

$$
\begin{aligned}
H(\nu'\eta_6^2)&=H(\nu'E\eta_5^2)\\
&=H(\nu')E\eta_5^2\\
&=\eta_5 E\eta_5^2=\eta_5^3.
\end{aligned}
$$

[R9] の $4\nu_5=\eta_5^3$ を用いて $H(\nu'\eta_6^2)=4\nu_5$。完全性より

$$
\operatorname{Im}H=\ker\Delta=\langle4\nu_5\rangle,\qquad
\operatorname{ord}(4\nu_5)=\frac{8}{\gcd(8,4)}=2.
$$

H は単射であり、上の像はこの部分群を生成する。よってその原像は位数2の生成元であり、

$$
\pi_8^3=\mathbb Z/2\{\nu'\eta_6^2\}.
$$

□

内部の10出典には Chapter V, iii) の ν-family 定義も含まれる。R3R60R2 はこれを表示だけから省略し、内部番号10の (5.5) を表示9へ移す。ProofStep と出典リンクを保持し、表示番号を内部証明に戻さない。原著印刷版の全命題の独立照合を意味しない。先行 DB 3件を再証明せず、型付き先行結果として利用する。

''' + ja_evidence
    return dict(zip(DOCUMENT_BLOBS, (readme, design, log, roadmap, proof)))


def render_full(name, raw, section):
    """Preserve original bytes except explicitly historical headings and insertion."""
    if name not in DOCUMENT_BLOBS or MARKER.encode() in raw:
        raise ValueError('INVALID_DOCUMENT_BASELINE:' + name)
    if section.count(MARKER) != 1:
        raise ValueError('INVALID_SECTION_MARKER')
    raw.decode('utf-8-sig')  # Reject a corrupt baseline rather than replace characters.
    eol = b'\r\n' if raw.count(b'\r\n') > raw.count(b'\n') // 2 else b'\n'
    addition = section.replace('\n', eol.decode('ascii')).encode('utf-8')
    if name in HISTORICAL_HEADINGS:
        old, new = (s.encode('utf-8') for s in HISTORICAL_HEADINGS[name])
        if raw.count(old) != 1:
            raise ValueError('HISTORICAL_HEADING_NOT_UNIQUE:' + name)
        updated = raw.replace(old, new, 1)
        title_end = updated.index(b'\n') + 1
        return updated[:title_end] + eol + addition + eol + updated[title_end:]
    # Append-only for history and proof records; never rewrite old content.
    return raw + (eol if raw.endswith(b'\n') else eol + eol) + addition
