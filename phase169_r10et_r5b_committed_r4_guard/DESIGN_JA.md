# Phase 169 R10ET-R5B — コミット済み R4 対応

## 監査で確定した事実

R10ET-R5 はパッチ適用前に Git ガードで停止した。GitHub `develop` HEAD は `3a8014efb91ddf76060c4d07d73153e55ea52c75`（`10et4`）であり、R4 の2ファイルの変更は HEAD にコミットされている。R5 の対象5ファイルは旧監査済み Git blob と一致している。

## 変更対象と関数

**R5B パッケージ固有の変更:** `run.py` の `verify_preconditions()` 全体。新規 `tests/test_r5b_head_guard.py` のテスト2関数。`run.py` 内の実行ログ名と新フォルダに合わせた import/パス、README、設計書を更新する。

**R5 本体に適用する変更（前回と同一）:** `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` 全体と、既存テスト4ファイル。変更後の完全な関数とファイルは `output/<実行時刻>/full_sources/` に保存する。R4 の Production ファイル、Trust Boundary、Reference 登録、DB prior、Toda (4.5)、Renderer は変更しない。

## 安全なガード

`develop` かつ HEAD が既知の2件のいずれかであることを要求する。元の R4 コミット前 HEAD から既存 R4 patch による完全な変換を実行し、現在の R4 ファイルのバイト列と照合する。コミット済み R4 HEAD では、HEAD 内ファイルとも一致させる。さらに R5 の5つの入力ファイルの Git blob を作業ツリーと HEAD の双方で照合する。既存の追跡対象差分は、R4 未コミット時のみ既知の2ファイルを許容し、コミット済み R4 では一切許容しない。ステージ済み差分は常に拒否する。

## 検証・完了条件

限定 pytest は R5B・R5 相当・R4・R10A・R10EC・R10EL・R10ER・R10EQ・R10EN・R10ES。実際の本番探索16ケースすべて complete、Trust PASS。共通 Definition の適用数と Reference が R2 の基準に一致し、巡回群2ケース・直和群7ケースの圧縮表示が維持される。

パッチやテスト・監査に失敗した場合は R5B が変更した5ファイルのみ原状復帰し、コミット済み R4 の2ファイルは維持する。全体 pytest は Phase 169 の終了時まで実行しない。

## 次 Phase との境界

R5B は R5 のガード修正のみを追加する。個別 Definition 台帳の削除、証明の意味の拡張、Renderer の別経路追加、Phase の全体 closeout は実施しない。
