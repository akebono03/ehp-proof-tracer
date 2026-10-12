# Phase 163 R4-R49 変更一覧

## 変更対象

既存ファイル・クラス・関数の変更なし。次のファイルを新規追加する。

1. `phase163_r4_r49_candidate_triage/phase163_r4_r49_candidate_triage.py`
   - `strip_comments`：行番号を保持した TeX コメント除去。
   - `parse_displays`：独立数式開始子と範囲の抽出。
   - `triage`：R4-R48 候補316件の対応を残したまま構文上の誤検出と入れ子重複を区別。
   - `save_report`：JSON / CSV / Markdown を生成。
   - `main`：監査を実行する CLI。
2. `phase163_r4_r49_candidate_triage/tests/test_phase163_r4_r49_candidate_triage.py`
   - 新規テスト9件。コメント、改行幅指定、入れ子、316件の保存、ハッシュ不整合、再実行の決定性、出力を確認する。
3. `phase163_r4_r49_candidate_triage/run.ps1`：必要な既存成果物の存在確認、限定 pytest と監査実行。
4. `README.md`（本パッケージ内、英語全文）および本書（日本語全文）。

## 完了条件

- R4-R48 の316候補を欠落させず、各候補に元データの行番号と文脈を付与する。
- 正規の数式表示・入れ子の数式・改行幅指定の誤認を区別する。
- 第1〜5章の原稿 SHA-256 および既存108登録単位を確認する。
- 全ての数学的意味判断は未審査のまま維持する。

## 次 Phase との境界

R4-R50 以降で定義・数学的主張の内容と、既存命題／証明途中の式との関係を具体的に審査する。今回の Phase では数学的意味の判定、既存 Registry への統合、Statement ID の発行を行わない。全体 pytest は Phase 163 終了時にのみ実施する。
