# Phase 169 R4A — Proposition 4.4 / EHP 経路監査

本監査は読み取り専用であり、証明完了を宣言しない。

- Git HEAD: `b999b4bbea651782b2238732c1d16d805dfbe530`
- 既存探索: `partial`、証明 Step: 2、未解決 Goal: 4
- 原文 Proposition 4.4: True
- 原文 Proposition 5.3 の証明: True
- Proposition 4.4 の型付き台帳エントリ数: 1
- 引用審査済み Proposition 4.4 の数: 1
- Proposition 4.4 出版順が前: [True]
- 直前の π₅³ 出典成分: ['shared:0:boundary:Proposition 5.3:pi5_3_group_relation']
- (5.1) による π₆⁷=0 候補: 1
- EHP の E 全射候補: 1
- EHP の添字検証: [(3, 6, 'e_h')]
- E 単射の出典登録: True
- 型付き MapInjective 展開候補: 0
- 型付き TodaSuspensionInjective 展開候補: 0
- η² 合成生成元の E 像展開候補: 1
- 安定範囲外の (4.5) 輸送候補: 0
- Git 追跡ファイルの変更なし: True

## 未解決 Goal

1. `CyclicStructureStatement(group=TodaPrimaryGroup(group_dimension=6, sphere_dimension=4), generator=Composition(left=HomotopyElement(name='η₄', dimension=4, source=5, target=4, generator=GeneratorSymbol(family='η', index=4, decoration=None)), right=HomotopyElement(name='η₅', dimension=5, source=6, target=5, generator=GeneratorSymbol(family='η', index=5, decoration=None))), order=2)`
2. `TodaSuspensionIsomorphismStatement(map=TodaSuspensionMap(source_group=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3), target_group=TodaPrimaryGroup(group_dimension=6, sphere_dimension=4)))`
3. `Relation(lhs=TodaPrimaryGroup(group_dimension=6, sphere_dimension=4), rhs=FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='η₄', dimension=4, source=5, target=4, generator=GeneratorSymbol(family='η', index=4, decoration=None)), right=HomotopyElement(name='η₅', dimension=5, source=6, target=5, generator=GeneratorSymbol(family='η', index=5, decoration=None)))), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)`
4. `Relation(lhs=FiniteCyclicGroup(order=2, generator=Composition(left=HomotopyElement(name='η₄', dimension=4, source=5, target=4, generator=GeneratorSymbol(family='η', index=4, decoration=None)), right=HomotopyElement(name='η₅', dimension=5, source=6, target=5, generator=GeneratorSymbol(family='η', index=5, decoration=None)))), rhs=TodaPrimaryGroup(group_dimension=6, sphere_dimension=4), relation_type=<RelationType.EQUALITY: 'equality'>, source=None, note=None)`

## 判定

Proposition 5.3 の原文では π₅³→π₆⁴ の全射性を (5.1)、単射性を Proposition 4.4 によって示す。
この監査はその引用・型付き候補を検査するものであり、単射性が既に証明済みかを候補数だけで判定しない。
Toda (4.5) の n=3,k=2 への適用は許可しない。

## 原文 Proposition 4.4

```tex
\begin{proposition}\label{prop:4.4}
% Prop4.4.\
$\alpha\in\pit{2n-1}{n}$ で $H(\alpha)=\pm\iota_{2n-1}$ とする. 
このとき,\\
\(
\pit{i-1}{n-1}\oplus\pit{i}{2n-1}\to\pit{i}{n},\quad
(\beta,\gamma) \longmapsto E\beta + \alpha\circ\gamma
\)
は, 任意の \(i\) で同型である. \\
特に, 
\(
E:\pit{i-1}{n-1}\to \pit{i}{n}
\)
は, 任意の \(i\) で単射である. 
\end{proposition}
```

## 原文 Proposition 5.3 の証明

```tex
\begin{proposition}\label{prop:5.3}
% Prop5.3.\
\(\pi^{n}_{n+2}=\gen{\eta_n^{2}}\cong \mathbb Z_2\ (n\ge2).\) \
\((G_2;2)=\gen{\eta^{2}}\cong \mathbb Z_2 .\)
\end{proposition}

\noindent
\textbf{Proof.}\ 
 (5.2) より, \(\pi_{4}^{2}=\gen{\eta_2^{2}}\cong \mathbb Z_2 .\)
完全列 (4.4)
\[
\pi_{6}^{3}\xrightarrow{\ H}\pi_{6}^{5}\xrightarrow{\ \Delta\ }\pi_{4}^{2}
\xrightarrow{\ E\ }\pi_{5}^{3}\xrightarrow{\ H\ }\pi^{5}_{5}
\xrightarrow{\ \Delta\ }\pi_{3}^{2}
\]
を考える. Prop 5.1 から,
\(\Delta:\pi^{5}_{5}\to\pi_{3}^{2}\) は単射である. \\
したがって, \(H(\pi_{5}^{3})=0\) で, \(E\) は全射. \\
さらに, (5.3) とProp 5.1 より,
\(H:\pi^{3}_{6}\to\pi^{5}_{6}\) は全射である. \\
ゆえに, \(\Delta(\pi^{5}_{6})=0\) であり, 
\(E\) は単射となる. \\
よって, \(E:\pi_4^2\xrightarrow{}\pi_5^3\) は同型となり, \(n=3\) の場合が示せた. \\
次に, 
\(\pi_5^3\xrightarrow{E}\pi_6^4\xrightarrow{}\pi_6^7\)
において, (5.1) により,
\(\pit{6}{7}=0\) なので,
\(E\) は全射である. \\
Prop4.4 により, \(E\) は単射なので, 
\(E:\pit{5}{3}\to\pit{6}{4}\) は同型であるので, \(n=4\) の場合が示せた. \\
\(n>4\) と, \((G_2;2)\) については, (4.5) から分かる. 
\qed
```
