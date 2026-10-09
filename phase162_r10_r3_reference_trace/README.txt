Phase 162 R10-R3 — 97ノード分類 / Reference 欠落原因の読み取り専用監査

対象ファイル: 既存の phase162_r10_r2_tree_audit.json（ユーザーのプロジェクト直下）
監査元: 実 Web replay, 共通 Reference エントリ抽出, fixed-statement filter, 最終 Markdown
今回の変更: 新規の監査パッケージのみ。production files は変更しない。
結果: phase162_r10_r3_reference_trace.md / .json
テスト: python -B -m pytest -q phase162_r10_r3_reference_trace/tests/test_audit.py
注意: 97件の分類を列挙し、引用が取得できなかった段階を区別する。修正は次のラウンド。
