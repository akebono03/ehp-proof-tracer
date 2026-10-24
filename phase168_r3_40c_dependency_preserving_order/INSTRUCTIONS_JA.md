# Phase 168 R3-40C — 共通の依存関係保存型 Narrative 順序

## 変更対象

- `phase168_r3_29_order_projection.py`: `project_narrative_order()` の全文置換。
- `phase168_r3_27_typed_statement_projection.py`: `typed_sentence()` の直前に `project_stable_eta_notation_transition()` を追加。
- `phase168_r3_5_model_renderer.py`: `render_model_backed_narrative_markdown()` の全文置換。
- 上記3ファイルの module-level import は変更しない。変更後の関数内 import は全文関数ファイルに含まれる。

## 方針

ProofStep の全依存関係を構築し、非表示ステップも含めて安定した Topological Sort で出力順序を決定する。商群表示と生成元の関係は、Proof Tree に存在する型付き命題を参照し、矛盾なく追加できる場合に限って表示上の優先関係として追加する。旧 `after_indices` API は保持するが、この Projection では延期描画を使用しない。

既存の `stable_eta_notation_rule` から得られた証拠と Reference を照合できる場合に限り、反復懸垂の生成元対応を明示する。新たな数学的推論規則や文献出典は導入しない。

## 実行

PowerShell でリポジトリ直下に移動し、ZIP を展開したのち `phase168_r3_40c_dependency_preserving_order/run.ps1` を実行する。変更前の3ファイルをバックアップし、限定テストや監査が失敗した場合は元に戻す。

## 限定テストと完了条件

4群の全 Proof Step を保ち、依存関係の逆転がゼロであること。π₅⁴ と π₆⁵ の文章順序が改善すること。π₆⁵ の $E^2\eta_3=\eta_5$ が実在する一般定義の引用を伴うこと。π₃²、π₄³、π₅⁴ の固定基準説明12項目が維持されること。全体 pytest は Phase 終了まで実行しない。

## Phase 境界

このパッケージは Phase 168 R3-40C の Narrative Projection のみ。Proof Search、命題登録、文献順判定、他の Renderer、将来 Phase の機能には触れない。
