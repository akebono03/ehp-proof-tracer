# Phase 169 R10EH-R1 — Git blob 事前検査の更新

## 原因

R10EH が想定した `transport.py` の Git blob は R10EG 適用前の `d60770fff1b6e14791db6b952733f4062a64c8eb` だった。R10EG を `develop` の `1a132f382b4fe93b1ab3cb30f5d9178684e9c65a` にコミットした後、実際の blob は `3865d1e57923a0d45f0240cc357110e51b20a3e1` に変わった。そのため監査実行前の検査だけが停止した。

## 変更範囲

既存の本番コード・Proof Tree・推論規則・引用・データベース・既存テスト・元の R10EH `run.ps1` は変更しない。R10EH-R1 に PowerShell ランナー全文、3件の独立テスト、説明ファイルを新設する。

修正したランナーは R10EG の commit 祖先、HEAD 内の `transport.py` blob、実際の作業ファイルの blob が一致することを検査する。他の既存 blob 検査、4群の監査、限定 pytest、追跡ファイル状態の前後比較を維持する。元のランナーについて SHA-256 を検査し、一時的な `run_r1_verified.ps1` を呼び出した後、検証済みの一時ファイルだけ削除する。

## テストと完了境界

新規ガードテスト3件と既存 R10EH の限定テスト8件を実行し、4群の監査を続行する。`complete` が期待される群については Trust Boundary を検査し、`partial` の群は未解決のまま記録する。監査失敗なら成功と表示しない。全体 pytest は Phase 169 終了時にのみ実施する。
