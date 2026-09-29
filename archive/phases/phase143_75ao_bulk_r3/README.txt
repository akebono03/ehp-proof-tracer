Phase 143-75AO bulk R3

The old defective patcher is not used.

R3 patches the current syntactically valid production source directly,
using AST only to locate import/function boundaries and real newline
characters for inserted source.

Scope remains the same nine semantic statement renderers.
No docs changes.
Focused tests only.
No full pytest.
