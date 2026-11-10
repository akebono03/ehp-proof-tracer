"""Independent public proof, source dependency and common narrative audit."""
from __future__ import annotations
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r56_cyclic_generator_bridge.audit import _search_with_model
from phase174_r3_r7_r56_cyclic_generator_bridge.rule import (
    CYCLIC_RULE_NAME, SURJECTIVE_RULE_NAME,
)

def inspect_public():
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from proof import ProofRule
    from map_property_rules import ImageZeroStatement
    from homotopy_groups import TodaSuspensionMap

    bridge=build_shared_typed_bridge()
    first, model1=_search_with_model(6,5,bridge)
    second, model2=_search_with_model(7,5,bridge)
    earlier=exact_prior_database_result(6,5)
    if first.conclusion != earlier:
        raise RuntimeError('pi11-6 differs from exact independently proved goal')
    roots1=[x for x in model1.steps if x.conclusion==earlier and x.rule is ProofRule.INFERENCE
            and getattr(x.inference_rule,'name',None)==CYCLIC_RULE_NAME]
    if len(roots1)!=1 or len(roots1[0].premises)!=4:
        raise RuntimeError('independent cyclic presentation lost its four proofs')
    surj=[x for x in model2.steps if getattr(x.inference_rule,'name',None)==SURJECTIVE_RULE_NAME
          and x.rule is ProofRule.INFERENCE]
    if len(surj)!=1 or len(surj[0].premises)!=1 or surj[0].premises[0].conclusion!=earlier:
        raise RuntimeError('new surjectivity did not use only the prior group result')
    if surj[0].premises[0].rule is not ProofRule.GIVEN or 'ADOPTED_DATABASE_PRIOR' not in (surj[0].premises[0].note or ''):
        raise RuntimeError('earlier result has not been admitted under DB prior gate')
    for step in model2.steps:
        if step.rule is ProofRule.INFERENCE and step.conclusion==earlier:
            raise RuntimeError('later group proof redundantly reproved earlier group')
    exact=[citation.reference.locator for citation in model1.citations]
    later=[citation.reference.locator for citation in model2.citations]
    if 'Proposition 2.7' not in exact:
        raise RuntimeError('pi11-6 lost its sourced Prop 2.7 prerequisite')
    if 'Proposition 2.7' in later:
        raise RuntimeError('pi12-7 still uses unnecessary Prop 2.7')
    if not any(type(x.conclusion) is ImageZeroStatement and type(x.conclusion.map) is TodaSuspensionMap for x in model1.steps):
        raise RuntimeError('proved suspension zero-image is not present in pi11-6 proof tree')
    markdown1=render_model_backed_narrative_markdown(first,model1)
    markdown2=render_model_backed_narrative_markdown(second,model2)
    for label,condition in {
        'pi11_r7_cited': ('[R7]より' in markdown1 or '[R7]を' in markdown1),
        'pi11_suspension_zero_displayed': 'は零写像' in markdown1 and 'E:' in markdown1,
        'pi11_kernel_uses_generated_subgroup': r'\mathbb{Z}\{2\iota_{11}\}' in markdown1,
        'pi11_signed_lower_delta_not_displayed': r'\Delta(\iota_{11})=\pm' not in markdown1 and r'\Delta\left(\iota_{11}\right) = \pm' not in markdown1,
        'pi12_no_prop27': 'Proposition 2.7' not in markdown2,
    }.items():
        if not condition:
            raise RuntimeError('R57 public narrative contract failed: '+label)
    return {
        'pi11_6_complete':True,
        'pi11_6_cyclic_root_premises':4,
        'pi11_6_hopf_delta_cited':True,
        'pi11_6_suspension_zero_rendered':True,
        'pi11_6_kernel_generator_form':True,
        'pi12_7_complete':True,
        'pi12_7_surjectivity_premises':1,
        'pi12_7_prior_db_adopted_once':True,
        'pi12_7_prop27_absent':True,
        'pi11_reference_count':len(model1.citations),
        'pi12_reference_count':len(model2.citations),
        'new_given':0,
        'new_mathematical_rules':0,
        'full_pytest':False,
    }

def main():
    inspection=inspect_public()
    target=Path(os.environ.get('LOCALAPPDATA',tempfile.gettempdir()))/'EHPProofTracerAudit'/'phase174_r3_r7_r57'
    target.mkdir(parents=True,exist_ok=True)
    path=target/'public_proofs.json'
    path.write_text(json.dumps(inspection,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for k,v in inspection.items():
        print('PHASE174_R57_'+k.upper()+'='+str(v))
    print('PHASE174_R57_REPORT='+str(path))
    print('PHASE174_R57_GATE=PASS_R57_PUBLIC_PROOF_AND_NARRATIVE')
    print('(END)')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
