# Phase 174 R3-R7-R4：Delta 全射性の Source-first 監査

## 変更対象

新規 `phase174_r3_r7_r4_delta_surjectivity_audit/` 内のみです。

- `audit.py`：GitHub HEAD、出典、過去の監査結果、型付き Goal の候補を確認します。
- `tests/test_audit.py`：新規の監査契約テストを実行します。
- `run.ps1`：DryRun、本実行、限定 pytest を実行します。
- `README.md`：英語の実行説明です。
- `AUDIT_PLAN_JA.md` と `CODE_FULL_JA.md`：日本語の監査資料です。
- `__init__.py`：空の Python パッケージ識別ファイルです。

既存の関数、メソッド、クラス、import、共通5文書、Web、Proof Tree、Narrative は変更しません。

## 数学的な焦点

Toda Proposition 5.9 の証明では、

$$
\pi_{10}^{5}=\mathbb Z/2\{\nu_5\eta_8^2\}
\quad\text{かつ}\quad E\pi_{10}^{5}=0
$$

です。前者は非零群であり、後者は写像 $E$ が零であることを意味します。
「$\pi_{10}^{5}=0$」という誤った前提に置き換えません。

さらに、

$$
\pi_{10}^{5}\xrightarrow{E}\pi_{11}^{6}
\xrightarrow{H}\pi_{11}^{11}
\xrightarrow{\Delta}\pi_{9}^{5}
$$

について、2つの EHP Exactness Window（完全列の隣接部分）、
Hopf injectivity（Hopf 写像の単射性）、
および $\Delta:\pi_{13}^{13}\to\pi_{11}^{6}$ の全射性を
既存の Source-first provider に照会します。

Toda の転写にある $H\Delta(\iota_{13})=\pm2\iota_{11}$ と
$\pi_{11}^{6}=\mathbb Z\{\Delta(\iota_{13})\}$ は、証明上の
参照対象であって、直接 GIVEN にしません。

## 完了条件と境界

DryRun と本実行で Source Guard と限定 pytest が PASS し、
候補数と隣接群のライブ検索結果が JSON に記録されれば、監査完了です。
未解決の写像性質は未解決のまま保持します。

次の R3-R7-R5 では、独立に検証された写像の零性、核、像から
一般的な推論を導けるか検討します。条件が満たせなければ、
推論規則を追加せず未完成のままとします。

全体 pytest は Phase 174 終了時にのみ実施します。
