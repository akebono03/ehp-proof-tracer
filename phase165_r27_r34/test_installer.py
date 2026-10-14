from apply import transform


def test_r34_transform_function():
    source = 'def build_standard_web_operation_query_view(query_input):\n    return None\n'
    changed = transform(source)
    assert 'search_typed_operation_statements' in changed
    assert 'return None' not in changed


def test_r34_transform_idempotent():
    source = 'def build_standard_web_operation_query_view(query_input):\n    return None\n'
    assert transform(transform(source)) == transform(source)


def test_r34_transform_preserves_other_functions():
    source = 'def other():\n    return 9\n\ndef build_standard_web_operation_query_view(query_input):\n    return None\n'
    assert 'def other():\n    return 9' in transform(source)


def test_r34_removes_old_web_facade_imports():
    source = (
        "from repository_operation_query_facade import (\n"
        "  query_standard_repository_operation_input,\n)\n"
        "from repository_operation_query_presentation import (\n"
        "  build_repository_operation_query_presentation,\n)\n"
        "def build_standard_web_operation_query_view(query_input):\n"
        "    return None\n"
    )
    changed = transform(source)
    assert "repository_operation_query_facade" not in changed
    assert "repository_operation_query_presentation" not in changed
