# Phase 158-R2 repair5

## 原因

repair4 の production code 適用は成功しており、apply script 内の syntax check も PASS している。

追加で実行した

`python -m py_compile toda_group_proof_narrative_renderer.py`

が Windows 上で `__pycache__` の `.pyc` ファイルを置換できず、`WinError 5` で停止した。

これは Python source の SyntaxError ではない。

## 変更対象

Production code:
- 変更なし

Test:
- 変更なし

Runner:
- `run_phase158_r2_repair5.ps1` のみ新規

## 修正

`.pyc` を生成する `python -m py_compile` を使わず、

`compile(source, filename, "exec")`

で source text の syntax check だけを行う。

## 続行

repair4 はすでに適用済みなので、production code を再適用しない。

1. no-pyc syntax check
2. focused tests
3. 112-group baseline-preservation audit
4. summary

全体 pytest は Phase 158 の最後のみ。
