# Phase 174 R3-R7-R20：Δ-image の出典・証明依存関係監査

## 変更対象

本番コード・既存テストは変更しない。新規ディレクトリ `phase174_r3_r7_r20_delta_image_evidence_audit/` のみを追加。

- `audit.py`：現行 develop HEAD、採用 Toda Prop. 5.9 の根拠、R19 公開 frontier の読み取り監査。
- `tests/test_audit.py`：出典マーカー、順序、誤った証明昇格防止の限定テスト。
- `run.ps1`：DryRun → 限定 pytest → 公開 frontier 検査。
- `README.md`：英語の説明。

## 数学的境界

採用 Toda (Prop. 5.9) の証明中に $\pi_{13}^{13}\xrightarrow[\cong]{\Delta}\pi_{11}^6$ が記述される。その根拠となる $E\pi_{10}^5=0$、$H(\Delta(\iota_{13}))=\pm 2\iota_{11}$ などの依存関係を監査する。

この印刷された導出を、独立した GIVEN や型付き `TodaDeltaImageFreeCyclicStatement` の検証済み ProofStep と同一視しない。

## 完了条件

Source Guard PASS、限定テスト PASS、現行公開検索が未完成のまま、新しい GIVEN=0、数学的規則=0、全体 pytest 未実施。

## 次段階との境界

R21 では元の Proposition 2.7 と EHP 完全列を用いた一般規則の既存実装可否を監査する。R20 では推論規則や本番 provider を追加しない。
