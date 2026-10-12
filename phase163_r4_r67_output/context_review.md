# Phase 163 R4-R67：出典前後の確認資料

10件の暫定範囲について前後の TeX を示す。太字等による自動承認は行わない。

## pointed_homotopy_classes（第1章）

出典: `Toda_01_corrected.tex`、元の範囲: 155–159、確認表示: 141–173

保留理由: TRAILING_SENTENCE_OUTSIDE_SPAN

```text
  141 [BEFORE  ] と
  142 [BEFORE  ] \(s_{j+1}\)
  143 [BEFORE  ] が置き換わる.
  144 [BEFORE  ] 
  145 [BEFORE  ] 以後, 本書では各位相空間 $X$ に対し, 
  146 [BEFORE  ] 基点 $x_0\in X$ を固定しておき, 球面の場合は $e_0\in S^n$ を基点にとる. \\
  147 [BEFORE  ] 全ての写像と homotopy は基点を保つものとする.\\
  148 [BEFORE  ] i.e.
  149 [BEFORE  ] 写像 \(f:X\to Y\),
  150 [BEFORE  ]  homotopy  \(H:X\times I\to Y\)
  151 [BEFORE  ] は, 条件 
  152 [BEFORE  ] \(f(x_0) = y_0\), 
  153 [BEFORE  ] \(H(x_0, t) = y_0,\ (t\in I)\)
  154 [BEFORE  ] を満たす.\\
  155 [ORIGINAL] 写像 $f:(X,x_0)\to (Y,y_0)$ の (基点付き) ホモトピー類の集合を,
  156 [ORIGINAL] \[
  157 [ORIGINAL] [X,Y]=\{\, [f]\ \mid\ f:(X,x_0)\to (Y,y_0)\,\}
  158 [ORIGINAL] \]
  159 [ORIGINAL] で表す. 特に, $X=S^n$ のとき,
  160 [AFTER   ] $[X,Y]$ は通常の $n$ 次ホモトピー群 $\pi_n(Y)$ と一致する. 
  161 [AFTER   ] 
  162 [AFTER   ] % \subsection*{合成 (composition) }
  163 [AFTER   ] $\alpha\in[X,Y]$, $\beta\in[Y,Z]$ に対して,
  164 [AFTER   ] それぞれの代表写像を $f:X\to Y$, $g:Y\to Z$ とするとき, \\
  165 [AFTER   ] 合成
  166 [AFTER   ] \(g\circ f\) は \([X,Z]\) の元を表し,
  167 [AFTER   ] \(f, g\) の選び方によらない.\\
  168 [AFTER   ] \(g\circ f\) の類を
  169 [AFTER   ] \(\beta\circ \alpha \in [X,Z]\)
  170 [AFTER   ] と書き, \(\alpha\) と \(\beta\) の合成 (composition) という.\\
  171 [AFTER   ] 式 \(\beta\circ \alpha = f^*(\beta) = g_*(\alpha)\)
  172 [AFTER   ] は, 次の写像を定義する.
  173 [AFTER   ] \[
```

判断欄（未決定）：このまま／範囲拡張／文献項目分割／追加調査

## composition_homotopy_classes（第1章）

出典: `Toda_01_corrected.tex`、元の範囲: 163–170、確認表示: 149–184

保留理由: CONTEXT_FOR_COMPOSITION

```text
  149 [BEFORE  ] 写像 \(f:X\to Y\),
  150 [BEFORE  ]  homotopy  \(H:X\times I\to Y\)
  151 [BEFORE  ] は, 条件 
  152 [BEFORE  ] \(f(x_0) = y_0\), 
  153 [BEFORE  ] \(H(x_0, t) = y_0,\ (t\in I)\)
  154 [BEFORE  ] を満たす.\\
  155 [BEFORE  ] 写像 $f:(X,x_0)\to (Y,y_0)$ の (基点付き) ホモトピー類の集合を,
  156 [BEFORE  ] \[
  157 [BEFORE  ] [X,Y]=\{\, [f]\ \mid\ f:(X,x_0)\to (Y,y_0)\,\}
  158 [BEFORE  ] \]
  159 [BEFORE  ] で表す. 特に, $X=S^n$ のとき,
  160 [BEFORE  ] $[X,Y]$ は通常の $n$ 次ホモトピー群 $\pi_n(Y)$ と一致する. 
  161 [BEFORE  ] 
  162 [BEFORE  ] % \subsection*{合成 (composition) }
  163 [ORIGINAL] $\alpha\in[X,Y]$, $\beta\in[Y,Z]$ に対して,
  164 [ORIGINAL] それぞれの代表写像を $f:X\to Y$, $g:Y\to Z$ とするとき, \\
  165 [ORIGINAL] 合成
  166 [ORIGINAL] \(g\circ f\) は \([X,Z]\) の元を表し,
  167 [ORIGINAL] \(f, g\) の選び方によらない.\\
  168 [ORIGINAL] \(g\circ f\) の類を
  169 [ORIGINAL] \(\beta\circ \alpha \in [X,Z]\)
  170 [ORIGINAL] と書き, \(\alpha\) と \(\beta\) の合成 (composition) という.\\
  171 [AFTER   ] 式 \(\beta\circ \alpha = f^*(\beta) = g_*(\alpha)\)
  172 [AFTER   ] は, 次の写像を定義する.
  173 [AFTER   ] \[
  174 [AFTER   ] f^*:[Y,Z]\to[X,Z],\quad g_*:[X,Y]\to[X,Z].
  175 [AFTER   ] \]
  176 [AFTER   ] \[
  177 [AFTER   ] f^*(\beta)=[g\circ f],\qquad g_*(\alpha)=[g\circ f]
  178 [AFTER   ] \]
  179 [AFTER   ] 明らかに, 合成は結合的である. 
  180 [AFTER   ] \[
  181 [AFTER   ] (\gamma\circ \beta)\circ\alpha=\gamma\circ(\beta\circ\alpha).
  182 [AFTER   ] \]
  183 [AFTER   ] \[
  184 [AFTER   ] (f_2\circ f_1)^*=f_1^*\circ f_2^*,\quad 
```

判断欄（未決定）：このまま／範囲拡張／文献項目分割／追加調査

## secondary_composition（第1章）

出典: `Toda_01_corrected.tex`、元の範囲: 535–540、確認表示: 521–554

保留理由: PRECEDING_CONSTRUCTION_REQUIRED

```text
  521 [BEFORE  ] H(d(w,t))=
  522 [BEFORE  ] \begin{cases}
  523 [BEFORE  ] a\bigl(\Ex^n B_{2t-1}(w)\bigr), & \tfrac12\le t\le 1,\\[2mm]
  524 [BEFORE  ] A_{1-2t}\bigl(\Ex^n c(w)\bigr), & 0\le t\le \tfrac12.
  525 [BEFORE  ] \end{cases}
  526 [BEFORE  ] \end{equation}
  527 [BEFORE  ] ここで,
  528 [BEFORE  ] $d:\Ex^n W\times I\to \Ex^{n+1}W$ は,
  529 [BEFORE  ] \(E^{n+1}W= E(E^n W)\) を定める等化写像で, 
  530 [BEFORE  ] $w\in \Ex^n W$ とする.\\
  531 [BEFORE  ] $H$ は well-defined で, 連続であり, 
  532 [BEFORE  ] $A_t,B_t$ の取り方と, $a,b,c$ に依存する. 
  533 [BEFORE  ] 
  534 [BEFORE  ] %\begin{definition}
  535 [ORIGINAL] \emph{secondary composition}
  536 [ORIGINAL] \[
  537 [ORIGINAL] \{\alpha,\ \Ex^n\beta,\ \Ex^n\gamma\}_n\ \subset\ [\Ex^{n+1}W, Z]
  538 [ORIGINAL] \]
  539 [ORIGINAL] を, 上の方法で得られる写像 $H$ の, 
  540 [ORIGINAL] ホモトピー類全体の集合として定める. 
  541 [AFTER   ] %\end{definition}
  542 [AFTER   ] 
  543 [AFTER   ] ここで, 以下の記法を用いる. 
  544 [AFTER   ] $A\subset[Y, Z]$, $B\subset[X, Y]$ に対し,
  545 [AFTER   ] \[
  546 [AFTER   ] A\circ B=\{\ \alpha\circ\beta\mid \alpha\in A,\ \beta\in B\ \}
  547 [AFTER   ] \]
  548 [AFTER   ] と書く. また, $A_1,A_2\subset[\Ex X, Y]$ に対し,
  549 [AFTER   ] \[
  550 [AFTER   ] A_1+A_2=\{\ \alpha_1+\alpha_2\mid \alpha_i\in A_i\ \}
  551 [AFTER   ] \]
  552 [AFTER   ] とする. 
  553 [AFTER   ] 
  554 [AFTER   ] \begin{lemma}\label{lem:double-coset}
```

判断欄（未決定）：このまま／範囲拡張／文献項目分割／追加調査

## extension（第1章）

出典: `Toda_01_corrected.tex`、元の範囲: 1099–1103、確認表示: 1085–1117

保留理由: ATTACHING_SPACE_CONTEXT_REQUIRED

```text
 1085 [BEFORE  ] \[
 1086 [BEFORE  ] CX=(X\times I)/\bigl(X\times\{1\}\ \cup\ x_0\times I\bigr).
 1087 [BEFORE  ] \]
 1088 [BEFORE  ] $d'_X:X\times I\to CX$ を, \(CX\) を定義する等化写像とする.\\
 1089 [BEFORE  ] 対応 $x\longleftrightarrow d'_X(x,0)$ により, 
 1090 [BEFORE  ] $X$ と $d'_X(X\times {0})$ を同一視する. 
 1091 [BEFORE  ] 
 1092 [BEFORE  ] $\beta\in[X, Y]$ と, その代表 $f:(X,x_0)\to(Y,y_0)$ を考える.\\
 1093 [BEFORE  ] \(CX\) と \(Y\) の disjoint union \(Y \sqcup CX\)
 1094 [BEFORE  ] において, \\
 1095 [BEFORE  ] \(X\) と \(f\) による像を同一視した空間を,
 1096 [BEFORE  ] \(Y\cup_f CX\) または, \(Y\cup_\beta CX\) で表す.\\
 1097 [BEFORE  ] $Y\cup_f CX$ のホモトピー型は, \(\beta\) の代表 $f$ の選び方によらない. 
 1098 [BEFORE  ] 
 1099 [ORIGINAL] \(\overline{\alpha}\in[Y\cup_\beta CX, Z]\)
 1100 [ORIGINAL] は, \(\overline{\alpha}\) を表す写像 \(g\)
 1101 [ORIGINAL] に対して, 
 1102 [ORIGINAL] 制限 \(g|_{Y}\) が \(\alpha\in[Y,Z]\) を表すとき,\\
 1103 [ORIGINAL] $\alpha$ の \emph{extension} と呼ぶ.
 1104 [AFTER   ] 
 1105 [AFTER   ] \(\widetilde{\gamma}\in[EW,Y\cup_\beta CX]\)
 1106 [AFTER   ] に対して, \(\widetilde{\gamma}\) を表す写像 
 1107 [AFTER   ] \(h:EW\to Y\cup_\beta CX\)
 1108 [AFTER   ] が, 次の条件を満たすとする.
 1109 [AFTER   ] \[
 1110 [AFTER   ] h(d_W(w, t)) \left\{
 1111 [AFTER   ] \begin{array}{ll}
 1112 [AFTER   ] = d'_X(c(w), 1-2t), & 0 \leq t \leq \frac{1}{2}, \\
 1113 [AFTER   ] \in Y, & \frac{1}{2} \leq t \leq 1. \\
 1114 [AFTER   ] \end{array}\right.
 1115 [AFTER   ] \]
 1116 [AFTER   ] ここで, \(c:W\to X\) は \(\gamma\in[W,X]\) を表す写像とする.
 1117 [AFTER   ] このとき, \(\widetilde{\gamma}\) を \(\gamma\) の \emph{coextension} と呼ぶ.\\
```

判断欄（未決定）：このまま／範囲拡張／文献項目分割／追加調査

## coextension（第1章）

出典: `Toda_01_corrected.tex`、元の範囲: 1105–1117、確認表示: 1091–1131

保留理由: ATTACHING_SPACE_CONTEXT_REQUIRED

```text
 1091 [BEFORE  ] 
 1092 [BEFORE  ] $\beta\in[X, Y]$ と, その代表 $f:(X,x_0)\to(Y,y_0)$ を考える.\\
 1093 [BEFORE  ] \(CX\) と \(Y\) の disjoint union \(Y \sqcup CX\)
 1094 [BEFORE  ] において, \\
 1095 [BEFORE  ] \(X\) と \(f\) による像を同一視した空間を,
 1096 [BEFORE  ] \(Y\cup_f CX\) または, \(Y\cup_\beta CX\) で表す.\\
 1097 [BEFORE  ] $Y\cup_f CX$ のホモトピー型は, \(\beta\) の代表 $f$ の選び方によらない. 
 1098 [BEFORE  ] 
 1099 [BEFORE  ] \(\overline{\alpha}\in[Y\cup_\beta CX, Z]\)
 1100 [BEFORE  ] は, \(\overline{\alpha}\) を表す写像 \(g\)
 1101 [BEFORE  ] に対して, 
 1102 [BEFORE  ] 制限 \(g|_{Y}\) が \(\alpha\in[Y,Z]\) を表すとき,\\
 1103 [BEFORE  ] $\alpha$ の \emph{extension} と呼ぶ.
 1104 [BEFORE  ] 
 1105 [ORIGINAL] \(\widetilde{\gamma}\in[EW,Y\cup_\beta CX]\)
 1106 [ORIGINAL] に対して, \(\widetilde{\gamma}\) を表す写像 
 1107 [ORIGINAL] \(h:EW\to Y\cup_\beta CX\)
 1108 [ORIGINAL] が, 次の条件を満たすとする.
 1109 [ORIGINAL] \[
 1110 [ORIGINAL] h(d_W(w, t)) \left\{
 1111 [ORIGINAL] \begin{array}{ll}
 1112 [ORIGINAL] = d'_X(c(w), 1-2t), & 0 \leq t \leq \frac{1}{2}, \\
 1113 [ORIGINAL] \in Y, & \frac{1}{2} \leq t \leq 1. \\
 1114 [ORIGINAL] \end{array}\right.
 1115 [ORIGINAL] \]
 1116 [ORIGINAL] ここで, \(c:W\to X\) は \(\gamma\in[W,X]\) を表す写像とする.
 1117 [ORIGINAL] このとき, \(\widetilde{\gamma}\) を \(\gamma\) の \emph{coextension} と呼ぶ.\\
 1118 [AFTER   ] extension $\overline\alpha$ が存在するための必要十分条件は,
 1119 [AFTER   ] $\alpha\circ \beta=0$ であり,\\
 1120 [AFTER   ] coextension $\widetilde{\gamma}$ が存在するための必要十分条件は,
 1121 [AFTER   ] $\beta\circ\gamma=0$ である. 
 1122 [AFTER   ] 
 1123 [AFTER   ] 次の同一視を使用する.
 1124 [AFTER   ] \begin{equation}\label{eq:cone-susp}
 1125 [AFTER   ] % (1.16)
 1126 [AFTER   ] \Ex^n(Y\cup_\beta CX)\ =\ 
 1127 [AFTER   ] \Ex^nY\ \cup_{\beta'}\ C\Ex^n X,\quad \beta'=\Ex^n \beta.
 1128 [AFTER   ] \end{equation}
 1129 [AFTER   ] ここで, 対応は
 1130 [AFTER   ] \[
 1131 [AFTER   ] \phi(d'_X(x,t),\psi_n(t_1,\ldots,t_n))\longleftrightarrow d'_Z(\phi'(x,\psi_n(t_1,\ldots,t_n)),t)
```

判断欄（未決定）：このまま／範囲拡張／文献項目分割／追加調査

## stable_homotopy_group（第3章）

出典: `Toda_03_2(2).tex`、元の範囲: 1199–1206、確認表示: 1185–1220

保留理由: SOURCE_ENDS_AT_DISPLAY

```text
 1185 [BEFORE  ] 
 1186 [BEFORE  ] \end{paracol}
 1187 [BEFORE  ] 
 1188 [BEFORE  ] \begin{paracol}{2}
 1189 [BEFORE  ] 
 1190 [BEFORE  ] \medskip
 1191 [BEFORE  ] \noindent
 1192 [BEFORE  ] (2.11) の完全列の結果として Freudenthal の懸垂定理を得る：
 1193 [BEFORE  ] \begin{equation}\label{3.2}
 1194 [BEFORE  ] % (3.2)
 1195 [BEFORE  ] \Ex: \pis{i}{S^m} \longrightarrow \pis{i+1}{S^{m+1}}
 1196 [BEFORE  ] \quad\text{は, } i<2m-1 \text{で同型, } i=2m-1 \text{で全射である. }
 1197 [BEFORE  ] \end{equation}
 1198 [BEFORE  ] 
 1199 [ORIGINAL] 球面の $k$ 次安定ホモトピー群を
 1200 [ORIGINAL] \[
 1201 [ORIGINAL] G_k\ :=\ \lim_{n\to\infty}\ \pis{n+k}{S^n}
 1202 [ORIGINAL] \]
 1203 [ORIGINAL] と書き, 射影を
 1204 [ORIGINAL] \[
 1205 [ORIGINAL] \Ex^\infty:\ \pis{n+k}{S^n}\ \longrightarrow\ G_k
 1206 [ORIGINAL] \]
 1207 [AFTER   ] で表す. (3.2) から,
 1208 [AFTER   ] \begin{equation}\label{3.3}
 1209 [AFTER   ] % (3.3)
 1210 [AFTER   ] \Ex^\infty:\ \pis{n+k}{S^n}\ \xrightarrow{\;\;}\ G_k
 1211 [AFTER   ] \quad\text{は, } n>k+1 \text{で同型, } n=k+1 \text{で全射である. }
 1212 [AFTER   ] \end{equation}
 1213 [AFTER   ] 
 1214 [AFTER   ] (1.6) より,
 1215 [AFTER   ] \(\Ex^{m}(\alpha\circ\beta)=\Ex^{m}\alpha\circ\Ex^{m}\beta\)
 1216 [AFTER   ] なので, 合成
 1217 [AFTER   ] \[
 1218 [AFTER   ] \circ:G_k\times G_h \rightarrow G_{k+h}
 1219 [AFTER   ] \]
 1220 [AFTER   ] が, \(E^\infty(\alpha\circ\beta)=E^\infty\alpha\circ E^\infty\beta\) 
```

判断欄（未決定）：このまま／範囲拡張／文献項目分割／追加調査

## stable_toda_bracket（第3章）

出典: `Toda_03_2(2).tex`、元の範囲: 1236–1266、確認表示: 1222–1280

保留理由: DEFINITION_HYPOTHESES_AND_INDETERMINACY

```text
 1222 [BEFORE  ] (1.7) または (2.1) は, 合成が stable の範囲では bilinear であることを示している. 
 1223 [BEFORE  ] \[
 1224 [BEFORE  ] \alpha\circ(\beta_1\pm\beta_2)=\alpha\circ\beta_1\pm\alpha\circ\beta_2,\qquad
 1225 [BEFORE  ] (\alpha_1\pm\alpha_2)\circ\beta=\alpha_1\circ\beta\pm\alpha_2\circ\beta .
 1226 [BEFORE  ] \]
 1227 [BEFORE  ] Prop3.1 は, anti-commutativity を示している. 
 1228 [BEFORE  ] \begin{equation}\label{3.4}
 1229 [BEFORE  ] % (3.4)
 1230 [BEFORE  ] \alpha\circ\beta=(-1)^{kh}\,\beta\circ\alpha,
 1231 [BEFORE  ] \qquad(\alpha\in G_k,\ \beta\in G_h) .
 1232 [BEFORE  ] \end{equation}
 1233 [BEFORE  ] 
 1234 [BEFORE  ] \medskip
 1235 [BEFORE  ] \noindent
 1236 [ORIGINAL] \[
 1237 [ORIGINAL] \alpha\in G_k,\quad \beta\in G_h,\quad \gamma\in G_\ell,\qquad
 1238 [ORIGINAL] \alpha\circ\beta=\beta\circ\gamma=0
 1239 [ORIGINAL] \]
 1240 [ORIGINAL] に対する, stable Toda bracket 
 1241 [ORIGINAL] \[
 1242 [ORIGINAL] \langle \alpha,\beta,\gamma\rangle 
 1243 [ORIGINAL] \in G_{k+h+\ell+1}(\alpha\circ G_{h+\ell+1} + \gamma\circ G_{k+h+1}) .
 1244 [ORIGINAL] \]
 1245 [ORIGINAL] を以下の様に定義する. 
 1246 [ORIGINAL] 十分大きな $n$ をとれば, 
 1247 [ORIGINAL] \[
 1248 [ORIGINAL] \alpha'\in\pis{n+k}{S^n},\ 
 1249 [ORIGINAL] \beta'\in\pis{n+k+h}{S^{n+k}},\
 1250 [ORIGINAL] \gamma'\in\pis{n+k+h+\ell}{S^{n+k+h}}
 1251 [ORIGINAL] \]
 1252 [ORIGINAL] が存在して, 
 1253 [ORIGINAL] \(
 1254 [ORIGINAL] \alpha=\Ex^\infty\alpha',\
 1255 [ORIGINAL] \beta=\Ex^\infty\beta',\
 1256 [ORIGINAL] \gamma=\Ex^\infty\gamma'
 1257 [ORIGINAL] \)
 1258 [ORIGINAL] と書ける. \\
 1259 [ORIGINAL] このとき, 
 1260 [ORIGINAL] \(\langle \alpha,\beta,\gamma\rangle\)
 1261 [ORIGINAL] を, 次で定義する.
 1262 [ORIGINAL] \[
 1263 [ORIGINAL] \langle \alpha,\beta,\gamma\rangle
 1264 [ORIGINAL] \ :=\ \Ex^\infty (-1)^{\,n-1}\ \toda{\alpha',\beta',\gamma'}.
 1265 [ORIGINAL] \]
 1266 [ORIGINAL] Prop1.3 により, この定義は $n$ によらず well-defined である. 
 1267 [AFTER   ] 
 1268 [AFTER   ] \switchcolumn
 1269 [AFTER   ] 
 1270 [AFTER   ] \noindent
 1271 [AFTER   ] \textbf{(2.11).}\
 1272 [AFTER   ] \(\cdots\ \longrightarrow\ 
 1273 [AFTER   ] \pi_i(S^m)\xrightarrow{\,E\,}\pi_{i+1}(S^{m+1})\xrightarrow{\,H\,}
 1274 [AFTER   ] \pi_{i+1}(S^{2m+1})\xrightarrow{\,\Delta\,}\pi_{i-1}(S^m)\xrightarrow{\,E\,}\cdots.\)
 1275 [AFTER   ] 
 1276 [AFTER   ] \noindent
 1277 [AFTER   ] \textbf{(1.6).}\
 1278 [AFTER   ] \(\textbf{0).}\ 
 1279 [AFTER   ] f\simeq g:X\to Y \text{ は, }
 1280 [AFTER   ] E^n f\simeq E^n g \text{ を導く.}\)\\
```

判断欄（未決定）：このまま／範囲拡張／文献項目分割／追加調査

## nu4_generator_notation（第5章）

出典: `Toda_05_2(6).tex`、元の範囲: 567–579、確認表示: 553–593

保留理由: PRIOR_CHOICES_ALPHA_STAR_U_S

```text
  553 [BEFORE  ] \(
  554 [BEFORE  ] \eta_n\circ E\pi_{n+2}(S^n) + \pi_{n+2}(S^n)\circ\eta_{n+2} .
  555 [BEFORE  ] \)\\
  556 [BEFORE  ] (1.15) から, これらの Toda bracket は一致する. \\
  557 [BEFORE  ] これから, \(t=0\) のとき, (5.4) が成り立つことが分かる. 
  558 [BEFORE  ] \qed
  559 [BEFORE  ] 
  560 [BEFORE  ] 今, \(2E\alpha^{\ast}=\pm E^{2}\nu'\) である. \\
  561 [BEFORE  ] \(H:\pi^{3}_{6}\to \pi^{5}_{6}\) は,
  562 [BEFORE  ] \(\nu'\) を \(\pi_6^5\) の生成元 \(\eta_{5}\) に写すので, \(\nu'\) は 2 で割れない. \\
  563 [BEFORE  ] 一方, \(2E\alpha^{\ast}=\pm E^{2}\nu'\) より,
  564 [BEFORE  ] \(E^{2}\nu'\) は 2 で割れる. \\
  565 [BEFORE  ] (4.8) より,
  566 [BEFORE  ] \(H(\alpha^{\ast})=(2s+1)\iota_{7}\), (\(s\in\mathbb Z\)). \\
  567 [ORIGINAL] そこで,
  568 [ORIGINAL] \(H[\iota_4,\iota_4]=(-1)^u 2\iota_7\) とし, 
  569 [ORIGINAL] \(\nu_4\) を次で定義する. 
  570 [ORIGINAL] (\([\iota_4,\iota_4]\) は Whitehead product)
  571 [ORIGINAL] \[
  572 [ORIGINAL] \nu_{4}:=
  573 [ORIGINAL] \begin{cases}
  574 [ORIGINAL] \alpha^{\ast}-(-1)^{u}\,s[\iota_4,\iota_4] 
  575 [ORIGINAL] & (\text{if } 2E\alpha^{\ast}=E^{2}\nu'),\\[1mm]
  576 [ORIGINAL] -\alpha^{\ast}+(-1)^{u}(s+1)[\iota_4,\iota_4] 
  577 [ORIGINAL] & (\text{if } 2E\alpha^{\ast}=-E^{2}\nu').
  578 [ORIGINAL] \end{cases}
  579 [ORIGINAL] \]
  580 [AFTER   ] このとき, \(\nu_4\) がLem5.4 の条件を満たすことは簡単に確かめられる. 
  581 [AFTER   ] 
  582 [AFTER   ] \begin{lemma}\label{lem:5.5}
  583 [AFTER   ] % Lem5.5.\
  584 [AFTER   ] $Lem 5.4$ の元 \(\nu_{4}\) に対し, 
  585 [AFTER   ] Toda bracket 
  586 [AFTER   ] \(\todai[3]{\eta_{m+2},\,E^{3}\beta,\,\eta_{t+5}}\) は,\\
  587 [AFTER   ] \(
  588 [AFTER   ] E^{2}\beta\circ E^{t}\nu_{4}\text{または,} -E^{2}\beta\circ E^{t}\nu_{4}
  589 [AFTER   ] \)
  590 [AFTER   ] を含む. \\
  591 [AFTER   ] ここで, \(\beta\in\pi_{t+2}(S^{m})\) は,
  592 [AFTER   ] \(\beta\circ \eta_{t+2}=0\), \(t>0\) を満たす元である. 
  593 [AFTER   ] \end{lemma}
```

判断欄（未決定）：このまま／範囲拡張／文献項目分割／追加調査

## nu_n_notation（第5章）

出典: `Toda_05_2(6).tex`、元の範囲: 605–607、確認表示: 591–621

保留理由: ADJACENT_NOTATION_BLOCK

```text
  591 [BEFORE  ] ここで, \(\beta\in\pi_{t+2}(S^{m})\) は,
  592 [BEFORE  ] \(\beta\circ \eta_{t+2}=0\), \(t>0\) を満たす元である. 
  593 [BEFORE  ] \end{lemma}
  594 [BEFORE  ] 
  595 [BEFORE  ] \noindent
  596 [BEFORE  ] \textbf{Proof.}\ 
  597 [BEFORE  ] 前Lemの証明より, \\
  598 [BEFORE  ] \(E^{2}\beta\circ E^{t}\alpha^{\ast}\) あるいは,
  599 [BEFORE  ] \(-E^{2}\beta\circ E^{t}\alpha^{\ast}\) 
  600 [BEFORE  ] が, 当該 Toda bracket に含まれる. \\
  601 [BEFORE  ] \(E[\iota_4,\iota_4]=0\) なので, 定義より,
  602 [BEFORE  ] \(E^{t}\nu_{4}=\pm E^{t}\alpha^{\ast}\) である. 
  603 [BEFORE  ] \qed
  604 [BEFORE  ] 
  605 [ORIGINAL] \[
  606 [ORIGINAL] \nu_n:=E^{\,n-4}\nu_{4},\ (n\ge 4),\qquad \nu:=E^{\infty}\nu_{4}
  607 [ORIGINAL] \]
  608 [AFTER   ] \[
  609 [AFTER   ] \eta^{3}_{n}:=\eta_{n}\circ\eta_{n+1}\circ\eta_{n+2},\ (n\ge2),\qquad
  610 [AFTER   ] \eta^{3}:=\eta\circ\eta\circ\eta .
  611 [AFTER   ] \]
  612 [AFTER   ] と記す.
  613 [AFTER   ] Lem 5.4 とProp 5.3 より,
  614 [AFTER   ] \begin{equation}\label{eq:5.5}
  615 [AFTER   ] % (5.5).\
  616 [AFTER   ] n\ge5\ \text{に対して, } 2\nu_n=E^{\,n-3}\nu',\qquad
  617 [AFTER   ] 4\nu_{n}=\eta_n^{3},\quad 4\nu=\eta^{3}.
  618 [AFTER   ] \end{equation}
  619 [AFTER   ] \noindent
  620 [AFTER   ] Prop 4.4 とLem 5.4 から,
  621 [AFTER   ] \begin{equation}\label{eq:5.6}
```

判断欄（未決定）：このまま／範囲拡張／文献項目分割／追加調査

## eta_n_cubed_notation（第5章）

出典: `Toda_05_2(6).tex`、元の範囲: 608–612、確認表示: 594–626

保留理由: ADJACENT_NOTATION_BLOCK

```text
  594 [BEFORE  ] 
  595 [BEFORE  ] \noindent
  596 [BEFORE  ] \textbf{Proof.}\ 
  597 [BEFORE  ] 前Lemの証明より, \\
  598 [BEFORE  ] \(E^{2}\beta\circ E^{t}\alpha^{\ast}\) あるいは,
  599 [BEFORE  ] \(-E^{2}\beta\circ E^{t}\alpha^{\ast}\) 
  600 [BEFORE  ] が, 当該 Toda bracket に含まれる. \\
  601 [BEFORE  ] \(E[\iota_4,\iota_4]=0\) なので, 定義より,
  602 [BEFORE  ] \(E^{t}\nu_{4}=\pm E^{t}\alpha^{\ast}\) である. 
  603 [BEFORE  ] \qed
  604 [BEFORE  ] 
  605 [BEFORE  ] \[
  606 [BEFORE  ] \nu_n:=E^{\,n-4}\nu_{4},\ (n\ge 4),\qquad \nu:=E^{\infty}\nu_{4}
  607 [BEFORE  ] \]
  608 [ORIGINAL] \[
  609 [ORIGINAL] \eta^{3}_{n}:=\eta_{n}\circ\eta_{n+1}\circ\eta_{n+2},\ (n\ge2),\qquad
  610 [ORIGINAL] \eta^{3}:=\eta\circ\eta\circ\eta .
  611 [ORIGINAL] \]
  612 [ORIGINAL] と記す.
  613 [AFTER   ] Lem 5.4 とProp 5.3 より,
  614 [AFTER   ] \begin{equation}\label{eq:5.5}
  615 [AFTER   ] % (5.5).\
  616 [AFTER   ] n\ge5\ \text{に対して, } 2\nu_n=E^{\,n-3}\nu',\qquad
  617 [AFTER   ] 4\nu_{n}=\eta_n^{3},\quad 4\nu=\eta^{3}.
  618 [AFTER   ] \end{equation}
  619 [AFTER   ] \noindent
  620 [AFTER   ] Prop 4.4 とLem 5.4 から,
  621 [AFTER   ] \begin{equation}\label{eq:5.6}
  622 [AFTER   ] % (5.6).\
  623 [AFTER   ] (\alpha,\beta)\ \longmapsto\ E\alpha+\nu_{4}\circ\beta
  624 [AFTER   ] \quad\text{は,}\quad
  625 [AFTER   ] \pi^{\,3}_{i-1}\oplus \pi^{\,7}_{i}\ \xrightarrow{\ \cong\ }\ \pi_{\,i}^{4}
  626 [AFTER   ] \ \text{の同型を与える. }
```

判断欄（未決定）：このまま／範囲拡張／文献項目分割／追加調査

正式 ID、数学的承認、Registry 変更、証明探索への接続は行わない。
全体 pytest は実施しない。
