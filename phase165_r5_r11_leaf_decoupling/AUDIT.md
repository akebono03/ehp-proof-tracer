# Phase 165 R5-R11 変更監査

## 対象ファイル・関数

1. 新規 `phase162_ehp_leaf_inputs.py`：旧コードと同じ `_phase162_ehp_leaves()` を追加。
2. 既存 `phase162_web_narrative_integration.py`：同関数の定義を削除し、互換 import に置換。他の関数は変更しない。
3. 既存 `phase162_pi5_3_web_replay.py`：`_phase162_ehp_leaves` の import 元だけ変更。`build_phase162_pi5_3_web_replay()` は変更しない。
4. ZIP 内 `install.py`・`restore.py`・`test_r5_r11.py`・`run.ps1`：導入、復元、限定テスト。

## 事前確認

GitHub `akebono03/ehp-proof-tracer` の現行 `phase162_web_narrative_integration.py`、`phase162_pi5_3_web_replay.py`、`phase162_r3_narrative_connection.py`、および Phase 162 の関連テストを確認した。旧 Web モジュール内で `_phase162_ehp_leaves()` が2か所で利用され、Web replay が1か所で import している。新規モジュールの関数 AST と移設元の関数 AST が同一でなければ、インストールを拒否する。

## 完了条件

- 共通 EHP 入力生成が Narrative モジュールに依存しない。
- 旧モジュールからの import は互換エイリアスとして残る。
- Web replay の関数本体、既存 ProofStep、Reference、数学的推論規則は不変。
- 限定 pytest が成功する。失敗時には復元する。

## 次の作業との境界

旧 Narrative 表示経路の撤去、Proof Chain / Concrete Transport の判断、Phase 162 の破損した `prop51_steps` fixture の修復は **今回実施しない**。全体 pytest は Phase 165 の終盤のみ実施する。
