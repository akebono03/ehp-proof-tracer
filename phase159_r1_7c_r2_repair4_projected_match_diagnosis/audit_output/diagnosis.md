# Phase 159-R1-7c R2 repair4 projected-match diagnosis

Production code changes: none
Test changes: none
pytest: not run

## transitivity step id=2625451891040
- conclusion: Relation(lhs=Multiple(coefficient=2, expression=HomotopyElement(name='ν′', dimension=3, source=6, target=3, generator=GeneratorSymbol(family='ν', index=None, decoration='′'))), rhs=Composition(left=HomotopyElement(name='η₃', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None)), right=Composition(left=HomotopyElement(name='η₄', dimension=4, source=5, target=4, generator=GeneratorSymbol(family='η', index=4, decoration=None)), right=HomotopyElement(name='η₅', dimension=5, source=6, target=5, generator=GeneratorSymbol(family='η', index=5, decoration=None)))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)
- first: Relation(lhs=Multiple(coefficient=2, expression=HomotopyElement(name='ν′', dimension=3, source=6, target=3, generator=GeneratorSymbol(family='ν', index=None, decoration='′'))), rhs=Composition(left=HomotopyElement(name='η₃', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None)), right=Composition(left=Suspension(expression=HomotopyElement(name='η₃', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None))), right=HomotopyElement(name='η₅', dimension=5, source=6, target=5, generator=GeneratorSymbol(family='η', index=5, decoration=None)))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)
- second: Relation(lhs=Composition(left=HomotopyElement(name='η₃', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None)), right=Composition(left=Suspension(expression=HomotopyElement(name='η₃', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None))), right=HomotopyElement(name='η₅', dimension=5, source=6, target=5, generator=GeneratorSymbol(family='η', index=5, decoration=None)))), rhs=Composition(left=HomotopyElement(name='η₃', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None)), right=Composition(left=HomotopyElement(name='η₄', dimension=4, source=5, target=4, generator=GeneratorSymbol(family='η', index=4, decoration=None)), right=HomotopyElement(name='η₅', dimension=5, source=6, target=5, generator=GeneratorSymbol(family='η', index=5, decoration=None)))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)
- lhs_latex="2\\nu'"
- middle_latex='\\eta_{3}E\\eta_{3}\\eta_{5}'
- rhs_latex='\\eta_{3}\\eta_{4}\\eta_{5}'
- body[1] content="\\nu'"; starts_lhs=False; ends_middle=False; equals_lhs_middle=False; ends_rhs=False
- body[7] content="2\\nu' = \\eta_{3}E\\eta_{3}\\eta_{5} = \\eta_{3}\\eta_{4}\\eta_{5}"; starts_lhs=True; ends_middle=False; equals_lhs_middle=False; ends_rhs=True
- body[9] content="H\\left(\\nu'\\right) = \\eta_{5}"; starts_lhs=False; ends_middle=False; equals_lhs_middle=False; ends_rhs=False
- body[13] content="H\\left(\\nu'\\eta_{6}\\right) = \\eta_{5}^{2}"; starts_lhs=False; ends_middle=False; equals_lhs_middle=False; ends_rhs=False
- body[17] content='\\pi_{5}^{2} = \\mathbb{Z}/2\\{\\eta_{2}\\eta_{3}\\eta_{4}\\}'; starts_lhs=False; ends_middle=False; equals_lhs_middle=False; ends_rhs=False
- body[35] content='\\operatorname{ord}\\left(\\eta_{3}^{3}\\right) = 2'; starts_lhs=False; ends_middle=False; equals_lhs_middle=False; ends_rhs=False
- body[39] content="\\operatorname{ord}\\left(\\nu'\\right) = 4"; starts_lhs=False; ends_middle=False; equals_lhs_middle=False; ends_rhs=False
- body[43] content="\\nu' \\in \\pi_{6}^{3}"; starts_lhs=False; ends_middle=False; equals_lhs_middle=False; ends_rhs=False
- body[60] content="\\pi_{6}^{3} = \\mathbb{Z}/4\\{\\nu'\\}"; starts_lhs=False; ends_middle=False; equals_lhs_middle=False; ends_rhs=False

## transitivity step id=2625451922032
- conclusion: Relation(lhs=MapApplication(map=MapSymbol(name='H'), expression=HomotopyElement(name='ν′', dimension=3, source=6, target=3, generator=GeneratorSymbol(family='ν', index=None, decoration='′'))), rhs=HomotopyElement(name='η₅', dimension=5, source=6, target=5, generator=GeneratorSymbol(family='η', index=5, decoration=None)), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)
- first: Relation(lhs=MapApplication(map=MapSymbol(name='H'), expression=HomotopyElement(name='ν′', dimension=3, source=6, target=3, generator=GeneratorSymbol(family='ν', index=None, decoration='′'))), rhs=IteratedSuspension(expression=HomotopyElement(name='η₃', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None)), exponent=2), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)
- second: Relation(lhs=IteratedSuspension(expression=HomotopyElement(name='η₃', dimension=3, source=4, target=3, generator=GeneratorSymbol(family='η', index=3, decoration=None)), exponent=2), rhs=HomotopyElement(name='η₅', dimension=5, source=6, target=5, generator=GeneratorSymbol(family='η', index=5, decoration=None)), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)
- lhs_latex="H\\left(\\nu'\\right)"
- middle_latex='E^{2}\\eta_{3}'
- rhs_latex='\\eta_{5}'
- body[1] content="\\nu'"; starts_lhs=False; ends_middle=False; equals_lhs_middle=False; ends_rhs=False
- body[7] content="2\\nu' = \\eta_{3}E\\eta_{3}\\eta_{5} = \\eta_{3}\\eta_{4}\\eta_{5}"; starts_lhs=False; ends_middle=False; equals_lhs_middle=False; ends_rhs=False
- body[9] content="H\\left(\\nu'\\right) = \\eta_{5}"; starts_lhs=True; ends_middle=False; equals_lhs_middle=False; ends_rhs=True
- body[13] content="H\\left(\\nu'\\eta_{6}\\right) = \\eta_{5}^{2}"; starts_lhs=False; ends_middle=False; equals_lhs_middle=False; ends_rhs=False
- body[17] content='\\pi_{5}^{2} = \\mathbb{Z}/2\\{\\eta_{2}\\eta_{3}\\eta_{4}\\}'; starts_lhs=False; ends_middle=False; equals_lhs_middle=False; ends_rhs=False
- body[35] content='\\operatorname{ord}\\left(\\eta_{3}^{3}\\right) = 2'; starts_lhs=False; ends_middle=False; equals_lhs_middle=False; ends_rhs=False
- body[39] content="\\operatorname{ord}\\left(\\nu'\\right) = 4"; starts_lhs=False; ends_middle=False; equals_lhs_middle=False; ends_rhs=False
- body[43] content="\\nu' \\in \\pi_{6}^{3}"; starts_lhs=False; ends_middle=False; equals_lhs_middle=False; ends_rhs=False
- body[60] content="\\pi_{6}^{3} = \\mathbb{Z}/4\\{\\nu'\\}"; starts_lhs=False; ends_middle=False; equals_lhs_middle=False; ends_rhs=False

## full pi6_3 proof body

```text

まず, $\nu'$ の位数を決定するために, 次の完全列を考える.

\[
\pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3}.
\]

[R2] より, $2\nu' = \eta_{3}E\eta_{3}\eta_{5} = \eta_{3}\eta_{4}\eta_{5}$.

[R2] より, $H\left(\nu'\right) = \eta_{5}$.

$\eta_{6}=E\eta_{5}$ である.

[R5] より, $H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}$.

[R1] と $E$ の単射性より, $E(\eta_{2}^{3})=\eta_{3}^{3}\neq0$ であり, 単射写像は元の位数を保つ.

[R1] より, $\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$.

[R3] より, $\pi_{7}^{5} = \mathbb{Z}/2\{\eta_{5}\eta_{6}\}$.

$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射.

完全性より, $\ker \Delta=\operatorname{Im}H=\pi_{7}^{5}$ である.

完全性より, $\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ は零写像.

この完全性と $Δ=0$ より, $\ker E=\operatorname{Im}Δ=0$ である.

\[
\pi_{5}^{2} \xrightarrow{E} \pi_{6}^{3} \xrightarrow{H} \pi_{6}^{5}.
\]

完全性より, $E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射.

$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$.

$\operatorname{ord}(\eta_{3}^{3})=2$ かつ $2\nu'=\eta_{3}^{3}$ より, $4\nu'=0$ かつ $2\nu'\neq0$ である.

$\operatorname{ord}\left(\nu'\right) = 4$.

最後に, $\pi_{6}^{3}$ の群構造を決定するために, 次の完全列を考える.

[R2] より, $\nu' \in \pi_{6}^{3}$.

[R4] より, $\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}$.

$\eta_{5} = \eta_{5}$.

$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射.

この完全性と, 左の写像が単射, 右の写像が全射であることより, 次の短完全列を得る.

\[
0\longrightarrow \pi_{5}^{2}\xrightarrow{E} \pi_{6}^{3}\xrightarrow{H} \pi_{6}^{5}\longrightarrow 0.
\]

この短完全列と両端の群の位数より, 中央の群の位数は $2\cdot2=4$ である.
また, $\nu'$ は中央の群に属し, $\operatorname{ord}(\nu')=4$ であるから, $\nu'$ は中央の群を生成する.

$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}$.

□
```
