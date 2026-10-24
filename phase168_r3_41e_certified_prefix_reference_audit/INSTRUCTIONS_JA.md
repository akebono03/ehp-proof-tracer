# Phase 168 R3-41E — 出典を持つ実証明ステップの部分表示監査

既存の実装ファイル・クラス・関数を**変更しません**。新規の監査専用 `audit.py`、テストファイル、`run.ps1` のみです。

R3-41D1 の5群はすべて `SEARCH_FAILED` で証明ステップ0件でした。引用を持つ「真の部分探索」を監査できていないため、実際に完了した π₄³ の ProofStep から、証明依存関係に閉じた**真部分集合**を切り出して検査します。部分状態への再構成は監査専用であり、実検索が PARTIAL を返したという意味では**ありません**。新しい数学的証明や Reference は作成しません。

確認事項：
- 元の完成検索から実在する ProofStep だけを同一オブジェクトのまま採用すること
- screened bridge に実在する登録命題・Reference のみを引用すること
- Reference の見出しと**命題本文**が Web にあること
- 各 GIVEN/推論ステップに付いた出典番号が、Reference 部分にあるだけでなく、そのステップの文章に表示されているかを確認すること
- 未解決 Goal・診断が保持され、未完成証明に `□` が付かないこと

PowerShell：

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase168_r3_41e_certified_prefix_reference_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41e_certified_prefix_reference_audit\run.ps1"
```

結果：`phase168_r3_41e_certified_prefix_reference_audit\output\review_bundle.zip` をアップロードしてください。

限定 pytest のみ実施。全体テストは Phase の最後に実行します。
