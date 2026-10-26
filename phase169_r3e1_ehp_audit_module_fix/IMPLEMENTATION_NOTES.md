# Phase 169 R3E1 — 監査の import 経路修正

## 原因

前回の R3E は限定 pytest 22件 PASS の後、`python -B "$package\audit.py"` で監査を実行した際に `ModuleNotFoundError: No module named 'homotopy_groups'` となった。これは監査スクリプトをファイルパスで起動する場合の Python モジュール探索経路に起因する。失敗後の guarded restore が正常に実行され、本番変更は残っていない。

## 変更対象

- 修正：`phase169_r3e1_ehp_audit_module_fix/run.ps1` の監査起動コマンド。
- 新規パッケージ内の README と本記録は R3E1 の説明全文として更新。
- 数学コード：R3E の `full_functions/shared_expansion_provider.py` を変更せず収録。実行時に `phase165_r52_r9_shared_math.py` の当該関数全体を既存のガード付き適用器で置換。
- `apply.py`、`audit.py`、新規テスト関数：R3E から変更なし。
- 本番コードへの追加 import：`shared_expansion_provider()` 内にある `from phase165_r14_r5_ehp_connection import expand_registered_ehp_goal` のみ（前回と同一）。

## 修正内容

`python -B -m phase169_r3e1_ehp_audit_module_fix.audit` に変更し、`Set-Location $repo` で既に確保されたリポジトリ直下からモジュールとして起動する。`sys.path` の追加や環境変数の書き換えは行わない。

## 検証と完了条件

新 ZIP 内の Python 構文と ZIP CRC を検査する。Windows の実際の実探索はユーザー環境で限定 pytest 後に実行し、候補と文献順を判定する。失敗したら改変された1ファイルを一致検査付きで復元する。全体 pytest は Phase 169 最終時のみ実行。

## 次工程との境界

R3E1 は import 不備の修正だけであり、EHP 同型性の終端命題の証明や Renderer の変更には進まない。R3F で終端 Goal の証明可能性を検討する。
