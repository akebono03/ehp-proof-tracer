# Phase 174 R55R3R2 専用 Narrative 全撤去

## 監査に使用した GitHub の現行 develop

- 2026-11-10 確認した HEAD：`d923ff2a34b6ba9d4c23d3da0221402f0b815f46`
- `phase168_r3_37c_reference_projection.py`：Git blob `0a7800b3bd9d140fc22c1b92ab74bcdf48740546`
- `phase168_r3_5_model_renderer.py`：Git blob `913a7030e209a689f58a5215013d3708140052e7`
- `phase168_r3_27_typed_statement_projection.py`：Git blob `26ce3632fe1b32bab7e822e8f701409b26f4f04a`

関連監査・テスト：R55R2 の引用証明木監査、R55 の HTTP テスト、R37 の Δ 全射性規則テスト、R55R3・R55R3R1 のテストと Installer を確認した。

## 変更対象ファイル・関数

1. `phase168_r3_37c_reference_projection.py`
   - 新規 `_project_certified_general_reference_body` を既存 `project_reference_bodies` の直前に追加
   - `project_reference_bodies`：R55R3 専用モジュールへの import を削除し、同一ファイルの共通 Reference 関数に置換
2. `phase168_r3_5_model_renderer.py`
   - `render_model_backed_narrative_markdown`：R55R3 の `project_certified_proof_sentence` 呼び出しを削除し、実装を GitHub 現行版へ戻す
3. `phase168_r3_27_typed_statement_projection.py`
   - `typed_sentence`：型付き Statement に保持されている命題そのものの一般的な数式表示だけを追加
4. `phase174_r3_r7_r55r3_common_proof_display/`
   - R55R3 の4つの専用 Formatter、統合関数、不要となった専用テスト、Installer・文書をハッシュ検証後に削除
5. `phase174_r3_r7_r55r3r1_public_sentence_correction/`（存在する場合）
   - 同じ専用投影を再導入できる旧 Installer を検証後に削除

トップレベルの README.md、design.md、development_log.md、roadmap.md、proof_records.md は、この限定修正では変更しない。Phase Closeout 時に全文を作成する。

## 設計上の境界

- Proof Search → Verified Proof Tree → ProofNarrativeModel → 共通 Typed Statement / Reference projection → Renderer → Web。
- 共通表示の追加関数は、`model.steps`、探索目標の `(n,k)`、`step.premises` の特殊な組合せから文章を創作しない。
- Source-first、First Successful Proof Search を維持。数学的 GIVEN / INFERENCE を変更しない。
- Toda (5.10) の ± は、Source GIVEN の内容を Renderer が推測で強めないため、元のまま維持する。余計な重複説明は削除。
- 上下の Δ を `upper/lower` という公開 LaTeX で表示しない。必要な区別は定義域・値域による。
- n=4、n=6、n=8 の偶数 n に対する Proposition 2.7 表示で一般性を確認する。
- Phase 174 の全体 pytest は最後だけ。

## 完了条件

- R55R3 専用コードと呼出しが存在しない。
- 2つの一般 Source Reference に本文がある。
- 型付き特殊化と核の数式は共通 Statement 表示にある。
- π₁₂⁷=0 が28祖先 ProofStep・0 Open Goal で維持される。
- HTTP 双方 200・Complete、紹介文1回。
- 限定 pytest PASS、全体 pytest 未実施。

**注意**：過去 Phase の表示補助はその Phase の既存 API とテストを守るため、今回の R55R3 由来の専用 Narrative 撤去とは区別する。旧 Phase の汎用性監査を行わずに「リポジトリ全体に専用コードが皆無」とは主張しない。
