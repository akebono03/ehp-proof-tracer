Phase 143-75AB-3-R2

Minimal repair after the focused tests showed that ScalarSymbol(name='u')
was incorrectly passed to render_toda_expression_latex().

The repair changes only the sign-parameter rendering call:
render_toda_expression_latex(statement.sign_parameter)
->
_render_scalar_latex(statement.sign_parameter)

No new renderer capability is introduced.
No documentation is changed.
No full pytest suite is run.
