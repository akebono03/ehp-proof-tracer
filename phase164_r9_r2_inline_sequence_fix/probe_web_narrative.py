"""Real n=3, k=2 shared Web narrative, checked after rendering."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from phase164_r9_narrative_contract import _MATH_SPAN, _sequence_signature, _contained
from phase164_r5_web_registry_connection import build_phase164_r5_web_pi5_3_proof


def main():
    out = Path(sys.argv[1])
    _, markdown = build_phase164_r5_web_pi5_3_proof(max_depth=2)
    (out / 'pi5_3_narrative.md').write_text(markdown, encoding='utf-8')
    sequences = [s for match in _MATH_SPAN.finditer(markdown)
                 if (s := _sequence_signature(match.group())) is not None]
    duplicate_pairs = [(i, j) for i, newer in enumerate(sequences)
                       for j, older in enumerate(sequences[:i]) if _contained(newer, older)]
    report = {
        'group': 'pi_5^3', 'depth': 2,
        'sequence_math_span_count': len(sequences),
        'remaining_duplicate_subwindows': duplicate_pairs,
        'text_contains_repeated_connector': bool(re.search(r'完全性より\s*[,，]\s*これより', markdown)),
        'proof_heading_present': '## 証明' in markdown,
        'proof_goal_present': '## 証明対象' in markdown,
        'first_sequences': [{'terms': terms, 'maps': labels} for terms, labels in sequences[:3]],
    }
    (out / 'web_probe.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if len(sequences) < 1 or duplicate_pairs or report['text_contains_repeated_connector'] or not report['proof_heading_present']:
        raise SystemExit('live π5³ Web narrative did not satisfy R9 requirements')


if __name__ == '__main__':
    main()
