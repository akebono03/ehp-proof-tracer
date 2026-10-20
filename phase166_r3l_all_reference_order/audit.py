from __future__ import annotations
import json
from pathlib import Path
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase166_r3l_reference_order import connect_all_reference_orders

bridge=build_shared_typed_bridge()
_, report=connect_all_reference_orders(bridge)
output={'phase':'166-R3L','all_registered_references_scanned':report.total,
        'resolved':report.connected,'preexisting_unmapped':report.previously_connected,
        'unresolved_count':len(report.unresolved),'unresolved_reference_ids':report.unresolved,
        'reviewed_aliases_used':report.aliases_used,'full_pytest_run':False,
        'production_code_modified_by_audit':False}
target=Path('phase166_r3l_all_reference_order_results.json')
target.write_text(json.dumps(output,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps(output,indent=2,ensure_ascii=False))
print('AUDIT SAVED:',target)
