# Phase 172 R2R1 — 型付き生成元同一性の訂正

## 原因

2026年10月31日の R2 実行では `PHASE172_R2_FOCUSED_1=FAIL`、`PHASE172_R2_RESTORED=PASS`。これは Renderer の修正が適用後テストで失敗し、既存ソースに戻されたことを示す。R2 は未完了。

R1 の `proof_steps.json` によると、ProofStep 5 は `GeneratorSuspension` で、source_generator の名前は `η_5`。そこから得られる ProofStep 6 の `Relation` の左辺は `Suspension(HomotopyElement(name='η₅', ...))`。両者の `GeneratorSymbol(family='η', index=5, decoration=None)`、dimension=5、source=6、target=5 は一致する。元の R2 比較では name の違いを含む構造体の直接等号のため、判定候補が0件になった。

この綴り差は既存の `phase165_r12_r28_presentation_connection._matching_eta_name` と、共通の生成元表現比較でも考慮されている。R2R1 では η family に限定しない構造比較を採用する。比較対象は**同じ型の `HomotopyElement`、非空で同一の GeneratorSymbol、同じ次元・始域・終域**に限定する。

## 修正ファイル・関数

- `phase172_r2_suspension_relation_display/projection.py`
  - import 全文（`HomotopyElement` の追加）
  - 新規関数 `same_typed_generator()`（`redundant_suspension_relation_indices()` の直前に追加）
  - 既存関数 `redundant_suspension_relation_indices()` の全文置換
- `phase172_r2_suspension_relation_display/tests/test_projection.py`
  - import 全文（`same_typed_generator` の追加）
  - テストヘルパー `_verified_direct_and_symmetric_relation_indices()` の全文置換
  - 新規テスト `test_typed_identity_recognizes_a_display_alias_without_matching_others()`（ファイル末尾）
- 新規パッケージ `phase172_r2r1_typed_generator_correction/`
  - `install.py`、`run.ps1`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`payload/`

既存 Renderer の関数 `render_model_backed_narrative_markdown()` は元の R2 変更のまま。この訂正自体に新たな import や処理を追加しない。数学的推論・出典・Proof Tree・Trust Boundary に変更なし。

## 安全検査

1. `develop` ブランチを確認する。Renderer のコミット済み Git blob `94996b403f1c01f81319824565db422463714f02` を確認し、作業ツリーの Renderer が復元前の元状態か、正確に確認済み R2 適用後状態のいずれかであることを確認する。
2. R2 の既存2ファイルは記録済み旧版または修正版の正規化 SHA-256 のみに許可する。差異があれば拒否する。
3. `-DryRun` は変更なし。実行時には元ファイルを作業ツリー外に保存する。
4. 既存 R2 Runner の限定 pytest 5セットを実行する。異常があれば元の R2 ファイルに戻す。Renderer は元 R2 Runner が復元する。

## 完了条件

- 元 R2 テスト5件に加え、型付き同一性テスト1件を PASS。
- 既存の限定回帰（4セット）がすべて PASS。
- `π₆³` の Web 証明は complete、未解決目標0、Reference 8件を維持する。
- 引用付き `E(η₅)=η₆` は残り、表示上重複する直行・対称の2行のみ省略する。
- `π₆³=ℤ/4{ν′}` と Hopf 写像の導出を維持する。新しい数学的 Goal は追加しない。
- 全体 pytest は Phase 172 最終 R6 に1回だけ実行する。

## 確認状況

この訂正コードについて AST 構文確認および模擬の型付き生成元・ProofStep 依存関係テストを実行し PASS。Windows 上での実際の限定 pytest はユーザー環境での実行結果によって判定する。
