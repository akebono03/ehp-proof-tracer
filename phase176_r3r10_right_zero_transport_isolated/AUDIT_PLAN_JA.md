# Phase 176 R3R10 — 右合成零像の一般推論（独立監査）

## 対象と背景

R3R9 は、Toda Lemma 5.7 の出典付き基礎零像を `INFERENCE` ProofStep として導出できる一方、合成した生成元については `GeneratorImage` の零像候補が存在しないことを示した。現行 `relation_rules.py` は `Relation` 型の右合成の等式を扱うが、既存 `GeneratorImage` を合成した零像へ直接移す共有規則は確認できない。

## 数学的規則

`E(a)=0` と `a∘b` が定義されるなら、懸垂と合成の両立性から $E(a\circ b)=E(a)\circ E(b)=0$。この推論を特定の Toda 生成元に限定せず、厳密な型・次数・合成因子の一致・証明済み `INFERENCE` 前提で表現する。

## 変更対象

- 新規 `rule.py` — `right_zero_transport_inputs`、`right_zero_transport_rule`、`expand_right_zero_transport`。
- 新規 `audit.py` — `git`、`check_sources`、`preflight`、`observe`、`worker`、`report_path`、`execute`、`main`。
- 新規 `tests/test_rule.py` — 実際の推論生成、直接 GIVEN 拒否、型・因子不一致拒否、DryRun 検証。
- 新規 `run.ps1`、`README.md`、監査計画・コード全文ドキュメント。

既存 Python モジュール・出典・共有 Provider・Renderer の変更はない。

## 完了条件

DryRun PASS、限定 pytest PASS、source-first の実際の Lemma 5.7 `ProofStep` から、右合成後の `GeneratorImage` 零像の `INFERENCE` ProofStep が独立に得られること。`public_mathematical_rules_added=0` と `root_proof_complete=false` は維持する。次 R3R11 で公開 Provider 接続を検討する。全体 pytest は Phase 終了時のみ行う。
