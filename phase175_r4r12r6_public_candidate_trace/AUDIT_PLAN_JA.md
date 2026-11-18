# Phase 175 R4R12R6 — 公開候補の経路診断

- R4R12R5R2 は DryRun PASS・本実行では `R4R12_PUBLIC_ROOT_QUOTIENT_PROPOSAL_MISSING`。
- R4R3 の反復懸垂型対応と現行 Git HEAD を検証する。
- 候補生成直後・公開 Provider 呼び出し・共有探索返却の件数を記録する。
- 変更対象は新規 `trace.py`、新規 `tests/test_trace.py` と実行用ファイルのみ。
- 数学規則、先行群、証明済み ProofStep を追加・変更しない。
- 全体 pytest と実際の群証明探索は実施しない。
- Gate は診断の実行成功のみを意味し、候補が0件ならそのまま記録する。
