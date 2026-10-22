from phase168_r2_6_registry_bridge_audit.audit_registry_bridge import (
    is_typed_content,
    literature_locator,
    semantic_key,
    strip_shared_prefix,
)


class Ref:
    def __init__(self, locator=None, title=None):
        self.locator = locator
        self.title = title


class Assertion:
    def __init__(self, content):
        self.content = content


def test_strip_shared_prefix_removes_only_shared_namespace():
    assert strip_shared_prefix("shared:12:boundary:Proposition 5.3:x") == "boundary:Proposition 5.3:x"
    assert strip_shared_prefix("boundary:Proposition 5.3:x") == "boundary:Proposition 5.3:x"


def test_literature_locator_recognizes_proposition_lemma_and_equation():
    assert literature_locator(Ref(locator="Proposition 5.3")) == "Proposition 5.3"
    assert literature_locator(Ref(title="Lemma 4.1")) == "Lemma 4.1"
    assert literature_locator(Ref(locator="Toda (5.2)")) == "(5.2)"


def test_is_typed_content_rejects_metadata_scalars():
    assert not is_typed_content("metadata only")
    assert not is_typed_content(3)
    assert is_typed_content(("typed", "tuple"))


def test_semantic_key_uses_type_and_value_representation():
    assert semantic_key(Assertion(("x", 1))) == ("tuple", "('x', 1)")
