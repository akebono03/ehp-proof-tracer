import inspect

import pytest

import web_group_proof as web
from phase165_goal_only_search import GoalSearchIncompleteError


def test_pi53_proof_does_not_claim_success_without_typed_catalog():
    with pytest.raises(
        GoalSearchIncompleteError,
        match="Registered goal/rule catalog not configured",
    ):
        web.build_standard_web_group_proof_view(3, 2, 2, "narrative")


