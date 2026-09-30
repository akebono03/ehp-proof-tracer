from proof import Relation, RelationType
from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step
from toda_group_proof_narrative_semantics import build_toda_group_proof_narrative_semantic_closure_presentation
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_proof_dependency import extract_toda_recursive_proof_provenance

def rn(s):
    return None if s.inference_rule is None else s.inference_rule.name

def eq(s):
    x=s.conclusion
    return isinstance(x,Relation) and x.relation_type is RelationType.EQUALITY

def main():
    g=build_standard_toda_report(n=3,k=3).candidates[0].source_candidate.group_result
    p=build_toda_group_proof_presentation(build_toda_group_result_proof_replay(g,max_depth=2))
    c=build_toda_group_proof_narrative_semantic_closure_presentation(p)
    prov=extract_toda_recursive_proof_provenance(g)
    orig={id(n.proof_step) for n in p.nodes}
    node_by_id={id(n.proof_step):n for n in prov.nodes}
    byprem={}; bypar={}
    for e in prov.edges:
        byprem.setdefault(id(e.premise_step),[]).append(e)
        bypar.setdefault(id(e.parent_step),[]).append(e)
    added=[n for n in c.nodes if id(n.proof_step) not in orig]
    print("="*72)
    print("R3.1 CLOSURE EDGE AUDIT")
    print(f"input={len(p.nodes)} closure={len(c.nodes)} added={len(added)}")
    for i,n in enumerate(added,1):
        s=n.proof_step
        print("-"*72)
        print(f"ADDED[{i}] depth={n.depth} role={n.role.value} eq={eq(s)}")
        print("statement="+_render_generic_narrative_step(s))
        print("step_rule="+repr(rn(s)))
        for e in byprem.get(id(s),[]):
            par=e.parent_step; pe=bypar.get(id(par),[])
            ee=[x for x in pe if eq(x.premise_step)]
            pn=node_by_id[id(par)]
            print(f" consumer index={e.premise_index} parent_depth={pn.shortest_depth} parent_role={pn.role.value} parent_original={id(par) in orig} parent_eq={eq(par)} total={len(pe)} equality={len(ee)} rule={rn(par)!r}")
            print(" parent="+_render_generic_narrative_step(par))
            for x in pe:
                xn=node_by_id[id(x.premise_step)]
                print(f"   premise index={x.premise_index} depth={xn.shortest_depth} eq={eq(x.premise_step)} role={xn.role.value} rule={rn(x.premise_step)!r}")
                print("     "+_render_generic_narrative_step(x.premise_step))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
