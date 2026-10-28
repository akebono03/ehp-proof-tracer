# Phase 169 R10EC — 直和群の証明文章圧縮

## 現状と目的

R10EB-R1 の限定テストは49件 PASS、$\pi_{22}^{13}$、$\pi_{23}^{15}$、$\pi_{24}^{15}$、$\pi_{39}^{30}$ の探索はすべて complete、Trust Boundary も PASS。$\nu_{30}^3$ は適切に表示できるようになった。ただし $\pi_{39}^{30}$ の証明本文は4167文字となり、$\eta$ 系列の像の重複表示が19件残った。

本 Phase は **Proof Tree（証明木）を変更せず、完全な直和群の群構造輸送だけを共通の Narrative Renderer（文章生成器）で要約する**。各生成元の像が証明済みであることと、それを文章上で何十回も繰り返す必要があることを区別する。

## 変更ファイルと関数

- 既存 `phase168_r3_5_model_renderer.py`：`render_model_backed_narrative_markdown()` 全体の中で1か所だけ共通 Projection を接続する。モジュールの import は変更しない。パッチ適用時に変更後の **関数全文**とファイル全文を `output/` へ保存する。
- 新規 `phase169_r10ec_direct_sum_narrative_projection/projection.py`：新規 `VerifiedDirectSumTransportDisplay` クラス、新規 `project_verified_direct_sum_transport()` 関数。配置は package root。
- 新規 `patch.py`：`_git_sha()`、`_decode_and_style()`、`_function()`、`transform()`、`prepare_patch()`、`main()`。関数全文は当該ファイルに収録。
- 新規 `audit.py`：`inspect_case()`、`main()`。関数全文は当該ファイルに収録。
- 新規限定テストファイル2件：各 import とテスト関数全文を収録。
- 新規 `run.ps1`、`README.md`、`DESIGN_JA.md`。

既存の他のファイル、数学的規則、データベース、文献台帳、文書5件は変更しない。

## 数学的意味を変更しないための条件

根の `Relation` が実際に `DirectSumGroup` であり、既存の `generator_images_for_group_transport()` が生成する全 `GeneratorImage` が、**順序付きの、型が一致する、INFERENCE として証明された根の直接前提**と完全一致することを要求する。`Toda45IsomorphismStatement` の型付き写像は先行群構造と目標群構造に一致させる。各像の証明祖先に実際の Reference に紐づく GIVEN がなければ要約を拒否する。

非表示にしてよいのは、根の証明に専用で、他の消費者を持たず、独自引用のない `GeneratorImage` または `GeneratorSuspension` の INFERENCE の本文のみ。ProofStep 自体は削除しない。関連する一般定義の Reference もすべて残す。共通 Projection が不成立なら従来の長い文章へ戻し、未完成証明には適用しない。

例として、証明済みの19回懸垂は本文で次のように表せる。

$$
E^{19}(\nu_{11}^3)=\nu_{30}^3,\qquad
E^{19}(\mu_{11})=\mu_{30},\qquad
E^{19}(\eta_{11}\circ\varepsilon_{12})=\eta_{30}\circ\varepsilon_{31}.
$$

この表示は新たな懸垂命題の採用ではなく、既存の19段階の各成分の `GeneratorImage` の検証済み証明を省略表示したものである。

## 実行・テスト・完了条件

`run.ps1` を実行する。検証済みの Git HEAD と blob、作業ファイルの汚染、R10EB 適用を事前検査する。既存レンダラー1ファイルの改行形式を保持し、失敗時は原本へ復元する。

限定 pytest は今回の Projection／パッチ、既存の R10A 巡回群表示、R10EB 累乗表示、R10EA 監査テストに絞る。4群を再探索し、Trust Boundary の再検証、引用の保存、重複画像式の0件化、$\pi_{39}^{30}$ の文字数削減を確認する。全体 pytest は **Phase 169 の最後だけ**実施する。

次の Phase では、Reference と特殊化の表示整形や、本文の残る一般的な冗長表現を監査する。R10EC では証明規則もデータベースも増やさない。
