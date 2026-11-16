# Phase 175 R3R11R1 — テストおよび実行結果

## 修正前のユーザー実行（確認済み）

- R3R11 DryRun: `PASS_R3R11_READ_ONLY_DRYRUN`、終了コード0。
- R3R11 本実行: `29 passed, 3 failed`、`R3R11_FOCUSED_PYTEST_FAILED`、`PHASE175_R3R11_ROLLBACK=RESTORED`、終了コード1。
- 失敗3件: [R6] 引用本文の未表示、Hopf 連鎖未圧縮、Phase 174 R70 の履歴上の source pin が R3R10 の変更を拒否。

## 修正版の作成環境で確認

- `python -m compileall`: 修正パッケージの構文チェック PASS。
- パッケージ内 `tests/test_install.py`: `4 passed`（Linux 上のローカル確認。Windows での本実行とは異なる）。
- 実際のユーザー Windows リポジトリに対する公開 Proof Search / Web と全限定 pytest は **未実施**。成功を先取りして記載しない。

## Windows で実行する限定 pytest

`audit.py` の `TEST_PATHS` のみを実行する。旧 R70 installer baseline テストだけは現在の R3R10 後のファイルに対して意味を持たず除外し、対応する新しい R3R10/R3R11 インストーラーテストを実施する。旧 Source Guard の実装は変更しない。

### 最終合格基準

- `PHASE175_R3R11R1_FOCUSED_PYTEST=PASS`
- `PHASE175_R3R11R1_SEARCH=complete`、`PHASE175_R3R11R1_TRUST=True`
- `PHASE175_R3R11R1_WEB=generic-complete-proof`
- [R2] と [R6] の引用内容および Hopf 等式連鎖の圧縮を確認
- `PHASE175_R3R11R1_GATE=PASS_R3R11R1_CITED_REFERENCES_AND_HOPF_CHAIN_COMPACT`

失敗時は `ROLLBACK=RESTORED` を確認し、`%LOCALAPPDATA%\EHPProofTracerAudit\phase175_r3r11_cited_hopf_narrative\focused_pytest.txt` を調査する。
