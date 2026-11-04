# Phase 173 最終 Gate R2R2 — 以前の失敗記録が利用できない場合

## 状況と責務

最初の Phase 173 全体 pytest は、ユーザーが提示したコンソールログ上で `5 failed, 3541 passed` となった。R1 では、この5件に対応する Phase 167 の旧 Reference 境界テストを修正し、限定 pytest 6件が PASS した。次の R2 では以前の全体 pytest に由来する4ファイルを必須としたが、実行環境が `C:\Users\oomae` から `C:\Users\user` に変わり、元の記録を参照できない。

この R2R2 は、**原本証拠の不存在と、現在の修正済みソースの再検証を別の事実として扱う**。原本を検証済みと偽って先へ進めるのではなく、`UNAVAILABLE_ORIGINAL_FILES` と `NOT_VERIFIABLE` を明示する。

## 変更対象と最小性

- `phase173_final_gate_r2_recovery/gate.py` 全体：`verify_prior_failure()` に厳密なオプトインを追加し、`prior_evidence_status()` を追加。`main()` に `--allow-missing-prior-evidence` を追加。新たな再検証レポートに原本の状態を明記する。
- `phase173_final_gate_r2_recovery/run.ps1` 全体：`-AllowMissingPriorEvidence` を追加。4ファイル全欠如のみ受理し、一部欠如は拒否する。
- 新規ディレクトリ `phase173_final_gate_r2r2_missing_evidence/`：審査済みハッシュ付き差替え、完全なソース・テスト、復元可能なバックアップ、実行スクリプト。

証明探索、群構造、Proof Tree、Narrative、Web、既存の数学的出典、5つの主要文書は変更しない。`run.ps1` は既存の Git index を保持し、全体 pytest を一切実行しない。

## 安全性と終了判定

1. 記録が4ファイルすべて揃えば、R2 の既存照合により原本を検証する。
2. 記録が一部でも揃い残りが欠ければ、オプトインがあっても停止する。
3. 記録がすべて欠ける場合に限り、明示的なオプトインで原本のハッシュを空集合として扱い、原本未検証を新しいレポートへ保存する。
4. 修正済みのソース、R1 の3テストファイル、Git HEAD と差分は R2 の既存厳格検査を通す。
5. 新しいレポートと実行マーカーが既存なら、再実行による上書きを拒否する。
6. 修正後の全体 pytest が 3,546 PASS・終了コード0で完了した場合にのみ、Phase 173 終了文書の記録作業に進む。失敗は残す。

全体 pytest の PASS は現在のコードに対する新たな実測結果であって、過去の欠落したファイルを事後的に証明するものではない。
