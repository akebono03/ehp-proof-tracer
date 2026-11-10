# テスト結果（2026-11-10）

## 今回の生成環境での実測

- `python -m py_compile audit.py tests/test_audit.py`：PASS
- `python -m pytest -q --import-mode=importlib phase174_r3_r7_r55r2_reference_tree_audit/tests/test_audit.py`：**4 passed**
- ZIP integrity (`unzip -t`)：PASS

## 未実施

この ZIP の生成環境には `ehp-proof-tracer` の実行可能な全リポジトリがないため、実際の公開 Group query と既存 R55/R37 pytest は **未実施**。

利用者の `develop` 作業ツリーで `run.ps1 -DryRun` の後、限定 pytest と Source-first 実測監査を行う。結果は `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r55r2\reference_tree_audit.json` に保存する。

全体 pytest は R56 まで保留する。
