from proof import ProofRule, ProofStep
from audit import describe_step, compare_derivations


def step(value, parents=()):
    return ProofStep(conclusion=value,premises=parents,rule=ProofRule.INFERENCE)


def test_r32_ancestry_is_read_only_and_records_two_branches():
    left=step('left')
    right=step('right')
    root=step('goal',(left,right))
    report=describe_step(root)
    assert report['node_count']==3
    assert report['root_premises']==["'left'","'right'"]
    assert not report['cycles']
    assert root.premises==(left,right)


def test_r32_distinct_roots_retained_in_diagnostic():
    first=step('goal',(step('first'),))
    second=step('goal',(step('second'),))
    report=compare_derivations([first,second])
    assert report['candidate_count']==2
    assert report['pair_comparisons'][0]['same_conclusion']
    assert not report['pair_comparisons'][0]['same_premise_conclusions']


def test_r32_empty_result_is_not_certified():
    assert compare_derivations([])=={'candidate_count':0,'pair_comparisons':[]}
