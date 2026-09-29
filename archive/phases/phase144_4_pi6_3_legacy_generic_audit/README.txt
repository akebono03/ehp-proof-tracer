Phase 144-4: π₆³ legacy vs generic 残存差分監査
================================================

目的
----
Phase 139〜143 で構築した一般化をやり直さず、現在の π₆³ legacy Narrative と
generic proof renderer の残存差分を機能単位で監査する。

このパッケージは監査専用であり、本番コードを変更しない。

監査対象
--------
- Definition
- Toda の定理・補題参照
- EHP 完全列
- 計算過程
- 位数決定
- 短完全列
- 群構造
- 式番号とその参照
- 段落構成・接続語
- 最終結論

分類
----
A:
  Phase 143 までに一般化済みで generic renderer から表示可能。
  本番経路で表示されない場合も、再実装対象にはしない。

B:
  generic Semantic / Block / Argument に必要情報はあるが、
  generic renderer の表示規則が不足している。

C:
  legacy renderer にしかないが不要、または現在の基準出力にも確認できない。

D:
  数学的情報そのものが generic Semantic / Argument structure に届いていない疑い。

変更対象
--------
新規監査ファイルのみ。

- phase144_4_pi6_3_legacy_generic_audit/audit_phase144_4_pi6_3.py
- phase144_4_pi6_3_legacy_generic_audit/run_phase144_4_pi6_3_audit.ps1
- phase144_4_pi6_3_legacy_generic_audit/README.txt

本番ソース、既存テスト、ドキュメントは変更しない。

実行方法
--------
PowerShell でリポジトリルートへ移動して実行する。

cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase144_4_pi6_3_legacy_generic_audit.zip" `
  -DestinationPath "." `
  -Force

powershell -ExecutionPolicy Bypass `
  -File ".\phase144_4_pi6_3_legacy_generic_audit\run_phase144_4_pi6_3_audit.ps1"

生成物
------
実行後、以下が作成される。

- output/legacy_pi6_3.md
- output/generic_pi6_3.md
- output/semantic_inventory.txt
- output/phase144_4_audit_report.md

pytest
------
Phase の途中なので全体 pytest は実行しない。

focused regression のみ実行する。

pytest -q `
  ".\tests\test_phase134_9_pi6_3_snapshot.py" `
  ".\tests\test_phase142_2_generic_narrative_renderer.py" `
  ".\tests\test_phase142_3_generic_proof_text.py" `
  ".\tests\test_phase143_2_generic_short_exact_sequence.py"

完了条件
--------
1. legacy と generic の両出力が保存される。
2. Semantic / Block inventory が保存される。
3. 10 個の機能監査項目が A/B/C/D に分類される。
4. Phase 144-5 で修正候補とする B/D が明示される。
5. 本番コードに変更がない。
6. focused regression が通る。

次 Phase との境界
-----------------
Phase 144-4 では監査のみを行う。

Phase 144-5 で初めて、144-4 の B/D に分類された不足だけを一般規則として修正する。
π₆³ 座標専用の本番処理は追加しない。
他の群の個別修正は Phase 144-7 以降まで行わない。
