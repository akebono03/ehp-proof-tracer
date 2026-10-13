# Phase 165 R14-R35: strict leaf binding audit

## 変更対象（新規、既存ファイルは変更なし）
- `phase165_r14_r35_leaf_binding.py`: `LeafBindingCandidate`、`backward_leaf_goals`、`known_source_candidates`、`audit_r35` を全て追加。
- `test_phase165_r14_r35_leaf_binding.py`: 関連するテスト6件を追加。
- `audit.py`、`run.ps1`、`toda_51_complete.tex` を追加。

## 目的
R34 が返した未解決9葉を文字列から復元するのでなく、**元の型付き目標**のまま列挙する。R23/R26/R30/R31/R33 の採用 TeX から作成した暫定的な前提と照合する。候補がない場合は未照合とし、曖昧な場合は曖昧なまま記録する。必要な次の作業を `phase165_r14_r35_output/report.json` に残す。

## 制限
今回は **source locator candidate**（出典候補）の照合であり、厳密な Registry 引用資格を新規認定しない。証明木・既存 API・既存テストには一切変更を加えない。Proposition 5.1 の source_id は候補表記にすぎず、厳密な台帳 ID として承認しない。R35 の実行で未解決葉がすべて解消すると保証するものではない。

## 完了条件
対象 pytest 6件合格、R34 と一致する9件の未解決葉と候補の照合報告を作成し、推論で導くべき葉と文献のまま残すべき葉の区別に必要な情報を確保する。全体 pytest は Phase 165 末尾のみ。

## 次工程
監査で未対応となる命題を既存の一般規則へ接続し、出典の確認が済んだものだけ Registry に昇格して、strict backward search を再実行する。
