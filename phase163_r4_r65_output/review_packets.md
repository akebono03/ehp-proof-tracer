# Phase 163 R4-R65 境界確認パケット

暫定的な原文抜粋です。数学的確認・原本照合・正式登録は実施していません。

分類: 通常9件／外部文脈5件／隣接記法2件。

## 外部文脈の確認が必要

### composition_homotopy_classes（第1章、Toda_01_corrected.tex:163–170）

Assertion 候補: beta circ alpha

```tex
$\alpha\in[X,Y]$, $\beta\in[Y,Z]$ に対して,
それぞれの代表写像を $f:X\to Y$, $g:Y\to Z$ とするとき, \\
合成
\(g\circ f\) は \([X,Z]\) の元を表し,
\(f, g\) の選び方によらない.\\
\(g\circ f\) の類を
\(\beta\circ \alpha \in [X,Z]\)
と書き, \(\alpha\) と \(\beta\) の合成 (composition) という.\\
```

判定: 未確認。確認事項: Reference の境界と Assertion 分割が数学的に妥当か。

### secondary_composition（第1章、Toda_01_corrected.tex:535–540）

Assertion 候補: secondary composition

```tex
\emph{secondary composition}
\[
\{\alpha,\ \Ex^n\beta,\ \Ex^n\gamma\}_n\ \subset\ [\Ex^{n+1}W, Z]
\]
を, 上の方法で得られる写像 $H$ の, 
ホモトピー類全体の集合として定める. 
```

判定: 未確認。確認事項: Reference の境界と Assertion 分割が数学的に妥当か。

### extension（第1章、Toda_01_corrected.tex:1099–1103）

Assertion 候補: extension alpha

```tex
\(\overline{\alpha}\in[Y\cup_\beta CX, Z]\)
は, \(\overline{\alpha}\) を表す写像 \(g\)
に対して, 
制限 \(g|_{Y}\) が \(\alpha\in[Y,Z]\) を表すとき,\\
$\alpha$ の \emph{extension} と呼ぶ.
```

判定: 未確認。確認事項: Reference の境界と Assertion 分割が数学的に妥当か。

### coextension（第1章、Toda_01_corrected.tex:1105–1117）

Assertion 候補: coextension gamma

```tex
\(\widetilde{\gamma}\in[EW,Y\cup_\beta CX]\)
に対して, \(\widetilde{\gamma}\) を表す写像 
\(h:EW\to Y\cup_\beta CX\)
が, 次の条件を満たすとする.
\[
h(d_W(w, t)) \left\{
\begin{array}{ll}
= d'_X(c(w), 1-2t), & 0 \leq t \leq \frac{1}{2}, \\
\in Y, & \frac{1}{2} \leq t \leq 1. \\
\end{array}\right.
\]
ここで, \(c:W\to X\) は \(\gamma\in[W,X]\) を表す写像とする.
このとき, \(\widetilde{\gamma}\) を \(\gamma\) の \emph{coextension} と呼ぶ.\\
```

判定: 未確認。確認事項: Reference の境界と Assertion 分割が数学的に妥当か。

### stable_toda_bracket（第3章、Toda_03_2(2).tex:1236–1266）

Assertion 候補: stable Toda bracket

```tex
\[
\alpha\in G_k,\quad \beta\in G_h,\quad \gamma\in G_\ell,\qquad
\alpha\circ\beta=\beta\circ\gamma=0
\]
に対する, stable Toda bracket 
\[
\langle \alpha,\beta,\gamma\rangle 
\in G_{k+h+\ell+1}(\alpha\circ G_{h+\ell+1} + \gamma\circ G_{k+h+1}) .
\]
を以下の様に定義する. 
十分大きな $n$ をとれば, 
\[
\alpha'\in\pis{n+k}{S^n},\ 
\beta'\in\pis{n+k+h}{S^{n+k}},\
\gamma'\in\pis{n+k+h+\ell}{S^{n+k+h}}
\]
が存在して, 
\(
\alpha=\Ex^\infty\alpha',\
\beta=\Ex^\infty\beta',\
\gamma=\Ex^\infty\gamma'
\)
と書ける. \\
このとき, 
\(\langle \alpha,\beta,\gamma\rangle\)
を, 次で定義する.
\[
\langle \alpha,\beta,\gamma\rangle
\ :=\ \Ex^\infty (-1)^{\,n-1}\ \toda{\alpha',\beta',\gamma'}.
\]
Prop1.3 により, この定義は $n$ によらず well-defined である. 
```

判定: 未確認。確認事項: Reference の境界と Assertion 分割が数学的に妥当か。

## 隣接する記法との境界確認が必要

### nu_n_notation（第5章、Toda_05_2(6).tex:605–607）

Assertion 候補: nu_n, nu

```tex
\[
\nu_n:=E^{\,n-4}\nu_{4},\ (n\ge 4),\qquad \nu:=E^{\infty}\nu_{4}
\]
```

判定: 未確認。確認事項: Reference の境界と Assertion 分割が数学的に妥当か。

### eta_n_cubed_notation（第5章、Toda_05_2(6).tex:608–612）

Assertion 候補: eta_n^3, eta^3

```tex
\[
\eta^{3}_{n}:=\eta_{n}\circ\eta_{n+1}\circ\eta_{n+2},\ (n\ge2),\qquad
\eta^{3}:=\eta\circ\eta\circ\eta .
\]
と記す.
```

判定: 未確認。確認事項: Reference の境界と Assertion 分割が数学的に妥当か。

## 原文の当該範囲内で確認可能な候補

### unit_sphere（第1章、Toda_01_corrected.tex:80–83）

Assertion 候補: S^n

```tex
$(n+1)$ 次元ユークリッド空間内の単位 $n$–球面を, 次で表す.
\[
S^n=\{(t_1,\ldots,t_{n+1})\mid t_1^2+\cdots+t_{n+1}^2=1\}.
\]
```

判定: 未確認。確認事項: Reference の境界と Assertion 分割が数学的に妥当か。

### pointed_homotopy_classes（第1章、Toda_01_corrected.tex:155–159）

Assertion 候補: [X,Y]

```tex
写像 $f:(X,x_0)\to (Y,y_0)$ の (基点付き) ホモトピー類の集合を,
\[
[X,Y]=\{\, [f]\ \mid\ f:(X,x_0)\to (Y,y_0)\,\}
\]
で表す. 特に, $X=S^n$ のとき,
```

判定: 未確認。確認事項: Reference の境界と Assertion 分割が数学的に妥当か。

### iterated_suspension（第1章、Toda_01_corrected.tex:283–288）

Assertion 候補: E^n X

```tex
空間 $X$ と $S^n$ の reduced join を,
\[
\Ex^n X\ :=\ X\ \wedge\ S^n
\]
と書き, $X$ の $n$-重 suspension と呼ぶ. 
特に, $n=1$ のときは, 単に $\Ex X=X\ \wedge\ S^1$ と書く. \\
```

判定: 未確認。確認事項: Reference の境界と Assertion 分割が数学的に妥当か。

### addition_inverse_suspension（第1章、Toda_01_corrected.tex:341–354）

Assertion 候補: f+g, -f

```tex
ホモトピー集合 \([EX, Y]\) を考える.\\
写像 $f,g:(\Ex X,x_0)\to(Y,y_0)$ に対し, 
\(f+g,\ -f: (EX,x_0)\to (Y,y_0)\) を, 次で定義する.
\[
(f+g)(d_X(x,t)) :=
\begin{cases}
f(d_X(x,2t)), & 0\le t\le \tfrac12,\\[2mm]
g(d_X(x,2t-1)), & \tfrac12\le t\le 1,
\end{cases}
\]
\[
(-f)(d_X(x, t)) := 
f(d_X(x, 1-t)).
\]
```

判定: 未確認。確認事項: Reference の境界と Assertion 分割が数学的に妥当か。

### reduced_cone（第1章、Toda_01_corrected.tex:1084–1087）

Assertion 候補: CX

```tex
基空間 $X$ 上の \emph{cone} \(CX\) を, 次で定義する.
\[
CX=(X\times I)/\bigl(X\times\{1\}\ \cup\ x_0\times I\bigr).
\]
```

判定: 未確認。確認事項: Reference の境界と Assertion 分割が数学的に妥当か。

### stable_homotopy_group（第3章、Toda_03_2(2).tex:1199–1206）

Assertion 候補: G_k, E^infty

```tex
球面の $k$ 次安定ホモトピー群を
\[
G_k\ :=\ \lim_{n\to\infty}\ \pis{n+k}{S^n}
\]
と書き, 射影を
\[
\Ex^\infty:\ \pis{n+k}{S^n}\ \longrightarrow\ G_k
\]
```

判定: 未確認。確認事項: Reference の境界と Assertion 分割が数学的に妥当か。

### stable_composition（第3章、Toda_03_2(2).tex:1214–1221）

Assertion 候補: composition on G

```tex
(1.6) より,
\(\Ex^{m}(\alpha\circ\beta)=\Ex^{m}\alpha\circ\Ex^{m}\beta\)
なので, 合成
\[
\circ:G_k\times G_h \rightarrow G_{k+h}
\]
が, \(E^\infty(\alpha\circ\beta)=E^\infty\alpha\circ E^\infty\beta\) 
により定義される. \\
```

判定: 未確認。確認事項: Reference の境界と Assertion 分割が数学的に妥当か。

### nu4_generator_notation（第5章、Toda_05_2(6).tex:567–579）

Assertion 候補: nu_4

```tex
そこで,
\(H[\iota_4,\iota_4]=(-1)^u 2\iota_7\) とし, 
\(\nu_4\) を次で定義する. 
(\([\iota_4,\iota_4]\) は Whitehead product)
\[
\nu_{4}:=
\begin{cases}
\alpha^{\ast}-(-1)^{u}\,s[\iota_4,\iota_4] 
& (\text{if } 2E\alpha^{\ast}=E^{2}\nu'),\\[1mm]
-\alpha^{\ast}+(-1)^{u}(s+1)[\iota_4,\iota_4] 
& (\text{if } 2E\alpha^{\ast}=-E^{2}\nu').
\end{cases}
\]
```

判定: 未確認。確認事項: Reference の境界と Assertion 分割が数学的に妥当か。

### nu_n_squared_notation（第5章、Toda_05_2(6).tex:1320–1323）

Assertion 候補: nu_n^2, nu^2

```tex
\[
\nu_n^2:=\nu_n\circ\nu_{n+3},(n\ge4)\qquad
\nu^2:=\nu\circ\nu.
\]
```

判定: 未確認。確認事項: Reference の境界と Assertion 分割が数学的に妥当か。

正式 ID、証明探索との接続は次段階以降。
全体 pytest は Phase 終了時のみ実施。
