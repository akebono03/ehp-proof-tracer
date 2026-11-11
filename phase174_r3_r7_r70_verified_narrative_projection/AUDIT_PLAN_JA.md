# Phase 174 R70 — 一般 Narrative Projection 実装と監査

## 変更対象

1. **既存変更**：`phase171_r20r13_eta_sentence_layout/projection.py` の `format_complete_proof_sentences()` 全体を置換。import 部は変更しない。関数内 import で新規モジュールを呼ぶ。
2. **新規追加**：`phase174_r3_r7_r70_verified_narrative_projection/projection.py`（純粋な共通表示処理）。
3. **新規追加**：同ディレクトリの `install.py`、`audit.py`、`tests/test_projection.py`、`run.ps1`、監査文書・コード全文。

既存の Renderer 本体、ProofStep、数学的推論規則、文献 GIVEN、既存 Reference 数は変更しない。README.md、design.md、development_log.md、roadmap.md、proof_records.md のルート文書も変更しない。

## 照合した現行 GitHub コードと関連テスト

GitHub `akebono03/ehp-proof-tracer` の `develop` から、共通 Renderer、`phase171_r20r13_eta_sentence_layout/projection.py`、関連テスト、R3/R5/R7/R56 の一般推論規則と R68/R69 監査を確認。対象関数は完全証明の場合のみ共通 Renderer から呼ばれる。

## 数学的解釈

- 合成元の像：一般的な `GeneratorImage(E, g, a∘b)`、その構成2前提、左因子の零関係とその GIVEN 出典が全てルートの祖先にある場合に限る。未認証の印刷名・CSV 行を根拠にしない。
- Δ 全射性：`MapSurjective(Δ)` を得た一般規則の直接前提に、表示済みの巡回群生成元関係があることを要する。「よって」は引用の再掲を避ける**表示の接続詞**であり、出典は直前の前提に残す。
- 零群の説明：既存の4前提一般規則から `Im Δ=ker E`、`Im E=ker H`、終端群 `0` を読み取り、`E=0`・`H` 単射を説明文として表示。**独立した ProofStep が新たに証明されたと記録しない。**

## 非対象

一般規則の分割・追加、数学的根拠の独立再証明、全20文章の意味監査、他群の Narrative 専用分岐、全体 pytest、ルート5文書の更新。

## 実行ゲート

- Source Guard：変更する関数の Git blob と関連8ファイルを確認。
- DryRun：ファイル内容を変更しない。
- 通常実行：対象関数を全文単位で置換。変更後の関数全文を output に書き出す。
- 限定 pytest：新規テスト、Phase171 の既存共通表示テスト、R68/R69 監査テスト。
- 公開完成証明：`π_11^6` と `π_12^7` を実検索し、文言・順序・Reference 7件/3件を照合。

完了条件：`PASS_R70_FOCUSED_AND_PUBLIC_GENERAL_NARRATIVE`。
