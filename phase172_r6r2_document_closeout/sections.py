"""Phase 172 closure narrative, strictly documentation only.

All supplied sections are full prose. The installer writes complete revised
file contents, retaining every prior byte except README's outdated status heading.
"""
from __future__ import annotations

MARKER = "<!-- PHASE172_FINAL_CLOSEOUT_20261031 -->"

README_CURRENT = r"""<!-- PHASE172_FINAL_CLOSEOUT_20261031 -->

## Current status — Phase 172 closed (2026-10-31)

Phase 172 is closed after presentation-only improvements to the verified public
proof of $\pi_6^3=\mathbb Z/4\{\nu'\}$. The common model-backed renderer now
suppresses redundant, certified suspension equalities, compresses a cited Hopf
image derivation, avoids a second display of the same Hopf surjectivity, and
renders admitted prior database results in readable Japanese while retaining
their internal database provenance and reference identities.

The proof itself is unchanged: the completed backward search still verifies
50 ProofSteps, 8 references, no open goals, and the `generic-complete-proof`
Web route. Regression checks passed for $\pi_3^2$, $\pi_4^3$, $\pi_5^3$,
$\pi_6^4$, and $\pi_6^3$. The Phase 172 R6 closeout gate passed ten focused
test groups, all five public-Web proof checks, and the active `tests/` full
suite **once**: `3546 passed in 107.52s (0:01:47)` (exit code 0). Local and
`origin/develop` heads matched at `6ac7fd8a4ccdf628a0767a0d865dddcf88bbd92a`,
and tracked files were unchanged during that gate.

The two adopted `sphere.csv` prior results remain database assumptions, **not**
independently authenticated literature theorems; proposition numbers shown as
references are explicitly supplemental. This phase neither changes the
mathematical proof, introduces new GIVEN facts, nor certifies arbitrary other
homotopy groups. The next phase scope is not yet determined.

"""

DESIGN_ADDENDUM = r"""<!-- PHASE172_FINAL_CLOSEOUT_20261031 -->

## Phase 172 — 表示専用射影と終了時の不変条件（2026-10-31）

Phase 172 は、Phase 171 で完成した $\pi_6^3=\mathbb Z/4\{\nu'\}$ の証明に対して、**検証済み Proof Tree を入力とする表示専用 Projection（射影処理）**を整備した。Backward Search（後向き証明探索）、Inference Rule（推論規則）、既存の `GIVEN`、群構造、文献出典の採用規則は変更していない。

- R1 は既存 Web Narrative（証明叙述）、Reference（引用）、50件の ProofStep（証明段階）を照合した監査である。
- R2 は引用済み `GeneratorSuspension`（生成元懸垂）から検証済みの直接等式と対称等式の重複表示を省く。`η_5` と `η₅` は印字名ではなく、`GeneratorSymbol`（型付き生成元識別子）・次元・始域・終域で対応を検証する。証明段階は残す。
- R3 は $H(\nu'\eta_6)=\eta_5^2$ に至る既証明の Hopf 導出の途中式を短縮し、Definition（定義）、Proposition 2.2、(5.3) の出典に対応する本文と最終等式を維持する。
- R4 は同じ型付き Hopf 写像の全射性を二度表示しない。後の全射性の推論依存と先行する検証済みの全射性を確認した場合だけ後者の重複行を抑制する。
- R5 は `ADOPTED_DATABASE_PRIOR` の出典を Web Reference 見出しに限って日本語化する。元の `DB prior: sphere.csv` locator と対応する ProofStep、Reference 番号、Trust Boundary（証明の検証境界）は保持する。`[参考: Proposition ...]` は独立の文献定理として採用したことを意味しない。

これらは型付きの根・祖先・Citation（引用対応）と表示順を検査し、欠損・不整合・未完成の証明では不正な圧縮を行わない **fail-closed（不確実な場合は変換しない）**方式である。特定の生成元名による新しい数学的例外や、新しい公理を追加しない。

R6 Closeout（終了監査）では、`develop` の `6ac7fd8a4ccdf628a0767a0d865dddcf88bbd92a` に対し、限定 pytest 10セット、公開 Web 検証5群（$\pi_3^2,\pi_4^3,\pi_5^3,\pi_6^4,\pi_6^3$）がすべて PASS。$\pi_6^3$ の ProofStep 50件、Reference 8件、未解決 Goal 0、Web key `generic-complete-proof`、内部 DB 出典の不変を確認した。Phase 末尾の**現行アクティブ `tests/` 全体 pytest は1回のみ**実施し、`3546 passed in 107.52s (0:01:47)`、終了コード0。実行前後の追跡済みファイルの状態は一致した。

過去の「Phase 172 は候補・未実装」という記述は記録時点の履歴であり、本節が最新の正式状態である。次 Phase の内容はこの Phase 172 に含まれず、別途決定する。
"""

DEVELOPMENT_ADDENDUM = r"""<!-- PHASE172_FINAL_CLOSEOUT_20261031 -->

## 2026-10-31 — Phase 172 正式終了（R1〜R6）

R1 `AUDIT_ONLY` では、Phase 171 完成済みの $\pi_6^3=\mathbb Z/4\{\nu'\}$ について、ProofStep 50件、Reference 8件、`complete`、`generic-complete-proof`、未解決 Goal 0を確認し、懸垂関係・Hopf 導出・全射性・`DB prior` 見出しの表示上の重複と内部表現を分類した。

R2 は $E(\eta_5)=\eta_6$ の派生等式と対称等式の重複を証明木から取り除かず、表示上だけ抑制した。最初の限定テストは `η_5`／`η₅` の印字名の差によって失敗し、R2R1 で同一の型付き生成元を構造的に比較する方式へ訂正。限定 pytest 5セット PASS。

R3R1 は Hopf 導出の出典と中間段階を監査した。R3R1R1 では、R2 がコミット済みの Renderer を監査 Gate が誤って拒否する問題を訂正した。R3 では $H(\nu'\eta_6)=\eta_5^2$ に至る既証明の途中式を整理した。R2 の歴史的な表示期待と衝突したテスト1件を R3R2 で修正し、R3 限定 pytest 5セット PASS。数学的推論・Proof Tree は変更していない。

R4 は Hopf 写像 $H:\pi_6^3\to\pi_6^5$ の全射性の重複表示を整理し、限定 pytest 6セット PASS。R5 は先行 `sphere.csv` DB 結果の Web Reference 見出しを日本語化し、内部 locator・引用番号・Trust Boundary を維持したまま限定 pytest 6セット PASS。R5 までの数学的な推論規則と既知の群構造は不変である。

R6 の Git HEAD は `6ac7fd8a4ccdf628a0767a0d865dddcf88bbd92a`（`origin/develop` と一致）。Renderer は R5 コミット済み。内容検査・DryRun PASS、限定 pytest **10セットすべて PASS**、公開 Web の5群 $\pi_3^2,\pi_4^3,\pi_5^3,\pi_6^4,\pi_6^3$ がすべて PASS。Phase 終了 Gate の現行アクティブ `tests/` 全体 pytest を**1回**実行し、`3546 passed in 107.52s (0:01:47)`、終了コード0。追跡済みファイルの状態は実行前後で不変。最終結果は `PASS_PHASE172_R6_FULL_CLOSEOUT_GATE`。

終了証拠は `%LOCALAPPDATA%/EHPProofTracerRecovery/phase172_r6_20261031_144642_024616Z/closeout.json`、同 `full_active_pytest.log` と `pi_6_3_web_narrative.md` に保存されている。直前の DryRun は全体 pytest を実行していない。過去の途中失敗は修正済みであり、この正式終了記録は R6 の成功結果に基づく。

**Phase 172 正式終了。** 次 Phase の機能は先取りせず、別途計画する。本節は開発履歴への追記であり、過去の失敗・修正履歴を削除しない。
"""

ROADMAP_ADDENDUM = r"""<!-- PHASE172_FINAL_CLOSEOUT_20261031 -->

## Phase 172 正式終了・次 Phase の境界（2026-10-31）

Phase 172 の R1〜R5 は、Phase 171 で完成した $\pi_6^3=\mathbb Z/4\{\nu'\}$ の Web 表示を、証明木と出典を不変にして改善した。懸垂等式の重複、Hopf 導出の過長表示、全射性の重複、`DB prior` の内部的見出しを整理済みである。R6 にて限定10セット・Web 5群の回帰検証が PASSし、現行アクティブ `tests/` 全体 pytest は**3,546 PASS（107.52秒、終了コード0）**である。`develop` の検証 HEAD は `6ac7fd8a4ccdf628a0767a0d865dddcf88bbd92a`、追跡済みファイルの状態は不変。**Phase 172 は正式終了。**

次 Phase は未決定であり、Phase 172 の終了認定は未完成群の新規証明・一般化・未検証の文献内容には及ばない。新たな目標は、現行の登録結果・Proof Tree・必要な出典を個別に監査してから設定する。全体 pytest は次 Phase の終了 Gate まで再実行しない。

旧節の「Phase 172 — 候補（未実装）」は当時の計画の履歴であって、最新の状態は本節による。
"""

PROOF_ADDENDUM = r"""<!-- PHASE172_FINAL_CLOSEOUT_20261031 -->

## 2026-10-31 — Phase 172 表示改善後の完成証明・保存記録

登録済み $\pi_6^3=\mathbb Z/4\{\nu'\}$ について、Phase 171 で確立した証明の数学的根拠を維持している。EHP の短完全列

$$
0\longrightarrow\pi_5^2\xrightarrow{E}\pi_6^3\xrightarrow{H}\pi_6^5\longrightarrow0
$$

と、両端の位数が2であることから $|\pi_6^3|=4$。さらに、単射性により $E(\eta_2^3)\ne0$、証明済みの $2\nu'=E(\eta_2^3)$ から $2\nu'\ne0$ となり、$\nu'$ の位数は4である。この数学的な Proof Tree は Phase 172 で変更していない。

表示整理では、型付きの $E(\eta_5)=\eta_6$ の重複二式を非表示化し、$H(\nu'\eta_6)=\eta_5^2$ の導出を既知の Proposition 2.2・(5.3)・Definition の引用を保って簡素化し、同じ Hopf 全射性の反復を抑制した。Reference 見出しの2件は `sphere.csv` に採録された先行群結果であり、内部 `ADOPTED_DATABASE_PRIOR` と `DB prior: sphere.csv` locator はそのまま維持する。参考の Proposition 番号を独立の出典証明として昇格させていない。

R6 終了監査は検証済み ProofStep **50件**、Reference **8件**、未解決 Goal **0件**、公開 Web `generic-complete-proof` を確認した。$\pi_3^2,\pi_4^3,\pi_5^3,\pi_6^4,\pi_6^3$ の Web 回帰はすべて PASS。限定 pytest 10セットが PASSし、Phase 末尾のアクティブ `tests/` 全体 pytest は `3546 passed in 107.52s (0:01:47)`、終了コード0である。終了証拠は `%LOCALAPPDATA%/EHPProofTracerRecovery/phase172_r6_20261031_144642_024616Z/closeout.json` と関連ログに保存した。Gate の実行 HEAD は `6ac7fd8a4ccdf628a0767a0d865dddcf88bbd92a`。

Phase 172 は**表示品質の改善の認定**であり、新しい数学的定理の証明、任意のホモトピー群の完成、出典データベース全体の検証を意味しない。過去の Phase 171 数学的証明の記録は履歴として維持する。
"""

APPENDS = {
    "docs/design.md": DESIGN_ADDENDUM,
    "docs/development_log.md": DEVELOPMENT_ADDENDUM,
    "docs/roadmap.md": ROADMAP_ADDENDUM,
    "docs/proof_records.md": PROOF_ADDENDUM,
}


def make_revision(path: str, original: bytes) -> bytes:
    """Return a *complete* revised file; preserve historical bytes."""
    if not isinstance(original, bytes):
        raise TypeError("original document must be bytes")
    text = original.decode("utf-8-sig")
    if MARKER in text:
        raise ValueError("Phase 172 closeout already exists")
    newline = "\r\n" if original.count(b"\r\n") > original.count(b"\n") // 2 else "\n"
    if path == "README.md":
        anchor = b"<!-- PHASE171_FINAL_CLOSEOUT_20261031 -->"
        old_heading = "## Current status — Phase 171 closed (2026-10-31)".encode("utf-8")
        historical_heading = "## Historical closeout — Phase 171 (2026-10-31)".encode("utf-8")
        if original.count(anchor) != 1 or original.count(old_heading) != 1:
            raise ValueError("unreviewed README status structure")
        new_section = README_CURRENT.replace("\n", newline).encode("utf-8")
        return original.replace(anchor, new_section + anchor, 1).replace(
            old_heading, historical_heading, 1,
        )
    elif path in APPENDS:
        addition = APPENDS[path]
    else:
        raise ValueError("unreviewed documentation path")
    # Keep every original byte unchanged; append a complete closure record.
    ending = b"" if original.endswith((b"\n", b"\r")) else newline.encode()
    payload = addition.replace("\n", newline).encode("utf-8")
    return original + ending + newline.encode() + payload
