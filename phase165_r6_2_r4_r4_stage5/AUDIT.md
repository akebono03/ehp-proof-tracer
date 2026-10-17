# Phase 165 R6-2 R4-4 第5段階

## 変更対象

- `map_property_rules.py`: 末尾に `injective_and_surjective_imply_isomorphism_inference_rule()` を追加。既存の import、クラス、関数は変更しない。
- `install.py`, `new_rule.py`, `test_install.py`, `test_integration.py`, `run.ps1`: 新規。

## 数学的な内容

同一の群準同型 $f$ について、$f$ が単射かつ全射ならば $f$ は同型。逆向きでは同型性の Goal から単射性と全射性の2つの Subgoal を作る。別々の写像についての主張は結合しない。

## 境界

- `ProofStep` と文献出典を捏造しない。完成証明はまだ得られていない。
- 第2〜4段階の追加が既に導入されていることを前提とする。
- GitHub 公開版とユーザー環境の差分を考慮し、既存コードを上書きしない。
- 全体 pytest は Phase 165 終了時のみ実施。
