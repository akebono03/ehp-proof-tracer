# Phase 169 R4C2 — コミット済み R4C の読み取り専用監査

## 原因

`develop` の HEAD `75cbee31865594fa65202e4d49d6bef9a6b50816` では、
`phase165_r52_r9_shared_math.py` に R4B と R4C の両方の接続がコミット済み。
R4C1 は「R4B のみが存在する状態」をパッチ前提としていたため失敗した。

## 変更対象

本番コードの変更はなし。追加ファイルは次のとおり。

- `phase169_r4c2_committed_audit/verify.py`: Git HEAD 内の5ファイルの blob と作業ツリーの同一性、R4B・R4C 接続位置を確認。
- `phase169_r4c2_committed_audit/run.ps1`: 限定 pytest と既存の R4C 監査を再実行。
- `phase169_r4c2_committed_audit/tests/test_r4c2_verifier.py`: 安全確認の5テスト。

新規関数は `verify.py` の `normalized_text`、`verify_provider_source`、`git`、
`verify_committed_state`、`main`、およびテスト内の `fixture_provider` と
5個のテスト関数。いずれもファイル内に省略のない全文を収録。

## 限定テスト

新規5件、既存 R4C 6件、R4B 6件、R3O 7件の合計24件を実行する。
全体 pytest は実行しない。

## 完了条件

5ファイルの blob・内容の照合、限定 pytest、Proposition 4.4・
Proposition 4.2 (4.4)・(5.1) を祖先に持つ E 同型の実際の ProofStep を検証。
その後の `pi6_4` 完了判定は既存 R4C の監査に従い、未解決 Goal を残せば
次工程で検討する。

## Phase との境界

R4C2 は読み取り専用。追加の証明規則、Renderer 更新、
安定範囲変更および他の群の完了を先取りしない。
