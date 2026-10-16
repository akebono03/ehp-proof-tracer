"""Inspect existing Toda rule reversibility; do not assert proof completion."""
from __future__ import annotations
import inspect
import json
from pathlib import Path
from phase165_r8_rule_provider import _pattern_variable_names
from proof import InferenceRule, PremisePattern
import toda_rules

NAMES = (
 "toda_pi4_3_finite_cyclic_inference_rule",
 "toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule",
 "toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule",
)

def inspect_rule(name: str) -> dict:
    factory = getattr(toda_rules,name,None)
    if not callable(factory):
        return {"name":name,"status":"FACTORY_MISSING","invertible":False}
    signature=inspect.signature(factory)
    required=[p.name for p in signature.parameters.values()
              if p.default is inspect.Parameter.empty and
              p.kind in (inspect.Parameter.POSITIONAL_ONLY,
                         inspect.Parameter.POSITIONAL_OR_KEYWORD,
                         inspect.Parameter.KEYWORD_ONLY)]
    if required:
        return {"name":name,"status":"REQUIRES_INPUT","required":required,"invertible":False}
    try:
        rule=factory()
    except Exception as exc:
        return {"name":name,"status":"FACTORY_ERROR","error_type":type(exc).__name__,"invertible":False}
    if not isinstance(rule,InferenceRule):
        return {"name":name,"status":"NOT_INFERENCE_RULE","invertible":False}
    conclusion=rule.conclusion_pattern
    reasons=[]
    if conclusion is None:
        reasons.append("NO_EXPLICIT_CONCLUSION_PATTERN")
    if not rule.premise_patterns:
        reasons.append("NO_PREMISE_PATTERNS")
    bindings=_pattern_variable_names(conclusion) if conclusion is not None else frozenset()
    for i,pattern in enumerate(rule.premise_patterns):
        if not isinstance(pattern,PremisePattern):
            reasons.append(f"PREMISE_{i}_NOT_PATTERN")
            continue
        template=(pattern.relation_pattern if pattern.relation_pattern is not None
                  else pattern.statement_pattern)
        if template is None:
            reasons.append(f"PREMISE_{i}_NO_TEMPLATE")
            continue
        missing=_pattern_variable_names(template)-bindings
        if missing:
            reasons.append(f"PREMISE_{i}_UNBOUND_VARIABLES:"+",".join(sorted(missing)))
    return {"name":name,"rule_name":rule.name,
            "status":"EXPLICITLY_INVERTIBLE" if not reasons else "REQUIRES_GENERIC_INVERSION_DESIGN",
            "reasons":reasons,"invertible":not reasons}

def make_report() -> dict:
    rows=[inspect_rule(name) for name in NAMES]
    return {"phase":"165 R6-2 R1",
            "scope":"existing Toda inference rule shape; no group-specific reverse adapter executed",
            "rules":rows,
            "all_explicitly_invertible":all(x["invertible"] for x in rows),
            "full_pytest_run":False}

def main():
    path=Path(__file__).with_name("report.json")
    report=make_report()
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
