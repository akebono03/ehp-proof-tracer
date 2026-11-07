# Phase 174 R3-R7-R23：Proposition 2.7 型付き推論境界監査

## 変更対象

既存ファイル・クラス・関数は変更しない。新規ディレクトリ `phase174_r3_r7_r23_prop27_typed_inference_audit/` のみ追加する。

- `audit.py`：Git Source Guard、採用文献、現行型・公開証明状態を検証する読み取り専用関数を新設。
- `tests/test_audit.py`：文献の前提順序、Git lineage、Windows 改行、禁止事項のテスト関数を新設。
- `tests/test_public.py`：未完成の公開経路を監査するテスト関数を新設。
- `run.ps1`：DryRun／通常実行と限定 pytest。
- `README.md`：英語の実行概要。
- `CODE_FULL_JA.md`：今回追加するコードの全文。

## 数学的な境界

採用 TeX の Proposition 2.7 に一般関係 $H\Delta(\iota_{2n+1})=\pm 2\iota_{2m-1}$ があり、Proposition 5.9 に $H(\Delta(\iota_{13}))=\pm 2\iota_{11}$ がある。ただし原典印刷版との照合や、一般命題からの型付き特殊化の証明は、この監査の完了条件に含めない。

既存の `tests/test_phase50_prop27_theorem_semantics.py` は Whitehead product の Hopf 不変量を検査するもので、今回の Delta map を通る signed witness と同一ではない。記号名だけで証明を代用しない。

## 完了条件

1. `SOURCE_GUARD=PASS`、採用出典と既存規則がレビュー済みのままである。
2. 今回と関連テストの限定 pytest が PASS。
3. 公開 signed Delta witness と Verified ProofStep がゼロであることを再確認する。
4. GIVEN と数学的推論規則の追加ゼロ。全体 pytest は実施しない。
5. 根の証明は未完成のまま維持。

## 次段階との境界

R24 は一般命題の型付き条件（次元・符号・写像構成・出典）の具体的な定式化を検討する。出典の意味が確認できるまで本番への一般規則追加を行わない。
