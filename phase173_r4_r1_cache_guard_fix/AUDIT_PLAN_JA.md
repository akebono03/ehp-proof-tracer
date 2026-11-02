# Phase 173 R4-R1 — pytest キャッシュ例外の限定修正

## 原因

ユーザーの Git 状態は以下の一行だけであった。

```text
 M .pytest_cache/v/cache/nodeids
```

既存の監査前置検査は追跡済みファイルの変更を一律拒否していた。このキャッシュは数学的な GIVEN、ProofStep、引用可能な証拠には該当しない。また、既存の `git()` が `strip()` で先頭の空白を落としていたため、porcelain のステージ区分を厳格に照合できなかった。

## 変更対象（すべて R4-R1 の未追跡監査パッケージ）

- `phase173_r4_r1_audit_only/audit.py`: `git()` 全体を修正。新規 `verify_tracked_worktree()` を `preflight()` の直前に追加。`preflight()` 全体と `main()` 全体を変更。
- `phase173_r4_r1_audit_only/run.ps1`: テスト実行時に `-p no:cacheprovider` を付与。
- `phase173_r4_r1_audit_only/tests/test_audit.py`: import 全文、既存テストを維持し、新規キャッシュ境界テストと `git()` 先頭空白保持テストを追加。
- 新規 `phase173_r4_r1_cache_guard_fix/` 配下: `install.py`, `manifest.py`, `run.ps1`, `tests/test_install.py`, `README.md`, `AUDIT_PLAN_JA.md`, `CODE_FULL_JA.md`, `__init__.py`。

本体の `toda_rules.py`、Provider、正式5文書（`README.md`, `design.md`, `development_log.md`, `roadmap.md`, `proof_records.md`）は変更しない。

## 認可条件

以下のいずれかのみを受け入れる。

- Git の追跡済みファイルが完全にクリーン（空文字列）。
- porcelain v1 が一行のみで、正確に ` M .pytest_cache/v/cache/nodeids` と一致する。

同じキャッシュのステージ済み変更、削除、複数変更、他のキャッシュファイル、証明探索ソースの変更はすべて拒否する。

修正前の3ファイルは SHA-256 による完全一致を要する。未知の編集があれば中断し、既存ファイルを上書きしない。インストール前に原本を `%LOCALAPPDATA%` へバックアップし、Git の reset/checkout/clean は行わない。

## テストと完了条件

1. 修正インストーラーの限定 pytest。
2. 修正版 R4-R1 の限定 pytest。
3. Toda (5.6) 原文、現行 Git HEAD、既存規則、出典付き Root Candidate の AUDIT_ONLY。
4. `audit.json` へ観測結果を保存する。
5. 数学的な ProofStep の生成や出典の昇格は行わない。全体 pytest は Phase 173 終了時のみ。

## Phase 境界

この修正はキャッシュの扱いだけであり、$\pi_7^4$ の直和分解完成、$\pi_8^5$ の位数8導出、Web 公開表示、Closeout は行わない。
