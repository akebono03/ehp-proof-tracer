# Phase 175 R4R11 — 検証計画

## 目的

R4R10 で公開接続済みの Toda (5.8) と Proposition 2.5 を**再証明も再登録もしない**。R4R10 が導出する符号付き `TodaDeltaImageUpToSignStatement` と、以前の一般的位数零規則から導いた $2\eta_n=0$ と、出典付きの $\eta$ 族定義を要求して、等式を導く一般規則を追加する。

条件：$n\ge3$ かつ $\beta=\eta_n$（普遍的定義から懸垂）であること、$2\beta=0$ が独立に証明済みであること、$a,b$ が型付きで同じ群の元であること、$2k$ が偶数であることを確認する。

$$
\Delta(\gamma)=\pm((2k a-b)\circ\eta_n)
\quad\Longrightarrow\quad
\Delta(\gamma)=b\circ\eta_n.
$$

後段の導出は、$\eta_n$ が懸垂であることから合成の左変数に関する分配法則が成り立ち、$2\eta_n=0$ より $2(a\circ\eta_n)=2(b\circ\eta_n)=0$ が従うことを用いる。したがって正負の両場合が同じ $b\circ\eta_n$ に一致する。任意の非懸垂な2-捩れ元には適用しない。

## 変更対象

- 既存 `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` 全体のみ。`build_shared_typed_bridge()` と既存 import は変更しない。
- `phase175_r4r11_signed_eta_torsion_public/rule.py`：新規 `eta_two_torsion_normalization_inputs()`、`signed_eta_two_torsion_rule()`、`expand_signed_eta_two_torsion()`。
- `provider.py`：新規 `build_signed_eta_torsion_provider()`。
- `installer.py`：新規 `git()`、`git_blob_sha()`、`function_replacement()`、`plan()`、`install()`。
- `audit.py`：新規 `git()`、`preflight()`、`validate_prior()`、`find_prior()`、`exact_delta_eta9_goal()`、`replay_general_rule()`、`inspect_shared_connection()`、`report_folder()`、`run()`、`main()`。
- `tests/`：新規限定テスト。既存テストは変更しない。

## 出典・履歴ガード

- 前提 R4R10 の成功レポートを、ゲート・出典付き3経路・署名保持・PI95 未完成の内容で検証する。
- GitHub の現行 `develop` HEAD `abf619040d52aa9fd61c5bca60db81e28912e24d`、またはコミット前の審査済み R4R8 HEAD `5c263cc69dc409842d3a13cb3fc65c2347df0bef` のみ許可する。
- 本番コードは R4R10 適用後の完全な作業内容と一致する場合に限る。CRLF は正規化して照合。
- Toda 原文と新旧推論規則の Git blob を照合し、本文改ざん時は停止する。

## 検証と境界

- DryRun：対象関数の全文を出力し、既存本番ファイルは書き換えない。
- 本実行：1関数だけ更新し、共有 Provider の新規候補、R4R10 の符号付き候補、以前の $2\eta_7=0$ 候補を検証する。
- 新規 GIVEN 0件。新規数学規則1件。共有探索の新規候補であって、$\pi_9^5$ の直接結論ではない。
- 全体 pytest は実行しない。
- R4R12 以降の境界：EHP 完全性による $E$ の全射、$\pi_8^4$ の商群計算、生成元の懸垂像の推論が残る。

## 既存 DB の代表元と文献名の差

既存の `phase166_r3af_goal_adapter.py` は $k=1$ の `η7` を Python オブジェクトの `name="η_7"` として構成する。一方 R4R10 の表示用 `sample_delta_eta9()` は `name="η₇"` である。`HomotopyElement` の等価判定は名称も比較するため、直接比較してはいけない。R4R11 の実環境 `inspect_shared_connection()` は `exact_prior_database_result(7,1)` の**実際の生成元オブジェクト**を利用して Prop 2.5 の型付き特殊化を再構成し、$2\eta_7=0$ の既存規則と一致することを検証する。これは既知群を新しい GIVEN として登録することではない。


## R4R11R2：Git blob 改行コードの検証修正

ユーザー実行では限定 pytest が `128 passed` であったが、DryRun の `preflight()` が `R4R11_SOURCE_DRIFT: expression.py` を返して停止した。GitHub 上で、`expression.py`、`sources/toda/Toda_02_2.tex`、`sources/toda/Toda_05_2.tex` は元の Git blob が CRLF であることを確認した。R4R11R1 のガードは LF 正規化バイト列の SHA-1 のみを参照し、Git に記録された CRLF バイト列のハッシュと一致しなかった。

R4R11R2 では、検証対象の実バイト列、LF に統一した全バイト列、および CRLF に統一した全バイト列の Git blob SHA-1 を、既存のピン値と厳密比較する。照合候補を改行コード表現に限定し、数式・コード・出典の内容変化は受理しない。既存の HEAD・コミット範囲・先行レポート・本番コード検証の条件は変更しない。

変更範囲は `audit.py` の `reviewed_eol_blob_matches()` 追加と `preflight()` 変更、`tests/test_audit.py` の1テスト追加、および4文書の全文更新だけ。`rule.py`、`provider.py`、`installer.py`、`run.ps1` および本番 `phase165_r52_r9_shared_math.py` は変更しない。R4R11R1 の `ProofStepLink(step=...)` 修正はそのまま保持する。
