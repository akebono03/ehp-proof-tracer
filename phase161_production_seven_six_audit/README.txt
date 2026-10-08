Phase 161: Production 7-rule / 6-premise audit

目的：Phase 59 を比較用基準（oracle）としてのみ利用し、現在の Production Repository と Catalog に、必要な７規則と６前提が存在するか調べる。

注意：Phase 59 のデータを Production Repository に登録・注入しません。固定点安全性を数学的に証明する監査ではありません。既存コードの変更、pytest 全体実行はありません。

実行：リポジトリ直下から
powershell -ExecutionPolicy Bypass -File '.\phase161_production_seven_six_audit\run_phase161_seven_six.ps1'

出力：phase161_production_seven_six_audit.json

判定：
production_catalog_entries=0: 規則名の factory が Production Catalog に見つからない
any_search_eligible=false: 現在の探索で選択対象にならない
scope_matches: 証明グラフの内部で同一 statement が見つかった位置
usable_as_current_search_initial_premise: repository_available_steps から直接見えるか

Phase 59 基準の証明経路そのものは既に別途検証済み。今回は Production 接続境界のみ監査。
