# Phase 169 R4F — Proposition 4.4 の適用根拠の文章化

## 変更対象

- 既存ファイル `phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown` のみ。
- 既存 import、クラス、証明規則、Proposition 台帳、Proof Tree、Web API の変更なし。
- 新規ファイル: `phase169_r4f_prop44_hopf_application_display/patch.py`、`audit.py`、`run.ps1`、2つのテストモジュール。
- 新規関数: `patch.py` の `git_bytes`、`git_blob_hash`、`checked_replacement`、`updated_renderer`、`reviewed_r4e_worktree`、`updated_hopf_application`、`main`。`audit.py` の `main`。全関数と import はファイル全文で同梱。
- 既存コード変更後の関数全文およびファイル全文は、`run.ps1` の実行時に `output` へ生成。

## 文献順の確認

Toda 第4章 `sources/toda/Toda_04_2.tex` では、Proposition 4.4 の直前に $n=2,4,8$ における Hopf fibration の存在を明記している。$n=4$ について、その射影 $h:S^7\to S^4$ は $H(h)=\pm\iota_7$ を満たすため、命題の仮定を満たす $\alpha=h$ を選べる。

Proposition 4.4 に $(n,i)=(4,6)$ を代入すると、$E:\pi_5^3\to\pi_6^4$ の単射性が従う。$H(\nu_4)=\iota_7$ の明示的な命名は第5章の後続 Lemma 5.4 にあるため、Proposition 5.3 の証明根拠には用いない。

## 修正前の不足

`[R2]より, $E:\pi_5^3\to\pi_6^4$ は単射.` の一行だけでは、Proposition 4.4 の条件 $H(\alpha)=\pm\iota_7$ が $n=4$ で成立する理由が不明だった。

## 修正後の表現

`$n=4$ の Hopf fibration $h:S^7\to S^4$ により, $\alpha=h\in\pi_7^4$, $H(\alpha)=\pm\iota_7$ と取れる. [R2]を $(n,i)=(4,6)$ に適用すると, $E:\pi_5^3\to\pi_6^4$ は単射.`

この文章の採用条件は、実際の `MapInjective` 型付き推論、その直接 `GIVEN` 親に対応する `TodaProp44UniversalStatement`、正しい $n=4$ の群次元と、既に登録された `[R2]` の祖先関係である。文字列検索や命題名だけで証明を推測することはしない。

## 実行 pytest と完了条件

- R4F 新規6件、R4E/R4D/R4C/R3Z 既存限定テストを実行。
- $\pi_6^4$ の18 ProofSteps、未解決0、`generic-complete-proof` が変わらない。
- Reference 5件がすべて本文の引用と一致する。
- 先行する Hopf fibration により $\alpha=h$ を明示し、後続 Lemma 5.4 や $\nu_4$ を証明の前提に追加しない。
- 範囲外の追跡ファイルに差分を生じさせない。
- 全体 pytest は Phase 169 最終工程まで実行しない。

## 次工程との境界

R4F は Proposition 4.4 の適用を文章で説明する Phase であり、$\pi_7^5$ の探索、出典台帳の新規登録、証明規則の追加、既存文書の改訂は行わない。

## R4F1 回帰修正（追記）

R4F 失敗の原因は、(1) 第5章 TeX の `\\begin{lemma}[]` と `\\label{lem:5.4}` の改行を考慮しないテスト、および (2) R4E で既に表示していた `[R2]より, E は単射` の文章を R4F が置き換えたことだった。

R4F1 は `render_model_backed_narrative_markdown` の同じブロック内で適用条件を `lines.extend` により追加し、R4E の `sentence` を変えない。既存 R4E テストは変更しない。原文検索テストは空の任意引数と改行を許容する正規表現へ変更し、文献順を厳密に検証する。`audit.py` は保持された結論文と前置きの両方を要求する。

対象ファイル・関数は R4F と同一。新規回帰テスト `test_r4f1_patch_keeps_the_original_r4e_injectivity_sentence` を `tests/test_r4f_patch_safety.py` の末尾へ追加。テスト関数・import はモジュール全文を同梱。全体 pytest は実施しない。
