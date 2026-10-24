# Phase 168 R3-41J1 — 修正記録

## 変更対象

- `phase168_r3_5_model_renderer.py`：`render_model_backed_narrative_markdown()` 全体を置換
- 今回の新規限定テスト：`tests/test_phase168_r3_41j1_citation_provenance.py`
- 実行・監査用：この ZIP 内の `run.ps1`, `install.py`, `audit.py`

## 原因

1. R3-41J は完全列導入文を変更し、既存 R3-26a の「次の完全列を考える」を含むという契約を壊した。
2. 新規テストだけが未選別の Bridge を Model に渡し、公開 Web 経路で確認済みの Reference 本文の存在条件を満たさなかった。

## 対応

- 既存の導入文言を保持しつつ、その前に既存 ProofStep 由来の `[R番号]` を配置。
- 公開 Web と同じ `context_sink` の選別済み Bridge からテスト用 Model を構築。本文の存在条件は削除しない。
- 数学的な推論・モデル構造・Reference 台帳・固定基準を変更しない。

## 検証

- 新規限定テスト8件、既存 R3-41I の6件、R3-26a の2件、R3-19 の3件（計19件）を実行する。
- 事後の R3-41I 監査で3群の未使用引用番号、説明ギャップ、Reference 本文欠落を確認。
- インストーラーは変更前 SHA256 を照合。失敗時はバックアップをバイト単位で復元・検証。
- 全体 pytest は実行しない。

## 境界

R3-41J1 は失敗した R3-41J の局所修復。文体一般の修正や新規推論、legacy 撤去はしない。
固定基準の全文一致を自動達成したとは判定しない。
