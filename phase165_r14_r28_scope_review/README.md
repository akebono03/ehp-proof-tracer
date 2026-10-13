# Phase 165 R14-R28 — Proposition 4.2 の TeX 前提確認

## 変更対象

- 新規 `phase165_r14_r28_scope_review.py`：`PropositionContext`、`_normalized_backslashes`、`find_toda_tex`、`proposition_context`、`audit_r28` の全文
- 新規 `test_phase165_r14_r28_scope_review.py`：関連6テスト全文
- 新規 `audit.py`, `run.ps1`, `README.md`

既存の API、Registry、推論規則は変更しない。第4章を含む `Toda_01.tex` がリポジトリ直下または規定のフォルダに存在する場合のみローカルで参照する。

## 重要な数学的制約

アップロードされた Proposition 4.2 の抜粋 (4.4) 自体は `n=1` の適用範囲を明言していない。近傍 TeX の検索は前提確認の補助であり、文脈に `n≥1` の文字があってもそれだけでは適用を承認しない。R23 の同型導出と R26 の型付き完全性は維持し、R28 は $\Delta=0$ を無根拠に証明済みにしない。

## 完了条件

対象6テスト合格、Proposition 4.2 の文脈があれば監査ファイル `phase165_r14_r28_output/report.json` に記録、なければ明示的な未確認状態を表示する。全体 pytest は Phase 165 終了時のみ。

## 次の工程

第4章の前提文の論理的範囲を数学的に確認し、$n=1$ が正当化される場合のみ R24 の $\Delta=0$ 導出へ渡す。適用外の場合は低次元専用の別根拠を検討する。
