# Phase 174 R3-R7-R32 — 下側 Δ 核の一般推論監査

## 実装前に確認した GitHub の現行状態

- リポジトリ：`akebono03/ehp-proof-tracer`、ブランチ `develop`。
- 監査対象 HEAD：`25118e281445ca17b30c60c8fd02d00acaa25ea5`。
- 直前の R31 はユーザー実行で DryRun PASS、監査 PASS、限定 pytest 71 PASS を確認済み。
- R30 の Provider 接続 10 行は GitHub へ統合済み。R31 の未追跡ディレクトリは保存する。

検査した関連コードとテスト：

- `sources/toda/Toda_05_2.tex`：Proposition 5.8、式 (5.10)、Proposition 5.9。
- `homotopy_groups.py` / `expression.py` / `proof.py`：群、生成元、型付き Statement と ProofStep。
- `phase165_r12_r2_quotient_rules.py`：`KernelMultipleStatement` と有限巡回商の一般規則。
- `phase165_r12_r11_prop42_unified.py`：EHP 完全列の添字整合性。
- `phase165_r57_r19_delta_image_backward.py` / `toda_delta_image_rules.py`：符号付き Δ 像と逆向き探索。
- `phase169_r10e4_ordered_db_prior/db_prior.py`：DB prior は文献定理と同一ではない。
- `phase174_r3_r7_r18_delta_image_surjectivity/rule.py` および `tests/test_rule.py`：既存の全射性一般規則と検査。
- `phase174_r3_r7_r31_delta_surjectivity_general_audit/audit.py`：直前の課題と監査境界。

## 数学的な正当性

一般の群準同型 $f:\mathbb Z\{g\}\to\mathbb Z/m\{h\}$ について、

$$
f(g)=\pm h,\qquad m\ge1
$$

であれば、任意の $k\in\mathbb Z$ に対して $f(kg)=\pm kh$ であり、
$f(kg)=0$ と $m\mid k$ が同値である。したがって

$$
\ker f=\langle mg\rangle
$$

が従う。ただし、**自由巡回群の表示・有限巡回群の表示・生成元像の3件は独立して証明されなければならない**。

今回対象とする写像は

$$
\Delta:\pi_{11}^{11}\longrightarrow\pi_9^5
$$

である。Toda の文献では、Proposition 5.8 に $\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\}$、式 (5.10) に $\Delta(\iota_{11})=\nu_5\eta_8$ が記されており、Proposition 5.9 の証明で $\ker\Delta=\langle2\iota_{11}\rangle$ が導出される。

**Proposition 5.9 に書かれた結論を直接 GIVEN にすることは禁止する。** 文献の TeX 表示と、検証済み型付き ProofStep は区別する。

## 今回の変更対象（既存コードは一切変更しない）

新規ディレクトリ `phase174_r3_r7_r32_lower_delta_kernel_audit/` 配下のみ追加する。

| ファイル | 追加する関数・内容 |
|---|---|
| `kernel_contract.py` | `valid_ehp_lower_delta()`、`generator_has_group_coordinates()`、`conditional_kernel_premises()`、`signed_cyclic_kernel_membership()` |
| `audit.py` | `git()`、`git_blob_sha()`、`matches_pin()`、`verify_checkout()`、`inspect_toda_citations()`、`inspect_typed_contract()`、`inspect_screened_frontier()`、`report()`、`main()` |
| `tests/test_kernel_contract.py` | 有限巡回群、符号、添字、生成元・像の不一致を検査する新規テスト全文 |
| `tests/test_audit.py` | Source Guard・出典境界・未証明維持の新規テスト全文 |
| `run.ps1` | DryRun、監査本実行、分離した限定 pytest の実行 |
| `README.md` | 英語での利用説明（新規全文） |
| `CODE_FULL_JA.md`、`IMPORTS_FULL.txt`、`__init__.py` | 置換可能な全コード、全 import、パッケージ宣言 |

**既存クラス、既存関数、既存 import への変更なし。新規クラスなし。** 新規関数の追加位置は記載の新規モジュール先頭の import の後。新規テスト関数の追加位置は各新規 test ファイル内。すべて全文を ZIP に収録する。

`kernel_contract.py` は ProofStep、InferenceRule、GIVEN を生成せず、`shared_expansion_provider` に登録しない。監査対象となる前提を型検査するだけである。

## 解凍から実行まで

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
$ErrorActionPreference = 'Stop'

Expand-Archive `
  -Path "$HOME\Downloads\EHP_Phase174_R3_R7_R32_LOWER_DELTA_KERNEL_GENERAL_AUDIT.zip" `
  -DestinationPath "." `
  -Force

powershell -NoProfile -ExecutionPolicy Bypass `
  -File ".\phase174_r3_r7_r32_lower_delta_kernel_audit\run.ps1" `
  -DryRun
if ($LASTEXITCODE -ne 0) { throw "R32 DryRun failed" }

powershell -NoProfile -ExecutionPolicy Bypass `
  -File ".\phase174_r3_r7_r32_lower_delta_kernel_audit\run.ps1"
if ($LASTEXITCODE -ne 0) { throw "R32 audit failed" }

git status -sb
git diff --stat
Write-Output "(END)"
```

`run.ps1` が実行する限定 pytest：

```powershell
python -B -m pytest -q --import-mode=importlib -p no:cacheprovider .\phase174_r3_r7_r32_lower_delta_kernel_audit\tests\test_kernel_contract.py
python -B -m pytest -q --import-mode=importlib -p no:cacheprovider .\phase174_r3_r7_r32_lower_delta_kernel_audit\tests\test_audit.py
python -B -m pytest -q --import-mode=importlib -p no:cacheprovider .\phase174_r3_r7_r31_delta_surjectivity_general_audit\tests\test_audit.py .\phase174_r3_r7_r31_delta_surjectivity_general_audit\tests\test_static_helpers.py
python -B -m pytest -q --import-mode=importlib -p no:cacheprovider .\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_rule.py
python -B -m pytest -q --import-mode=importlib -p no:cacheprovider .\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py
```

全体 pytest は Phase 174 最終段階まで実施しない。

## 完了条件・境界

- Source Guard PASS、R30/R31 保持、指定した出典の照合 PASS。
- 一般群準同型について $\ker f=\langle mg\rangle$ の条件を型付きに監査。
- 不正な添字、位数、元の型、生成元、写像、符号に対する拒否テスト PASS。
- 文献引用の事実・DB prior と、共通探索で得られる検証済み ProofStep の区別を維持。
- 限定 pytest PASS。既存コード・データ・Renderer 変更なし。
- `LOWER_DELTA_KERNEL_PROVED=False`、`DELTA_SURJECTIVITY_PROVED=False`、`ROOT_COMPLETE=False` を維持。

予定 Gate：`PASS_R32_LOWER_DELTA_KERNEL_CONDITIONAL_AUDITED_TYPED_PROOF_PENDING`。

次工程 R33 は、各前提の source-first 型付き独立証明を構築できるか検討する。今回の R32 で一般推論規則を本番登録したと誤認しない。
