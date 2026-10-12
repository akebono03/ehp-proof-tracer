# Phase 163 R4-R72：数学的役割の個別判定案

TeX 前後の文脈から作成した編集上の判定案。正式な数学的認定・Registry 登録ではない。

- 総候補：237件
- 個別判定案：34件
- 未判定：203件

|候補種別|件数|
|---|---:|
|ADJACENT_DEFINITION_EXTENSION|1|
|DEPENDENCY_CONTEXT_CANDIDATE|2|
|EXISTING_REFERENCE_COMPONENT|2|
|EXTERNALLY_SOURCED_ASSERTION_CANDIDATE|1|
|PROOF_INTERNAL_CANDIDATE|10|
|PROOF_LOCAL_CONSTRUCTION_CANDIDATE|4|
|SEPARATE_DEFINITION_CANDIDATE|5|
|UNNUMBERED_ASSERTION_CANDIDATE|9|
|UNREVIEWED|203|

## 個別判定案（原文付き）

### R48 #73（第1章 1109行）

候補：`EXISTING_REFERENCE_COMPONENT`。coextension の代表写像に課した条件式。既存 Reference の本文に含める。

```tex
\[
h(d_W(w, t)) \left\{
\begin{array}{ll}
= d'_X(c(w), 1-2t), & 0 \leq t \leq \frac{1}{2}, \\
\in Y, & \frac{1}{2} \leq t \leq 1. \\
\end{array}\right.
\]
```

文脈：

```text
1106: に対して, \(\widetilde{\gamma}\) を表す写像 
1107: \(h:EW\to Y\cup_\beta CX\)
1108: が, 次の条件を満たすとする.
1109: \[
1110: h(d_W(w, t)) \left\{
1111: \begin{array}{ll}
1112: = d'_X(c(w), 1-2t), & 0 \leq t \leq \frac{1}{2}, \\
1113: \in Y, & \frac{1}{2} \leq t \leq 1. \\
1114: \end{array}\right.
```

### R48 #275（第5章 571行）

候補：`EXISTING_REFERENCE_COMPONENT`。ν₄ の場合分けによる定義式。既存 Reference の本文に含める。

```tex
\[
\nu_{4}:=
\begin{cases}
\alpha^{\ast}-(-1)^{u}\,s[\iota_4,\iota_4] 
& (\text{if } 2E\alpha^{\ast}=E^{2}\nu'),\\[1mm]
-\alpha^{\ast}+(-1)^{u}(s+1)[\iota_4,\iota_4] 
& (\text{if } 2E\alpha^{\ast}=-E^{2}\nu').
\en
```

文脈：

```text
568: \(H[\iota_4,\iota_4]=(-1)^u 2\iota_7\) とし, 
569: \(\nu_4\) を次で定義する. 
570: (\([\iota_4,\iota_4]\) は Whitehead product)
571: \[
572: \nu_{4}:=
573: \begin{cases}
574: \alpha^{\ast}-(-1)^{u}\,s[\iota_4,\iota_4] 
575: & (\text{if } 2E\alpha^{\ast}=E^{2}\nu'),\\[1mm]
576: -\alpha^{\ast}+(-1)^{u}(s+1)[\iota_4,\iota_4] 
```

### R48 #5（第1章 173行）

候補：`ADJACENT_DEFINITION_EXTENSION`。f* と g* の定義。合成の定義の直後に連続し、出典境界の拡張を確認する。

```tex
\[
f^*:[Y,Z]\to[X,Z],\quad g_*:[X,Y]\to[X,Z].
\]
```

文脈：

```text
170: と書き, \(\alpha\) と \(\beta\) の合成 (composition) という.\\
171: 式 \(\beta\circ \alpha = f^*(\beta) = g_*(\alpha)\)
172: は, 次の写像を定義する.
173: \[
174: f^*:[Y,Z]\to[X,Z],\quad g_*:[X,Y]\to[X,Z].
175: \]
176: \[
177: f^*(\beta)=[g\circ f],\qquad g_*(\alpha)=[g\circ f]
178: \]
```

### R48 #21（第1章 336行）

候補：`SEPARATE_DEFINITION_CANDIDATE`。懸垂写像 Ef の作用式。次の加法・逆元の定義と混同しない。

```tex
\[
\Ex f(d_X(x, t)) = 
d_Y(f(x), t),\quad x\in X,\quad t \in I.
\]
```

文脈：

```text
333: 写像 $f:(X,x_0)\to(Y,y_0)$ に対し, 
334: その suspension $\Ex f:\Ex X\to \Ex Y$ はまた,
335: 次によっても定められる.
336: \[
337: \Ex f(d_X(x, t)) = 
338: d_Y(f(x), t),\quad x\in X,\quad t \in I.
339: \]
340: 
341: ホモトピー集合 \([EX, Y]\) を考える.\\
```

### R48 #40（第1章 545行）

候補：`SEPARATE_DEFINITION_CANDIDATE`。集合の合成 A∘B の記法の導入。secondary composition の定義とは別の概念。

```tex
\[
A\circ B=\{\ \alpha\circ\beta\mid \alpha\in A,\ \beta\in B\ \}
\]
```

文脈：

```text
542: 
543: ここで, 以下の記法を用いる. 
544: $A\subset[Y, Z]$, $B\subset[X, Y]$ に対し,
545: \[
546: A\circ B=\{\ \alpha\circ\beta\mid \alpha\in A,\ \beta\in B\ \}
547: \]
548: と書く. また, $A_1,A_2\subset[\Ex X, Y]$ に対し,
549: \[
550: A_1+A_2=\{\ \alpha_1+\alpha_2\mid \alpha_i\in A_i\ \}
```

### R48 #63（第1章 884行）

候補：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`。証明途中で使う自己同相 σ の具体式。恒久的定義としての独立登録は保留。

```tex
\[
\sigma(\phi_{V,S^{n+1}}(v,\psi_{n+1}(t_{1},\cdots,t_{n},t))) :=
\phi_{V,S^{n+1}}(v,\psi_{n+1}(1-t,t_{1},\cdots,t_{n})).
\]
```

文脈：

```text
881: \]
882: \(\sigma:\Ex^{n+1}V\to\Ex^{n+1}V \notag\)
883: を, 次で定義される同相写像とする.
884: \[
885: \sigma(\phi_{V,S^{n+1}}(v,\psi_{n+1}(t_{1},\cdots,t_{n},t))) :=
886: \phi_{V,S^{n+1}}(v,\psi_{n+1}(1-t,t_{1},\cdots,t_{n})).
887: \]
888: また, 写像 \(K:EV\to Y\) を次で定義する.
889: \[
```

### R48 #70（第1章 1056行）

候補：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`。H と H′ から証明中に構成する H′′。一般 Definition にしない。

```tex
\[
H''(\phi(w,\psi_2(s, t))) :=
\begin{cases}
H(\phi(w, \psi_2(2s, t))), & 0\le s\le \tfrac12,\\
H'(\phi(w, \psi_2(2s-1, t))), & \tfrac12\le s\le 1.
\end{cases}
\]
```

文脈：

```text
1053: 任意の \(H_0:(E^{n+1}W,w_0)\to(Z,z_0)\) に対して,
1054: \([H_0\circ\sigma] = -[H_0]\) である.\\
1055: $H'':(E^{n+1}W,w_0)\to(Z,z_0)$ を, 次で定義する.
1056: \[
1057: H''(\phi(w,\psi_2(s, t))) :=
1058: \begin{cases}
1059: H(\phi(w, \psi_2(2s, t))), & 0\le s\le \tfrac12,\\
1060: H'(\phi(w, \psi_2(2s-1, t))), & \tfrac12\le s\le 1.
1061: \end{cases}
```

### R48 #102（第2章 198行）

候補：`SEPARATE_DEFINITION_CANDIDATE`。(f)_t の点ごとの定義式。直前の写像の域・値域と合わせて扱う。

```tex
\[
(f)_t(y_1\ldots y_t):=f(y_1)\ldots f(y_t)
\]
```

文脈：

```text
195: (f)_t:\ (S^q)_t\longrightarrow(S^m)_t,\qquad (t=1,2,\ldots,\infty)
196: \]
197: を
198: \[
199: (f)_t(y_1\ldots y_t):=f(y_1)\ldots f(y_t)
200: \]
201: で定める. 明らかに $s\le t$ ならば $(f)_s=(f)_t\ |_{(S^q)_s}$ が成り立つ. 
202: 
203: 標準的な埋め込み $i:S^m\into\Omega S^{m+1}$ は,
```

### R48 #109（第2章 329行）

候補：`SEPARATE_DEFINITION_CANDIDATE`。combinatorial extension h の定義式。写像と係数の条件を一体で扱う。

```tex
\[
h(x_1\ldots x_t)\ 
:=\ \prod_{\sigma}\ h'\!\bigl(x_{\sigma(1)}\cdots x_{\sigma(k)}\bigr),
\]
```

文脈：

```text
326: h:\ (S^m)_\infty\ \longrightarrow\ (S^{km})_\infty
327: \]
328: は, 次式で定義される：
329: \[
330: h(x_1\ldots x_t)\ 
331: :=\ \prod_{\sigma}\ h'\!\bigl(x_{\sigma(1)}\cdots x_{\sigma(k)}\bigr),
332: \]
333: ここで, $\sigma$ は, 
334: $\{1,2,\ldots,k\}$ を, $\{1,2,\ldots,t\}$ へ, 
```

### R48 #125（第2章 649行）

候補：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`。mapping track X の具体的構成。後続の Serre fibration の議論に依存する。

```tex
\[
X := \gen{(\ell, x)\in Map(I, (S^{pm})_{\infty})\times (S^m)_{\infty}\ 
|\ \ell(1) = h(x)};\
h \text{ の mapping track} .
\]
```

文脈：

```text
646: \end{paracol}
647: 
648: \begin{paracol}{2}
649: \[
650: X := \gen{(\ell, x)\in Map(I, (S^{pm})_{\infty})\times (S^m)_{\infty}\ 
651: |\ \ell(1) = h(x)};\
652: h \text{ の mapping track} .
653: \]
654: \[
```

### R48 #126（第2章 654行）

候補：`PROOF_LOCAL_CONSTRUCTION_CANDIDATE`。mapping track の射影 p の具体的構成。後続の fibration 性質とは別。

```tex
\[
p:X\longrightarrow (S^{pm})_\infty,\qquad 
p(\ell,x):=\ell(1)=h(x),
\]
```

文脈：

```text
651: |\ \ell(1) = h(x)};\
652: h \text{ の mapping track} .
653: \]
654: \[
655: p:X\longrightarrow (S^{pm})_\infty,\qquad 
656: p(\ell,x):=\ell(1)=h(x),
657: \]
658: と定義すると, $(X,p,(S^{pm})_\infty)$ は Serre の意味での fibration になる [13]. \\
659: この fibration に付随するスペクトル列 $\{E_r^{s,t}\}$ を考える. 
```

### R48 #11（第1章 201行）

候補：`UNNUMBERED_ASSERTION_CANDIDATE`。smash product の結合性を表す自然同相。

```tex
\[
(A\ \wedge\ B)\ \wedge\ C\ \cong\ A\ \wedge\ (B\ \wedge\ C),
\]
```

文脈：

```text
198: A\times B/A\vee B = A\ \wedge\ B
199: \]
200: で表す. 3つの空間 $A,B,C$ に対して, 次の自然な同相がある.
201: \[
202: (A\ \wedge\ B)\ \wedge\ C\ \cong\ A\ \wedge\ (B\ \wedge\ C),
203: \]
204: \[
205: \phi_{A\wedge B, C}(\phi_{A,B}(a,b),c)\longleftrightarrow
206: \phi_{A,B\wedge C}(a, \phi_{B,C}(b,c)).
```

### R48 #25（第1章 364行）

候補：`UNNUMBERED_ASSERTION_CANDIDATE`。X が局所コンパクトなときの自然同型。適用条件の保持が必要。

```tex
\[
[\Ex X,Y]\cong \pi_1\bigl(Y^X_{0}\bigr).
\]
```

文脈：

```text
361: 実際, 
362: \(X\) が locally compact のとき,
363: これらは自然に同型となる.
364: \[
365: [\Ex X,Y]\cong \pi_1\bigl(Y^X_{0}\bigr).
366: \]
367: 次の事は容易に得られる.
368: 写像 $f:Y\to Z$ と $g:W\to X$ に対して, 次は準同型である.
369: \begin{equation}
```

### R48 #30（第1章 415行）

候補：`UNNUMBERED_ASSERTION_CANDIDATE`。ループ空間の操作が合成を保つという一般的関係。

```tex
\[
\Ox(\beta\circ\alpha)=\Ox\beta\circ \Ox\alpha
\]
```

文脈：

```text
412: \]
413: が得られる. 明らかに, 
414: $\Ox(g\circ f)=\Ox g\circ \Ox f$, および,
415: \[
416: \Ox(\beta\circ\alpha)=\Ox\beta\circ \Ox\alpha
417: \]
418: が成り立つ. 
419: 
420: $EX$ の loop 空間 $\Ox EX$ を考える. 各 $x\in X$ に対し,
```

### R48 #41（第1章 549行）

候補：`SEPARATE_DEFINITION_CANDIDATE`。部分集合の和 A₁+A₂ の記法。A∘B と同一 Reference とするか出典文脈要確認。

```tex
\[
A_1+A_2=\{\ \alpha_1+\alpha_2\mid \alpha_i\in A_i\ \}
\]
```

文脈：

```text
546: A\circ B=\{\ \alpha\circ\beta\mid \alpha\in A,\ \beta\in B\ \}
547: \]
548: と書く. また, $A_1,A_2\subset[\Ex X, Y]$ に対し,
549: \[
550: A_1+A_2=\{\ \alpha_1+\alpha_2\mid \alpha_i\in A_i\ \}
551: \]
552: とする. 
553: 
554: \begin{lemma}\label{lem:double-coset}
```

### R48 #52（第1章 661行）

候補：`PROOF_INTERNAL_CANDIDATE`。異なる null-homotopy による H と H′ の比較に現れる証明内関係式。

```tex
\[
H'\ \simeq\ F'\circ \Ex^{n+1}c\ +\ (H+a\circ \Ex^n G').
\]
```

文脈：

```text
658: \(a\circ E^n b,\ b\circ c\) の null homotopy が得られる.\\
659: この \(A'_t,\ B'_t\) を用いて, $H'$ を作ると,
660: 次が成り立つ.
661: \[
662: H'\ \simeq\ F'\circ \Ex^{n+1}c\ +\ (H+a\circ \Ex^n G').
663: \]
664: よって,
665: \([H]\)
666: の同じ double coset に属する任意の元は,
```

### R48 #65（第1章 916行）

候補：`PROOF_INTERNAL_CANDIDATE`。Prop1.4 の証明を閉じる包含式。既存命題の証明に属する。

```tex
\[
[a\circ E^n K\circ\sigma]
\in \todai[n]{\alpha, E^n\beta, E^n\gamma}\circ E^{n+1}\delta
\]
```

文脈：

```text
913: 上のような合成 \(a\circ E^n K\circ \sigma\)
914: で表される.\\
915: homotopy \(H_{1-u}\) を使うことにより,
916: \[
917: [a\circ E^n K\circ\sigma]
918: \in \todai[n]{\alpha, E^n\beta, E^n\gamma}\circ E^{n+1}\delta
919: \]
920: が示される.
921: 以上で, Prop1.4 の証明が完了した.
```

### R48 #94（第2章 92行）

候補：`UNNUMBERED_ASSERTION_CANDIDATE`。任意の整数 k に対する合成と倍数の関係式。

```tex
\[
k(\alpha\circ\beta)=\alpha\circ(k\beta),\qquad
k(\alpha\circ E\beta)=(k\alpha)\circ E\beta
\]
```

文脈：

```text
89: \end{aligned}
90: \end{equation}
91: 特に, 任意の整数 $k$ に対して,
92: \[
93: k(\alpha\circ\beta)=\alpha\circ(k\beta),\qquad
94: k(\alpha\circ E\beta)=(k\alpha)\circ E\beta
95: \]
96: が成り立つ. \\
97: $\alpha\in\pis{p}{S^m}$ と $\beta\in\pis{q}{S^n}$ の \emph{reduced join}
```

### R48 #96（第2章 104行）

候補：`UNNUMBERED_ASSERTION_CANDIDATE`。Eⁿα と reduced join の一般的な関係式。

```tex
\[
E^n\alpha=\alpha\ \redjoin\ \iota_n
\]
```

文脈：

```text
101: は, 第1章で導入した (1.3) の特別な写像 
102: $\phi_{p,q}$ と $\phi_{m,n}$ を用いて定義される. \\
103: 特に, $E^n$ の定義から次が成り立つ. 
104: \[
105: E^n\alpha=\alpha\ \redjoin\ \iota_n
106: \]
107: また \emph{secondary composition}
108: \[
109: \todai[n]{\alpha,\ E^n\beta,\ E^n\gamma}
```

### R48 #110（第2章 348行）

候補：`DEPENDENCY_CONTEXT_CANDIDATE`。Hopf 準同型の域と値域の表示。直前の定義と合わせる。

```tex
\[
H:\ \pi_{i+1}(S^{m+1})\ \longrightarrow\ \pi_{i+1}(S^{2m+1})
\]
```

文脈：

```text
345: \end{equation}
346: で定める. 
347: 特に, すべての $i$ について準同型,
348: \[
349: H:\ \pi_{i+1}(S^{m+1})\ \longrightarrow\ \pi_{i+1}(S^{2m+1})
350: \]
351: を得る. 
352: 
353: \begin{proposition}\label{prop:2.2}
```

### R48 #117（第2章 457行）

候補：`PROOF_INTERNAL_CANDIDATE`。Prop1.7 の適用から得る証明内包含式。

```tex
\[
(-1)^n H(\ext{\alpha})\circ E^n\coext{\gamma}\ \in\
\{\,H(\alpha),\ E^n\beta,\ E^n\gamma\,\}_n
\]
```

文脈：

```text
454: \]
455: が従い, $H(\overline\alpha)$ は $H(\alpha)$ の extension である. 
456: よってProp1.7 を再び用いると,
457: \[
458: (-1)^n H(\ext{\alpha})\circ E^n\coext{\gamma}\ \in\
459: \{\,H(\alpha),\ E^n\beta,\ E^n\gamma\,\}_n
460: \]
461: となり, 主張が従う. 
462: \qed
```

### R48 #118（第2章 509行）

候補：`PROOF_INTERNAL_CANDIDATE`。外部定理 [6] を引用する証明中での h* の表示。

```tex
\[
h_*:\ \pi_i\bigl((S^m)_\infty,(S^m)_{p-1}\bigr)\ \longrightarrow\ \pi_i\bigl((S^{pm})_\infty\bigr)
\]
```

文脈：

```text
506: \noindent
507: \textbf{Proof.}\
508: [6]のTh2 を用いれば, 
509: \[
510: h_*:\ \pi_i\bigl((S^m)_\infty,(S^m)_{p-1}\bigr)\ \longrightarrow\ \pi_i\bigl((S^{pm})_\infty\bigr)
511: \]
512: が, $i<(p+1)m-1$ に対して同型であることが従う. 
513: 
514: \switchcolumn
```

### R48 #119（第2章 552行）

候補：`UNNUMBERED_ASSERTION_CANDIDATE`。m が奇数の場合のコホモロジー積の関係式。偶数の場合も別 Assertion として確認。

```tex
\[
u_1\,u_{2k}=u_{2k+1},\qquad
u_{2k}\,u_{2h}=\binom{k+h}{k}\,u_{2(k+h)}.
\]
```

文脈：

```text
549: $H^{km}\bigl((S^m)_\infty\bigr)$ の生成元 $u_k$ を, 
550: $km$-cell $e^{km}$ に双対な元としてとると, 次が成り立つ：\\
551: $m$ が奇数のとき, 
552: \[
553: u_1\,u_{2k}=u_{2k+1},\qquad
554: u_{2k}\,u_{2h}=\binom{k+h}{k}\,u_{2(k+h)}.
555: \]
556: $m$ が偶数のとき, 
557: \[
```

### R48 #129（第2章 711行）

候補：`PROOF_INTERNAL_CANDIDATE`。スペクトル列を用いる推論中の i₁* 同型性。

```tex
\[
i_1^*:H^{i}(X;\Lambda)\ \longrightarrow\ H^{i}(F;\Lambda)
\]
```

文脈：

```text
708: \]
709: $\,i_1:F\hookrightarrow X$ を包含とする. このとき $i_0^*\circ i_1^*$ は $i^*$ に同値である. 
710: ゆえに,
711: \[
712: i_1^*:H^{i}(X;\Lambda)\ \longrightarrow\ H^{i}(F;\Lambda)
713: \]
714: は $i<pm$ に対して単射同型である. 
715: 
716: 
```

### R48 #139（第2章 907行）

候補：`DEPENDENCY_CONTEXT_CANDIDATE`。直前の Theorem の帰結。既存 Reference への接続を優先確認する。

```tex
\[
h_{m*}:\ \pi_i\bigl((S^m)_\infty,\ S^m\bigr)\ \longrightarrow\ \pi_i\bigl((S^{2m})_\infty\bigr)
\]
```

文脈：

```text
904: h_m:\ \bigl((S^m)_\infty,\ S^m\bigr)\ \longrightarrow\ \bigl((S^{2m})_\infty,\ e_0\bigr)
905: \]
906: は, 上のTh の条件を満たす. したがって,
907: \[
908: h_{m*}:\ \pi_i\bigl((S^m)_\infty,\ S^m\bigr)\ \longrightarrow\ \pi_i\bigl((S^{2m})_\infty\bigr)
909: \]
910: は, $m$ が奇数なら全ての $i$ で同型, $m$ が偶数なら
911: 2-primary 成分について全ての $i$ で同型. \\
912: また, $m$ が偶数で \(i<(3m-1)\) のとき同型である.
```

### R48 #149（第2章 1297行）

候補：`UNNUMBERED_ASSERTION_CANDIDATE`。偶数 n における Whitehead square の Hopf 不変量の既知事実。

```tex
\[
H[\,\iota_n,\ \iota_n\,]\ =\ \pm\,2\,\iota_{2n-1}
\]
```

文脈：

```text
1294: \qed
1295: 
1296: 最後に, よく知られている事実として, $n$ が偶数のとき, 
1297: \[
1298: H[\,\iota_n,\ \iota_n\,]\ =\ \pm\,2\,\iota_{2n-1}
1299: \]
1300: が成り立つ. これとProp \ref{prop:2.5} から直ちに次が成り立つ. 
1301: 
1302: \begin{proposition}\label{prop:2.7}
```

### R48 #255（第4章 281行）

候補：`PROOF_INTERNAL_CANDIDATE`。EHP 完全列の証明で提示した列の一部。

```tex
\[
\cdots\to\pit{n}{n}\xrightarrow{E}\pit{n+1}{n+1}\to\cdots
\]
```

文脈：

```text
278: が現れない箇所は, \\
279: \eqref{4.1} と,
280: $\Ex:\pis{n}{S^n}\xrightarrow{\cong}\pis{n+1}{S^{n+1}}$ が同型である事実から,
281: \[
282: \cdots\to\pit{n}{n}\xrightarrow{E}\pit{n+1}{n+1}\to\cdots
283: \]
284: の完全性を得る. 
285: 残る問題は,
286: \[
```

### R48 #257（第4章 454行）

候補：`EXTERNALLY_SOURCED_ASSERTION_CANDIDATE`。n=2,4,8 と任意の i の Hopf fibration 由来の同型。Steenrod を出典とする。

```tex
\[
E+h_*:\ \pis{i-1}{S^{n-1}}\oplus\pis{i}{S^{2n-1}}
\ \xrightarrow{\ \cong\ }\ \pis{i}{S^n}
\]
```

文脈：

```text
451: \noindent
452: $n=2,4,8$ のとき, Hopf fibration
453: $S^n\hookrightarrow S^{2n-1}\xrightarrow{h} S^n$ が存在し, これに付随して,
454: \[
455: E+h_*:\ \pis{i-1}{S^{n-1}}\oplus\pis{i}{S^{2n-1}}
456: \ \xrightarrow{\ \cong\ }\ \pis{i}{S^n}
457: \]
458: が, 任意の \(i\) で同型になることが知られている \cite{Steenrod1951}.\\
459: これは, $h$ を Hopf 不変量 $\pm1$ を持つ写像に置き換えても成り立つ. \\
```

### R48 #274（第5章 542行）

候補：`PROOF_INTERNAL_CANDIDATE`。(5.4) の証明中に Prop1.3 と (1.15) を用いる包含計算。

```tex
\begin{align*}
E^{\,n-3}\nu'\in E^{\,n-3}\todai[1]{\eta_3,\,2\iota_{4},\,\eta_4}
& \subset(-1)^{n-3}\todai[n-2]{\eta_n, 2\iota_{n+1}, \eta_{n+1}}\\
& \subset(-1)^{n-3}\todai[t]{\eta_n, 2\iota_{n+1}, \eta_{n+1}}
\end{
```

文脈：

```text
539: 
540: \noindent
541: \(\nu'\) の定義, Prop 1.3, (1.15) から, 
542: \begin{align*}
543: E^{\,n-3}\nu'\in E^{\,n-3}\todai[1]{\eta_3,\,2\iota_{4},\,\eta_4}
544: & \subset(-1)^{n-3}\todai[n-2]{\eta_n, 2\iota_{n+1}, \eta_{n+1}}\\
545: & \subset(-1)^{n-3}\todai[t]{\eta_n, 2\iota_{n+1}, \eta_{n+1}}
546: \end{align*}
547: が従うので, \(t\ge1\) で (5.4) が成立する. \\
```

### R48 #280（第5章 867行）

候補：`PROOF_INTERNAL_CANDIDATE`。特定のホモトピー群に対する Prop の証明に現れる EHP 列。

```tex
\[
\pi^{9}_{10}\xrightarrow{\ \Delta\ }\pi^{9}_{8}\xrightarrow{\ E\ }\pi^{5}_{9}
\xrightarrow{\ H }\pi^{9}_{9}\xrightarrow{\ \Delta\ }\pi^{4}_{7}
\]
```

文脈：

```text
864: \textbf{Proof.}\ 
865: \(\pi_8^4\) に対する結果は, (5.6) とProp5.1 から従う. 
866: (4.4) の完全列
867: \[
868: \pi^{9}_{10}\xrightarrow{\ \Delta\ }\pi^{9}_{8}\xrightarrow{\ E\ }\pi^{5}_{9}
869: \xrightarrow{\ H }\pi^{9}_{9}\xrightarrow{\ \Delta\ }\pi^{4}_{7}
870: \]
871: を考える. (5.8) とProp5.6 により, \(\Delta:\pi_9^9\to\pi_7^4\) は単射である. \\
872: よって, 完全性から, \(E\) は全射となることが分かる. \\
```

### R48 #287（第5章 1083行）

候補：`PROOF_INTERNAL_CANDIDATE`。Prop の証明中に Prop2.2 と (5.3) を適用する計算。

```tex
\[
H(\nu'\circ \eta_6^2)=H(\nu')\circ \eta_6^2=\eta_5\circ \eta_6^2=\eta_5^{3}.
\]
```

文脈：

```text
1080: は完全列である. 
1081: Lem5.7, Prop 5.6, (5.5) により, \(\ker\Delta\) は \(4\nu_5=\eta_5^3\) で生成される. \\
1082: Prop2.2 と (5.3) により, 次を得る. 
1083: \[
1084: H(\nu'\circ \eta_6^2)=H(\nu')\circ \eta_6^2=\eta_5\circ \eta_6^2=\eta_5^{3}.
1085: \]
1086: よって, 完全性から, Propの2番目が成り立つ. \\
1087: (5.6) により, \(\pi_9^4\) の結果を得る. 
1088: 
```

### R48 #290（第5章 1201行）

候補：`PROOF_INTERNAL_CANDIDATE`。Prop の証明末尾の完全列と消滅の帰結。

```tex
\[
\pi^{13}_{13}\xrightarrow[\cong]{\Delta}\pi^{6}_{11}\xrightarrow{E}\pi^{7}_{12}\xrightarrow{}\pi_{12}^{13}=0
\]
```

文脈：

```text
1198: Prop5.8 と (5.10) により, \(\Delta\) は全射で, \(\ker\Delta=\gen{2\iota_{11}}\) である. \\
1199: Prop2.7 により, \(H(\Delta(\iota_{13}))=\pm2\iota_{11}\) なので, 
1200: \(\pi_{11}^6=\mathbb Z \gen{\Delta(\iota_{13})}\) である. 
1201: \[
1202: \pi^{13}_{13}\xrightarrow[\cong]{\Delta}\pi^{6}_{11}\xrightarrow{E}\pi^{7}_{12}\xrightarrow{}\pi_{12}^{13}=0
1203: \]
1204: の完全性により, \(\pi_{12}^7=0\) である. 
1205: (4.5) により, Propの最後の結果が得られる. 
1206: \qed
```

### R48 #7（第1章 180行）

候補：`UNNUMBERED_ASSERTION_CANDIDATE`。合成の結合律を述べる番号なしの一般的関係式。

```tex
\[
(\gamma\circ \beta)\circ\alpha=\gamma\circ(\beta\circ\alpha).
\]
```

文脈：

```text
177: f^*(\beta)=[g\circ f],\qquad g_*(\alpha)=[g\circ f]
178: \]
179: 明らかに, 合成は結合的である. 
180: \[
181: (\gamma\circ \beta)\circ\alpha=\gamma\circ(\beta\circ\alpha).
182: \]
183: \[
184: (f_2\circ f_1)^*=f_1^*\circ f_2^*,\quad 
185: (g_2\circ g_1)_*=g_{2*}\circ g_{1*}.
```

### R48 #8（第1章 183行）

候補：`UNNUMBERED_ASSERTION_CANDIDATE`。誘導写像の合成に関する関手性の関係式。

```tex
\[
(f_2\circ f_1)^*=f_1^*\circ f_2^*,\quad 
(g_2\circ g_1)_*=g_{2*}\circ g_{1*}.
\]
```

文脈：

```text
180: \[
181: (\gamma\circ \beta)\circ\alpha=\gamma\circ(\beta\circ\alpha).
182: \]
183: \[
184: (f_2\circ f_1)^*=f_1^*\circ f_2^*,\quad 
185: (g_2\circ g_1)_*=g_{2*}\circ g_{1*}.
186: \]
187: 
188: 
```

## 登録境界

Math role 認定、Original edition 照合、ID 採番、Registry 変更、proof search 接続はいずれも行っていない。
全体 pytest は Phase 163 の最後に実施する。
