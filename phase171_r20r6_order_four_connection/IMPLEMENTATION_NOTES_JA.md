# Phase 171 R20R6 実装記録

## R20R5 からの引継ぎ

監査では、群の位数4に対応する公開候補だけが照合成功。残りは元の位数4、二倍元の非零性、懸垂像の非零性、型付き二倍等式の4経路。既存の独立証明木はこれらの推論を保持している。

## 今回の対象

1. `phase171_r2j_r4_r7_nonzero_nu_order/source.py` の末尾に `expand_public_order_four_from_nonzero_double()` を追加する。
2. `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` 内の `expand()` に、上記の候補生成器の接続を追加する。
3. `phase171_r20r6_order_four_connection/` にインストーラ、限定テスト、監査、実行スクリプトを新規追加する。

既存のクラスと既存の推論関数の変更、トップレベル import の変更は行わない。

## 数学的条件

`FiniteElementOrder(G,x,4)` に対し、証明義務 `FiniteGroupCardinality(G,4)` および `NonZeroGroupElement(G,2*x)` を提案する。後者が成り立たない場合や、対象元が型付きでない場合は候補を返さない。`inferred_order_four_rule()` の既存の `INFERENCE` 判定をそのまま利用する。既知の群構造を証拠として取り込まない。

## 安全性

- Git HEAD の文字列だけでなく、対象の2ファイルの Git Blob SHA を固定した前提条件として検証する。
- 適用前に元ファイルを個別バックアップする。別バージョンや半適用状態は停止する。
- 既存の正規の推論 API と引用条件を変更しない。
- 事前に存在した `GIVEN` の新規登録なし。
- 指定した本番ソース2ファイルと本パッケージ内の `output/` のみを更新する。Git commit はしない。

## 検証

限定 pytest は新規テスト5件と既存の2件を実行する。独立 R4-R7 の実証明を公的 provider への照合用としてだけ使用し、探索の前提には注入しない。

## 完了条件と次工程との境界

- `PHASE171_R20R6_NU_ORDER_FOUR=CERTIFIED_PUBLIC_PROPOSAL_PRESENT`
- 限定 pytest PASS
- `PHASE171_R20R6_NEW_GIVEN=0`
- 次工程で $2\nu'\ne 0$、$E(\eta_2^3)\ne 0$、$2\nu'=E(\eta_2^3)$ の候補を別個に接続する。本工程では $\pi_6^3$ の公開完成も Web 完成も宣言しない。


## R20R6R1 — 改行対応（2026-10-31）

ユーザー環境で R20R6 の DryRun は `provider anchor absent or duplicated` として停止。
GitHub のレビュー対象 `phase165_r52_r9_shared_math.py` は CRLF 改行なのに対し、
インストーラの `PROVIDER_ANCHOR` は LF 改行で検索していたため、0件と判定された。

修正対象：`phase171_r20r6_order_four_connection/install.py` 内 `patched_text()` の
挿入位置判定のみ。`tests/test_install.py` に CRLF 成功・重複拒否の2件を追加。
Git Blob ハッシュの確認、既存の部分適用拒否、先行バックアップと改行の保存、
`GIVEN` を増やさない推論条件、`run.ps1` は維持。
修正後の DryRun と限定 pytest をユーザー環境で確認するまで本番適用成功とはしない。
全体 pytest は Phase 終了時のみとする。
