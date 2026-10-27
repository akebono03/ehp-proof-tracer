# Phase 169 R5A — 診断方針

## 対象

- 新規: `phase169_r5a_pi75_premise_diagnostic/audit.py` — `git`, `diagnostic_attempt`, `summarize`, `inspect`, `main`。
- 新規: `phase169_r5a_pi75_premise_diagnostic/tests/test_r5a_premise_diagnostic.py` — テスト関数4件。
- 新規: `run.ps1`, `README.md`, `AUDIT_JA.md`。
- 既存の本番コードと関連テストは変更しない。

## 根拠

Toda (4.5) は $n\ge k+2$ の範囲で $E$ による安定輸送を与える。
今回の $n=4,k=2$ は範囲内。ただし、群の DB 行は証明ではない。

先行する固定命題によって $\pi_6^4$ を GIVEN として引用できるか、
できなければ同じ citation-screened context 内で下位群の証明を再構成できるか調査する。
Toda (4.5) の具体化、合成生成元の懸垂についても独立に調査する。

## 検証

限定 pytest：R5A 4件、R5 4件、R3O 7件の計15件。全体 pytest は実行しない。

## 完了条件

前提3項目の可否、引用位置、下位群の利用不可の理由、Git 無変更が報告されること。

## 次工程との境界

実装・新規証明規則の追加・GIVEN への昇格は行わない。次の Phase で監査結果に応じて
必要な接続のみを行う。
