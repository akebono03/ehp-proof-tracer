# Phase 165 R6-1 — 文献登録の固定 Goal 直接依存の縮小

対象 production ファイルは `phase165_r14_r38_direct_registry.py`、変更する関数は `build_adopted_typed_reference_registry()` です。ファイル全体の変更ではなく、対象関数の内部で取得順と照合対象のみを変更します。import・クラス・その他の関数は変更しません。

旧処理では `backward_leaf_goals(pi32_goal())` を先に呼び出し、その結果に登録する型付き文献命題を対応付けていました。新処理では `adopted_leaf_steps()` の型付き `ProofStep.conclusion` を照合キーに使用します。登録内容、文献出典、内部 Goal と固定命題の分離は維持します。

**境界**: `adopted_leaf_steps()` 自身が現状では旧 `pi32_goal()` と `phase165_r34_expansions()` に依存します。従って今回の変更は全体の群専用依存の除去ではありません。別の出典候補から独立に葉を構築・検証する仕組みを整えるまでは、当該旧関数を削除してはいけません。

`run.ps1` は変更前バックアップ・構文検証・対象限定 pytest を実行し、全体 pytest は実施しません。これらの変更は R6-2 の汎用逆向き推論を先取りしません。
