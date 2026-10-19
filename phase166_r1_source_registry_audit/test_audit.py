from audit import classify, inspect


def test_reference_prefixes_are_only_candidates():
    assert classify('(5.3), \\eta^3=2\\nu') == ('toda_equation', '(5.3)')
    assert classify('Prop3.1, example') == ('toda_proposition', 'Proposition 3.1')
    assert classify('Lem5.14, example') == ('toda_lemma', 'Lemma 5.14')
    assert classify('[MT] (15.5), example')[0] == 'external_tag'


def test_no_registry_never_grants_proof_permission():
    details, counts = inspect([{'reference': '(5.3), sample', 'n': '3', 'k': '3'}], None)
    assert counts['toda_equation'] == 1
    assert details[0]['reference_ids'] == []
    assert details[0]['proof_step_granted'] is False
    assert details[0]['citation_eligible'] is False


class FakeReference:
    reference_id = 'fake'
    locator = '(5.3)'


class FakeRegistry:
    _references = {'fake': FakeReference()}

    def assertions_for(self, reference_id):
        return ()


class FakeBridge:
    registry = FakeRegistry()


def test_matching_locator_does_not_grant_proof():
    details, _ = inspect([{'reference': '(5.3), content', 'n': '3', 'k': '3'}], FakeBridge())
    assert details[0]['match_status'] == 'locator_candidates_only'
    assert details[0]['typed_relation_verified'] is False
    assert details[0]['citation_eligible'] is False
