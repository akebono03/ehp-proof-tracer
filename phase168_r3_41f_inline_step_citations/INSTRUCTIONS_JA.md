# Phase 168 R3-41F — 未完成 ProofStep の出典番号接続

## 対象と境界

変更する既存ファイルは `phase168_r3_5_model_renderer.py` のみ。対象関数は `render_model_backed_narrative_markdown()` 全体です。import の変更はなく、クラスや他の関数は変更しません。完全版は `full_functions/render_model_backed_narrative_markdown_FULL.py` と `full_files/phase168_r3_5_model_renderer.py` に収録しています。

未完成証明の各ステップに `model.step_citation_numbers[index]` の**既存番号だけ**を表示します。与件は `[R1]より,`、推論は `[R1]を用いて,` と表示し、番号のない行は変更しません。Reference の本文、検索規則、文献順、完成証明、Web Adapter は変更しません。

## 実行

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase168_r3_41f_inline_step_citations.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41f_inline_step_citations\run.ps1"
```

元ファイルの完全関数と照合してからバックアップ・置換します。失敗時は自動復元します。限定 pytest のみ実行します。

## 検証項目

- 完成した4群 $\pi_3^2,\pi_4^3,\pi_5^4,\pi_6^5$ の Narrative がバイト単位で一致すること。
- 明示的な legacy と直接 fallback の出力がバイト単位で一致すること。
- 監査用の再構成部分証明で、出典番号の欠落4件が0件になること。
- Reference の数・本文数・番号、未解決 Goal・探索診断、未完成を示す状態が変わらないこと。
- 不正な引用対応を拒否し、未登録の Reference を推測しないこと。

完成条件は限定 pytest 全件 PASS と比較監査 PASS です。成果物は `output/review_bundle.zip`。R3-41G 以降の実探索・完全性・Reference と固定基準の全文比較は次の工程とし、今回先取りしません。全体 pytest は Phase 168 の最後にのみ実行します。
