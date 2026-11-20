# Phase 176 R3R26 監査計画

## 対象

Toda (5.3) の $2\nu'=\eta_3\eta_4\eta_5$ と Toda (5.5) の $2\nu_n=E^{n-3}\nu'$ を対象とする。今回の根は $\pi_8^3$ の群構造である。

## 変更ファイル

すべて新規 `phase176_r3r26_toda53_55_reuse_audit/` 配下。

- `audit.py`：`verify_sources`、`git`、`verify_checkout`、`audit_live`、`report_path`、`execute`、`main` を新規定義。
- `tests/test_audit.py`：3つの fail-closed テストを新設。
- `__init__.py`、`run.ps1`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`。

## 実証の境界

1. Source-first で当該 GIVEN が許容されるかを調べる。
2. $2\nu_5=E^2\nu'$ の特殊化候補が共通 provider に現れるか調べる。
3. $4\nu_5=\eta_5\eta_6\eta_7$ は今回は導出したと主張しない。
4. Hopf 像および $\pi_8^3$ の群構造も未完成のまま維持する。

## pytest

`python -B -m pytest -q -p no:cacheprovider phase176_r3r26_toda53_55_reuse_audit/tests phase171_r2e_toda53_double_source/tests/test_source.py phase174_r3_r6_source_extension/tests/test_source.py`

## 完了条件・次段階

DryRun、本監査、限定 pytest が PASS。R3R27 は実際に不足する接続だけを検討する。全体 pytest は Phase 終了時のみ。
