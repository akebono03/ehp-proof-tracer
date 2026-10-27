# Phase 169 R4C1 — Git HEAD の R4B コミット対応

## 発生した停止

R4C のパッチ前検証が、コミット前の Git blob `8a9d534f87cb04b807dca4b3b2ef09e2d3eaa1c5` のみを許可していた。現在の GitHub `develop` (`7f4db3c50b817e2501238ec5c1ab966378ea5409`) では、R4B がコミットされ `c94dc82fc28214fff63020773c2e9c5c126414ae` になったため、コード編集前に安全停止した。

## 今回の変更

変更対象：`phase169_r4c_pi64_suspension_iso/patch.py` の `main`, `expected_r4b_source` と新規 `git_blob_hash`, `verified_r4b_worktree`。`run.ps1` は回帰テストを追加する。`tests/test_r4c1_patch_baseline.py` を新規追加（6件）。**既存実装の `rule.py`、`audit.py`、既存 R4C テストは変更しない。**

`patch.py` は旧コミット＋R4B 作業ツリーの状態と、R4B コミット済みの状態のみを受理する。Git blob の SHA-1 と R4B 挿入行を照合し、予期しない編集がある場合は本番ファイルへの書き込み前に停止する。検証成功時は従来と同じく `phase165_r52_r9_shared_math.py` の `shared_expansion_provider` だけに R4C 接続を追加する。

## テスト・境界

新規安全確認6件、既存 R4C 6件、R4B 6件、R3O 7件：予定 **25件**。全体 pytest は実施しない。失敗時は R4C 導入前のバイト列へロールバックする。R4C の同型証明を検証した後にのみ $\pi_6^4$ の公開探索結果を確認する（公開完了判定を先取りしない）。
