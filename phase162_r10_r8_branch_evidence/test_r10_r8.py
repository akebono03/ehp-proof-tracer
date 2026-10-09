from audit import analyze, branches_of_root, issue_labels, shortest_root_branch


def _fixture():
    return {"steps":[
       {"id":0,"parent_node_ids":[],"premise_node_ids":[1,2],"statement_latex":"ROOT"},
       {"id":1,"parent_node_ids":[0],"premise_node_ids":[3],"statement_latex":"X","inference_rule":"rule-x"},
       {"id":2,"parent_node_ids":[0],"premise_node_ids":[3],"statement_latex":"Y","inference_rule":"rule-y"},
       {"id":3,"parent_node_ids":[1,2],"premise_node_ids":[],"statement_latex":"Z"}],
       "body_lines":[{"line":4,"text":r"$\Delta(\iota_{5})$", "origin":"STEP_EXACT_MATH","candidate_step_ids":[3]}]}


def test_branch_membership_shared():
    nodes={n['id']:n for n in _fixture()['steps']}
    result=branches_of_root(nodes,0)
    assert 3 in result[1] and 3 in result[2]


def test_parent_path_shortest():
    nodes={n['id']:n for n in _fixture()['steps']}
    assert shortest_root_branch(3,nodes,0) in ((3,1,0),(3,2,0))


def test_tag_detection():
    assert 'OFF_TARGET_H_MAP' in issue_labels({'text':r'$H: \pi_{3}^{2} \\to \pi_{3}^{3}$'})
    assert 'WHITEHEAD_SQUARE' in issue_labels({'text':r'$[\iota_{2},\iota_{2}]$'})


def test_audit_never_licenses_delete():
    data=_fixture()
    result=analyze(data)
    assert result['counts']['nodes']==4
    assert result['flagged_lines']
    assert all(not row['safe_to_delete'] for row in result['flagged_lines'])
