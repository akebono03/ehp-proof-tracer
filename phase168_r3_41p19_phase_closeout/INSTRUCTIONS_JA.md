# Phase 168 R3-41P19 R3 — 現行 Reference テストの更新と終了判定

## 事前確認

GitHub `akebono03/ehp-proof-tracer` の `develop`（2026-10-25、SHA `9a66865c465135e0d5892c4e772b5a48371a939a`）のコード、Phase 167/168 関連テスト、Phase 165 の退避記録を確認した。

前回の全体 pytest は `3541 passed, 5 failed, 2 errors`。失敗5件は、共通 Renderer が `使用する結果` と `証明` の節見出しを Markdown の通常行（Web `kind="text"`）として出すのに対し、古い Phase 167 テストが `kind="heading"` として探したことによる。また、共通モデルの一般命題表示は `\pi_i^1`、`\pi_i^n`、`n\ge 1` を使うが、以前のテストは旧 LaTeX 表記を要求していた。

収集エラー2件は、現行 `tests/` の Phase 144 テストが、Phase 143 の退避済みテストを import することによる。**その Phase 144 テスト2ファイルは、Phase 165 R6 が `phase165_r6_audit_results/retired_phase144_tests/20261019T070710Z/` に既に保存したファイルと GitHub blob SHA が完全一致する。** 退避先の実ファイルとのバイト一致を実行時に確認した上で、現行 `tests/` 側の重複コピーだけを除く。

## 今回変更するファイル／関数

- `phase168_r3_41p13_trust_boundary/verification.py`：**前回 P19 と同一**の `verify_proof_tree_for_narrative()` 全文を適用。群の結論を検索対象に結び付ける修正。トップレベル import は変更しない。
- `tests/test_phase167_r2_range_dedup.py`：`_reference_text()`、テスト2関数を全文更新。節見出しの区別と一般数式の現在の表示を検証。
- `tests/test_phase167_r2_shared_reference.py`：テスト `test_phase167_r2_pi43_reference_has_two_general_results()` を全文更新。もう1つのテストは維持。
- `tests/test_phase167_r2_unified_reference.py`：`_reference_text()`、テスト2関数を全文更新。一般命題の提示と局所特殊化の不混入を確認。
- `tests/test_phase144_6_pi6_generic_production_route.py`、`tests/test_phase144_6_public_route_cutover.py`：既存の Phase 165 退避先に**同一バイトのコピーが存在する場合に限り**現行 `tests/` から重複を除去。元ファイルのバックアップも保存し、失敗時に復元。現行テストへの無条件の `--ignore` は行わない。
- `phase168_r3_41p19_phase_closeout/active_tests.py`：新規。上記5ファイルの事前照合、更新、退避重複の除去、バックアップ、復元を担当。`install()`、`restore()`、`main()` を追加。
- `phase168_r3_41p19_phase_closeout/tests/test_active_test_migration.py`：新規。模擬的な2回の適用・復元、改変された退避先、変更済みテストへの拒否を検査。
- `phase168_r3_41p19_phase_closeout/run.ps1`：適用→限定 pytest→3群全文・Citation・文献順→**現行 `tests/` 全体**の pytest→ログ保存・失敗時復元。実行スクリプトを全文置換。
- `phase168_r3_41p19_phase_closeout/review_bundle.py`：`main()` を全文更新し、5ファイルの元・変更後・退避の根拠をレビュー ZIP に収録。

関係しないアプリのクラス・関数・数学的規則・Renderer は変更しない。3つのテストの変更後全文と変更前全文は `active_test_full_files/` に全て収録。新規ファイル `active_tests.py`、`test_active_test_migration.py` の全文も含む。README.md、design.md、development_log.md、roadmap.md、proof_records.md は変更しない。

## 実行

Windows PowerShell で次を実行する。

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase168_r3_41p19_phase_closeout_r3_active_test_reconciliation.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_r3_41p19_phase_closeout\run.ps1"
```

## 完了条件と限界

1. 限定 pytest で P19、P18、P17、P15、P13 と更新した Reference テスト等が PASS。
2. $\pi_3^2$、$\pi_4^3$、$\pi_5^4$ の証明本文・Reference・Citation が固定基準と完全一致。
3. GIVEN 14件すべてに関して文献掲載順の検証が PASS。
4. `python -m pytest tests -q --tb=short --continue-on-collection-errors` が **0エラー、0失敗**で完了。
5. `active_suite_diagnostics.json` が `ACTIVE_SUITE_PASS` / `full_suite_certified=true` と報告。

条件4の「全体」は Phase 165 R6 の現行ルート `tests/` を意味し、`archive/` や独立の Phase 退避ディレクトリを無差別に収集する意味ではない。重複していた Phase 144 の退避済み2ファイルの一覧、対応する archive と変更前 SHA は `output/active_tests_manifest.json` に明記される。これらの旧テストを実行して成功したと主張しない。

失敗した場合は3つのテストと2つの重複ファイルを復元し、さらに `verification.py` の P19 修正を復元する。バックアップは `output/active_test_backups/` と `verification.py.before` に保持し、不一致なら上書きしない。

Origin Observation は単独の数学的証明書として採用しない。標準 Web の P13 検証と Renderer の数学的保護2箇所は維持する。今回の修正で Phase 168 の共通 Renderer の責務をこれ以上拡張しない。
