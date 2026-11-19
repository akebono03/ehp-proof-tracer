# Phase 175 R4R14R7 監査計画

## 対象

- `phase175_r4r14r7_zero_image_match_audit/audit.py`：新規の読み取り専用監査。
- `phase175_r4r14r7_zero_image_match_audit/tests/test_audit.py`：監査の限定テスト。
- `phase175_r4r14r7_zero_image_match_audit/run.ps1`：実行入口。

## 既存コードの検証対象

- `phase174_r3_r7_r40_adopted_db_zero_image_isolated/rule.py`
- `phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/provider.py`
- `phase175_r4r14r5_public_zero_transport/provider.py`
- `phase175_r4r14r6_surjective_zero_codomain/rule.py`
- `phase165_r52_r9_shared_math.py`

## 確認事項

1. 先行データベース群の型付き GIVEN と厳密な順序規則。
2. 生成元の零像が実際の部分 ProofStep に含まれるか。
3. R41 の2前提に対応する ProofStep の存在と推論マッチング。
4. 人為的な GIVEN の注入なしに、現在の部分証明が閉じない理由。
5. 失敗を成功に変更せず、JSON 報告に事実を出力する。

## 境界

新たな数学規則・GIVEN・本番 Provider の変更は行わない。R41 の修正は監査結果で欠落箇所が確認された後に判断する。全体 pytest は Phase 175 終了時のみ行う。
