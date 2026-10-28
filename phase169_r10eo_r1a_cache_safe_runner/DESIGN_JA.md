# Phase 169 R10EO-R1A — pytest キャッシュ安全化

## 監査結果と原因候補

R10EO-R1 の実行では限定 pytest が73 PASS、Definition メタデータと $\pi_{41}^{30}$ の監査も完了したが、最後の tracked diff 名称比較で失敗した。

GitHub `develop` の HEAD `57f807901f87c8d66acf4ee4db16ce05b00dccd4` では `.pytest_cache/v/cache/nodeids` および `.pytest_cache/v/cache/lastfailed` が追跡対象である。通常の pytest はキャッシュを更新することがあり、本番コードを変更しなくても監査後の tracked diff 集合が変化しうる。ただし今回の実際の差分ファイル名は未報告であり、原因は確定していない。

## 変更対象

新規 `phase169_r10eo_r1a_cache_safe_runner/run.ps1` のみを実行する。これは元の `phase169_r10eo_r1_definition_audit/run.ps1` を上書きしない独立したランチャーである。新規 README.md と DESIGN_JA.md は本監査パッケージの実行説明資料である。

既存本番モジュール、既存テスト、既存ドキュメント、Proof Tree、Reference、データベースは変更しない。関数・クラス・import の変更はない。

## 修正内容

- 限定 pytest に `-p no:cacheprovider` を指定し、pytest 標準キャッシュの更新を抑止する。
- `develop` と監査済み HEAD のチェックを維持する。
- 監査対象ソースのローカル未コミット変更の拒否を維持する。
- 監査前後の Git tracked diff 名称集合を比較し、差異が残った場合に新たに dirty となったファイルと dirty が解消したファイルを明示する。
- Git の修復・リセット・クリーンアップ処理は含めない。
- 既に変更されていた `.pytest_cache` 等のファイルは元に戻さない。

## 実行する pytest

`python -m pytest -p no:cacheprovider -q` を使い、R10EO-R1、R10B、R10D2、R10E8、R10E1 の既存限定テスト5ファイルだけを実行する。全体テストは Phase 169 終了時に限定する。

## 完了条件と境界

限定 pytest と監査を完了し、監査対象ソースが clean のままで tracked diff の前後集合に差異がない場合に PASS とする。失敗時は変更ファイル名を報告し、その内容を確認する。R10EO-R1A では Definition 登録、GeneratorImage 推論、11-stem 未解決 Goal の解消には着手しない。次の R10EO-R2 の実装判断は独立の設計監査結果に基づく。
