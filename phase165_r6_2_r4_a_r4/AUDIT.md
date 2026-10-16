# Phase 165 R6-2 R4-A-R4 監査記録

## 変更対象

- 新規 `r4_probe.py`：`evaluate_goal()`、`probe()`、`markdown()`、`main()`。
- 新規 `test_r4_probe.py`：テスト5件。
- 新規 `run.ps1`：対象 pytest と読み取り専用調査。
- 新規 `README.md`、`AUDIT.md`。
- 既存コード、import、クラス、関数は変更しない。

## 既存実装の確認

GitHub `akebono03/ehp-proof-tracer` の `phase165_r8_rule_provider.py`、`phase165_r57_r26_generic_search_connection.py`、`phase165_r57_r25_premise_generation.py`、`phase165_r57_r23_conclusion_unification.py`、`phase165_r52_r9_shared_math.py` および `tests/test_phase165_r8_rule_provider.py` を確認した。

## 判定上の限界

R3の77 factory・55生成規則・25構造候補のうち、実在する登録済み型付き命題を Goal にして R8 と R26 の候補生成を呼ぶ。Goal に一致しなくても数学的な逆適用不可能とは断定しない。R26 の Provider が候補を返すことと、共通再帰探索から証明が完成することは別である。R8以外の専用 Provider と群別 Adapter の完全照合は今後。完成証明件数は0（未実施）。

## 完了条件

対象テストが成功し、登録 Goal の取得、候補生成の有無、エラー、打ち切り有無が JSON と Markdown に出力されること。全体 pytest は Phase 最後のみ。

## 次の境界

共通探索の再帰到達性と Adapter 置換可能性の確認は次段で扱う。数学的推論規則の追加・変更はしない。
