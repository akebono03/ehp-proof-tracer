# Phase 163 R4-R73：文脈に基づく追加個別判定案

出典 TeX と既存 R72 提案に基づく編集上の提案。原本照合・数学的検証・Registry 登録は未実施。

- 追加で個別判定した候補: 138
- 判定案の累計: 172
- 未判定: 65

|Role|Count|
|---|---:|
|ADJACENT_DEFINITION_EXTENSION|1|
|DEFINITION_COMPONENT|23|
|DEPENDENCY_CONTEXT_CANDIDATE|10|
|EXISTING_REFERENCE_COMPONENT|2|
|EXTERNALLY_SOURCED_ASSERTION_CANDIDATE|1|
|PROOF_INTERNAL_CANDIDATE|62|
|PROOF_LOCAL_CONSTRUCTION_CANDIDATE|43|
|SEPARATE_DEFINITION_CANDIDATE|5|
|UNNUMBERED_ASSERTION_CANDIDATE|25|
|UNREVIEWED|65|

## 追加判断（出典と根拠）

### R48 #3（第1章 119行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：Chapter 1 sphere parametrization
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
\psi_{n+1}(t_{1},\cdots,t_{n},\frac{1}{2})=
i(\psi_{n}(t_{1},\cdots,t_{n})).
\]
```

```text
116: を,
117: \(i(s_{0},\cdots,s_{n}) := (s_{0},\cdots,s_{n},0)\)
118: で定義するとき,
119: \[
120: \psi_{n+1}(t_{1},\cdots,t_{n},\frac{1}{2})=
121: i(\psi_{n}(t_{1},\cdots,t_{n})).
122: \]
123: \(\psi_{n}(t_{1},\cdots,t_{n})=(s_{0},\cdots,s_{n})\)
124: と置く.\\
```

### R48 #9（第1章 191行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：smash product definition
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
A\vee B=\bigl(A\times\{b_0\}\bigr)\cup\bigl(\{a_0\}\times B\bigr)
\]
```

```text
188: 
189: 二つの基点付き空間 $(A,a_0)$ と $(B,b_0)$ の \emph{reduced join} を, 
190: $A\ \wedge\ B$ と書き, 積 $A\times B$ の部分集合
191: \[
192: A\vee B=\bigl(A\times\{b_0\}\bigr)\cup\bigl(\{a_0\}\times B\bigr)
193: \]
194: を, 一点につぶす (shrinking) ことにより得られる空間とする. 
195: 縮約写像 (shrinking map) を,
196: \[
```

### R48 #10（第1章 196行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：smash product definition
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
\shrink_{A,B}:A\times B\longrightarrow
A\times B/A\vee B = A\ \wedge\ B
\]
```

```text
193: \]
194: を, 一点につぶす (shrinking) ことにより得られる空間とする. 
195: 縮約写像 (shrinking map) を,
196: \[
197: \shrink_{A,B}:A\times B\longrightarrow
198: A\times B/A\vee B = A\ \wedge\ B
199: \]
200: で表す. 3つの空間 $A,B,C$ に対して, 次の自然な同相がある.
201: \[
```

### R48 #13（第1章 218行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：sphere smash identification
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
\shrink_{m,n}\bigl(\psi_m(x),\,\psi_n(y)\bigr)=\psi_{m+n}(x,y)
\]
```

```text
215: 
216: \end{equation}
217: と書く. $(x,y)\in I^m\times I^n=I^{m+n}$ に対して,
218: \[
219: \shrink_{m,n}\bigl(\psi_m(x),\,\psi_n(y)\bigr)=\psi_{m+n}(x,y)
220: \]
221: で定める.
222: さらに原本の球面の reduced join の同一視に関して, 次の関係が成り立つ.
223: \[
```

### R48 #14（第1章 223行）

- 判定案：`UNNUMBERED_ASSERTION_CANDIDATE`
- 帰属：smash identification associativity
- 理由：表示された数学的関係を主張候補として保持。ただし既存の番号付き命題内かは未確定。

```tex
\[
\shrink_{m+n,p}\bigl(\shrink_{m,n}(a,b),c\bigr)
=\shrink_{m,n+p}\bigl(a,\shrink_{n,p}(b,c)\bigr),
\quad (a,b,c)\in S^m\times S^n\times S^p.
\]
```

```text
220: \]
221: で定める.
222: さらに原本の球面の reduced join の同一視に関して, 次の関係が成り立つ.
223: \[
224: \shrink_{m+n,p}\bigl(\shrink_{m,n}(a,b),c\bigr)
225: =\shrink_{m,n+p}\bigl(a,\shrink_{n,p}(b,c)\bigr),
226: \quad (a,b,c)\in S^m\times S^n\times S^p.
227: \]
228: 写像
```

### R48 #16（第1章 234行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：smash product on maps
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
f\ \wedge \ g:\ A\ \wedge\ B\ \longrightarrow\ A'\ \wedge\ B'
\]
```

```text
231: \]
232: は基点を保存し, $f(a_0)=a'_0$, $g(b_0)=b'_0$ を満たすものとする.
233: このとき, reduced join
234: \[
235: f\ \wedge \ g:\ A\ \wedge\ B\ \longrightarrow\ A'\ \wedge\ B'
236: \]
237: を, 次により自然に定める.
238: \[
239: (f\wedge g)\circ \phi_{A,B} = \phi_{A',B'}\circ (f\times g).
```

### R48 #17（第1章 238行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：smash product on maps
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
(f\wedge g)\circ \phi_{A,B} = \phi_{A',B'}\circ (f\times g).
\]
```

```text
235: f\ \wedge \ g:\ A\ \wedge\ B\ \longrightarrow\ A'\ \wedge\ B'
236: \]
237: を, 次により自然に定める.
238: \[
239: (f\wedge g)\circ \phi_{A,B} = \phi_{A',B'}\circ (f\times g).
240: \]
241: 次が成り立つ：
242: \begin{equation}
243: 
```

### R48 #19（第1章 294行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：iterated suspension of a map
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
\Ex^n f:\ \Ex^n X\longrightarrow \Ex^n Y,\quad
(Ef = E^1 f)
\]
```

```text
291: \(E^n(E^m X) = E^{m+n} X\) を得る.
292: 
293: 写像 $f:X\to Y$ に対し, その $n$–重 suspension
294: \[
295: \Ex^n f:\ \Ex^n X\longrightarrow \Ex^n Y,\quad
296: (Ef = E^1 f)
297: \]
298: を, $f\ \wedge\ \id_{S^n}$ により定める. これにより,
299: \(
```

### R48 #28（第1章 404行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：loop space induced map
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
\Ox f:\ \Ox X\longrightarrow \Ox Y,\qquad
(\Ox f(\ell))(t)=f(\ell(t)),\ \ \ell\in\Ox X,\ t\in I
\]
```

```text
401: 
402: $\Ox Y=\{\ \ell:(I,\partial I)\to (Y,y_0)\ \}$ を, 
403: $Y$ の loop 空間とする. 写像 $f:X\to Y$ に対し,
404: \[
405: \Ox f:\ \Ox X\longrightarrow \Ox Y,\qquad
406: (\Ox f(\ell))(t)=f(\ell(t)),\ \ \ell\in\Ox X,\ t\in I
407: \]
408: で定める. もし, $f\simeq g$ なら, $\Ox f\simeq \Ox g$ であり, したがって,
409: \[
```

### R48 #29（第1章 409行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：loop space induced map
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
\Ox:\ [X,Y]\longrightarrow [\Ox X,\Ox Y],\qquad
\Omega [f] = [\Ox f]
\]
```

```text
406: (\Ox f(\ell))(t)=f(\ell(t)),\ \ \ell\in\Ox X,\ t\in I
407: \]
408: で定める. もし, $f\simeq g$ なら, $\Ox f\simeq \Ox g$ であり, したがって,
409: \[
410: \Ox:\ [X,Y]\longrightarrow [\Ox X,\Ox Y],\qquad
411: \Omega [f] = [\Ox f]
412: \]
413: が得られる. 明らかに, 
414: $\Ox(g\circ f)=\Ox g\circ \Ox f$, および,
```

### R48 #31（第1章 422行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：canonical inclusion
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
i(x)(t) = d_X(x,t)\qquad (t\in I).
\]
```

```text
419: 
420: $EX$ の loop 空間 $\Ox EX$ を考える. 各 $x\in X$ に対し,
421: \(EX\) の loop \(i(x)\) を次で定める.
422: \[
423: i(x)(t) = d_X(x,t)\qquad (t\in I).
424: \]
425: このとき, 次の包含写像が得られる.
426: \[
427: i:X\to \Ox EX.
```

### R48 #32（第1章 426行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：canonical inclusion
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
i:X\to \Ox EX.
\]
```

```text
423: i(x)(t) = d_X(x,t)\qquad (t\in I).
424: \]
425: このとき, 次の包含写像が得られる.
426: \[
427: i:X\to \Ox EX.
428: \]
429: これを, \emph{canonical injection} と呼ぶ. 
430: 任意の $f:X\to Y$ に対して, 次の図式は可換である：
431: \begin{equation}\label{eq:loop-susp-comm}
```

### R48 #33（第1章 446行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：loop-suspension adjunction
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
\Omega_0F=
\Ox F\circ i:\ X\xrightarrow{\ i\ }\Ox EX\xrightarrow{\ \Ox F\ }\Ox Y
\]
```

```text
443: \end{equation}
444: 
445: $F:EX\to Y$ に対して,
446: \[
447: \Omega_0F=
448: \Ox F\circ i:\ X\xrightarrow{\ i\ }\Ox EX\xrightarrow{\ \Ox F\ }\Ox Y
449: \]
450: と書く. これは
451: \[
```

### R48 #34（第1章 451行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：loop-suspension adjunction
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
\Omega_0F(x)(t) = F(d_X(x,t))
\]
```

```text
448: \Ox F\circ i:\ X\xrightarrow{\ i\ }\Ox EX\xrightarrow{\ \Ox F\ }\Ox Y
449: \]
450: と書く. これは
451: \[
452: \Omega_0F(x)(t) = F(d_X(x,t))
453: \]
454: で直接に与えられる. \\
455: 対応 $F\longmapsto \Omega_0F$ は,
456: $\map(EX,Y), \map(X,\Omega Y)$ のコンパクト部分集合
```

### R48 #37（第1章 514行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
A_0=a\circ \Ex^n b,\quad A_1(\Ex^n X)=z_0,\qquad
B_0=b\circ c,\quad B_1(W)=y_0.
\]
```

```text
511: B_t:(W,w_0)\to (Y,y_0),\qquad (0\le t\le 1)
512: \]
513: で, 次を満たすものが存在する. 
514: \[
515: A_0=a\circ \Ex^n b,\quad A_1(\Ex^n X)=z_0,\qquad
516: B_0=b\circ c,\quad B_1(W)=y_0.
517: \]
518: 写像 $H:\ (\Ex^{n+1}W,w_0)\to (Z,z_0)$ を, 次で定める. 
519: \begin{equation}\label{eq:H-def}
```

### R48 #42（第1章 585行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
F:(\Ex^{n+1}X,x_0)\to (Z,z_0), \quad
G:(\Ex W,w_0)\to (Y,y_0)
\]
```

```text
582: 別の null-homotopy $A'_t,\ B'_t$ を用いて定義されたものとする.
583: \newpage
584: 
585: \[
586: F:(\Ex^{n+1}X,x_0)\to (Z,z_0), \quad
587: G:(\Ex W,w_0)\to (Y,y_0)
588: \]
589: を, 次で定義する.
590: \[
```

### R48 #43（第1章 590行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
F(d_{E^{n}Z}(x,t))\equiv\left\{
\begin{array}{ll}
A_{2t-1}(x), & \frac{1}{2} \leq t \leq 1, \\
A'_{1-2t}(x), & 0 \leq t \leq \frac{1}{2}, \\
\end{array}\right.
\]
```

```text
587: G:(\Ex W,w_0)\to (Y,y_0)
588: \]
589: を, 次で定義する.
590: \[
591: F(d_{E^{n}Z}(x,t))\equiv\left\{
592: \begin{array}{ll}
593: A_{2t-1}(x), & \frac{1}{2} \leq t \leq 1, \\
594: A'_{1-2t}(x), & 0 \leq t \leq \frac{1}{2}, \\
595: \end{array}\right.
```

### R48 #55（第1章 787行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
d_{ER}(d_R(w,s),t) = \phi(w, \psi_2(s, t)).
\]
```

```text
784: \(E^2 R\) を定義する等化写像
785: \(\phi:R\times S^2\to R\wedge S^2 = E^2 R\)
786: に対して,
787: \[
788: d_{ER}(d_R(w,s),t) = \phi(w, \psi_2(s, t)).
789: \]
790: \(\sigma:E^{n+2}W\to E^{n+2}W\)
791: を, 次で与えられる同相写像とする.
792: \[
```

### R48 #62（第1章 871行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
H_{u}(d_{\Ex^{n}V}(s,t))\equiv\left\{
\begin{array}{ll}
A_{1-2t}(\Ex^{n}C_{2u(1-2t)}(s)), &
0\leq t \leq \frac{1}{2},\ 0\leq u \leq \frac{1}{2}, \\
A_{(2-2u)(1-2t)}(\Ex^{n}C_{1-2t}(s)), &
0\leq t \leq \frac{1}{2
```

```text
868: homotopy
869: \(H_{u}:(\Ex^{n+1}V,v_0) \longrightarrow (Z,z_0)\)
870: を, 次で定義する.
871: \[
872: H_{u}(d_{\Ex^{n}V}(s,t))\equiv\left\{
873: \begin{array}{ll}
874: A_{1-2t}(\Ex^{n}C_{2u(1-2t)}(s)), &
875: 0\leq t \leq \frac{1}{2},\ 0\leq u \leq \frac{1}{2}, \\
876: A_{(2-2u)(1-2t)}(\Ex^{n}C_{1-2t}(s)), &
```

### R48 #64（第1章 889行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
K(d_{V}(v, t)) = \left\{
\begin{array}{ll}
  B_{1-2t}(d(v)),
  & 0\leq t \leq \frac{1}{2},\\
  b(C_{2t-1}(v)), 
  & \frac{1}{2} \leq t \leq 1.  
\end{array}
\right.
\]
```

```text
886: \phi_{V,S^{n+1}}(v,\psi_{n+1}(1-t,t_{1},\cdots,t_{n})).
887: \]
888: また, 写像 \(K:EV\to Y\) を次で定義する.
889: \[
890: K(d_{V}(v, t)) = \left\{
891: \begin{array}{ll}
892:   B_{1-2t}(d(v)),
893:   & 0\leq t \leq \frac{1}{2},\\
894:   b(C_{2t-1}(v)), 
```

### R48 #75（第1章 1155行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
h\bigl(d_W(w,t)\bigr)=
\begin{cases}
d'_X(c(w),1-2t), & 0\le t\le \tfrac12,\\
B_{2t-1}(w), & \tfrac12\le t\le 1.
\end{cases}
\]
```

```text
1152: \(B_t\) を \(b\circ c\) の null-homotopy とする.\\
1153: $h:EW\to Y\cup_f CX$ を,
1154: 次で定める.
1155: \[
1156: h\bigl(d_W(w,t)\bigr)=
1157: \begin{cases}
1158: d'_X(c(w),1-2t), & 0\le t\le \tfrac12,\\
1159: B_{2t-1}(w), & \tfrac12\le t\le 1.
1160: \end{cases}
```

### R48 #77（第1章 1230行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
p(d'_W(w, t)) = d_W(w, t),\qquad
p(X) = x_0.
\]
```

```text
1227: p:X\cup_\gamma CW\to EW
1228: \end{equation}
1229: を, 次で与えらえる写像とする.
1230: \[
1231: p(d'_W(w, t)) = d_W(w, t),\qquad
1232: p(X) = x_0.
1233: \]
1234: このとき,
1235: \(p\) は \(X\) を一点につぶす写像であり, 次が成り立つ.
```

### R48 #95（第2章 98行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：reduced join definition
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
\alpha\ \redjoin\ \beta\ \in\ \pis{p+q}{S^{m+n}}
\]
```

```text
95: \]
96: が成り立つ. \\
97: $\alpha\in\pis{p}{S^m}$ と $\beta\in\pis{q}{S^n}$ の \emph{reduced join}
98: \[
99: \alpha\ \redjoin\ \beta\ \in\ \pis{p+q}{S^{m+n}}
100: \]
101: は, 第1章で導入した (1.3) の特別な写像 
102: $\phi_{p,q}$ と $\phi_{m,n}$ を用いて定義される. \\
103: 特に, $E^n$ の定義から次が成り立つ. 
```

### R48 #103（第2章 211行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：canonical embedding
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
i:\ (S^m)_\infty\longrightarrow\Omega S^{m+1}
\]
```

```text
208: \(t\) 個の loop $i(x_1),\ldots,i(x_t)$ の適切に重み付けした和で表される\\
209: \(S^{m+1}\) の loop を対応させる.
210: 得られる写像は単射であり, 
211: \[
212: i:\ (S^m)_\infty\longrightarrow\Omega S^{m+1}
213: \]
214: と書き, これも「標準 (canonical) 埋め込み」と呼ぶ. 
215: 
216: 次の図式は homotopy 的に可換である：
```

### R48 #106（第2章 292行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：James-Hopf map
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
h'_m:\ \bigl((S^m)_2, S^m\bigr)\ \to\ (S^{2m},e_0),
\]
```

```text
289: \end{equation}
290: 
291: 写像 \(h'_m\) を, 次で定める.
292: \[
293: h'_m:\ \bigl((S^m)_2, S^m\bigr)\ \to\ (S^{2m},e_0),
294: \]
295: \[
296: h'_m(xy)=\phi_{m,m}(x,y)\qquad(x,y\in S^m).
297: \]
```

### R48 #124（第2章 629行）

- 判定案：`UNNUMBERED_ASSERTION_CANDIDATE`
- 帰属：cohomology decomposition
- 理由：表示された数学的関係を主張候補として保持。ただし既存の番号付き命題内かは未確定。

```tex
\[
h^*H^*\!\bigl((S^{pm})_\infty;\Lambda\bigr)\ \otimes\ G\ \cong\
H^*\!\bigl((S^{m})_\infty;\Lambda\bigr)
\]
```

```text
626: 
627: \noindent
628: さらに, cup-product に関して,
629: \[
630: h^*H^*\!\bigl((S^{pm})_\infty;\Lambda\bigr)\ \otimes\ G\ \cong\
631: H^*\!\bigl((S^{m})_\infty;\Lambda\bigr)
632: \]
633: が成り立つ. ここで, $G\subset H^*\!\bigl((S^{m})_\infty;\Lambda\bigr)$ は,\\
634: 包含 $i:(S^m)_{p-1}\hookrightarrow(S^m)_\infty$ による制限
```

### R48 #127（第2章 661行）

- 判定案：`UNNUMBERED_ASSERTION_CANDIDATE`
- 帰属：Serre spectral sequence E2
- 理由：表示された数学的関係を主張候補として保持。ただし既存の番号付き命題内かは未確定。

```tex
\[
E_2^{*}\ \cong\ H^{*}\!\bigl((S^{pm})_\infty;\Lambda\bigr)
\ \otimes\ H^{*}(F;\Lambda).
\]
```

```text
658: と定義すると, $(X,p,(S^{pm})_\infty)$ は Serre の意味での fibration になる [13]. \\
659: この fibration に付随するスペクトル列 $\{E_r^{s,t}\}$ を考える. 
660: [13] の主定理により,
661: \[
662: E_2^{*}\ \cong\ H^{*}\!\bigl((S^{pm})_\infty;\Lambda\bigr)
663: \ \otimes\ H^{*}(F;\Lambda).
664: \]
665: 
666: $\ell(I)=h(x)$ となる constant path の組 $(\ell,x)$ は, 
```

### R48 #136（第2章 834行）

- 判定案：`UNNUMBERED_ASSERTION_CANDIDATE`
- 帰属：Whitehead theorem application
- 理由：表示された数学的関係を主張候補として保持。ただし既存の番号付き命題内かは未確定。

```tex
\[
i_{0*}:\ \pi_i\bigl((S^m)_{p-1}\bigr)\ \xrightarrow{}\ \pi_i(F)
\]
```

```text
831: \noindent
832: 一般化された Whitehead の定理 (Serre \cite{Serre1953b}) を, 
833: 包含 $i_0:(S^m)_{p-1}\hookrightarrow F$ に適用すると, 
834: \[
835: i_{0*}:\ \pi_i\bigl((S^m)_{p-1}\bigr)\ \xrightarrow{}\ \pi_i(F)
836: \]
837: は, $m$ が奇数, かつ $p=2$ のとき同型であり, 
838: $m$ が偶数のとき, $p$-primary 成分の同型である. \\
839: 対 \(((S^m)_\infty,(S^m)_{p-1})\) と \((X,F)\) に付随する
```

### R48 #137（第2章 843行）

- 判定案：`UNNUMBERED_ASSERTION_CANDIDATE`
- 帰属：five lemma application
- 理由：表示された数学的関係を主張候補として保持。ただし既存の番号付き命題内かは未確定。

```tex
\[
i_*:\ \pi_i\bigl((S^m)_\infty,(S^m)_{p-1}\bigr)\ \xrightarrow{\;\cong\;}\ \pi_i(X,F)
\]
```

```text
840: homotopy 群の完全列を, \\
841: homotopy 同値な包含写像 $(S^m)_\infty\hookrightarrow X$ 
842: により比較すると, five lemma から, 
843: \[
844: i_*:\ \pi_i\bigl((S^m)_\infty,(S^m)_{p-1}\bigr)\ \xrightarrow{\;\cong\;}\ \pi_i(X,F)
845: \]
846: は, $m$ が奇数, かつ $p=2$ のとき同型であり, 
847: $m$ が偶数のとき, $p$-primary 成分の同型である. \\
848: よって, 図式
```

### R48 #141（第2章 1005行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\begin{align*}
\Delta\alpha\circ\beta
& =\partial\,(h_{m*}^{-1}\Omega_1\alpha)\circ\beta
=\partial(h_{m*}^{-1}(\Omega_1\alpha)\circ \partial_0^{-1}\beta)\\
& \subset \partial(h_{m*}^{-1}(\Omega_1(\alpha)\circ E\beta)
```

```text
1002: \partial_0:\pi_j(CS^{i-1},S^{i-1})\rightarrow \pi_{j-1}(S^{i-1})
1003: \)
1004: は同型である. よって,
1005: \begin{align*}
1006: \Delta\alpha\circ\beta
1007: & =\partial\,(h_{m*}^{-1}\Omega_1\alpha)\circ\beta
1008: =\partial(h_{m*}^{-1}(\Omega_1\alpha)\circ \partial_0^{-1}\beta)\\
1009: & \subset \partial(h_{m*}^{-1}(\Omega_1(\alpha)\circ E\beta))
1010: =\partial(h_{m*}^{-1}(\Omega_1(\alpha\circ E^2\beta)))\\
```

### R48 #148（第2章 1289行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
H\todai[1]{E\alpha,E\beta,E\gamma}\ 
=\ -\,\Delta^{-1}(\alpha\circ\beta)\circ E^2\gamma
\]
```

```text
1286: && \text{by (2.11).}
1287: \end{align*}
1288: 以上より, 
1289: \[
1290: H\todai[1]{E\alpha,E\beta,E\gamma}\ 
1291: =\ -\,\Delta^{-1}(\alpha\circ\beta)\circ E^2\gamma
1292: \]
1293: が成り立つ. 
1294: \qed
```

### R48 #155（第3章 100行）

- 判定案：`UNNUMBERED_ASSERTION_CANDIDATE`
- 帰属：permutation sign of suspension
- 理由：表示された数学的関係を主張候補として保持。ただし既存の番号付き命題内かは未確定。

```tex
\[
\iota_n \wedge \alpha
= [\sigma_{p,n}] \circ (\alpha \wedge \iota_n) \circ [\sigma_{n,p+k}]
= (-1)^{pn}\iota_{p+n}\circ E^n\alpha\circ (-1)^{(p+k)n}\iota_{p+k+n}.
\]
```

```text
97: \(\sigma_{r,s}\) は, 
98: $\deg(\sigma_{r,s})=(-1)^{rs}$ の同相写像である. 
99: 次の関係式が成り立つ.
100: \[
101: \iota_n \wedge \alpha
102: = [\sigma_{p,n}] \circ (\alpha \wedge \iota_n) \circ [\sigma_{n,p+k}]
103: = (-1)^{pn}\iota_{p+n}\circ E^n\alpha\circ (-1)^{(p+k)n}\iota_{p+k+n}.
104: \]
105: (2.1) から,
```

### R48 #160（第3章 185行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
[\iota_{p+q-1}, \iota_{p+q-1}]\circ E^{2q-2}H(\alpha)\circ E^{p+k-1}H(\beta)
\]
```

```text
182: \begin{paracol}{2}
183: 
184: Prop2.5 により, 次が成り立つ. 
185: \[
186: [\iota_{p+q-1}, \iota_{p+q-1}]\circ E^{2q-2}H(\alpha)\circ E^{p+k-1}H(\beta)
187: \]
188: \[
189: \in \Delta(E^{2q}H(\alpha)\circ E^{p+k+1}H(\beta))
190: \subset\pi_{p+q+k+h-1}(S^{p+q-1}).
```

### R48 #174（第3章 371行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
C'_t\circ(1_{p+h} \wedge b \wedge 1_{r+\ell})
= (1_p \wedge \sigma_{r,q})\circ(C_t \wedge b)\circ (1_{p+h} \wedge \sigma_{q+k,r+\ell})
= (1_p \wedge b \wedge 1_r) \circ C''_t.
\]
```

```text
368: \]
369: の null-homotopy である. 
370: ここで, 次の関係式が成り立つ. 
371: \[
372: C'_t\circ(1_{p+h} \wedge b \wedge 1_{r+\ell})
373: = (1_p \wedge \sigma_{r,q})\circ(C_t \wedge b)\circ (1_{p+h} \wedge \sigma_{q+k,r+\ell})
374: = (1_p \wedge b \wedge 1_r) \circ C''_t.
375: \]
376: \[
```

### R48 #182（第3章 404行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\begin{aligned}
\toda{\alpha\wedge\iota_{q+r},\ \iota_{p+h}\wedge\beta\wedge\iota_r,\ \iota_{p+h+q+k}\wedge\gamma}
& = (-1)^{\delta+h\ell}\toda{E^{q+r}\alpha,\ E^{p+h+r}\beta,\ E^{p+h+q+k}\gamma},\\
\toda{\iota_{p
```

```text
401: \]
402: と定義する.
403: このとき, $H,H',H''$ はそれぞれ, 次の Toda brackt の元を表す：
404: \[
405: \begin{aligned}
406: \toda{\alpha\wedge\iota_{q+r},\ \iota_{p+h}\wedge\beta\wedge\iota_r,\ \iota_{p+h+q+k}\wedge\gamma}
407: & = (-1)^{\delta+h\ell}\toda{E^{q+r}\alpha,\ E^{p+h+r}\beta,\ E^{p+h+q+k}\gamma},\\
408: \toda{\iota_{p+q}\wedge\gamma,\ \alpha\wedge\iota_{q+h+r+\ell},\ \iota_{p+h}\wedge\beta\wedge\iota_{r+\ell}}
409: & = (-1)^{\delta+ \ell k}\toda{E^{p+q}\gamma,\ E^{q+r+\ell}\beta,\ E^{q+h+r+\ell}\alpha},\\
```

### R48 #187（第3章 460行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：mapping cone K
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
d':S^{n+k}\times I\ \xrightarrow{d'}\ CS^{n+k}\ \rightarrow\ K
\]
```

```text
457: d'_{n+k}:S^{n+k}\times I\longrightarrow CS^{n+k}
458: \]
459: とし, 合成を
460: \[
461: d':S^{n+k}\times I\ \xrightarrow{d'}\ CS^{n+k}\ \rightarrow\ K
462: \]
463: と書く. 写像 $p:K\to S^{n+k+1}$ を, 次で定める.
464: \[
465: p\bigl(d'_{n+k}(x,t)\bigr)=d_{n+k}(x,t),\qquad 
```

### R48 #188（第3章 464行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：mapping cone quotient
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
p\bigl(d'_{n+k}(x,t)\bigr)=d_{n+k}(x,t),\qquad 
p(S^n) = e_0.
\]
```

```text
461: d':S^{n+k}\times I\ \xrightarrow{d'}\ CS^{n+k}\ \rightarrow\ K
462: \]
463: と書く. 写像 $p:K\to S^{n+k+1}$ を, 次で定める.
464: \[
465: p\bigl(d'_{n+k}(x,t)\bigr)=d_{n+k}(x,t),\qquad 
466: p(S^n) = e_0.
467: \]
468: 
469: このとき, $p$ は $K$ に含まれる $S^n$ を一点につぶす写像である.
```

### R48 #193（第3章 495行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
G_1\;=\;F\circ \Ex^{n}p
\]
```

```text
492: F:\ S^{2n+2k+1}\ \longrightarrow\ \Ex^{n}K
493: \]
494: が存在して,
495: \[
496: G_1\;=\;F\circ \Ex^{n}p
497: \]
498: が成り立つ. このような $F$ の類について次を得る. 
499: 
500: \switchcolumn
```

### R48 #196（第3章 618行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
G_s\bigl(\theta_{n+k,n}(x,y)\bigr)=
\begin{cases}
A_{2s}\!\bigl(\phi_{n+k,n}(x,y)\bigr), & 0\le s\le \tfrac12,\\[2pt]
\phi_{n}\!\bigl(d'(x,2s-1),\,\tau(y)\bigr), & \tfrac12\le s\le1.
\end{cases}
\]
```

```text
615: \(G_s:\ \Ex^{n+k}K\ \longrightarrow\ \Ex^{n}K\)
616: を, 次の式で定める. \\
617: $S^{2n+k}$ の点 $\phi_{n+k,n}(x,y)$ に対して,
618: \[
619: G_s\bigl(\theta_{n+k,n}(x,y)\bigr)=
620: \begin{cases}
621: A_{2s}\!\bigl(\phi_{n+k,n}(x,y)\bigr), & 0\le s\le \tfrac12,\\[2pt]
622: \phi_{n}\!\bigl(d'(x,2s-1),\,\tau(y)\bigr), & \tfrac12\le s\le1.
623: \end{cases}
```

### R48 #207（第3章 703行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：proof-local self-homeomorphism
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
\sigma(\psi(x_1,\ldots,x_{n+k}, t, y_1,\ldots,y_n))
= \psi(x_1,\ldots, x_n, t, x_{n+1},\ldots,x_{n+k} y_1,\ldots,y_n)
\]
```

```text
700: \]
701: また, degree \((-1)^k\) の自己同相写像 
702: \(\sigma:S^{2n+k+1}\to S^{2n+k+1}\) を, \\
703: \[
704: \sigma(\psi(x_1,\ldots,x_{n+k}, t, y_1,\ldots,y_n))
705: = \psi(x_1,\ldots, x_n, t, x_{n+1},\ldots,x_{n+k} y_1,\ldots,y_n)
706: \]
707: で与えるとき, $H_2$ に対して次が成り立つことが, 直接的に確かめられる.
708: \[
```

### R48 #208（第3章 708行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
[H_2] = (\iota_{n+k+1} \wedge (-1)^{kn} \iota_n) \circ (-1)^{k}\iota_{2n+k+1}
\circ (E\alpha \wedge \iota_{n+k})
 = (-1)^{kn+k}E^{n+k+1}\alpha .
\]
```

```text
705: = \psi(x_1,\ldots, x_n, t, x_{n+1},\ldots,x_{n+k} y_1,\ldots,y_n)
706: \]
707: で与えるとき, $H_2$ に対して次が成り立つことが, 直接的に確かめられる.
708: \[
709: [H_2] = (\iota_{n+k+1} \wedge (-1)^{kn} \iota_n) \circ (-1)^{k}\iota_{2n+k+1}
710: \circ (E\alpha \wedge \iota_{n+k})
711:  = (-1)^{kn+k}E^{n+k+1}\alpha .
712: \]
713: よって, 
```

### R48 #212（第3章 727行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
(\Ex^{n}p)_*\bigl(\,[F]\ -\ (-1)^{kn}\Ex^{h}\gamma\,\bigr) = 0 .
\]
```

```text
724: =\Ex^{h}\!\bigl((\Ex^{n-h}p)_*\gamma\bigr)
725: =\bigl(1-(-1)^k\bigr)\,\Ex^{n+k+1}\alpha,
726: \]
727: \[
728: (\Ex^{n}p)_*\bigl(\,[F]\ -\ (-1)^{kn}\Ex^{h}\gamma\,\bigr) = 0 .
729: \]
730: 仮定 $k\le 2n-2$ から, 
731: $2n+2k+1\le (2n+k)+(2n-1)$ が成り立つ. \\
732: 対 $(\Ex^{n}K, S^{2n})$ は, $(2n+k)$-connected であり, 
```

### R48 #213（第3章 735行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
(\Ex^{n}p)_*\ :\ 
\pi_{2n+2k+1}\bigl(\Ex^{n}K,S^{2n}\bigr)\
\longrightarrow\
\pi_{2n+k+1}\bigl(S^{2n+k+1}\bigr).
\]
```

```text
732: 対 $(\Ex^{n}K, S^{2n})$ は, $(2n+k)$-connected であり, 
733: $S^{2n}$ は $(2n-1)$-connected である. \\
734: したがって, \cite{BlakersMassey1952} Theorem2 より, 次の誘導準同型は同型である.
735: \[
736: (\Ex^{n}p)_*\ :\ 
737: \pi_{2n+2k+1}\bigl(\Ex^{n}K,S^{2n}\bigr)\
738: \longrightarrow\
739: \pi_{2n+k+1}\bigl(S^{2n+k+1}\bigr).
740: \]
```

### R48 #217（第3章 852行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
p'=\sigma\circ \Ex^{t}p
\]
```

```text
849: により与えられる, 次数 \((-1)^{t}\) の自己同相写像
850: $\sigma:S^{n+k+t+1}\to S^{n+k+t+1}$
851: に対して, 
852: \[
853: p'=\sigma\circ \Ex^{t}p
854: \]
855: が成り立つ. 
856: 次に, reduced join 
857: \[
```

### R48 #232（第3章 1086行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\Ex\beta\circ t\eta_{m+k+1}
\ \in\ \todai[1]{\,r\iota_{m+1},\ \Ex\beta,\ r\iota_{m+k+1}\,}.
\]
```

```text
1083: (\cite{Toda1952}, Chapter VIII 例2 を見よ. )\\
1084: Th3.6 において, $\alpha=r\,\iota_{m+1}$ と置くと, 
1085: ある \(r\) のみによって決まる整数 $t=t(r)$ が存在し, 
1086: \[
1087: \Ex\beta\circ t\eta_{m+k+1}
1088: \ \in\ \todai[1]{\,r\iota_{m+1},\ \Ex\beta,\ r\iota_{m+k+1}\,}.
1089: \]
1090: $r$ が奇数のとき, 
1091: \[
```

### R48 #235（第3章 1107行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
s^2(\eta_n\circ\eta_{n+1})
\in s\iota_n\circ\toda{2\iota_n, \eta_n, 2\iota_{n+1}}\circ s\iota_{n+2}
\subset \toda{r\iota_n, \eta_n, r\iota_{n+1}} .
\]
```

```text
1104: 
1105: 次に, $r$ を偶数とし, $r=2s$ と置く. 
1106: Prop1.2 により, 
1107: \[
1108: s^2(\eta_n\circ\eta_{n+1})
1109: \in s\iota_n\circ\toda{2\iota_n, \eta_n, 2\iota_{n+1}}\circ s\iota_{n+2}
1110: \subset \toda{r\iota_n, \eta_n, r\iota_{n+1}} .
1111: \]
1112: また, 
```

### R48 #258（第4章 461行）

- 判定案：`DEPENDENCY_CONTEXT_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：周辺の定義・前提・同一視の文脈。隣接した Reference と一体で再確認。

```tex
\[
i\cdot\Omega h: S^{n-1}\times\Ox S^{2n-1}\to\Ox S^n
\]
```

```text
458: が, 任意の \(i\) で同型になることが知られている \cite{Steenrod1951}.\\
459: これは, $h$ を Hopf 不変量 $\pm1$ を持つ写像に置き換えても成り立つ. \\
460: なぜなら, これらの同型は, 次の写像
461: \[
462: i\cdot\Omega h: S^{n-1}\times\Ox S^{2n-1}\to\Ox S^n
463: \]
464: によって誘導されるからである. 
465: ここで, "\(\cdot\)" は \(\Omega S^n\) の道の積を表す. \\
466: この写像は, コホモロジーの同型を誘導するので,ホモロジーとホモトピーの同型を誘導する. \\
```

### R48 #2（第1章 112行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：Chapter 1 sphere parametrization
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
\psi_1(t) = (\cos 2\pi t,\ \sin 2\pi t).
\]
```

```text
109:   \psi_n \text{ は, } I^n - \partial I^n \text{ を }
110:   S^n - e_0 \text{ の上に同相に写す.}
111: \end{equation}
112: \[
113: \psi_1(t) = (\cos 2\pi t,\ \sin 2\pi t).
114: \]
115: \(i:S^{n}\hookrightarrow S^{n+1}\)
116: を,
117: \(i(s_{0},\cdots,s_{n}) := (s_{0},\cdots,s_{n},0)\)
```

### R48 #6（第1章 176行）

- 判定案：`DEPENDENCY_CONTEXT_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：周辺の定義・前提・同一視の文脈。隣接した Reference と一体で再確認。

```tex
\[
f^*(\beta)=[g\circ f],\qquad g_*(\alpha)=[g\circ f]
\]
```

```text
173: \[
174: f^*:[Y,Z]\to[X,Z],\quad g_*:[X,Y]\to[X,Z].
175: \]
176: \[
177: f^*(\beta)=[g\circ f],\qquad g_*(\alpha)=[g\circ f]
178: \]
179: 明らかに, 合成は結合的である. 
180: \[
181: (\gamma\circ \beta)\circ\alpha=\gamma\circ(\beta\circ\alpha).
```

### R48 #12（第1章 204行）

- 判定案：`DEPENDENCY_CONTEXT_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：周辺の定義・前提・同一視の文脈。隣接した Reference と一体で再確認。

```tex
\[
\phi_{A\wedge B, C}(\phi_{A,B}(a,b),c)\longleftrightarrow
\phi_{A,B\wedge C}(a, \phi_{B,C}(b,c)).
\]
```

```text
201: \[
202: (A\ \wedge\ B)\ \wedge\ C\ \cong\ A\ \wedge\ (B\ \wedge\ C),
203: \]
204: \[
205: \phi_{A\wedge B, C}(\phi_{A,B}(a,b),c)\longleftrightarrow
206: \phi_{A,B\wedge C}(a, \phi_{B,C}(b,c)).
207: \]
208: これにより, $A\ \wedge\ B\ \wedge\ C$ と略記する. 
209: 
```

### R48 #15（第1章 229行）

- 判定案：`DEPENDENCY_CONTEXT_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：周辺の定義・前提・同一視の文脈。隣接した Reference と一体で再確認。

```tex
\[
f:A\to A',\quad g:B\to B'
\]
```

```text
226: \quad (a,b,c)\in S^m\times S^n\times S^p.
227: \]
228: 写像
229: \[
230: f:A\to A',\quad g:B\to B'
231: \]
232: は基点を保存し, $f(a_0)=a'_0$, $g(b_0)=b'_0$ を満たすものとする.
233: このとき, reduced join
234: \[
```

### R48 #20（第1章 325行）

- 判定案：`DEPENDENCY_CONTEXT_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：周辺の定義・前提・同一視の文脈。隣接した Reference と一体で再確認。

```tex
\[
d_X:X\times I \to EX,\qquad
d_X = \phi_{X,S^1}\circ (1_X\times \psi_1).
\]
```

```text
322: 
323: また, \(X\) の suspension \(EX\) は, 
324: 次の写像によっても定義される.
325: \[
326: d_X:X\times I \to EX,\qquad
327: d_X = \phi_{X,S^1}\circ (1_X\times \psi_1).
328: \]
329: ここで, \(1_X\) は \(X\) の恒等写像である.\\
330: \(d_X\) は, \(X\times \partial{I} \cup x_0 \times I\)
```

### R48 #26（第1章 375行）

- 判定案：`UNNUMBERED_ASSERTION_CANDIDATE`
- 帰属：homomorphism property of composition
- 理由：表示された数学的関係を主張候補として保持。ただし既存の番号付き命題内かは未確定。

```tex
\[
[f]\circ(\alpha + \alpha') = [f]\circ\alpha + [f]\circ\alpha',
\]
```

```text
372: (Eg)^*:[EX,Y]\longrightarrow[EW,Y].
373: \end{equation}
374: すなわち,
375: \[
376: [f]\circ(\alpha + \alpha') = [f]\circ\alpha + [f]\circ\alpha',
377: \]
378: \[
379: (\alpha + \alpha')\circ E[g] = \alpha\circ E[g] + \alpha'\circ E[g].
380: \]
```

### R48 #27（第1章 378行）

- 判定案：`UNNUMBERED_ASSERTION_CANDIDATE`
- 帰属：homomorphism property of composition
- 理由：表示された数学的関係を主張候補として保持。ただし既存の番号付き命題内かは未確定。

```tex
\[
(\alpha + \alpha')\circ E[g] = \alpha\circ E[g] + \alpha'\circ E[g].
\]
```

```text
375: \[
376: [f]\circ(\alpha + \alpha') = [f]\circ\alpha + [f]\circ\alpha',
377: \]
378: \[
379: (\alpha + \alpha')\circ E[g] = \alpha\circ E[g] + \alpha'\circ E[g].
380: \]
381: 特に, $n\ge 2$ のとき,
382: \([\Ex^n X,Y]\) はアーベル群である.
383: 
```

### R48 #35（第1章 502行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
a:(\Ex^n Y,y_0)\to (Z,z_0),\quad
b:(X,x_0)\to (Y,y_0),\quad
c:(W,w_0)\to (X,x_0)
\]
```

```text
499: \alpha\circ \Ex^n\beta=0,\qquad \beta\circ \gamma=0
500: \end{equation}
501: を満たすものとする. 代表写像を, それぞれ,
502: \[
503: a:(\Ex^n Y,y_0)\to (Z,z_0),\quad
504: b:(X,x_0)\to (Y,y_0),\quad
505: c:(W,w_0)\to (X,x_0)
506: \]
507: とする. 
```

### R48 #36（第1章 509行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
A_t:(\Ex^n X,x_0)\to (Z,z_0),\qquad
B_t:(W,w_0)\to (Y,y_0),\qquad (0\le t\le 1)
\]
```

```text
506: \]
507: とする. 
508: このとき, (1.13) の仮定から, それぞれの null homotopy
509: \[
510: A_t:(\Ex^n X,x_0)\to (Z,z_0),\qquad
511: B_t:(W,w_0)\to (Y,y_0),\qquad (0\le t\le 1)
512: \]
513: で, 次を満たすものが存在する. 
514: \[
```

### R48 #44（第1章 597行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
G(d_{W}(w,t))\equiv\left\{
\begin{array}{ll}
B'_{2t-1}(w), & \frac{1}{2} \leq t \leq 1, \\
B_{1-2t}(w), & 0 \leq t \leq \frac{1}{2}. \\
\end{array}\right.
\]
```

```text
594: A'_{1-2t}(x), & 0 \leq t \leq \frac{1}{2}, \\
595: \end{array}\right.
596: \]
597: \[
598: G(d_{W}(w,t))\equiv\left\{
599: \begin{array}{ll}
600: B'_{2t-1}(w), & \frac{1}{2} \leq t \leq 1, \\
601: B_{1-2t}(w), & 0 \leq t \leq \frac{1}{2}. \\
602: \end{array}\right.
```

### R48 #46（第1章 613行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
\sigma\bigl(\phi(w,\psi_{n+1}(t_1,\ldots,t_n,t))\bigr)=\phi(w, \psi_{n+1}(t, t_1,\ldots,t_n))
\]
```

```text
610: が確かめられる. 
611: ここで, 
612: $\sigma:\Ex^{n+1}W=W\ \wedge\ S^{n+1}\to \Ex^{n+1}W$ は,
613: \[
614: \sigma\bigl(\phi(w,\psi_{n+1}(t_1,\ldots,t_n,t))\bigr)=\phi(w, \psi_{n+1}(t, t_1,\ldots,t_n))
615: \]
616: で与えられる自己同相である. 対応
617: \[
618: \psi_{n+1}(t_1,\cdots,t_n, t) \longleftrightarrow
```

### R48 #47（第1章 617行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
\psi_{n+1}(t_1,\cdots,t_n, t) \longleftrightarrow
\psi_{n+1}(t,t_1,\cdots,t_n)
\]
```

```text
614: \sigma\bigl(\phi(w,\psi_{n+1}(t_1,\ldots,t_n,t))\bigr)=\phi(w, \psi_{n+1}(t, t_1,\ldots,t_n))
615: \]
616: で与えられる自己同相である. 対応
617: \[
618: \psi_{n+1}(t_1,\cdots,t_n, t) \longleftrightarrow
619: \psi_{n+1}(t,t_1,\cdots,t_n)
620: \]
621: は, $S^{n}$ 上の次数 $(-1)^n$ の同相写像なので,
622: \(\sigma\) は,
```

### R48 #49（第1章 635行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
F':(E^{n+1}X,x_0)\to(Z,z_0),\qquad
G':(EW, w_0)\to (Y,y_0)
\]
```

```text
632: 同じ double coset に属する. \\
633: 逆に, \([H]\) と同じ double coset に属する \([E^{n+1}W,Z]\) の任意の元は,
634: ある写像
635: \[
636: F':(E^{n+1}X,x_0)\to(Z,z_0),\qquad
637: G':(EW, w_0)\to (Y,y_0)
638: \]
639: によって, 次の写像で表される.
640: \[
```

### R48 #50（第1章 640行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
F'\circ E^{n+1}c + (H + a\circ E^n G'\circ \sigma).
\]
```

```text
637: G':(EW, w_0)\to (Y,y_0)
638: \]
639: によって, 次の写像で表される.
640: \[
641: F'\circ E^{n+1}c + (H + a\circ E^n G'\circ \sigma).
642: \]
643: ここで,
644: \[
645: A'_t(x)=
```

### R48 #51（第1章 644行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
A'_t(x)=
\begin{cases}
F'(d_{E^n X}(x,2-2t)),& \tfrac12\le t\le 1,\\
A_{2t}(x),& 0\le t\le \tfrac12,
\end{cases}
\qquad
B'_t(w)=
\begin{cases}
G'(d_W(w,2t-1)),& \tfrac12\le t\le 1,\\
B_{2t}(w),& 0\le t\le \t
```

```text
641: F'\circ E^{n+1}c + (H + a\circ E^n G'\circ \sigma).
642: \]
643: ここで,
644: \[
645: A'_t(x)=
646: \begin{cases}
647: F'(d_{E^n X}(x,2-2t)),& \tfrac12\le t\le 1,\\
648: A_{2t}(x),& 0\le t\le \tfrac12,
649: \end{cases}
```

### R48 #53（第1章 768行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
H(d_{ER}(d_R(w,s),t))=
\begin{cases}
a(\Ex^{n+1}B_{2t-1}(d_R(w,s))), 
& \tfrac12\le t\le 1,\\[2mm]
A_{1-2t}(\Ex^{n+1}c(d_R(w,s))), 
& 0\le t\le \tfrac12,
\end{cases}
\]
```

```text
765: \(\todai[n+1]{\alpha, E^{n+1}\beta, E^{n+1}\gamma}\) 
766: の任意の元は, 次の写像 \(H:E^{n+2}W\to Z\)
767: で表される.
768: \[
769: H(d_{ER}(d_R(w,s),t))=
770: \begin{cases}
771: a(\Ex^{n+1}B_{2t-1}(d_R(w,s))), 
772: & \tfrac12\le t\le 1,\\[2mm]
773: A_{1-2t}(\Ex^{n+1}c(d_R(w,s))), 
```

### R48 #56（第1章 792行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
\sigma(d_{ER}(d_R(w,s),t))
= d_{ER}(d_R(w,t), s).
\]
```

```text
789: \]
790: \(\sigma:E^{n+2}W\to E^{n+2}W\)
791: を, 次で与えられる同相写像とする.
792: \[
793: \sigma(d_{ER}(d_R(w,s),t))
794: = d_{ER}(d_R(w,t), s).
795: \]
796: このとき, Lem1.1の証明で見たように,
797: \([H\circ \sigma] = -[H]\) である.\\
```

### R48 #57（第1章 799行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
\Omega_0(H\circ \sigma)(d_R(w,t))=
\begin{cases}
\Omega_0 a(\Ex^{n}B_{2t-1}(w)), 
& \tfrac12\le t\le 1,\\[2mm]
\Omega_0 A_{1-2t}(\Ex^{n}c(w)), 
& 0\le t\le \tfrac12.
\end{cases}
\]
```

```text
796: このとき, Lem1.1の証明で見たように,
797: \([H\circ \sigma] = -[H]\) である.\\
798: (1.12) と \(\Omega_0\) の定義により,
799: \[
800: \Omega_0(H\circ \sigma)(d_R(w,t))=
801: \begin{cases}
802: \Omega_0 a(\Ex^{n}B_{2t-1}(w)), 
803: & \tfrac12\le t\le 1,\\[2mm]
804: \Omega_0 A_{1-2t}(\Ex^{n}c(w)), 
```

### R48 #61（第1章 854行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
H(d_{E^n V}(s, t)) = \left\{
\begin{array}{ll}
  A_{1-2t}(E^n c(E^n d(s))),
  & 0\leq t \leq \frac{1}{2},\\
  a(E^n B_{2t-1}(E^n d(s))), 
  & \frac{1}{2} \leq t \leq 1.  
\end{array}
\right.
\]
```

```text
851: のnull homotopyとする.\\
852: このとき, 
853: \(H:E^{n+1}V\to Z\) を 
854: \[
855: H(d_{E^n V}(s, t)) = \left\{
856: \begin{array}{ll}
857:   A_{1-2t}(E^n c(E^n d(s))),
858:   & 0\leq t \leq \frac{1}{2},\\
859:   a(E^n B_{2t-1}(E^n d(s))), 
```

### R48 #71（第1章 1071行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
[H] + [H'] = [H''] \in 
\todai[n]{\alpha + \alpha', E^n\beta, E^n\gamma}
\]
```

```text
1068: \(a+a',\ b,\ c\) と, homotopy \(A_t + A'_t,\ B_t\) 
1069: から, (1.14) により構成されることが, 直接的に確かめられる.\\
1070: したがって,
1071: \[
1072: [H] + [H'] = [H''] \in 
1073: \todai[n]{\alpha + \alpha', E^n\beta, E^n\gamma}
1074: \]
1075: であり, 
1076: \([H'']\) は求める共通元である.
```

### R48 #74（第1章 1130行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
\phi(d'_X(x,t),\psi_n(t_1,\ldots,t_n))\longleftrightarrow d'_Z(\phi'(x,\psi_n(t_1,\ldots,t_n)),t)
\]
```

```text
1127: \Ex^nY\ \cup_{\beta'}\ C\Ex^n X,\quad \beta'=\Ex^n \beta.
1128: \end{equation}
1129: ここで, 対応は
1130: \[
1131: \phi(d'_X(x,t),\psi_n(t_1,\ldots,t_n))\longleftrightarrow d'_Z(\phi'(x,\psi_n(t_1,\ldots,t_n)),t)
1132: \]
1133: により与えられ, $Z=\Ex^n X$ であり, \\
1134: $\phi, \ \phi'$ は, それぞれ, 
1135: $\Ex^n(Y\cup_\beta CX)=(Y\cup_\beta CX)\wedge S^n$ と,
```

### R48 #76（第1章 1201行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
H_s\bigl(d(w,t)\bigr)=
\begin{cases}
d'_V\!\left(E^nB_{s(1-2t)}(w),\ (1-s)(1-2t)\right), & 0\le t\le \tfrac12,\\
A_{2t-1}\!\left(E^n c(w)\right), & \tfrac12\le t\le 1.
\end{cases}
\]
```

```text
1198: 次の式で与えられる homotopy  
1199: \(H_s:(E^{n+1}W,w_0)\to (Z\cup_\alpha CE^n Y, z_0)\)
1200: を考える.
1201: \[
1202: H_s\bigl(d(w,t)\bigr)=
1203: \begin{cases}
1204: d'_V\!\left(E^nB_{s(1-2t)}(w),\ (1-s)(1-2t)\right), & 0\le t\le \tfrac12,\\
1205: A_{2t-1}\!\left(E^n c(w)\right), & \tfrac12\le t\le 1.
1206: \end{cases}
```

### R48 #78（第1章 1273行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
\begin{cases}
  G(x) = a(E^n b(x)), & x \in E^n X,\\
  G(d'_V(w, t)) = a(E^n B_t(w)), & w \in E^n W = V,\ t \in I.
\end{cases}
\]
```

```text
1270: \(\alpha\circ E^n\overline{\beta}\) を表す写像 
1271: \(G:E^n(X\cup_\gamma CW)\to Z\) は,
1272: 次の形で与えられる.
1273: \[
1274: \begin{cases}
1275:   G(x) = a(E^n b(x)), & x \in E^n X,\\
1276:   G(d'_V(w, t)) = a(E^n B_t(w)), & w \in E^n W = V,\ t \in I.
1277: \end{cases}
1278: \]
```

### R48 #79（第1章 1287行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
G_0 = G,\qquad 
G_1(E^n X) = z_0.
\]
```

```text
1284: homotopy extension theorem により, 
1285: homotopy \(G_s:E^n(X\cup_\gamma CW) \to Z\)
1286: が存在し, 次を満たす.
1287: \[
1288: G_0 = G,\qquad 
1289: G_1(E^n X) = z_0.
1290: \]
1291: このとき,
1292: \(H_1\circ E^n p = G_1\) を満たす写像 
```

### R48 #80（第1章 1307行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
H_s\bigl(d_V(w,t)\bigr)=
\begin{cases}
A_{1-2t}\!\left(E^n c(w)\right), 
& 0\le t\le \dfrac{1-s}{2},\\
G_s\!\left(d'_V\!\left(w,\dfrac{2t-1+s}{1+s}\right)\right), 
& \dfrac{1-s}{2}\le t\le 1.
\end{cases}
\]
```

```text
1304: \(A_t\) は \(a\circ E^n b\) の null-homotopy である.\\
1305: 次で与えられる homotopy 
1306: $H_s:E^{n+1}W\to Z$ を考える.
1307: \[
1308: H_s\bigl(d_V(w,t)\bigr)=
1309: \begin{cases}
1310: A_{1-2t}\!\left(E^n c(w)\right), 
1311: & 0\le t\le \dfrac{1-s}{2},\\
1312: G_s\!\left(d'_V\!\left(w,\dfrac{2t-1+s}{1+s}\right)\right), 
```

### R48 #93（第2章 73行）

- 判定案：`DEPENDENCY_CONTEXT_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：周辺の定義・前提・同一視の文脈。隣接した Reference と一体で再確認。

```tex
\[
\pis{p}{S^m} \quad(=\hs{S^p}{S^m})
\]
```

```text
70: \begin{paracol}{2}
71: 
72: 以下では, 球面の homotopy 群
73: \[
74: \pis{p}{S^m} \quad(=\hs{S^p}{S^m})
75: \]
76: について考察を進める. \\
77: $\iota_n\in\pis{n}{S^n}$ を $S^n$ の恒等写像の homotopy クラスとする. \\
78: 明らかに, 
```

### R48 #97（第2章 108行）

- 判定案：`DEPENDENCY_CONTEXT_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：周辺の定義・前提・同一視の文脈。隣接した Reference と一体で再確認。

```tex
\[
\todai[n]{\alpha,\ E^n\beta,\ E^n\gamma}
\in\pi_{i+n+1}(S^m) / 
(\alpha\circ E^n\pi_{i+1}(S^k) + \pi_{j+n+1}(S^m)\circ E^{n+1}\gamma)
\]
```

```text
105: E^n\alpha=\alpha\ \redjoin\ \iota_n
106: \]
107: また \emph{secondary composition}
108: \[
109: \todai[n]{\alpha,\ E^n\beta,\ E^n\gamma}
110: \in\pi_{i+n+1}(S^m) / 
111: (\alpha\circ E^n\pi_{i+1}(S^k) + \pi_{j+n+1}(S^m)\circ E^{n+1}\gamma)
112: \]
113: は, 
```

### R48 #98（第2章 114行）

- 判定案：`DEPENDENCY_CONTEXT_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：周辺の定義・前提・同一視の文脈。隣接した Reference と一体で再確認。

```tex
\[
\alpha\in\pis{k+n}{S^m},\qquad
\beta\in\pis{j}{S^k},\qquad
\gamma\in\pis{i}{S^j}
\]
```

```text
111: (\alpha\circ E^n\pi_{i+1}(S^k) + \pi_{j+n+1}(S^m)\circ E^{n+1}\gamma)
112: \]
113: は, 
114: \[
115: \alpha\in\pis{k+n}{S^m},\qquad
116: \beta\in\pis{j}{S^k},\qquad
117: \gamma\in\pis{i}{S^j}
118: \]
119: が, (1.13) の条件が満たされるときに定義される. \\
```

### R48 #100（第2章 183行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
S^m\times\cdots\times S^m \ \longrightarrow\ (S^m)_t,\qquad
(x_1,\ldots,x_t)\ \longmapsto\ x_1\cdots x_t
\]
```

```text
180: $(S^m)_t$ の位相は,
181: 積空間 $S^m\times\cdots\times S^m$ ($t$ 回) 
182: からの等化写像
183: \[
184: S^m\times\cdots\times S^m \ \longrightarrow\ (S^m)_t,\qquad
185: (x_1,\ldots,x_t)\ \longmapsto\ x_1\cdots x_t
186: \]
187: のもとで与える. 
188: $(S^m)_t-(S^m)_{t-1}$ は開な $tm$-cell になる .\\ 
```

### R48 #101（第2章 194行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
(f)_t:\ (S^q)_t\longrightarrow(S^m)_t,\qquad (t=1,2,\ldots,\infty)
\]
```

```text
191: 自然な方法で $(S^m)_1$ を $S^m$ と同一視する. 
192: 
193: $f:(S^q,e_0)\to(S^m,e_0)$ に対して, 写像
194: \[
195: (f)_t:\ (S^q)_t\longrightarrow(S^m)_t,\qquad (t=1,2,\ldots,\infty)
196: \]
197: を
198: \[
199: (f)_t(y_1\ldots y_t):=f(y_1)\ldots f(y_t)
```

### R48 #162（第3章 244行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
H(d_s(x,t))=
\begin{cases}
\bigl(a \wedge i_{q+r}\bigr)\bigl(1_{p+h} \wedge B_{2t-1}\bigr)(x), & \tfrac12\le t\le1,\\[2pt]
\bigl(A_{1-2t} \wedge 1_r\bigr)\bigl(1_{p+h+q+k} \wedge c\bigr)(x), & 0\le t\le\tfrac12,\\
```

```text
241: $A_t$, $B_t$ とする. \\
242: また, $S^n$ の恒等写像を $i_n$ と記す. \\
243: $H,\ H':S^{s+1}\to S^{p+q+r}$ ($s=p+h+q+k+r+\ell$) を, 次で与える：
244: \[
245: H(d_s(x,t))=
246: \begin{cases}
247: \bigl(a \wedge i_{q+r}\bigr)\bigl(1_{p+h} \wedge B_{2t-1}\bigr)(x), & \tfrac12\le t\le1,\\[2pt]
248: \bigl(A_{1-2t} \wedge 1_r\bigr)\bigl(1_{p+h+q+k} \wedge c\bigr)(x), & 0\le t\le\tfrac12,\\[2pt]
249: \end{cases}
```

### R48 #165（第3章 251行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
H'(d_s(x,t))=
\begin{cases}
\bigl(1_{p+q} \wedge c\bigr)\bigl(A_{2t-1} \wedge 1_{r+\ell}\bigr)(x), & \tfrac12\le t\le1,\\[2pt]
\bigl(1_p \wedge B_{1-2t}\bigr)\bigl(a \wedge 1_{q+k+r+\ell}\bigr)(x), & 0\le t\le\tfr
```

```text
248: \bigl(A_{1-2t} \wedge 1_r\bigr)\bigl(1_{p+h+q+k} \wedge c\bigr)(x), & 0\le t\le\tfrac12,\\[2pt]
249: \end{cases}
250: \]
251: \[
252: H'(d_s(x,t))=
253: \begin{cases}
254: \bigl(1_{p+q} \wedge c\bigr)\bigl(A_{2t-1} \wedge 1_{r+\ell}\bigr)(x), & \tfrac12\le t\le1,\\[2pt]
255: \bigl(1_p \wedge B_{1-2t}\bigr)\bigl(a \wedge 1_{q+k+r+\ell}\bigr)(x), & 0\le t\le\tfrac12.
256: \end{cases}
```

### R48 #171（第3章 348行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
\begin{aligned}
C'_{t}
& = \bigl(1_p \wedge \sigma_{r,q}\bigr)\circ 
(C_t \wedge 1_{q})\circ
\bigl(1_{p+h} \wedge \sigma_{q,r+\ell}\bigr),\\
C''_{t}
& = \bigl(1_q \wedge \sigma_{r,q+k}\bigr)\circ 
(C_t \wedge
```

```text
345: 
346: ii)\
347: $a \wedge c$ の null-homotopy を $C_t$ とする. このとき,
348: \[
349: \begin{aligned}
350: C'_{t}
351: & = \bigl(1_p \wedge \sigma_{r,q}\bigr)\circ 
352: (C_t \wedge 1_{q})\circ
353: \bigl(1_{p+h} \wedge \sigma_{q,r+\ell}\bigr),\\
```

### R48 #175（第3章 376行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
H,\ H',\ H'':S^{s+1}\longrightarrow S^{p+q+r},\qquad
s=p+h+q+k+r+\ell
\]
```

```text
373: = (1_p \wedge \sigma_{r,q})\circ(C_t \wedge b)\circ (1_{p+h} \wedge \sigma_{q+k,r+\ell})
374: = (1_p \wedge b \wedge 1_r) \circ C''_t.
375: \]
376: \[
377: H,\ H',\ H'':S^{s+1}\longrightarrow S^{p+q+r},\qquad
378: s=p+h+q+k+r+\ell
379: \]
380: 
381: \[
```

### R48 #176（第3章 381行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
H(d_s(x,t))=
\begin{cases}
\bigl(a \wedge 1_{q+r}\bigr)\bigl(1_{p+h} \wedge B_{2t-1}\bigr)(x), & \frac12\le t\le1,\\[2pt]
\bigl(A_{1-2t} \wedge 1_r\bigr)\bigl(1_{p+h+q+k} \wedge c\bigr)(x), & 0\le t\le\frac12,
\e
```

```text
378: s=p+h+q+k+r+\ell
379: \]
380: 
381: \[
382: H(d_s(x,t))=
383: \begin{cases}
384: \bigl(a \wedge 1_{q+r}\bigr)\bigl(1_{p+h} \wedge B_{2t-1}\bigr)(x), & \frac12\le t\le1,\\[2pt]
385: \bigl(A_{1-2t} \wedge 1_r\bigr)\bigl(1_{p+h+q+k} \wedge c\bigr)(x), & 0\le t\le\frac12,
386: \end{cases}
```

### R48 #178（第3章 388行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
H'(d_s(x,t))=
\begin{cases}
C'_{2t-1}\bigl(1_{p+h} \wedge b \wedge 1_{r+\ell}\bigr)(x), & \frac12\le t\le1,\\[2pt]
\bigl(a \wedge 1_{q+r}\bigr)\bigl(1_{p+h} \wedge B_{1-2t}\bigr)(x), & 0\le t\le\frac12,
\end{case
```

```text
385: \bigl(A_{1-2t} \wedge 1_r\bigr)\bigl(1_{p+h+q+k} \wedge c\bigr)(x), & 0\le t\le\frac12,
386: \end{cases}
387: \]
388: \[
389: H'(d_s(x,t))=
390: \begin{cases}
391: C'_{2t-1}\bigl(1_{p+h} \wedge b \wedge 1_{r+\ell}\bigr)(x), & \frac12\le t\le1,\\[2pt]
392: \bigl(a \wedge 1_{q+r}\bigr)\bigl(1_{p+h} \wedge B_{1-2t}\bigr)(x), & 0\le t\le\frac12,
393: \end{cases}
```

### R48 #180（第3章 395行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
H''(d_s(x,t))=
\begin{cases}
\bigl(A_{2t-1} \wedge 1_r\bigr)\bigl(1_{p+q+h+k} \wedge c\bigr)(x), & \frac12\le t\le1,\\[2pt]
\bigl(1_p \wedge b \wedge 1_{r}\bigr)\, C''_t(x), & 0\le t\le\frac12 .
\end{cases}
\]
```

```text
392: \bigl(a \wedge 1_{q+r}\bigr)\bigl(1_{p+h} \wedge B_{1-2t}\bigr)(x), & 0\le t\le\frac12,
393: \end{cases}
394: \]
395: \[
396: H''(d_s(x,t))=
397: \begin{cases}
398: \bigl(A_{2t-1} \wedge 1_r\bigr)\bigl(1_{p+q+h+k} \wedge c\bigr)(x), & \frac12\le t\le1,\\[2pt]
399: \bigl(1_p \wedge b \wedge 1_{r}\bigr)\, C''_t(x), & 0\le t\le\frac12 .
400: \end{cases}
```

### R48 #185（第3章 452行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：mapping cone K
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
K = S^n\ \cup_{\,f}\ CS^{n+k}
\]
```

```text
449: \medskip
450: $\alpha$ の代表 $f:S^{n+k}\to S^n$ をとり, Chapter I と同様に,
451: cell complex
452: \[
453: K = S^n\ \cup_{\,f}\ CS^{n+k}
454: \]
455: を考える. $CS^{n+k}$ の等化写像を
456: \[
457: d'_{n+k}:S^{n+k}\times I\longrightarrow CS^{n+k}
```

### R48 #186（第3章 456行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：mapping cone K
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
d'_{n+k}:S^{n+k}\times I\longrightarrow CS^{n+k}
\]
```

```text
453: K = S^n\ \cup_{\,f}\ CS^{n+k}
454: \]
455: を考える. $CS^{n+k}$ の等化写像を
456: \[
457: d'_{n+k}:S^{n+k}\times I\longrightarrow CS^{n+k}
458: \]
459: とし, 合成を
460: \[
461: d':S^{n+k}\times I\ \xrightarrow{d'}\ CS^{n+k}\ \rightarrow\ K
```

### R48 #189（第3章 472行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
1_K \wedge f:\ \Ex^{n+k}K \;=\; K \wedge S^{n+k}\ \longrightarrow\ K \wedge S^{n}\;=\;\Ex^{n}K.
\]
```

```text
469: このとき, $p$ は $K$ に含まれる $S^n$ を一点につぶす写像である.
470: 
471: $K$ の恒等写像を $1_K$ とし, 次の reduced join を考える.
472: \[
473: 1_K \wedge f:\ \Ex^{n+k}K \;=\; K \wedge S^{n+k}\ \longrightarrow\ K \wedge S^{n}\;=\;\Ex^{n}K.
474: \]
475: 制限
476: \((1_K \wedge f) \big|_{S^{2n+k}}\) は, 
477: $\iota_n \wedge \alpha = (-1)^{kn}E^n \alpha$ を表す. \\
```

### R48 #190（第3章 482行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
G_s:\ \Ex^{n+k}K\ \longrightarrow\ \Ex^{n}K, \qquad (0\le s\le1)
\]
```

```text
479: $(2n+k+1)$-cell であるから, \\
480: 上の制限は, $\Ex^{n}K$ の中で null-homotopic である. 
481: ホモトピー拡張定理により, ホモトピー
482: \[
483: G_s:\ \Ex^{n+k}K\ \longrightarrow\ \Ex^{n}K, \qquad (0\le s\le1)
484: \]
485: が存在して, $G_0=1_K \wedge f$, で, 
486: \[
487: G_1:\ \Ex^{n+k}K\ \longrightarrow\ \Ex^{n}K
```

### R48 #191（第3章 486行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
G_1:\ \Ex^{n+k}K\ \longrightarrow\ \Ex^{n}K
\]
```

```text
483: G_s:\ \Ex^{n+k}K\ \longrightarrow\ \Ex^{n}K, \qquad (0\le s\le1)
484: \]
485: が存在して, $G_0=1_K \wedge f$, で, 
486: \[
487: G_1:\ \Ex^{n+k}K\ \longrightarrow\ \Ex^{n}K
488: \]
489: は, $G_1$ は $S^{2n+k}$ を一点に写す. 
490: 上記の写像 $p:K\to S^{n+k+1}$ に対して, ある写像
491: \[
```

### R48 #192（第3章 491行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
F:\ S^{2n+2k+1}\ \longrightarrow\ \Ex^{n}K
\]
```

```text
488: \]
489: は, $G_1$ は $S^{2n+k}$ を一点に写す. 
490: 上記の写像 $p:K\to S^{n+k+1}$ に対して, ある写像
491: \[
492: F:\ S^{2n+2k+1}\ \longrightarrow\ \Ex^{n}K
493: \]
494: が存在して,
495: \[
496: G_1\;=\;F\circ \Ex^{n}p
```

### R48 #194（第3章 602行）

- 判定案：`UNNUMBERED_ASSERTION_CANDIDATE`
- 帰属：suspension sign relation
- 理由：表示された数学的関係を主張候補として保持。ただし既存の番号付き命題内かは未確定。

```tex
\[
\iota_n \wedge \alpha \;=\;(-1)^{nk}\,\Ex^n\alpha
= \alpha \wedge\ (-1)^{kn} \iota_n .
\]
```

```text
599: $\phi_m:K\times S^m\to \Ex^{m}K$ ($m=n$ または $n+k$) を,
600: $\Ex^{m}K=K \wedge S^{m}$ の等化写像とする. \\
601: Prop3.1 により,
602: \[
603: \iota_n \wedge \alpha \;=\;(-1)^{nk}\,\Ex^n\alpha
604: = \alpha \wedge\ (-1)^{kn} \iota_n .
605: \]
606: このとき, ホモトピー
607: $A_s:(S^{2n+k},e_0)\to (S^{2n+k},e_0)$ で, 
```

### R48 #195（第3章 609行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
A_0=1_n \wedge f,\qquad A_1=f \wedge \tau.
\]
```

```text
606: このとき, ホモトピー
607: $A_s:(S^{2n+k},e_0)\to (S^{2n+k},e_0)$ で, 
608: 次を満たすものが存在する.
609: \[
610: A_0=1_n \wedge f,\qquad A_1=f \wedge \tau.
611: \]
612: ここで,  $1_n$ は $S^n$ の恒等写像, $\tau:S^n\to S^n$ は
613: degree が $(-1)^{kn}$ の写像である. \\
614: 次に, ホモトピー
```

### R48 #198（第3章 626行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
G_s\bigl(\phi_{n+k}(d'(u,t),v)\bigr)=
\begin{cases}
\phi_{n}\!\Bigl(d'\!\bigl(u,\,(2t-s)/(2-s)\bigr),\ f(v)\Bigr), & \tfrac{s}{2}\le t\le1,\\[3pt]
G_{s-2t}\!\bigl(\phi_{n,n+k}(f(u),v)\bigr), & 0\le t\le \tfrac{s}{
```

```text
623: \end{cases}
624: \]
625: また, $\Ex^{n+k}K$ の点 $\phi_{n+k}\!\bigl(d'(u,t),v\bigr)$ に対して,
626: \[
627: G_s\bigl(\phi_{n+k}(d'(u,t),v)\bigr)=
628: \begin{cases}
629: \phi_{n}\!\Bigl(d'\!\bigl(u,\,(2t-s)/(2-s)\bigr),\ f(v)\Bigr), & \tfrac{s}{2}\le t\le1,\\[3pt]
630: G_{s-2t}\!\bigl(\phi_{n,n+k}(f(u),v)\bigr), & 0\le t\le \tfrac{s}{2}.
631: \end{cases}
```

### R48 #200（第3章 639行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
F:\ S^{2n+2k+1}\longrightarrow \Ex^{n}K
\]
```

```text
636: また, $\Ex^{n+k}p$ は $S^{2n+k}$ をつぶす写像なので, 
637: 
638: $G_1=F\circ \Ex^{n+k}p$ を満たす写像
639: \[
640: F:\ S^{2n+2k+1}\longrightarrow \Ex^{n}K
641: \]
642: が一意に存在する. 
643: 次の合成を考える. 
644: \[
```

### R48 #201（第3章 644行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
\Ex^{n}p \circ F:\ S^{2n+2k+1}\longrightarrow S^{2n+k+1}
\]
```

```text
641: \]
642: が一意に存在する. 
643: 次の合成を考える. 
644: \[
645: \Ex^{n}p \circ F:\ S^{2n+2k+1}\longrightarrow S^{2n+k+1}
646: \]
647: 
648: \switchcolumn
649: 
```

### R48 #202（第3章 670行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
(E^n p\circ F)(\phi_{n+k+1, n+k}(d_{n+k}(u, t), v))=
\begin{cases}
\phi_{n+k+1, n}(d_{n+k}(u, 2t-1), f(v)), & \frac{1}{2}\le t\le1,\\[3pt]
e_0, & \frac{1}{4}\le t\le \frac{1}{2},\\[3pt]
\phi_{n+k+1, n+k}(d_{n+k}(
```

```text
667: \noindent
668: 上記の定義式を用いた直接計算から, 
669: \(E^n p\circ F\) は, 次の式で与えられる. 
670: \[
671: (E^n p\circ F)(\phi_{n+k+1, n+k}(d_{n+k}(u, t), v))=
672: \begin{cases}
673: \phi_{n+k+1, n}(d_{n+k}(u, 2t-1), f(v)), & \frac{1}{2}\le t\le1,\\[3pt]
674: e_0, & \frac{1}{4}\le t\le \frac{1}{2},\\[3pt]
675: \phi_{n+k+1, n+k}(d_{n+k}(x, 1-4t), \tau(y)), & 0\le t\le \frac{1}{4}.
```

### R48 #205（第3章 686行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
\begin{aligned}
H_1\bigl(\phi_{n+k+1,n+k}(d_{n+k}(u,t),v)\bigr)
&=\phi_{n+k+1,n}\bigl(d_{n+k}(u,t),\,f(v)\bigr),\\
H_2\bigl(\phi_{n+k+1,n+k}(d_{n+k}(u,t),v)\bigr)
&=\phi_{n+k+1,n}\bigl(d_{n+k}(u,t),\,\tau(y)\bigr
```

```text
683: \([E^n p\circ F] = [H_1] + [H_0] - [H_2]\) 
684: となるものと考えることができる. \\
685: ここで, \(H_0\) は自明な写像で, $H_1,H_2$ は次で与えられる. 
686: \[
687: \begin{aligned}
688: H_1\bigl(\phi_{n+k+1,n+k}(d_{n+k}(u,t),v)\bigr)
689: &=\phi_{n+k+1,n}\bigl(d_{n+k}(u,t),\,f(v)\bigr),\\
690: H_2\bigl(\phi_{n+k+1,n+k}(d_{n+k}(u,t),v)\bigr)
691: &=\phi_{n+k+1,n}\bigl(d_{n+k}(u,t),\,\tau(y)\bigr).
```

### R48 #214（第3章 780行）

- 判定案：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明のための補助写像・ホモトピー・具体構成。独立 Reference は保留。

```tex
\[
\begin{tikzpicture}[baseline=(current bounding box.center)]
  \node (A) at (0,1.2) {$\pis{2n+2k+1}{S^{2n}}$};
  \node (B) at (4.3,1.2) {$\pis{2n+2k+1}{\Ex^{n}K}$};
  \node (C) at (8.6,1.2) {$\pis{2n+2k+1}{\Ex^{n}K
```

```text
777: 
778: 次の図式において, 横の列は完全列である. 
779: 
780: \[
781: \begin{tikzpicture}[baseline=(current bounding box.center)]
782:   \node (A) at (0,1.2) {$\pis{2n+2k+1}{S^{2n}}$};
783:   \node (B) at (4.3,1.2) {$\pis{2n+2k+1}{\Ex^{n}K}$};
784:   \node (C) at (8.6,1.2) {$\pis{2n+2k+1}{\Ex^{n}K,S^{2n}}$};
785:   \node (D) at (8.6,0)   {$\pis{2n+k+1}{S^{2n+k+1}} .$};
```

### R48 #216（第3章 845行）

- 判定案：`DEFINITION_COMPONENT`
- 帰属：proof-local self-homeomorphism
- 理由：周辺文脈で導入された写像・空間・記法の構成要素。独立 Reference の新設は未決定。

```tex
\[
\sigma(\psi_{n+k+t+1}(t_1,\cdots,t_{n+k+t},t))
=\psi_{n+k+t+1}(t_1,\cdots,t_{n+k},t,t_{n+k+1},\cdots,t_{n+k+t})
\]
```

```text
842: を同一視する. \\
843: \(p':\Ex^{n}K = S^{n+t}\cup_{\alpha'}CS^{n+k+t} \to S^{n+k+t+1}\)
844: を (1.17) の中で定義された写像とすると, 
845: \[
846: \sigma(\psi_{n+k+t+1}(t_1,\cdots,t_{n+k+t},t))
847: =\psi_{n+k+t+1}(t_1,\cdots,t_{n+k},t,t_{n+k+1},\cdots,t_{n+k+t})
848: \]
849: により与えられる, 次数 \((-1)^{t}\) の自己同相写像
850: $\sigma:S^{n+k+t+1}\to S^{n+k+t+1}$
```

### R48 #250（第4章 140行）

- 判定案：`UNNUMBERED_ASSERTION_CANDIDATE`
- 帰属：Chapter 4 homotopy group calculation
- 理由：表示された数学的関係を主張候補として保持。ただし既存の番号付き命題内かは未確定。

```tex
\[
\pis{2n-2}{S^{n-1}} \xrightarrow{\ \Ex\ } \pis{2n-1}{S^{n}}
\xrightarrow{\ H\ } \pis{2n-1}{S^{2n-1}}
\xrightarrow{\ \Delta\ } \pis{2n-3}{S^{n-1}}.
\]
```

```text
137: 
138: 
139: 次に, $n$ を偶数とし, (2.11) の完全列を考える. 
140: \[
141: \pis{2n-2}{S^{n-1}} \xrightarrow{\ \Ex\ } \pis{2n-1}{S^{n}}
142: \xrightarrow{\ H\ } \pis{2n-1}{S^{2n-1}}
143: \xrightarrow{\ \Delta\ } \pis{2n-3}{S^{n-1}}.
144: \]
145: $\Delta$ の象は $[\,\iota_{n-1},\iota_{n-1}\,]$ によって生成され, 
```

### R48 #251（第4章 147行）

- 判定案：`UNNUMBERED_ASSERTION_CANDIDATE`
- 帰属：Chapter 4 homotopy group calculation
- 理由：表示された数学的関係を主張候補として保持。ただし既存の番号付き命題内かは未確定。

```tex
\[
\pis{2n-1}{S^{n}} \cong
\mathbb{Z}\gen{\beta}\ \oplus\ 
E\pis{2n-2}{S^{n-1}} .
\]
```

```text
144: \]
145: $\Delta$ の象は $[\,\iota_{n-1},\iota_{n-1}\,]$ によって生成され, 
146: また, $2[\,\iota_{n-1},\iota_{n-1}\,]=0$ であるから, 
147: \[
148: \pis{2n-1}{S^{n}} \cong
149: \mathbb{Z}\gen{\beta}\ \oplus\ 
150: E\pis{2n-2}{S^{n-1}} .
151: \]
152: ここで,
```

### R48 #252（第4章 202行）

- 判定案：`UNNUMBERED_ASSERTION_CANDIDATE`
- 帰属：Chapter 4 homotopy group calculation
- 理由：表示された数学的関係を主張候補として保持。ただし既存の番号付き命題内かは未確定。

```tex
\[
\begin{align*}
  \pit{2n-1}{n} = E^{-1}(\pis{2n}{S^{n+1}; 2})
  &= \Delta(\pis{2n+1}{S^{2n+1}}) \oplus (E \pis{2n-2}{n-1}; 2) \\
  &= \Delta(\pis{2n+1}{S^{2n+1}}) \oplus \pis{2n-1}{S^n;2} .
\end{align*}
\]
```

```text
199: $\beta=\pm[\,\iota_n,\iota_n\,]$ が取れる. \\
200: さらに, $\Ker \Ex:\pis{2n-1}{S^{n}}\to\pis{2n}{S^{n+1}}$ は,
201: \(\pm[\iota_n, \iota_n]=\Delta(\iota_{2n+1})\) で生成されるので, 
202: \[
203: \begin{align*}
204:   \pit{2n-1}{n} = E^{-1}(\pis{2n}{S^{n+1}; 2})
205:   &= \Delta(\pis{2n+1}{S^{2n+1}}) \oplus (E \pis{2n-2}{n-1}; 2) \\
206:   &= \Delta(\pis{2n+1}{S^{2n+1}}) \oplus \pis{2n-1}{S^n;2} .
207: \end{align*}
```

### R48 #254（第4章 244行）

- 判定案：`UNNUMBERED_ASSERTION_CANDIDATE`
- 帰属：Chapter 4 homotopy group calculation
- 理由：表示された数学的関係を主張候補として保持。ただし既存の番号付き命題内かは未確定。

```tex
\[
[\iota_n, \iota_n] \in E\pis{2n-2}{S^n; 2} \oplus \gen{\alpha}
= \pis{2n-1}{S^n; 2} \oplus \gen{\alpha} .
\]
```

```text
241: を 
242: \(\pis{2n}{S^{n+1}}\)
243: に同型に写すので, 
244: \[
245: [\iota_n, \iota_n] \in E\pis{2n-2}{S^n; 2} \oplus \gen{\alpha}
246: = \pis{2n-1}{S^n; 2} \oplus \gen{\alpha} .
247: \]
248: 以上より, 
249: \(
```

### R48 #259（第4章 570行）

- 判定案：`UNNUMBERED_ASSERTION_CANDIDATE`
- 帰属：multiplication order relation
- 理由：表示された数学的関係を主張候補として保持。ただし既存の番号付き命題内かは未確定。

```tex
\[
\begin{aligned}
2^{2t+1}(\beta\circ\alpha)
&=\beta\circ r 2^{2t}[\iota_m,\iota_m]
\ +\ \beta\circ 2^{2t}E\gamma\\
&=\beta\circ r\bigl[2^{t}\iota_m,\,2^{t}\iota_m\bigr]\ +\ 2^{2t}\beta\circ E\gamma\\
&=\beta\circ
```

```text
567: $\beta$ の位数を $2^{t}$ とする. \\
568: このとき, \(2^{2t+1}(\beta\circ\alpha) = \) を示す. 
569: (2.1) と, Whitehead 積の双線型性と自然性 \cite{Whitehead1941} から, 
570: \[
571: \begin{aligned}
572: 2^{2t+1}(\beta\circ\alpha)
573: &=\beta\circ r 2^{2t}[\iota_m,\iota_m]
574: \ +\ \beta\circ 2^{2t}E\gamma\\
575: &=\beta\circ r\bigl[2^{t}\iota_m,\,2^{t}\iota_m\bigr]\ +\ 2^{2t}\beta\circ E\gamma\\
```

### R48 #262（第5章 114行）

- 判定案：`UNNUMBERED_ASSERTION_CANDIDATE`
- 帰属：Delta iota5 special case
- 理由：表示された数学的関係を主張候補として保持。ただし既存の番号付き命題内かは未確定。

```tex
\[
\Delta(\iota_5)=\pm 2\,\eta_2 .
\]
```

```text
111: Prop 2.7 により,
112: \(H(\Delta(\iota_5))=\pm H[\iota_2,\iota_2]=\pm 2\iota_3\) である. \\
113: \(H:\pi^{2}_{3}\to\pi^{3}_{3}\) が同型なので, 
114: \[
115: \Delta(\iota_5)=\pm 2\,\eta_2 .
116: \]
117: 完全列 (4.4)
118: \[
119: \pi^{5}_{5}\xrightarrow{\ \Delta\ }\pi^{2}_{3}\xrightarrow{\ E\ }\pi^{3}_{4}\xrightarrow{\ \ }\pi_{4}^{5}=0
```

### R48 #269（第5章 358行）

- 判定案：`UNNUMBERED_ASSERTION_CANDIDATE`
- 帰属：eta square suspension
- 理由：表示された数学的関係を主張候補として保持。ただし既存の番号付き命題内かは未確定。

```tex
\[
E\,\eta_n^{2}=\eta_{n+1}^{2},\qquad E^{\infty}\eta_n^{2}=\eta^{2}.
\]
```

```text
355: \paragraph*{ii) The Group \(\pi^{n}_{n+2}\).}
356: \(\eta_n^{2}:=\eta_n\circ \eta_{n+1}\) および,
357: \(\eta^{2}:=\eta\circ\eta\) と記す. このとき,
358: \[
359: E\,\eta_n^{2}=\eta_{n+1}^{2},\qquad E^{\infty}\eta_n^{2}=\eta^{2}.
360: \]
361: 
362: \switchcolumn
363: 
```

### R48 #270（第5章 378行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\pi_{6}^{3}\xrightarrow{\ H}\pi_{6}^{5}\xrightarrow{\ \Delta\ }\pi_{4}^{2}
\xrightarrow{\ E\ }\pi_{5}^{3}\xrightarrow{\ H\ }\pi^{5}_{5}
\xrightarrow{\ \Delta\ }\pi_{3}^{2}
\]
```

```text
375: \textbf{Proof.}\ 
376:  (5.2) より, \(\pi_{4}^{2}=\gen{\eta_2^{2}}\cong \mathbb Z_2 .\)
377: 完全列 (4.4)
378: \[
379: \pi_{6}^{3}\xrightarrow{\ H}\pi_{6}^{5}\xrightarrow{\ \Delta\ }\pi_{4}^{2}
380: \xrightarrow{\ E\ }\pi_{5}^{3}\xrightarrow{\ H\ }\pi^{5}_{5}
381: \xrightarrow{\ \Delta\ }\pi_{3}^{2}
382: \]
383: を考える. Prop 5.1 から,
```

### R48 #271（第5章 460行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
E^{2}\beta\circ E^t\alpha^{\ast}\in (-1)^m \toda{E^{m}\eta_{2},\,E^{3}\beta,\,E^{t+3}\eta_{2}}_{3}
\]
```

```text
457: よって, ある元 \(\alpha^{\ast}\in\pis{7}{S^4}\) が存在し, \\
458: \(\beta\circ E^{t}\eta_{2}=0\) を満たす
459: 任意の \(\beta\in\pi_{\,t+2}(S^{\,m})\) に対して,
460: \[
461: E^{2}\beta\circ E^t\alpha^{\ast}\in (-1)^m \toda{E^{m}\eta_{2},\,E^{3}\beta,\,E^{t+3}\eta_{2}}_{3}
462: \]
463: となる. 
464: とくに, \(\beta=2\iota_{3}\) とし, \(t=1\) の場合,  (2.1) より
465: \(2\iota_3\circ E\eta_{2}=2E\eta_{2}=2\eta_3=0\). \\
```

### R48 #272（第5章 467行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
E^{2}(2\iota_{3})\circ E\alpha^{\ast}=2E\alpha^{\ast}
\]
```

```text
464: とくに, \(\beta=2\iota_{3}\) とし, \(t=1\) の場合,  (2.1) より
465: \(2\iota_3\circ E\eta_{2}=2E\eta_{2}=2\eta_3=0\). \\
466: したがって,
467: \[
468: E^{2}(2\iota_{3})\circ E\alpha^{\ast}=2E\alpha^{\ast}
469: \]
470: は, \(-\todai[3]{\eta_{5},\,2\iota_{6},\,\eta_{6}}\) に含まれる. 
471: ここで,
472: \(n\ge3,\ t\le n-2\) のとき, 
```

### R48 #273（第5章 482行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\eta_n\circ \pi^{n+1}_{n+3} + \pi^{n}_{n+2}\circ \eta_{n+2} 
= \gen{\eta_n\circ\eta_{n+1}\circ\eta_{n+2}}
= \gen{2E^{n-3}\nu'}
\]
```

```text
479: まず, \(t\ge1\) の場合を考える.  
480: (4.7) , Prop 5.3 と (5.3) より, 
481: 上の Toda bracket は,
482: \[
483: \eta_n\circ \pi^{n+1}_{n+3} + \pi^{n}_{n+2}\circ \eta_{n+2} 
484: = \gen{\eta_n\circ\eta_{n+1}\circ\eta_{n+2}}
485: = \gen{2E^{n-3}\nu'}
486: \]
487: の coset である. 
```

### R48 #279（第5章 710行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\pi^{3}_{7}\xrightarrow{H}\pi^{5}_{7}\xrightarrow{\Delta}\pi^{2}_{5}
\xrightarrow{E}\pi^{3}_{6}\xrightarrow{H}\pi^{5}_{6}
\]
```

```text
707: (5.2), Prop 5.3 より,
708: \(\pi^{2}_{5}=\gen{\eta_{2}^{3}}\cong\mathbb Z_{2}\). 
709: 完全列 (4.4)
710: \[
711: \pi^{3}_{7}\xrightarrow{H}\pi^{5}_{7}\xrightarrow{\Delta}\pi^{2}_{5}
712: \xrightarrow{E}\pi^{3}_{6}\xrightarrow{H}\pi^{5}_{6}
713: \]
714: を考える. Prop 2.2 とProp 5.3 から,
715: \(
```

### R48 #281（第5章 874行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\begin{align*}
\Delta(\eta_9)
& =  \Delta(\iota_9)\circ \eta_7
&& \text{by Prop2.5}\\
& =  (2\nu_4-E\nu')\circ \eta_7
&& \text{by (5.8)}\\
& =  \nu_4\circ (2\eta_7)-E\nu'\circ \eta_7
 =  E\nu'\circ \eta_7.
\e
```

```text
871: を考える. (5.8) とProp5.6 により, \(\Delta:\pi_9^9\to\pi_7^4\) は単射である. \\
872: よって, 完全性から, \(E\) は全射となることが分かる. \\
873: \(E\) の kernel は次で生成される. 
874: \[
875: \begin{align*}
876: \Delta(\eta_9)
877: & =  \Delta(\iota_9)\circ \eta_7
878: && \text{by Prop2.5}\\
879: & =  (2\nu_4-E\nu')\circ \eta_7
```

### R48 #283（第5章 887行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\pi^{11}_{11}\xrightarrow{\ \Delta\ }\pi^{5}_{9}\xrightarrow{\ E } \pi^{6}_{10}
\xrightarrow{\ H } \pi^{11}_{10}=0
\]
```

```text
884: \]
885: これから, \(\pi_9^5=E\pi_8^4=\mathbb Z_2\gen{\nu_5\circ\eta_8}\) である. 
886: 次に, (4.4) の完全列
887: \[
888: \pi^{11}_{11}\xrightarrow{\ \Delta\ }\pi^{5}_{9}\xrightarrow{\ E } \pi^{6}_{10}
889: \xrightarrow{\ H } \pi^{11}_{10}=0
890: \]
891: を考える. 
892: \(E\) は全射で, \(\pi_{10}^6\) は \(\nu_6\circ\eta_9\) で生成される. 
```

### R48 #284（第5章 912行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\begin{align*}
H(\eta_3\circ \nu_4)
& =  E(\eta_2\wedge\eta_2)\circ H(\nu_4)
&& \text{by Prop2.2}\\
& =  \pm (\eta_5\circ \eta_6)\circ \iota_7
&& \text{by Prop3.1, Lem5.4}\\
& =  \eta_5^{2}
&& \text{by Prop5.3
```

```text
909: よって, \(\eta_3\circ\nu_4\in\pi_7^3 .\)\\
910: \(\pi_7^3\) は \(\nu'\circ\eta_6\) で生成されるので, 
911: \(\eta_3\circ\nu_4=x\nu'\circ\eta_6 \ (x = 0 \text{ or } 1) .\)
912: \[
913: \begin{align*}
914: H(\eta_3\circ \nu_4)
915: & =  E(\eta_2\wedge\eta_2)\circ H(\nu_4)
916: && \text{by Prop2.2}\\
917: & =  \pm (\eta_5\circ \eta_6)\circ \iota_7
```

### R48 #286（第5章 1077行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
0\to \pi^{3}_{8}\xrightarrow{H}\pi^{5}_{8}\xrightarrow{\Delta}\pi^{2}_{6}
\]
```

```text
1074: (5.2) とProp5.8 から, 最初の結果を得る. \\
1075: Lem5.7 により, \(E\pi_7^2=\gen{E(\eta_2\circ\nu')\circ\eta_7}=0 .\)
1076: よって, (4.4) から, 
1077: \[
1078: 0\to \pi^{3}_{8}\xrightarrow{H}\pi^{5}_{8}\xrightarrow{\Delta}\pi^{2}_{6}
1079: \]
1080: は完全列である. 
1081: Lem5.7, Prop 5.6, (5.5) により, \(\ker\Delta\) は \(4\nu_5=\eta_5^3\) で生成される. \\
1082: Prop2.2 と (5.3) により, 次を得る. 
```

### R48 #288（第5章 1180行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\pi^{9}_{11}\xrightarrow{\ \Delta\ }\pi^{4}_{9}\xrightarrow{\ E }\pi^{5}_{10}
\xrightarrow{\ H }\pi^{9}_{10}\xrightarrow{\ \Delta\ }\pi^{4}_{8}\xrightarrow{E}\pi_9^5 .
\]
```

```text
1177: \begin{paracol}{2}
1178: 
1179: (4.4) の次の完全列を考える. 
1180: \[
1181: \pi^{9}_{11}\xrightarrow{\ \Delta\ }\pi^{4}_{9}\xrightarrow{\ E }\pi^{5}_{10}
1182: \xrightarrow{\ H }\pi^{9}_{10}\xrightarrow{\ \Delta\ }\pi^{4}_{8}\xrightarrow{E}\pi_9^5 .
1183: \]
1184: Prop5.8 と (5.11) により, \(\ker(E:\pi_8^4\to\pi_9^5)\cong\mathbb Z_2\) である. \\
1185: \(\pi_{10}^9\cong\mathbb Z_2\) は, \(\Delta\) により, \(\pi_8^4\) に単射で写る. 
```

### R48 #289（第5章 1194行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
0\to \pi^{6}_{11}\xrightarrow{H}\pi^{11}_{11}\xrightarrow{\ \Delta\ }\pi^{5}_{9}
\]
```

```text
1191: \(E\pi_{10}^5=0 .\)\\
1192: また, Prop2.5 と (5.10) により, \(\Delta(\eta_{11})=\nu_5\circ\eta_8^2\) である. 
1193: よって, (4.4) から, 
1194: \[
1195: 0\to \pi^{6}_{11}\xrightarrow{H}\pi^{11}_{11}\xrightarrow{\ \Delta\ }\pi^{5}_{9}
1196: \]
1197: が完全列である. 
1198: Prop5.8 と (5.10) により, \(\Delta\) は全射で, \(\ker\Delta=\gen{2\iota_{11}}\) である. \\
1199: Prop2.7 により, \(H(\Delta(\iota_{13}))=\pm2\iota_{11}\) なので, 
```

### R48 #291（第5章 1226行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\nu_6\circ \pi_{11}(S^9)+\pi_{11}(S^6)\circ2\iota_{11}
= \nu_6\circ\pi_{11}^9+2\pi_{11}(S^6)=2\pi_{11}(S^6) .
\]
```

```text
1223: \noindent
1224: \textbf{Proof.}\ 
1225: この Toda bracket は, 次の群の coset である. (cf. (4.7), (5.9)).
1226: \[
1227: \nu_6\circ \pi_{11}(S^9)+\pi_{11}(S^6)\circ2\iota_{11}
1228: = \nu_6\circ\pi_{11}^9+2\pi_{11}(S^6)=2\pi_{11}(S^6) .
1229: \]
1230: (5.10) とProp2.6 により, 
1231: \(H\toda{\nu_6,\eta_9,2\iota_{10}}\ni\iota_{11}\circ E(2\iota_{10})=2\iota_{11} .\)\\
```

### R48 #292（第5章 1233行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\pi_{10}(S^5)\xrightarrow{E}\pi_{11}(S^6)\xrightarrow{H}\pi_{11}(S^{11})
\]
```

```text
1230: (5.10) とProp2.6 により, 
1231: \(H\toda{\nu_6,\eta_9,2\iota_{10}}\ni\iota_{11}\circ E(2\iota_{10})=2\iota_{11} .\)\\
1232: また, \(H(\Delta(\iota_{13}))=\pm2\iota_{11}\) なので, (2.11) の完全列
1233: \[
1234: \pi_{10}(S^5)\xrightarrow{E}\pi_{11}(S^6)\xrightarrow{H}\pi_{11}(S^{11})
1235: \]
1236: から, 
1237: \(\Delta(\iota_{13})\in\toda{\nu_6,\eta_9,2\iota_{10}} + E\pi_{10}(S^5)\) である. \\
1238: \(E\pi_{10}(S^5)\) は有限で, \(E\pi_{10}^5=0\) なので, 
```

### R48 #294（第5章 1341行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
0\to \pi^{3}_{9}\xrightarrow{H}\pi^{5}_{9}\xrightarrow{\Delta}\pi^{2}_{7}\to 0
\]
```

```text
1338: Lem5.7 により, \(E\pi_8^2=\gen{E(\eta_2\circ\nu')\circ\eta_6^2}=0 .\)\\
1339: 同様に, \(E\pi_7^2=0\) である. 
1340: (4.4) により, 
1341: \[
1342: 0\to \pi^{3}_{9}\xrightarrow{H}\pi^{5}_{9}\xrightarrow{\Delta}\pi^{2}_{7}\to 0
1343: \]
1344: は完全である. 
1345: Prop \ref{prop:5.8}, \ref{prop:5.9} より,
1346: \(\Delta\) は同型で, 
```

### R48 #295（第5章 1351行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\pi^{2n+1}_{n+8}\xrightarrow{\Delta}\pi^{n}_{n+6}
\xrightarrow{E}\pi^{n+1}_{n+7}\xrightarrow{H}\pi^{2n+1}_{n+7}
\xrightarrow{P}\pi_{n+5}^n, 
\qquad(n=4,5,6) .
\]
```

```text
1348: さらに, Prop \ref{prop:5.6} と (\ref{eq:5.6}) により,
1349: \(\pi^{4}_{10}=\gen{\nu_4^{2}}\cong \mathbb Z_8 .\)\\
1350: 次の完全列を考える. 
1351: \[
1352: \pi^{2n+1}_{n+8}\xrightarrow{\Delta}\pi^{n}_{n+6}
1353: \xrightarrow{E}\pi^{n+1}_{n+7}\xrightarrow{H}\pi^{2n+1}_{n+7}
1354: \xrightarrow{P}\pi_{n+5}^n, 
1355: \qquad(n=4,5,6) .
1356: \]
```

### R48 #296（第5章 1367行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\Delta(\nu_9)=\Delta(\iota_9)\circ \nu_7=\pm\,(2\nu_4-E\nu')\circ \nu_7
=\pm\big(2\,\nu_4^{2}-E(\nu'\circ \nu_6)\big).
\]
```

```text
1364: \end{equation}
1365: 
1366: Prop 2.5 と (\ref{eq:5.8}) より,
1367: \[
1368: \Delta(\nu_9)=\Delta(\iota_9)\circ \nu_7=\pm\,(2\nu_4-E\nu')\circ \nu_7
1369: =\pm\big(2\,\nu_4^{2}-E(\nu'\circ \nu_6)\big).
1370: \]
1371: \(\nu'\circ \nu_6\in \pi^{3}_{9}=0\) なので, 
1372: \(\Delta(\nu_9)=\pm 2(\nu_4^{2}) .\) また,
```

### R48 #297（第5章 1373行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\begin{align*}
\Delta(\eta^{2}_{11})
& =  \Delta(\iota_{11})\circ \eta_9^2
&& \text{by Prop2.5}\\
& =  \nu_5\circ \eta_8\circ \eta_9^2
= \nu_5\circ \eta_8^{3}
&& \text{by (5.10)}\\
& =  4(\nu_5\circ\nu_8)
= 4
```

```text
1370: \]
1371: \(\nu'\circ \nu_6\in \pi^{3}_{9}=0\) なので, 
1372: \(\Delta(\nu_9)=\pm 2(\nu_4^{2}) .\) また,
1373: \[
1374: \begin{align*}
1375: \Delta(\eta^{2}_{11})
1376: & =  \Delta(\iota_{11})\circ \eta_9^2
1377: && \text{by Prop2.5}\\
1378: & =  \nu_5\circ \eta_8\circ \eta_9^2
```

### R48 #299（第5章 1388行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\begin{align*}
\Delta(\eta_{13})
& =  \Delta(\iota_{13})\circ \eta_{11}
&& \text{by Prop2.5}\\
& \in \toda{ \nu_6,\ \eta_9,\ 2\iota_{10} }\circ \eta_{11}
&& \text{by Lem5.10}\\
& =  \nu_6\circ\toda{\eta_9,2\iot
```

```text
1385: =0 .
1386: \end{align*}
1387: \]
1388: \[
1389: \begin{align*}
1390: \Delta(\eta_{13})
1391: & =  \Delta(\iota_{13})\circ \eta_{11}
1392: && \text{by Prop2.5}\\
1393: & \in \toda{ \nu_6,\ \eta_9,\ 2\iota_{10} }\circ \eta_{11}
```

### R48 #301（第5章 1563行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
0=\pi^{2}_{9}\xto
\pi^{3}_{10}\xrightarrow{H}
\pi_{10}^5\xrightarrow{\Delta}
\pi^{2}_{8}\xrightarrow{E}\pi^{3}_{9}=0 .
\]
```

```text
1560: (\ref{eq:5.2}) とProp \ref{prop:5.11} より,
1561: \(\pi^{2}_{9}=0\). 
1562: (4.4) から, 次の列は完全である. 
1563: \[
1564: 0=\pi^{2}_{9}\xto
1565: \pi^{3}_{10}\xrightarrow{H}
1566: \pi_{10}^5\xrightarrow{\Delta}
1567: \pi^{2}_{8}\xrightarrow{E}\pi^{3}_{9}=0 .
1568: \]
```

### R48 #302（第5章 1575行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
0=\pi^{4}_{11}\xto\pi^{5}_{12}\xrightarrow{H}
\pi^{9}_{12}\xrightarrow{\Delta}\pi^{4}_{10} .
\]
```

```text
1572: さらに (\ref{eq:5.6}) とProp \ref{prop:5.8} から, 
1573: \(\pi^{4}_{11}\cong \pi^{3}_{10}\oplus \pi^{7}_{11}=0\). \\
1574: ここで, 次の完全列を考える. 
1575: \[
1576: 0=\pi^{4}_{11}\xto\pi^{5}_{12}\xrightarrow{H}
1577: \pi^{9}_{12}\xrightarrow{\Delta}\pi^{4}_{10} .
1578: \]
1579: (\ref{eq:5.13}), Prop \ref{prop:5.11}, Prop \ref{prop:5.6} から, 
1580: \(\Delta\) は 次数 2 の準同型 で, \\
```

### R48 #303（第5章 1732行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\nu_5\circ\pis{12}{S^{8}}
=\nu_5\circ E\pis{11}{S^{7}}
=\nu_5\circ \pit{11}{7}=0.
\]
```

```text
1729: この Toda bracket は,
1730: \(\nu_5\circ \pi_{12}(S^{8})+\pi_{9}(S^{5})\circ \nu_9\) の coset である. \\
1731: (3.2),(4.7), Prop \ref{prop:5.8} から 
1732: \[
1733: \nu_5\circ\pis{12}{S^{8}}
1734: =\nu_5\circ E\pis{11}{S^{7}}
1735: =\nu_5\circ \pit{11}{7}=0.
1736: \]
1737: (3.2), Prop5.8, (5.9) により, 
```

### R48 #304（第5章 1738行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\pi_{9}(S^{5})\circ\nu_9=\pi_9^5\circ\nu_9
=\gen{\nu_5\circ \eta_8\circ \nu_9}=0 .
\]
```

```text
1735: =\nu_5\circ \pit{11}{7}=0.
1736: \]
1737: (3.2), Prop5.8, (5.9) により, 
1738: \[
1739: \pi_{9}(S^{5})\circ\nu_9=\pi_9^5\circ\nu_9
1740: =\gen{\nu_5\circ \eta_8\circ \nu_9}=0 .
1741: \]
1742: よって, Toda bracket は単一元から成る. \\
1743: さらに, (1.15) より,
```

### R48 #305（第5章 1750行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
H(\sigma''')
= H\todai[1]{\nu_5, 8\iota_8, \nu_8}
= \Delta^{-1}(\nu_4\circ 8\iota_7)\circ \nu_9 .
\]
```

```text
1747: 1つの元 \(\sigma'''\) だけから成り, 
1748: (4.7) により, \(\sigma'''\in\pi_{12}^5\) である. \\
1749: Prop 2.6 から, 
1750: \[
1751: H(\sigma''')
1752: = H\todai[1]{\nu_5, 8\iota_8, \nu_8}
1753: = \Delta^{-1}(\nu_4\circ 8\iota_7)\circ \nu_9 .
1754: \]
1755: (5.8) により, 
```

### R48 #306（第5章 1756行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\Delta(4\iota_9)=\pm4(2\nu_4-E\nu')
=\pm(8\nu_4-E4\nu')
=\pm8\nu_4
=\pm(\nu_4\circ8\iota_7) .
\]
```

```text
1753: = \Delta^{-1}(\nu_4\circ 8\iota_7)\circ \nu_9 .
1754: \]
1755: (5.8) により, 
1756: \[
1757: \Delta(4\iota_9)=\pm4(2\nu_4-E\nu')
1758: =\pm(8\nu_4-E4\nu')
1759: =\pm8\nu_4
1760: =\pm(\nu_4\circ8\iota_7) .
1761: \]
```

### R48 #307（第5章 1763行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\Delta^{-1}(\nu_4\circ8\iota_7)\circ\nu_9
\ni\pm(4\iota_9)\circ\nu_9
=4\nu_9
=\eta_9^3 .
\]
```

```text
1760: =\pm(\nu_4\circ8\iota_7) .
1761: \]
1762: よって, 
1763: \[
1764: \Delta^{-1}(\nu_4\circ8\iota_7)\circ\nu_9
1765: \ni\pm(4\iota_9)\circ\nu_9
1766: =4\nu_9
1767: =\eta_9^3 .
1768: \]
```

### R48 #308（第5章 1904行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
2E^{4-3}\nu_{4}\circ E^{7-3}\nu_{4}=2\nu_{5}^{2}=0,
\quad (h=3).
\]
```

```text
1901: Th 3.6 を \(\alpha=\nu_{4}\) に適用し, \\
1902: Prop \ref{prop:5.11} により, 
1903: \(\nu_4\) は (3.1) の条件を満たす. 
1904: \[
1905: 2E^{4-3}\nu_{4}\circ E^{7-3}\nu_{4}=2\nu_{5}^{2}=0,
1906: \quad (h=3).
1907: \]
1908: このとき, 
1909: \(\alpha^{\ast}\in\pi^{8}_{15}\) が存在し, 
```

### R48 #309（第5章 1911行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
E^{4}\beta\circ E^t\alpha^{\ast}
\in (-1)^{m}\todai[7]{\nu_{m+4},\,E^{7}\beta,\,\nu_{t+11}}
+(-1)^{t}\todai[t+3]{E^{4}\beta,\,\nu_{t+8},\,2\nu_{t+11}} .
\]
```

```text
1908: このとき, 
1909: \(\alpha^{\ast}\in\pi^{8}_{15}\) が存在し, 
1910: \(\beta\circ\nu_{t+4}=0\) を満たす任意の \(\beta\in\pi_{t+4}(S^m)\) に対して, 
1911: \[
1912: E^{4}\beta\circ E^t\alpha^{\ast}
1913: \in (-1)^{m}\todai[7]{\nu_{m+4},\,E^{7}\beta,\,\nu_{t+11}}
1914: +(-1)^{t}\todai[t+3]{E^{4}\beta,\,\nu_{t+8},\,2\nu_{t+11}} .
1915: \]
1916: 今, \(\beta=8\iota_{5}\) とする. 
```

### R48 #310（第5章 1918行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
8E\alpha^{\ast}=E^48\iota_5\circ E\alpha^{\ast}
\in -\todai[7]{\nu_9,8\iota_{12},\nu_{12}}
-\todai[4]{8\iota_9,\nu_9,2\nu_{12}} .  
\]
```

```text
1915: \]
1916: 今, \(\beta=8\iota_{5}\) とする. 
1917: \(8\iota_5\circ\nu_5=8\nu_5=0\) なので, 
1918: \[
1919: 8E\alpha^{\ast}=E^48\iota_5\circ E\alpha^{\ast}
1920: \in -\todai[7]{\nu_9,8\iota_{12},\nu_{12}}
1921: -\todai[4]{8\iota_9,\nu_9,2\nu_{12}} .  
1922: \]
1923: Toda bracket \(\todai[7]{\nu_{9},\,8\iota_{12},\,\nu_{12}}\) は, 
```

### R48 #311（第5章 1925行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
\nu_9\circ E^7\pi_9(S^5) + \pi_{13}^9\circ\nu_{13}
=\nu_9\circ E^7\pi_9^5 + \pi_{13}^9\circ\nu_{13} = 0
\]
```

```text
1922: \]
1923: Toda bracket \(\todai[7]{\nu_{9},\,8\iota_{12},\,\nu_{12}}\) は, 
1924: (4.7) とProp5.8 により, 
1925: \[
1926: \nu_9\circ E^7\pi_9(S^5) + \pi_{13}^9\circ\nu_{13}
1927: =\nu_9\circ E^7\pi_9^5 + \pi_{13}^9\circ\nu_{13} = 0
1928: \]
1929: の coset なので, ただ1つの元である. 
1930: Prop 1.3, Lem 5.13 により, 
```

### R48 #312（第5章 1931行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
E\sigma'''\in E^4\todai[3]{\nu_5,8\iota_8,\nu_8}
\subset \todai[7]{\nu_9,8\iota_{12},\nu_{12}} .
\]
```

```text
1928: \]
1929: の coset なので, ただ1つの元である. 
1930: Prop 1.3, Lem 5.13 により, 
1931: \[
1932: E\sigma'''\in E^4\todai[3]{\nu_5,8\iota_8,\nu_8}
1933: \subset \todai[7]{\nu_9,8\iota_{12},\nu_{12}} .
1934: \]
1935: したがって, \(-\todai[7]{\nu_9,8\iota_{12},\nu_{12}}
1936: =-E^4\sigma'''=E^4\sigma'''\) である. 
```

### R48 #313（第5章 1938行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\begin{align*}
\todai[4]{8\iota_9,\nu_9,2\nu_{12}}
& \subset\todai[4]{2\iota_9,4\iota_9\circ\nu_9\circ2\iota_{12}, \nu_{12}} \\
& =\todai[4]{2\iota_9,0,\nu_{12}}
=2\iota_9\circ E^4\pi_{12}(S^5) + \pi_{13}(S^9)\circ\n
```

```text
1935: したがって, \(-\todai[7]{\nu_9,8\iota_{12},\nu_{12}}
1936: =-E^4\sigma'''=E^4\sigma'''\) である. 
1937: Prop1.2 により, 
1938: \begin{align*}
1939: \todai[4]{8\iota_9,\nu_9,2\nu_{12}}
1940: & \subset\todai[4]{2\iota_9,4\iota_9\circ\nu_9\circ2\iota_{12}, \nu_{12}} \\
1941: & =\todai[4]{2\iota_9,0,\nu_{12}}
1942: =2\iota_9\circ E^4\pi_{12}(S^5) + \pi_{13}(S^9)\circ\nu_{13} \\
1943: & =2E^4\pi_{12}(S^5) + \pi_{13}^9\circ\nu_{13}
```

### R48 #314（第5章 1949行）

- 判定案：`PROOF_INTERNAL_CANDIDATE`
- 帰属：原文文脈に基づく暫定判断
- 理由：証明の推論・計算・特殊化に属する可能性が高く、独立 Reference は保留。

```tex
\[
8x E\alpha^{\ast}=xE^{4}\sigma'''=E^4\sigma'''\ , \ (x:\text{odd}) .
\]
```

```text
1946: 以上から, \(8E\alpha^{\ast} - E^4\sigma''' \in 2E^4\pi_{12}(S^5)\) である. \\
1947: \(\pi_{12}^5=\pi_{12}(S^5;2)\cong\mathbb{Z}_2\) なので, 
1948: \(2E^4\pi_{12}(S^5)\) は奇数位数の有限群である. 
1949: \[
1950: 8x E\alpha^{\ast}=xE^{4}\sigma'''=E^4\sigma'''\ , \ (x:\text{odd}) .
1951: \]
1952: (5.14) とLem5.13 により, \(\pi_{13}^6\) と \(\pi_{14}^7\) 
1953: の位数は, それぞれ 4 と 8 であり, \\
1954: \(E^2:\pi_{12}^5\to\pi_{14}^7\) は単射である. \\
```


追加判断はいずれも未承認。既存番号付き命題への所属確認と原本照合後に登録判断する。
全体 pytest は Phase 最終段階のみ。
