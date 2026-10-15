# Phase 165-R57-R23 監査と設計

## 実装前の確認

GitHub `akebono03/ehp-proof-tracer` の `proof.py`、`tests/test_inference_rule_pattern.py`、`phase165_r3_recursive_search.py`、`phase165_r52_r9_shared_math.py`、`phase165_r57_r20_general_specialization.py` を確認した。

- `InferenceRule` には `conclusion_pattern` と `conclusion_builder` が存在する。
- `match_pattern_value` は `PatternVariable` の照合または完全一致を担当し、入れ子の dataclass/tuple 全体を再帰照合する機能はない。
- `merge_variable_bindings` は同一変数への競合する束縛を拒否する。
- `reconstruct_registered_goal` は Provider が返した `GoalExpansion` の再帰探索・順方向検証を実施するが、任意の `InferenceRule` から前提を自動生成しない。

## 変更ファイル

- 新規 `phase165_r57_r23_conclusion_unification.py`。`ConclusionUnification`、`_match_nested`、`_instantiate_nested`、`unify_inference_conclusion` を追加。
- 新規 `phase165_r57_r23_conclusion_unification/test_phase165_r57_r23_conclusion_unification.py`。重点テスト7件を追加。
- 新規 `phase165_r57_r23_conclusion_unification/run.ps1`。設置と限定テスト。
- 文書 `README.md`、`AUDIT.md`、`CHANGED_CODE.md` をパッケージ内に追加。

## 完了条件・未検証

結論の型付き照合と束縛の整合性を検証する。実行環境で7件の限定 pytest が PASS となれば R23 の範囲の完了とする。現在の環境には全リポジトリがないため、既存コードに対する pytest は未実行。

R24 は候補となる推論規則・命題の発見、R25 は前提構築、R26 は既存探索器との結合。`conclusion_builder` しか持たない規則の逆向き適用は、R23 では保証しない。
