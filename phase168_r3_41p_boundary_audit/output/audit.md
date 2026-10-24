# Phase 168 R3-41P — Renderer と証明検証の責務境界監査

## 実行条件

- 監査専用。プロジェクトの Python 実装は変更していない。
- 数学的再判定と構造・表示の整合性確認を区別して記録する。
- 動的監査は公開 Web 経路を使用し、全体 pytest は実行しない。
- 比較は文字列の差分と既存固定基準の論証チェックであり、数学的正しさを新たに証明しない。

## Git 状態

- branch: `develop`
- HEAD: `02c2a6a1e13eb69f297dc50a363db958aa18f72c`
- working status (audit start): `?? phase168_r3_41p_boundary_audit/`

## 静的監査

| ファイル | 行 | 関数 | 呼び出し・条件 | 分類 |
|---|---:|---|---|---|
| `phase168_r3_5_model_renderer.py` | 71 | `render_model_backed_narrative_markdown.validated_specialization_citation_numbers` | `specialize_typed_statement` | MATHEMATICAL_REVALIDATION |
| `phase168_r3_5_model_renderer.py` | 74 | `render_model_backed_narrative_markdown.validated_specialization_citation_numbers` | `specialize_typed_statement` | MATHEMATICAL_REVALIDATION |
| `phase168_r3_5_model_renderer.py` | 229 | `render_model_backed_narrative_markdown` | `getattr(inference_rule, 'name')` | STRING_COUPLED_PRESENTATION |
| `phase168_r3_27_typed_statement_projection.py` | 84 | `toda45_specialization_evidence.find_source` | `specialize_typed_statement` | MATHEMATICAL_REVALIDATION |
| `phase168_r3_27_typed_statement_projection.py` | 142 | `project_stable_eta_notation_transition` | `_stable_eta_renaming_shape` | MATHEMATICAL_SHAPE_RECHECK |
| `phase168_r3_27_typed_statement_projection.py` | 208 | `typed_sentence` | `getattr(inference_rule, 'name')` | STRING_COUPLED_PRESENTATION |
| `phase168_r3_27_typed_statement_projection.py` | 232 | `typed_sentence` | `prop42_exactness_indices` | EXACTNESS_SHAPE_RECHECK |

## Model の現状

`ProofNarrativeModel` は `steps`, `citations`, `step_citation_numbers` を保持する。
`NarrativeCitation` は `step_indices`, `assertion_ids`, `reference_ids`, `statement_bodies` を保持する。
しかしパラメータ特殊化・引用祖先の確定済み導出記録を持つ専用フィールドは現行定義では確認できない。
不足が本当に問題になる実例は、動的ログとテスト結果に基づいて判断する。

## 3群の Web 経路比較

| 群 | ProofStep | Reference | 引用対応 | 固定論証 | 本文差分行 | Reference差分行 |
|---|---:|---:|---|---|---:|---:|
| 未実施 | — | — | — | — | — | — |

## 要注意点

1. Renderer 内の `validated_specialization_citation_numbers` は特殊化を再判定する。
2. Typed Projection の `toda45_specialization_evidence` は一般 Toda (4.5) を再特殊化する。
3. 安定 η 表記では `_stable_eta_renaming_shape`、完全性の文章では `prop42_exactness_indices` を呼ぶ。
4. 中間ステップ表示省略が `inference_rule.name` の固定文字列に依存する。
5. Citation の全番号が本文に現れることだけでは、各引用の数学的適用条件が保証されたとは言えない。

## 変更方針（監査の結論ではなく検討案）

既存の Narrative Model / Projection の拡張可能性を優先し、Renderer では数学的な Rule を再実行しない。
ただし構造検査・循環依存検出・Citation 番号の双方向一致チェックは維持する。
本 R3-41P 監査パッケージにはコード変更を含めない。

## 次の境界

監査結果を確認した後で、必要性を実証できた箇所だけ最小修正する。
全体 pytest は Phase 168 終了時に実行する。

## 動的監査エラー

```text
Traceback (most recent call last):
  File "C:\Users\user\Dropbox\Python\fitz\ehp_proof\phase168_r3_41p_boundary_audit\audit.py", line 459, in main
    report["runtime"] = runtime_audit()
  File "C:\Users\user\Dropbox\Python\fitz\ehp_proof\phase168_r3_41p_boundary_audit\audit.py", line 192, in runtime_audit
    import phase165_r57_r20_general_specialization as specialization
ModuleNotFoundError: No module named 'phase165_r57_r20_general_specialization'

```
