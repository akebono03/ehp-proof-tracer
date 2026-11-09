# Phase 174 R3-R7-R46 監査計画

## 変更対象（最初に列挙）

既存ファイル・クラス・関数・メソッドの変更：**なし**。
新規追加場所：リポジトリ直下 `phase174_r3_r7_r46_prop42_dfs_audit/`。
新規ファイル：`__init__.py`、`source_guard.py`、`audit.py`、`run.ps1`、`tests/test_audit.py`、`tests/test_guard.py`、`tests/test_static.py` およびこの文書群。
新規関数：`source_guard.normalized_sha256`、`source_guard.verify_checkout`、`audit.inspect_prop42_dfs_frontier`、`audit.main`、`tests/test_audit.observed` と各 `test_*` 関数。新規クラスはありません。

## 目的

R45R1 限定 pytest 65 PASS と本番コード無変更を前提として、R45 の `search_failed / proven_steps=0` が「Proposition 4.2 の一般規則の不能」を意味するか、「子 Goal の深さ優先順序による未訪問」を意味するかを区別する。

## 事前に確認した実装・テスト

- GitHub `develop` HEAD `4b06ef96628b39e591cfa0b423fa0e0dec366a3b`、R45R1 引き継ぎログ、R44/R45 監査。
- `phase165_r3_recursive_search.py`：子 Goal を tuple の順で解決し、最初の失敗でその展開を停止する。
- `phase165_r12_r11_prop42_unified.py`：出典付き普遍前提から具体的な EHP 完全性の特殊化へ進む。
- `phase165_r12_r12_ehp_consequences.py`：完全性から像と核の一致を導く。
- `phase165_r12_r11_prop42_unified/tests/test_phase165_r12_r11_prop42_unified.py` と R45 の関連テストを確認済み。

## 監査手順

1. 既存 R45 Source Guard と検索エンジン Git Blob を照合する。R45R1 ローカル未追跡コードも SHA256 で固定する。
2. R45 と同じ未接続零像の限定探索を再実行し、Provider が実際に受け取った Goal の訪問順を記録する。
3. 同じ出典を使い、4つの `TodaProp42ExactnessStatement` と下側 `EHPImageEqualsKernelStatement` から個別の Canonical Proof Search を開始する。
4. 推論 `ProofStep` が得られた場合に限り、実際の一般命題 `GIVEN` 祖先を検証する。
5. 一般命題の出典リンクを除外した場合、特殊化 Provider の候補が0件になることを検証する。

## 禁止事項

新規 GIVEN、結論直接登録、数学的に未検証の前提の補完、専用 Narrative、群・生成元ごとの例外、唯一性検査、全体 pytest を行わない。孤立した子証明を最終根の完成と取り違えない。

## 完了条件

Source Guard PASS、R45 の訪問順と個別標準探索の結果の監査報告、負の出典テスト PASS、限定 pytest PASS。最終目標 `π_{12}^{7}=0` の完成は完了条件ではない。

## 次工程との境界

R47 以降で、R44 の零像証明枝と R46 の出典付き EHP 完全性枝の実際の根探索での統合可否を調べる。R46 はその接続を実装しない。
