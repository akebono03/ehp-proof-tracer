# Phase 165 R27-R26-R2

修正対象: `standard_production_applicability_catalog.py` における同名の段階的な再定義。

初期 Builder 参照を持つ定義と、最後の有効な公開定義だけを廃止する。中間の分類器は編集しない。

旧 Production Repository や Bootstrap の削除は、ルートの本番 import が残存していない場合に限定。

対象 pytest のみ実行。全体 pytest は実施しない。
