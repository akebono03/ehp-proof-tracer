# Phase 173 R4-R15R2R1 — HEAD Lineage 修正設計

## 背景

R4-R15R2 は監査専用パッケージだが、元の `preflight.py` は HEAD `7104222524b63c9c517eaf8e09b8f0825842b316` だけを要求していた。R4-R15R1 のコア修正を GitHub `develop` にコミットした結果、実際の HEAD は `c44519a123fdbf2c5ec57fe9c89e2fb1027f41a5` となり、DryRun が Source Guard の段階で拒否された。

GitHub のコミット比較では、旧 HEAD の直後に1コミットがあり、変更対象は R15R1 のコアおよび R15R1 の実行・検査・記録ファイルに限られていた。監査対象の CSV と関連する数学的依存モジュールは変わっていない。

## 変更対象（全文コードを SOURCE_CODE.md に収録）

- 既存 `phase173_r4_r15r2_generator_obligation_audit/preflight.py`：`git()`、`preflight()`、`main()` を保持し、`git_content()`、`normalized()`、`reviewed_installed_core()` を追加。
- 既存 `phase173_r4_r15r2_generator_obligation_audit/run.ps1`：新しい HEAD 監査テストを DryRun に追加。
- 新規 `phase173_r4_r15r2_generator_obligation_audit/tests/test_head_lineage.py`：6つのテスト関数と、テスト用 Git リポジトリ構築関数を追加。
- `README.md` は英語、`design.md` と `SOURCE_CODE.md` は日本語で、いずれも全文を更新。
- 本番 `core.py`、推論規則、出典、既存数学的テスト、`audit.py` は変更しない。

## 検査手順

1. Git ブランチが `develop` でローカル HEAD と `origin/develop` が一致することを検証する。
2. HEAD が監査済みの旧コミット、または新コミットであることを検証し、無関係の後続コミットを拒否する。
3. 元のコアが旧 HEAD で `cd4b8feb29fbe95a4aedb355514a0267146935ee` であることを検証する。
4. 旧 HEAD から `transform()` で生成したコアとローカルの `core.py` が改行を正規化して厳密に一致することを検証する。
5. 新 HEAD ではさらにコミット済みコアの blob `d35600804ecbbc5f8566d52e45a2f6ecf8816347` と、コミット済みの変換元コード blob `06fcdb3c36362225332a1f49cda788b23f9cfc37` を確認する。
6. 既存依存5ファイルのコミット識別子とローカル実体、ステージ済み変更、既存の許可済み変更範囲を検査する。
7. DryRun の限定テストを実行する。本実行では既存監査テストを実行し、`factor_obligation_report.json` を出力する。

## 完了条件

- `PHASE173_R4_R15R2_HEAD_LINEAGE=PASS`
- `PHASE173_R4_R15R2_CORE_STATE=COMMITTED_PATCH`（今回の HEAD の場合）
- `PHASE173_R4_R15R2_SOURCE_GUARD=PASS`
- `PHASE173_R4_R15R2_FOCUSED_PYTEST=PASS`
- `PHASE173_R4_R15R2_K31_BASELINE=PASS`
- `PHASE173_R4_R15R2_AUDIT=PASS`

## 次工程との境界

本修正は HEAD Guard の系譜のみを拡張する。生成元の懸垂像や表示上の認証済み証明は一切追加しない。R4-R15R3 以降で、R15R2 の未解決生成元関係を根拠に基づいて推論規則へ接続する。全体 pytest は Phase 173 の終了時にのみ実施する。
