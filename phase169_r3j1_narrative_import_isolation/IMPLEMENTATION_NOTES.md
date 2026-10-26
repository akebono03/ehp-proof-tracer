# Phase 169 R3J1 — 変更内容と検査

## 今回の対象

- `run.ps1`：限定テストを2つの独立した pytest プロセスに分離。`python -m` で事前検査を実行。
- `preflight.py`：ルート側 EHP モジュールへの import を検証し、旧コピーが読み込まれた場合は中断。
- `tests/test_r3j1_import_isolation.py`：`test_r3j1_canonical_ehp_module_origin()` と `test_r3j1_both_terminal_adapters_resolve_from_canonical_module()` の2関数を追加。
- `audit.py`、`tests/test_r3j_narrative_boundary_audit.py`：R3J と完全同一。変更なし。

## 原因

`phase165_r14_r5_ehp_connection.py` と `phase165_r14_r5_ehp_connection/phase165_r14_r5_ehp_connection.py` は同名モジュールで、後者は更新前の実装を保持している。pytest が旧テストのディレクトリを `sys.path` に挿入した状態で監査テストを実行すると、後者を誤って import する。根本的なモジュール配置整理は Phase 169 R3J1 の対象外。

## 完了条件

- 正規モジュールがルート側の `.py` から読み込まれる。
- 既存 EHP テスト6件、新しい Narrative 監査4件と import 回帰テスト2件が限定 pytest で成功。
- 実際の Web 経路の監査が成功し、文章・Reference の診断 JSON と Markdown が保存される。
- 既存の Proof Tree、Registry、Renderer、既存テスト、文書は変更しない。
- 全体 pytest は Phase 169 終了時にのみ実行する。

## 次の Phase との境界

R3K で初めて Renderer の表示調整を行う。R3J1 は表示や証明の変更を行わない。
