# Phase 171 Closeout R1 — Git・回帰テスト事前監査

## 対象と基準

- GitHub: `akebono03/ehp-proof-tracer`, `develop`
- 2026年10月31日に確認した HEAD: `e814ec939652807d464fd76051d34a9da40328f8`
- 引き継ぎ HEAD: `98833d5652b2ebec44618516666c378af7a8762e`
- この監査は **既存リポジトリのファイルを変更しない**。`git pull`・`git reset`・`git checkout`・`git clean` は実行しない。
- 結果の JSON は `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_closeout_r1_日時\audit.json` に保存する。

## 調査項目

1. ローカル `develop`、HEAD、リモート `develop` の HEAD を比較する。
2. `git status` の tracked/untracked を区別する。引き継ぎで既知の変更と、それ以外を区別する。
3. GitHub 現行コードから採取した4つの blob SHA と、ローカル実ファイルを照合する。
4. 引き継ぎ時点で未追跡だった3ディレクトリが、最新 GitHub では追跡済みである点を記録する。
5. 完成した $\pi_6^3$ の Proof Tree と引用・η式表示に関するテスト、および既存1-stem/2-stemの限定回帰テストを実施する。
6. テスト実行前後の tracked status を比較する。全体 pytest はこの R1 では実行しない。

## 実行

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_Closeout_R1_Preflight_Audit.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_closeout_r1_preflight_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_closeout_r1_preflight_audit\run.ps1"
git status -sb
git diff --stat
```

`-DryRun` はテストを実行せず Git・内容を監査する。通常実行は、内容照合と既知の tracked diff の検査に成功した場合のみ、明示した17ファイルの **限定 pytest** を実行する。内容照合に失敗したら変更せず停止する。古いローカル HEAD からの同期処理は含まない。

## Closeout の終了条件（次段階）

- 最新 HEAD とローカルでの内容一致または履歴差分の妥当性の説明。
- 公開検索 `complete`, `open_goals=0`, `generic-complete-proof`, `Reference=8`, 検証済み Proof Tree の保持。
- 単射・全射、短完全列、位数4、$2\nu'=E(\eta_2^3)\ne0$ の証明・表示が維持されること。
- 既存1-stem/2-stemと出典・引用境界の回帰テストが PASS すること。
- 必要な5文書の更新（README は英語、その他日本語。追記型の記録を尊重）。
- これらを終えた時点で `python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests` を **Phase 終了時に一度** 実行する。
- 全体テストのログ、Git 差分、Phase 172 に先送りする任意の表示改善を記録する。

この ZIP は Closeout を完了させる実装パッチではない。監査専用であり、Proof Tree・Renderer・DB・文献・既存テストを変更しない。
