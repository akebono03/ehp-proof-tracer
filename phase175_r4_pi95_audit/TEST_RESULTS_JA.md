# Phase 175 R4 — 検証記録

## 作成側で実施済み

- `python -B -m pytest -q phase175_r4_pi95_audit/tests/test_audit.py`：**16 passed**（監査関数の純粋な契約テスト）。
- 監査ファイルの Python 構文検査、ZIP 内全ファイルの存在・整合性：梱包時検査。
- GitHub `develop` の既存 R1、R2、R3R12 監査コードおよび R34 出典テストを参照済み。

## ユーザーのローカル環境で実行する検証

- `run.ps1 -DryRun`：Source PIN、Git 状態、採用 TeX の証拠、型付き生成元、限定 pytest。
- `run.ps1`：上記に加え $\pi_9^5$ と $\pi_8^4$ の実際の探索、信頼性・Web 監査、Open Goals の記録。
- 実行時 Gate と限定 pytest 件数は、ユーザー環境の出力によって確定する。**作成側で本番統合テストを実行済みとは主張しない。**

## 未実施

- 開発リポジトリの全体 pytest：Phase 175 終了時のみ。
- R4 の一般 ProofStep 実装：Audit Only のため禁止。
- Toda 原本画像との誤植照合：採用 TeX しか確認していない。

## R4R1 — 2026年11月17日 初回ユーザーログからの補正

### ユーザーの初回 Windows DryRun

- 限定 pytest：**23 passed in 6.17s**。
- `PHASE175_R4_FOCUSED_PYTEST=PASS`。
- `PHASE175_R4_GATE=FAIL_R4_AUDIT_NOT_COMPLETED`。
- 停止原因：`R4_UNREVIEWED_TRACKED_CHANGES: ['.pytest_cache/v/cache/nodeids']`。
- Source PIN 検査および Proof Search 未実施。

### R4R1 作成環境での限定確認

- `python -B -m pytest -p no:cacheprovider -q phase175_r4_pi95_audit/tests/test_audit.py`：**22 passed**。
- Python ソース構文検査：PASS。
- `run.ps1` に `-p no:cacheprovider` が含まれること、その他の未確認パスを拒否することを確認。
- ZIP 内容と `CODE_FULL_JA.md` に含むソース一致は梱包時に照合。
- Windows の R4 + R34 限定統合 pytest、実際の Source PIN、Proof Search の本実行：**ユーザー環境で未実施**。
- 全体 pytest：**未実施**（Phase 175 の最後のみ）。

### 期待値

- `-DryRun`：`PASS_R4_AUDIT_ONLY_DRYRUN`。
- 本実行：`PASS_R4_PI95_FRONTIER_RECORDED_NOT_COMPLETE`。
- 上記は監査のみの成功を意味し、$\pi_9^5$ の完成証明を意味しない。


## R4R2 — 2026年11月17日の Source PIN 系譜補正

### ユーザー環境で観測された R4R1 の失敗

- 限定 pytest：**29 passed in 6.71s**。
- Source PIN 検査で `R4_SOURCE_PIN_DRIFT: phase165_r52_r9_shared_math.py` が発生。`PHASE175_R4_HEAD=UNVERIFIED`、`PHASE175_R4_PINNED_SOURCES=0`、終了コード1。
- R4 の Source Inventory、実群検索・Open Goals 調査にはまだ進んでいない。この失敗は証明完成・失敗のいずれも意味しない。

### 独立に照合した GitHub develop

- R3 引き継ぎ HEAD：`a1ce1558be6bab647c5d23d26047b9cce45d4e2e`。
- GitHub 現行 HEAD：`c77a26fdebe0eead67f1f7dad3a469aa446b134f`。
- `phase165_r52_r9_shared_math.py`：R1 旧 SHA `9fa11b383812570fae1a26868c98992a5934a327`、R3/現行 SHA `ee1efa2d91df479168b7b964d24e814e0f516449`。
- その他17件の R1/R2 Source PIN は GitHub 現行版と一致。

### R4R2 作成側での検証

- `python -B -m pytest -p no:cacheprovider -q phase175_r4_pi95_audit/tests/test_audit.py`：**24 passed**。
- R1 基点・R3 ソース blob の両固定値および非対象 PIN の変更を拒否するテストを追加。
- `audit.py`／`tests/test_audit.py` の構文、ZIP 内ファイルと `CODE_FULL_JA.md` の全コード一致：梱包時に検査。
- `run.ps1` の変更なし。現行の Git guard、テストキャッシュ抑止、証明探索観測、全体 pytest 禁止を維持。

### ユーザー環境で未実施

- R4R2 DryRun、本実行、関連 R34 監査テスト、実際の Web Proof Search 結果。
- 全体 pytest（Phase 175 終了時のみ）。

期待 Gate：DryRun `PASS_R4_AUDIT_ONLY_DRYRUN`、本実行 `PASS_R4_PI95_FRONTIER_RECORDED_NOT_COMPLETE`。実測値が異なる場合は監査を継続し、成功を捏造しない。
